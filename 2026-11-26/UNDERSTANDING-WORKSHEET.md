# JPA 연관관계와 Security 기초 이해 확인

코드와 그림을 보고 결과를 먼저 예상한다. 필요한 질문만 골라 말로 답해도 된다. 이 작업지 자체를 제출할 필요는 없다.

## 같은 데이터로 관계 읽기

사용자 표의 `id`와 링크 표의 `id`는 각각 자기 행을 구분하는 PK다. `owner_id`는 사용자 행을 가리키는 FK다. 숫자는 설명용이다.

| 사용자 id | username |
|---|---|
| 101 | learner |
| 102 | other |

| 링크 id | code | owner_id |
|---|---|---|
| 501 | abc | 101 |
| 502 | xyz | 101 |
| 503 | def | 102 |

| 질문 | 내 설명 |
|---|---|
| learner의 링크 두 개는 무엇이고, 어느 컬럼으로 찾았는가? | |
| 링크 503의 PK와 사용자를 가리키는 FK 값은 각각 무엇인가? | |
| 링크에서 사용자는 왜 N:1이고, 사용자에서 링크는 왜 1:N인가? | |

## 객체 참조와 저장 구분

```java
// Java 객체만 생성하는 예시 · 생성자는 해당 값을 필드에 설정
AppUser user = new AppUser("learner");
ShortLink first = new ShortLink(user, "abc", "https://example.com/a");
ShortLink second = new ShortLink(user, "xyz", "https://example.com/b");
```

| 질문 | 내 설명 |
|---|---|
| first.getOwner()와 second.getOwner()는 같은 객체를 가리키는가? | |
| first.getOwner().getUsername()은 무엇인가? | |
| new만 실행했는데 DB에도 링크가 저장되었다고 말할 수 있는가? | |

```java
// ShortLink 내부
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;

// 역방향 탐색이 필요할 때 추가하는 AppUser 내부 필드
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
```

| 질문 | 내 설명 |
|---|---|
| owner와 owner_id는 각각 Java와 DB 중 어디의 이름인가? | |
| mappedBy에는 왜 owner_id 대신 owner를 적는가? | |
| 양방향으로 바꾸면 FK도 두 개 필요한가? | |
| 이 매핑에서 FK 등록·수정의 기준은 어느 필드인가? | |

## 연관관계의 주인 찾기

‘주인’은 FK 값을 결정하는 **관계 필드**다. 업무상 누가 데이터를 소유하는지로 정하지 않는다. 이 다대일 양방향 매핑은 다음 순서로 찾는다.

1. FK가 있는 테이블은 `short_links`, 컬럼은 `owner_id`다. 링크 한 행에 사용자 한 명의 ID만 저장하면 되므로 N쪽 링크 테이블에 둔다.
2. 이 테이블을 매핑한 Entity는 `ShortLink`다.
3. FK를 매핑한 `ShortLink.owner`가 주인이다. `@ManyToOne`과 `@JoinColumn`이 있고, 주인에는 `mappedBy`를 붙이지 않는다.

`AppUser.links`에는 `mappedBy="owner"`를 둔다. 이 목록의 변경은 FK 갱신 기준이 아니라는 뜻이며, `AppUser`의 닉네임 같은 일반 속성도 수정할 수 없다는 뜻은 아니다.

- 사용자에게 링크 목록이 있다는 이유만으로 `AppUser.links`를 주인으로 고르면 안 되는 이유는?
- `user_profiles.user_id`를 `UserProfile.user`에 매핑했다면, 이 일대일 양방향 관계의 주인은 어느 필드인가?
- `ShortLinkTag`가 `link_id`와 `tag_id`를 각각 매핑한다면, 각 관계의 주인 필드는 무엇인가?

주인은 Entity마다 하나로 정하는 것이 아니라 **관계마다** 판단한다. 연결 Entity의 두 다대일 필드가 각각 자기 관계의 주인일 수 있다.

양방향의 두 Java 참조는 개발자가 함께 맞춘다. 주인 필드를 바꿔도 이미 읽은 반대쪽 컬렉션이 자동으로 동기화되지는 않는다.

## 변경 결과 예상

저장된 xyz의 `owner_id=101`이다. 각 행은 **새로 조회해서 시작하는 별개의 실험**이며, 관리 객체와 활성 트랜잭션을 가정한다.

| 동작 | flush·commit 후 예상 owner_id |
|---|---|
| other.getLinks().add(xyz)만 실행 | |
| xyz.owner를 other로 변경 | |

DB FK의 갱신 기준과 Java 양쪽 참조를 맞추는 일은 구분한다. 실제 사용자 간 소유권 이전 기능을 만들라는 뜻은 아니다.

- 새 링크 생성 편의 메서드가 맞추는 두 참조는 무엇인가?
- 새 링크 저장을 담당하는 호출은 무엇인가?
- 관계를 DTO로 바꾸면 추가 SQL이나 N+1도 자동으로 없어지는가?

## Security 기초 설명

| 질문 | 내 설명 |
|---|---|
| 비밀번호로 learner인지 확인하는 것과 다른 사람 링크를 차단하는 것은 각각 무엇인가? | |
| 요청이 거부되어도 Controller가 반드시 실행되는가? | |
| 브라우저의 세션 ID와 서버의 로그인 상태는 어떻게 연결되는가? | |
| 비밀번호를 다시 encode해 문자열 비교하지 않고 matches를 쓰는 이유는? | |
| 403의 원인을 권한 부족으로만 단정하면 안 되는 이유는? | |

## Security 자율 학습

수업 장표의 공식 문서 링크를 순서대로 참고한다. 기본 로그인 폼 → 내 DB 계정과 PasswordEncoder → 경로별 인가와 데이터 소유권 → CSRF 순서로 작은 동작부터 실행한다. JWT는 이후에 학습한다.

로그인 전후의 응답, 다른 사용자의 링크 요청, CSRF 토큰이 없는 변경 요청을 비교하고 이유를 설명해 본다. **Security 구현은 아래 JPA 과제의 필수 조건이 아니다.**

## JPA 과제: 스터디 모집·모임 관리 서비스

회원들이 스터디를 만들고 참여하며 모임 일정을 관리하는 새 REST API 프로젝트를 만든다. 핵심 기능은 회원·프로필 관리, 스터디 개설·조회, 참여·탈퇴와 참여 목록 조회, 스터디별 일정 등록·조회다.

Entity 구성·필드·API는 직접 설계한다. 일대일, 일대다/다대일, 여러 회원과 여러 스터디의 관계를 JPA로 표현하고 관계 방향·FK와 가입 정보를 어떻게 다룰지 결정한다. 중복 참여·정원·탈퇴 등의 서비스 규칙도 스스로 정한다. 여력이 있다면 재가입·스터디장 위임 등 원하는 기능을 확장한다.

새 Spring Boot 프로젝트에서 JPA로 DB에 저장한다. 기존 fork 저장소의 자율 이름 폴더에 추가하고 [공용 저장소](https://github.com/sesac-ddm-4-web/sesac-spring-boot-study)로 PR을 제출한다. 기존 프로젝트는 보존하며 프로젝트 구조·API·브랜치 이름은 자율이다.

PR에는 구현 기능, Entity 관계도, 관계와 트랜잭션 설계 이유, 직접 정한 서비스 규칙을 적는다. 로그인·프론트는 선택이며 테스트 코드 구현은 필수가 아니다. Security 자율 학습은 별도로 진행한다.
