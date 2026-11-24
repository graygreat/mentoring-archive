# JPA 연관관계와 Spring Security 이해 확인

짧은 코드와 장표의 표·화살표를 읽으며 자기 말로 설명한다. 필요한 질문만 고르거나 말로 답해도 된다. 별도 제출이나 완성 앱 실행은 필요하지 않다. 코드의 import·생성자·일부 설정은 생략되어 있다.

## 연관관계 이해 확인

장표와 같은 설명용 데이터다. 실제 저장 시 ID를 고정 숫자로 가정하지 않는다.

| app_users.id | username |
|---|---|
| 101 | learner |
| 102 | other |

| short_links.id | code | owner_id |
|---|---|---|
| 501 | abc | 101 |
| 502 | xyz | 101 |
| 503 | def | 102 |

```java
// ShortLink 내부
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;

// AppUser 내부
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
```

| 질문 | 내 설명 |
|---|---|
| @Entity·@Table·@Id는 각각 무엇과 연결되는가? | |
| owner_id=101인 링크 두 개는 어느 사용자를 참조하는가? | |
| DB의 owner_id 값과 Java의 owner 필드는 무엇이 다른가? | |
| 링크에서 사용자 이름으로 탐색하는 Java 코드는? | |
| 링크와 사용자는 각각 어느 쪽에서 N:1, 1:N인가? | |
| 양방향 참조를 추가하면 DB FK도 하나 더 필요한가? | |
| mappedBy는 owner와 owner_id 중 무엇을 사용하며 왜 그런가? | |
| 이 매핑에서 FK 등록·수정 기준인 주인 필드는 무엇인가? | |
| user.getLinks().add(link)만 하면 FK 설정이 끝나지 않는 이유는? | |
| addLink 편의 메서드가 맞추는 두 참조와 새 링크 저장 호출은? | |
| 일대일에서 FK에 UNIQUE 제약이 필요한 이유는? | |
| 태그를 연결한 시각까지 저장한다면 연결 Entity가 필요한 이유는? | |

관계 방향과 저장·삭제 전파는 별개다. 단방향부터 매핑하고, 필요한 역방향 탐색만 추가한다. 응답은 DTO로 구성하며 LAZY·N+1 조회도 함께 확인한다.

## 인증과 인가를 구분한다

| 상황 | 인증 / 인가 / 데이터 소유권 검사 중 무엇을 확인하는가? |
|---|---|
| learner의 username과 비밀번호가 맞는지 확인 | |
| /admin/**를 ADMIN에게만 허용 | |
| 로그인한 learner가 링크 503을 수정해도 되는지 확인 | |
| /s/abc 공개 리다이렉트를 로그인 없이 허용 | |

‘로그인했다’는 사실만으로 다른 사용자의 링크까지 수정할 수는 없다.

## 세션 로그인 흐름을 읽는다

다음 구성요소에 번호를 붙이거나 장표의 화살표와 연결한다. 성공 경로의 기본 formLogin·세션 설정을 가정한다.

| 단계 | 무엇을 확인하거나 전달하는가? |
|---|---|
| 브라우저가 로그인 폼을 전송 | |
| Security 필터가 인증을 처리 | |
| UserDetailsService가 username으로 DB 계정 조회 | |
| 인증 제공자가 PasswordEncoder.matches로 비밀번호 검증 | |
| SecurityContext에 Authentication 저장 | |
| 서버 세션과 브라우저 세션 ID 쿠키로 다음 요청 연결 | |
| 인증된 다음 요청이 DispatcherServlet과 Controller로 이동 | |

- 거부된 요청도 반드시 Controller까지 도달하는가? `________________`
- 브라우저 쿠키에 DB 사용자 엔티티가 담기는가? `________________`
- principal을 AppUser 엔티티와 같다고 가정하면 안 되는 이유는? `________________`
- 이번 기본 로그인은 JWT 발급 흐름인가? `________________`

## BCrypt 해시를 검증한다

```java
String first = encoder.encode("same-password");
String second = encoder.encode("same-password");
boolean accepted = encoder.matches("same-password", first);
```

| 질문 | 내 설명 |
|---|---|
| first와 second가 달라도 정상일 수 있는 이유는? | |
| accepted는 어떤 조건에서 true인가? | |
| 새 encode 결과와 저장 해시를 문자열 비교해 로그인하면 안 되는 이유는? | |
| 저장된 passwordHash를 복호화해서 비교하는가? | |
| 개발용 계정을 준비할 때 DB에 원문과 해시 중 무엇을 저장하는가? | |

## 요청 결과를 조건과 함께 판단한다

아래는 세션 기반 formLogin, CSRF 기본 활성화, 공개 GET /s/*·GET /csrf, /admin/**는 hasRole("ADMIN"), /api/links/**는 authenticated, 나머지는 denyAll인 정책을 가정한다. 각 결과는 요청 메서드·인증·CSRF·entry point 조건을 함께 보고 설명한다.

| 요청과 조건 | 예상 결과와 이유 |
|---|---|
| 익명 사용자가 GET /s/abc 요청, 해당 코드가 존재 | |
| 익명 사용자가 GET /api/links 요청, 기본 로그인 entry point 사용 | |
| 위 API 미인증 정책을 별도 401 entry point로 설정한 경우 | |
| 로그인한 USER가 GET /admin/panel 요청 | |
| 익명 사용자가 CSRF 토큰 없이 POST /api/links 요청 | |
| 로그인한 USER가 올바른 CSRF 토큰과 함께 POST /api/links 요청 | |
| fetch가 302를 자동 추적해 최종 로그인 HTML을 받은 경우 | |

마지막에서 두 번째 행은 **보안 필터를 통과할 수 있는지** 판단한다. 이후 Controller의 검증·업무 처리 성공까지 보장하지 않는다. hasRole("ADMIN")과 권한 문자열 ROLE_ADMIN의 기본 접두사도 확인한다.

## CSRF와 CORS를 구분한다

| 질문 | 내 설명 |
|---|---|
| 브라우저가 세션 ID 쿠키를 자동 전송하는 것이 왜 출발 조건인가? | |
| permitAll 경로의 POST는 CSRF 토큰도 자동 면제되는가? | |
| GET /csrf에서 받은 headerName과 token은 변경 요청의 어디에 넣는가? | |
| 로그인·로그아웃 뒤에는 왜 새 CSRF 토큰을 다시 받아야 하는가? | |
| 기본 로그아웃은 GET 링크와 POST 요청 중 무엇을 사용하는가? | |
| 교차 출처 읽기를 다루는 CORS가 CSRF 보호를 대신할 수 있는가? | |

## 다른 linkId를 넣으면 어떻게 될까?

learner(id=101)가 로그인했다. 주소의 linkId를 501에서 other의 링크 503으로 바꿔 요청했다고 가정한다.

```java
// 인증된 username으로 AppUser를 조회해 얻은 ID
long authenticatedUserId = currentUser.getId();

ShortLink link = linkRepository
    .findByIdAndOwnerId(linkId, authenticatedUserId)
    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
```

| 질문 | 내 설명 |
|---|---|
| linkId=503, authenticatedUserId=101이면 위 표에 맞는 행이 있는가? | |
| findById(linkId)만 사용할 때 놓치는 조건은? | |
| 클라이언트가 userId=102를 보내도 현재 사용자 ID로 믿을 수 없는 이유는? | |
| 이 코드가 다른 사용자의 링크에 돌려주는 상태 코드는? | |
| authenticated 또는 USER 역할 검사만으로 이 조건을 대신할 수 있는가? | |
| 로그인 없는 /s/def 공개 리다이렉트와 관리 API의 소유권 정책은 어떻게 다른가? | |

## 내 서비스에 선택해 연결한다

마지막 장표를 보고 지금 필요한 한 가지를 고른다. 새 기능을 모두 완성하거나 별도 결과를 제출하라는 과제가 아니다. 23일 JPA 전환 과제와 제출 방식은 그대로다.

- 내 표의 FK와 Java 관계 필드를 연결해 설명한다.
- 새 링크를 저장할 때 사용자 참조와 저장 호출이 어디에 있는지 찾는다.
- 로그인 요청과 다음 요청에서 세션 쿠키가 하는 일을 그려 본다.
- 본인 링크 조회에 인증 정보에서 얻은 사용자 ID가 포함되는지 확인한다.

내가 고른 내용과 더 확인할 질문: `________________________________`
