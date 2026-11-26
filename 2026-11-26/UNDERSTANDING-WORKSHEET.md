# JPA 연관관계와 보안 개념 이해 확인

장표의 짧은 코드와 그림을 보고 결과를 설명한다. 필요한 질문만 골라 말로 답해도 된다. 별도 제출 문서는 아니다. 코드는 import·일부 필드·생성자·getter가 생략된 발췌이며, 설명용 ID를 실제 생성 ID로 가정하지 않는다. 관계 이해용 예시이며 과제의 Entity 구성과 서비스 규칙은 자율이다.

## ① ManyToOne · 다대일

Java 스터디(id=201)에 연관관계 복습(id=501), 쿼리 연습(id=502) 모임이 있다. SQL 스터디(id=202)에는 SQL 문제 풀이(id=503) 모임이 있다. DB는 `study_meetings.study_id`, Java는 `StudyMeeting.study`로 연결한다.

| 질문 | 내 설명 |
|---|---|
| 모임 일정에서 스터디는 왜 다대일 관계인가? | |
| `@JoinColumn(name = "study_id")`는 어느 테이블의 무엇을 매핑하는가? | |
| 이 관계의 주인은 Study 전체인가, StudyMeeting.study 필드인가? | |
| 새 모임 일정 객체에 study를 연결한 것과 DB에 저장한 것은 어떤 차이인가? | |

다대일 단방향에서는 `StudyMeeting.study` 하나로 소속 스터디를 연결·저장·탐색할 수 있다. FK와 관계 필드가 직접 대응하고, 처음에는 한쪽 참조만 관리하면 된다. 스터디 객체에서 모임 목록으로 직접 탐색할 필요가 생기면 역방향 목록을 추가한다. 목록 필드가 없어도 Repository에 `List<StudyMeeting> findByStudyId(Long studyId)`를 선언해 조회할 수 있다.

## ② OneToMany · 일대다

앞의 StudyMeeting.study를 유지하면서 스터디에 `@OneToMany(mappedBy = "study")` 목록을 추가한다.

모임 501의 `study`는 Java 스터디(201)를 가리키는데 SQL 스터디(202)의 `meetings`에도 같은 모임을 넣었다면 Java 참조가 불일치한다. DB의 `study_id`는 한 값만 저장하므로 쓰기 기준이 필요하다. 이 다대일 양방향 매핑에서는 `StudyMeeting.study`를 기준으로 하므로 DB 값은 201이다. SQL 목록에만 추가해도 202로 바뀌지 않는다.

양쪽 Java 참조를 수정해도 되며 서로 같은 소속을 나타내도록 함께 맞춘다. 편의 메서드는 양쪽 객체 상태를 맞추고, FK 쓰기는 주인 필드를 기준으로 한다.

10장에서는 Java 스터디의 모임 목록이 처음에 비어 있고 생성자는 meeting.study만 설정한다고 가정한다. ① new StudyMeeting(javaStudy, ...) 후에는 모임의 소속만 Java로 설정되고 현재 Java 목록은 비어 있다. ② javaStudy.getMeetings().add(meeting) 후에는 목록에도 같은 모임이 포함된다. FK는 주인인 meeting.study가 결정하며 목록 추가만으로 결정하지 않는다. 두 줄은 Java 상태를 설정하며, 새 모임의 저장은 별도다.


| 질문 | 내 설명 |
|---|---|
| 두 Java 참조가 다른 소속을 나타내면 JPA가 FK를 판단할 기준은 무엇인가? | |
| SQL 목록에만 모임을 넣었는데 주인 필드는 Java를 가리키면 DB study_id는 무엇인가? | |
| Java 참조는 두 방향인데 DB FK는 왜 하나인가? | |
| mappedBy에는 왜 study_id 대신 study를 쓰는가? | |
| 역방향 목록에만 모임 일정을 추가하면 FK 설정이 완료되는가? | |
| 주인 필드를 바꿔도 이미 읽은 반대 목록을 직접 맞춰야 하는 이유는? | |
| 별도 대안인 일대다 단방향에서 Study.meetings에 @JoinColumn을 두면 FK 쓰기 관리 기준은 어디인가? | |

일대다 단방향 대안은 StudyMeeting.study가 없는 별도 모델이다. 앞의 mappedBy 양방향 설정과 같은 필드에 동시에 적용하지 않는다. 주인은 모든 관계에서 무조건 다쪽이라는 뜻이 아니다.

관계의 실제 개수에 맞게 매핑한다. 다대일 단방향은 일대다 관계를 구현할 때의 좋은 출발점이며, 일대일·다대다를 모두 다대일 하나로 바꾸라는 뜻은 아니다.

## ③ OneToOne · 일대일

이번 예시는 `member_profiles.member_id`를 회원 FK로 선택하고 UNIQUE를 둔다. MemberProfile.member가 이 FK를 매핑한다. 서연 회원(id=101)의 프로필 행은 member_id=101로 연결된다.

| 질문 | 내 설명 |
|---|---|
| 같은 member_id를 가진 프로필 두 개를 저장하면 어떤 제약에 걸리는가? | |
| UNIQUE만으로 모든 회원에게 프로필이 자동 생성되는가? | |
| Member에서 역방향 profile을 추가한다면 mappedBy에는 무엇을 적는가? | |

## ④ ManyToMany · 다대다

서연(id=101)은 Java 스터디(id=201), 민수(id=102)는 Java 스터디와 SQL 스터디(id=202)에 참여한다. DB 연결 테이블에는 `(101, 201)`, `(102, 201)`, `(102, 202)` 세 행이 필요하다.

| 질문 | 내 설명 |
|---|---|
| @ManyToMany + @JoinTable은 무엇을 저장하며 이 예시의 주인은 어느 필드인가? | |
| 가입한 시각을 저장하려면 연결 Entity가 더 적합한 이유는? | |
| StudyMember.member와 StudyMember.study는 각각 어떤 관계이고 어느 FK를 매핑하는가? | |
| 가입 Entity에 id가 있어도 (member_id, study_id) UNIQUE를 추가하는 이유는? | |
| 새 스터디 가입을 만들 때 새로 저장할 객체는 Study인가, StudyMember인가? | |

직접 @ManyToMany를 쓰는 모델과 연결 Entity 모델은 대안이다. 한 서비스에 같은 가입 관계를 중복 매핑하라는 예제가 아니다. 양쪽 객체 참조, cascade, 응답 DTO, LAZY·N+1은 관계의 개수와 별도로 판단한다.

## 객체지향 설계: 책임·참조·캡슐화

스터디 종료 시 예정된 미래 모임을 취소하는 기능을 예로 든다. Study는 자기 상태와 종료 가능 여부를, StudyMeeting은 자기 일정의 취소 조건을 판단한다. Service는 필요한 조회·권한 확인 조율·작업 순서와 트랜잭션 경계를 준비한다. Repository는 조회와 저장을 담당한다. 하나의 설계 예시이며, 업무 책임과 FK 쓰기 기준인 연관관계의 주인은 별개다.

| 질문 | 내 설명 |
|---|---|
| 여러 곳에서 setStatus를 호출하는 대신 cancelIfUpcoming(now)에 규칙을 모으면 무엇이 좋아지는가? | |
| Study가 모임들에 직접 취소 판단을 요청한다면 meetings 참조가 유용한 이유는? | |
| 목록 화면에 검색·페이징을 제공하려는 요구만으로 Entity의 양방향 목록이 꼭 필요한가? | |
| Service가 모임을 조회하고 각 객체의 메서드를 호출하는 설계에서도 책임을 나눌 수 있는가? | |

예시의 취소 규칙은 예정 상태이며 시작 시각이 현재보다 뒤인 모임만 취소하는 것이다. 객체 메서드 호출은 Java 상태를 바꾼다. DB 반영은 영속 상태와 트랜잭션을 함께 확인한다. 객체의 책임에 필요한 참조만 두며, 양방향이면 양쪽 참조를 맞춘다. 양방향 자체가 더 객체지향적이거나 조회 SQL을 줄이는 것은 아니다. 많은 모임의 처리는 별도 조회·일괄 처리도 검토한다.

## Security 기초와 요청 흐름

기능을 만들었다면 누가 사용하고 수정할 수 있는지도 정한다. 인증은 사용자가 누구인지, 인가는 해당 요청을 허용할지 확인하는 일이다. 그림의 화살표를 따라 설명한다.

| 질문 | 내 설명 |
|---|---|
| 로그인한 회원이라도 모든 스터디의 모임을 수정할 수 없는 이유는? | |
| 세션 로그인에서 브라우저 쿠키와 서버 세션에는 각각 무엇이 있는가? | |
| 다음 요청에서 서버는 세션 ID를 받아 무엇을 확인하는가? | |
| Filter를 사용하면 Controller마다 공통 처리를 반복하는 일을 어떻게 줄일 수 있는가? | |
| Filter와 HandlerInterceptor는 요청 처리의 어느 위치에 있는가? | |
| preHandle보다 먼저 HandlerMapping이 결정하는 것은 무엇인가? | |
| preHandle이 false라면 다음 처리는 어떻게 되며 필요한 응답은 누가 처리하는가? | |
| REST 응답 본문 수정에 postHandle을 쓰지 않는 이유는? | |
| 정상 동기 요청에서 자신의 preHandle이 true였던 Interceptor의 afterCompletion은 언제 실행되는가? | |
| 보안 Filter의 확인을 통과하지 못한 요청도 반드시 Controller까지 가는가? | |
| SSO에서 중앙 로그인 상태를 활용해도 앱마다 권한을 확인해야 하는 이유는? | |

Spring Security는 경로에 맞는 SecurityFilterChain 하나를 선택하고 그 안의 여러 Filter를 순서대로 실행한다. 장표는 주요 역할만 묶은 개념 흐름이다. MVC의 Interceptor만으로 보안을 대체하지 않는다.

## Security 자율 학습

프로젝트 버전에 맞는 공식 문서를 참고해 기본 로그인, 세션으로 로그인 상태 이어가기, 경로별 접근 허용 순서로 확인한다. 예를 들어 스터디 조회는 공개, 참여는 로그인 필요, 모임 수정은 해당 스터디 운영자만 허용하도록 구분해 볼 수 있다. 데이터에 따른 운영자 권한도 확인한다. Security 구현은 아래 과제의 필수 조건이 아니다.

## JPA 과제: 스터디 모집·모임 관리 서비스

회원들이 스터디를 만들고 참여하며 모임 일정을 관리하는 새 REST API 프로젝트를 만든다. 핵심 기능은 회원·프로필 관리, 스터디 개설·조회, 참여·탈퇴와 참여 목록 조회, 스터디별 일정 등록·조회다.

Entity 구성·필드·API는 직접 설계한다. 일대일, 일대다/다대일, 여러 회원과 여러 스터디의 관계를 JPA로 표현하고 관계 방향·FK와 가입 정보를 어떻게 다룰지 결정한다. 중복 참여·정원·탈퇴 등의 서비스 규칙도 스스로 정한다. 여력이 있다면 재가입·스터디장 위임 등 원하는 기능을 확장한다.

새 Spring Boot 프로젝트에서 JPA로 DB에 저장한다. 기존 fork 저장소의 자율 이름 폴더에 추가하고 [공용 저장소](https://github.com/sesac-ddm-4-web/sesac-spring-boot-study)로 PR을 제출한다. 기존 프로젝트는 보존하며 프로젝트 구조·API·브랜치 이름은 자율이다.

PR에는 구현 기능, Entity 관계도, 관계와 트랜잭션 설계 이유, 직접 정한 서비스 규칙을 적는다. 로그인·프론트는 선택이며 테스트 코드 구현은 필수가 아니다. Security 자율 학습은 별도로 진행한다.

## 객체지향 설계 참고

- [Martin Fowler: Domain Model](https://martinfowler.com/eaaCatalog/domainModel.html) — 데이터와 업무 동작을 함께 표현하는 객체 모델
- [Martin Fowler: Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html) — 도메인 객체의 동작과 Service의 조율 책임을 생각해 볼 참고 글

## MVC Interceptor 참고

정상 동기 요청에서는 HandlerMapping이 handler와 Interceptor를 선택한 뒤 preHandle이 실행된다. true면 HandlerAdapter를 통해 Controller 처리를 계속하고, false면 중단하므로 필요한 응답은 직접 처리한다. 정상 반환 후 postHandle, MVC 처리 완료 뒤 afterCompletion으로 이어진다. afterCompletion은 해당 Interceptor의 preHandle이 true였을 때 호출된다. REST의 응답 본문은 postHandle 전에 처리되므로 본문 수정 용도로 사용하지 않는다. 비동기 요청의 별도 동작은 이 예시에서 다루지 않는다.

- [Spring Framework: Interception](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/handlermapping-interceptor.html)
- [Spring Framework 6.2.1: HandlerInterceptor API](https://docs.spring.io/spring-framework/docs/6.2.1/javadoc-api/org/springframework/web/servlet/HandlerInterceptor.html)
