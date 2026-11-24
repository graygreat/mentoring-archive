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

기존 단축 URL 서비스를 수정하는 대신 새 Spring Boot 프로젝트를 만든다. Spring Web·Spring Data JPA·사용 DB 드라이버를 추가하고 데이터는 DB에 저장한다. 버전은 기존 학습 환경을 따른다. 기존 fork 저장소에서 자율적인 이름의 폴더에 추가하고 기존 프로젝트는 보존한다. 수업의 단축 URL은 학습 예시이며, 과제는 아래 별도 서비스다.

로그인 없이 학습용 `memberId`로 회원을 선택한다. 이 값은 인증 정보가 아니다. API 경로와 브랜치 이름은 직접 정한다. 프론트, 로그인, 테스트 코드 구현은 필수가 아니다.

### 사용할 관계

| Entity | 관계와 저장할 정보 |
|---|---|
| Member | 회원의 닉네임 |
| MemberProfile | 자기소개·관심 분야, Member와 일대일. member_id에 UNIQUE |
| Study | 제목·설명·정원, creator가 최초 개설자를 다대일로 참조 |
| StudyMeeting | 제목·일시·장소, study가 소속 스터디를 다대일로 참조 |
| StudyMember | member·study 각각 다대일, role·status·joinedAt 저장 |

`StudyMember`로 회원과 스터디의 다대다를 풀어낸다. `(study_id, member_id)`에 DB UNIQUE 제약을 둔다. 단방향부터 구현하고, 필요한 역방향 탐색만 추가한다.

### 1단계: 기본

- 닉네임을 가진 회원과 자기소개·관심 분야를 가진 프로필 하나를 같은 트랜잭션에서 등록한다. 회원 ID로 닉네임과 프로필을 함께 조회한다.
- 기존 회원을 개설자로 지정해 제목·설명·정원(2명 이상)을 가진 스터디를 만든다. 목록·상세에 개설자 닉네임도 응답한다.
- 기존 스터디에 제목·일시·장소를 가진 일정을 등록하고, 선택한 스터디의 일정만 목록으로 조회한다.
- 없는 회원·스터디를 참조하는 요청은 404로 처리한다. 개설자의 자동 가입은 2단계에서 생성 기능에 추가한다.

### 2단계: 응용

2단계는 새로 만든 스터디로 확인한다. 1단계 데이터를 계속 쓴다면 개설자의 `LEADER`·`ACTIVE` 가입 정보를 먼저 추가한다.

- 스터디 생성 시 개설자의 `StudyMember`를 `LEADER`·`ACTIVE`로 함께 등록한다. 스터디 생성과 자동 가입은 같은 트랜잭션으로 처리한다.
- 다른 회원은 `MEMBER`·`ACTIVE`로 가입한다. `joinedAt`은 최초 가입 시각이다. 같은 회원·스터디 쌍의 중복 행을 허용하지 않는다.
- 스터디별 ACTIVE 멤버의 닉네임·역할과, 회원별 ACTIVE 가입 스터디 목록을 조회한다.
- 일반 멤버 탈퇴는 가입 행을 지우지 않고 `WITHDRAWN`으로 바꾼다. 중복 가입, 탈퇴 후 재가입, 리더 탈퇴는 409로 거절한다.

예: Java 스터디에 서연(LEADER), 민수(MEMBER)가 가입했다. 민수가 탈퇴하면 스터디의 활동 멤버 목록에는 서연만 남는다. 민수의 가입 행은 WITHDRAWN으로 보존되고, 민수의 내 스터디 목록에서는 Java 스터디가 제외된다.

### 3단계: 선택 심화

아래 기능 중 **하나 이상을 선택**한다. 재가입을 선택하면 2단계의 재가입 거절 규칙을 아래 규칙으로 확장한다.

- **정원 제한:** LEADER를 포함한 ACTIVE 인원이 정원 이상이면 신규 가입과 재가입을 모두 거절한다(`인원 >= 정원`). 정원 변경도 만든다면 현재 ACTIVE 인원보다 작게 줄이는 요청을 거절한다. 예: 정원 3명에 서연·민수·지우가 ACTIVE이면 네 번째 가입은 409다.
- **재가입:** WITHDRAWN인 기존 가입 행을 ACTIVE로 변경하고 새 행을 만들지 않는다. joinedAt은 최초 가입 시각을 유지한다.
- **리더 위임:** 같은 스터디의 다른 ACTIVE 회원에게 위임한다. 기존 리더를 MEMBER로, 새 리더를 LEADER로 같은 트랜잭션에서 변경하고 ACTIVE 리더 한 명을 유지한다. 위임을 마친 이전 리더는 탈퇴할 수 있다. Study.creator는 최초 개설자로 유지하고 현재 리더는 StudyMember.role로 판단한다.

추가 도전으로 동시 가입 때문에 정원을 초과하는 상황도 해결해 볼 수 있다.

### 제출

1·2단계는 기본 제출 범위이고 3단계는 선택 심화다. 기존 fork 저장소에 push하고 [공용 저장소](https://github.com/sesac-ddm-4-web/sesac-spring-boot-study)로 PR을 제출한다.

PR description에는 구현 단계와 선택 기능, 관계 방향·FK·UNIQUE, 트랜잭션 범위, 응답 DTO에서 고민한 점을 적는다. Security 자율 학습은 기본 제출 조건에 포함하지 않는다.
