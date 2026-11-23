# JPA 연관관계와 Spring Security 이해 확인

짧은 코드와 장표의 표·화살표를 읽으며 자기 말로 설명한다. 필요한 질문만 고르거나 말로 답해도 된다. 별도 제출이나 완성 앱 실행은 필요하지 않다. 코드의 import·생성자·일부 설정은 생략되어 있다.

## FK가 가리키는 행을 찾는다

**app_users**

| id | username | role |
|---|---|---|
| 101 | learner | USER |
| 102 | other | USER |

**short_links**

| id | code | original_url | owner_id |
|---|---|---|---|
| 501 | abc | https://example.com/a | 101 |
| 502 | xyz | https://example.com/b | 101 |
| 503 | def | https://example.com/c | 102 |

실제 app_users에는 passwordHash 필드도 있지만 이 표에는 표시하지 않는다. 위 ID는 장표와 같은 설명용 식별자이며 실제 저장 시 생성될 ID를 예측하는 값이 아니다.

| 질문 | 내 설명 |
|---|---|
| 각 표의 PK는 무엇인가? | |
| 링크 502의 owner_id는 어느 사용자 행을 가리키는가? | |
| learner의 링크 두 개를 어떻게 찾을 수 있는가? | |
| 사용자가 링크 여러 개를 가져도 사용자 표에 링크 ID 열을 계속 늘리지 않는 이유는? | |

## 객체에서 사용자로 이동한다

```java
// ShortLink의 필드
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;
```

| 질문 | 내 설명 |
|---|---|
| ShortLink에서 AppUser로 이동하는 Java 필드 이름은? | |
| DB에서 연결을 저장하는 열 이름은? | |
| 링크 여러 개가 같은 사용자를 참조할 수 있는가? | |
| LAZY일 때 owner 접근과 실제 조회 시점을 구분해야 하는 이유는? | |

관계 필드는 객체 참조다. DB의 owner_id 열 자체를 Java 객체라고 부르지 않는다.

## 양방향에서는 두 참조를 맞춘다

```java
// AppUser의 역방향 필드
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
```

| 질문 | 내 설명 |
|---|---|
| mappedBy는 owner와 owner_id 중 무엇을 사용하는가? 왜 그런가? | |
| 양방향이 되면 DB FK가 하나 더 생기는가? | |
| FK 갱신 기준인 ‘연관관계 주인’은 어느 필드인가? | |
| 여기서 ‘주인’과 실제 링크를 소유한 사용자의 의미는 어떻게 다른가? | |

다음 두 동작을 비교한다. 기본 매핑에는 cascade가 없다.

```java
// A: 역방향만 변경 — owner를 설정했다고 볼 수 없다
user.getLinks().add(link);

// B: AppUser의 편의 메서드
public ShortLink addLink(String code, String url) {
    ShortLink link = new ShortLink(this, code, url); // owner 설정
    links.add(link);                              // 역방향도 맞춤
    return link;
}

// Service: user는 이미 저장된 사용자라고 가정
ShortLink created = user.addLink(code, url);
linkRepository.save(created);                    // 저장을 명시
```

- A만 실행했을 때 FK가 설정되었다고 말할 수 없는 이유: `________________`
- B에서 두 객체 참조가 맞춰지는 줄: `________________`
- 새 링크 저장을 담당하는 줄: `________________`
- 이 코드가 임의의 기존 링크 소유권 이전까지 처리하는가? `________________`

## 저장 전파와 삭제를 예상한다

각 행은 서로 다른 설정을 적용한 상황이다. 동일한 객체에 모든 설정이 동시에 있다고 가정하지 않는다.

| 상황 | 예상과 이유 |
|---|---|
| cascade 없는 기본 예제에서 새 링크를 만들고 user만 저장하면 링크 저장까지 보장되는가? | |
| AppUser.links에 PERSIST가 있으면 새 사용자 persist가 어떤 작업을 전파하는가? | |
| AppUser.links에 REMOVE가 있고 사용자를 삭제하면 연결된 링크에도 무엇이 전파되는가? | |
| orphanRemoval=true인 관리 사용자 컬렉션에서 자식 링크를 제거하면 무엇이 삭제 대상이 되는가? | |
| ShortLink.owner에 REMOVE나 ALL을 넣고 링크 하나를 삭제하면 왜 위험한가? | |
| 사용자 탈퇴 때 링크를 삭제할지 보존할지는 무엇을 먼저 정해야 하는가? | |

매핑 방향과 저장·삭제 전파는 별개다. 삭제 실행 시점은 flush 등 영속성 처리와 함께 판단한다.

## 응답에 필요한 값을 고른다

사용자에게 내 링크 목록을 보여주려 한다.

| 질문 | 내 설명 |
|---|---|
| 응답에 id·code·originalUrl 외에 무엇이 실제로 필요한가? | |
| AppUser 전체를 그대로 응답하면 passwordHash에 어떤 위험이 있는가? | |
| user.links → link.owner → user.links를 JSON으로 따라가면 어떤 문제가 생길 수 있는가? | |
| DTO로 바꾸는 중 관계 조회를 반복하면 N+1이 자동으로 사라지는가? | |
| 관리 컨텍스트가 닫힌 뒤 미초기화 LAZY 관계에 접근하면 왜 실패할 수 있는가? | |

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
