# 2026-11-09 · Spring MVC·REST 응답·유효성 검사

## 진행 기준

오늘 수업은 17:00~18:00과 19:30~21:30으로 총 3시간입니다. 7일 개인 위시리스트 과제를 간단히 발표한 뒤, 교재 9장의 상품 API를 예로 Servlet·Spring MVC 요청 흐름과 HTTP 응답을 설명합니다. 이어서 10장의 유효성 검사·전역 예외 처리·오류 응답을 책과 함께 봅니다. 요청 주소·쿼리·본문을 받는 방법은 이미 배웠으므로 별도 문법 강의를 반복하지 않습니다. 강사 코딩 시연 없이 책의 실제 코드와 교육생의 구현을 읽고 연결합니다.

PPT는 핵심 개념과 흐름 그림, 책에서 볼 부분, 발표·QA·제출 안내를 담습니다. 긴 코드 설명은 책을 중심으로 진행합니다. 정확한 쪽수는 소지한 판본에서 확인합니다. 수업 참고 코드는 교재 원문 복제가 아닌 독립 예제입니다.

첫 시간에는 과제 발표와 공통 질문 정리를 진행합니다. 19:30 이후에는 Servlet·MVC 요청 흐름과 검증 핵심을 약 30~40분 설명한 뒤 구매 계획 구현과 QA에 약 70~80분을 확보하고 제출 안내로 마무리합니다. 수업 중 공통 목표는 1단계이며 필수 2단계의 남은 부분은 과제로 이어갑니다. 이는 강사용 운영 예시이고, 슬라이드에는 고정 교시나 발표 타이머를 두지 않습니다.

## 발표와 책 연결

- 11명 모두 자신이 구현한 기능, Domain·Service·Repository 역할, 직접 정한 규칙이나 해결한 문제를 공유합니다. 별도 발표용 PPT를 요구하지 않습니다.
- 9장의 상품 조회를 MVC 흐름의 예로 사용합니다. 이미 배운 입력 수신 어노테이션은 따로 재강의하지 않습니다.
- 상품 API가 아직 없다면 생성·조회 연결을 먼저 마칩니다. 미완료 교육생에게 검증까지 전부 완료했다고 기록하게 하지 않습니다.
- 10장은 도메인/Controller 검증, 전역 예외 핸들러, HTTP 응답 상태와 바디 순서로 읽습니다.

## Servlet과 두 컨테이너

Servlet은 컨테이너 안에서 요청을 받아 처리하고 응답을 만드는 Java 서버 구성 요소입니다. HttpServlet은 HTTP 요청 처리를 위한 기반 클래스이고 DispatcherServlet은 Spring이 제공하는 Servlet입니다. Servlet을 독립 실행형 웹 서버나 일반 Controller 메서드와 같은 것으로 설명하지 않습니다.

Tomcat은 서블릿 컨테이너로 HTTP 요청을 받아 요청·응답 객체를 준비하고 Servlet의 init·service·destroy 수명주기를 관리합니다. Spring 컨테이너는 Controller·Service·Repository 등의 빈을 생성하고 의존성을 주입합니다. 역할을 구분한 것이며 물리 서버 두 대나 완전히 배타적인 관리 대상을 뜻하지 않습니다. 수업의 Spring Boot 프로그램 안에서 둘이 함께 동작하고 DispatcherServlet도 Boot 설정으로 등록됩니다. Controller마다 Servlet을 새로 만들거나 HTTP 요청마다 새 Controller 빈을 생성하는 구조가 아닙니다.

HttpServlet의 service가 HTTP 메서드에 맞는 처리를 연결한다는 정도만 소개하고 raw Servlet이나 doGet 구현 실습은 진행하지 않습니다. 이후 Spring MVC가 대신 처리해 주는 요청 전달·인자 준비·반환값 처리와 연결합니다.

보충 근거: [Jakarta Servlet API](https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/Servlet.html), [DispatcherServlet API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/DispatcherServlet.html).

## MVC·레이어드·REST 구분

먼저 용어가 가리키는 관점을 구분합니다. MVC는 입력 처리·데이터와 업무·결과 표현의 역할 분리, Spring MVC는 HTTP 요청을 처리하는 웹 프레임워크, REST는 API 설계 방식입니다. REST와 Spring MVC를 서로 대신 선택하는 기술로 설명하지 않습니다. JSON을 응답한다고 REST의 모든 설계 조건을 충족하는 것도 아닙니다.

현재 상품 API의 HTTP 진입점은 Spring MVC가 처리하고, 애플리케이션 내부에서는 Controller·Service·Repository가 표현·업무·데이터 접근 책임을 나눕니다. 같은 Controller가 두 설명에 등장해도 모순이 아닙니다. MVC의 Model을 Service 하나 또는 Repository 하나와 일대일 대응시키지 않습니다. 레이어드는 논리적인 책임 분리이며 계층마다 물리 서버를 따로 둔다는 뜻이 아닙니다.

MVP·MVVM은 프레젠테이션 로직을 분리하는 다른 패턴의 이름과 핵심만 비교합니다. Presenter는 Model과 View 사이의 처리를 담당하고, ViewModel은 화면 데이터·상태를 제공해 바인딩으로 화면과 연결합니다. 바인딩에는 플랫폼 지원이나 구현이 필요합니다. 오늘 별도 패턴 구현 과제는 없습니다. 헥사고날·클린 아키텍처는 내부 의존 관계를 설계하는 다른 선택지로 질문이 있을 때만 소개하고, Spring WebFlux도 다른 웹 프레임워크라는 정도만 구분합니다. 현업 전체의 기술 사용 비율을 단정하지 않습니다.

HTML 화면을 렌더링하는 경우와 JSON 본문을 반환하는 경우 모두 Spring MVC의 요청 처리 구조를 사용할 수 있습니다. 전자는 뷰 이름·Model을 통해 ViewResolver와 View로 화면을 만들고, 후자는 @ResponseBody 또는 @RestController의 반환값을 메시지 변환기로 본문에 씁니다. JSON을 MVC의 View 객체나 HTML 템플릿과 같은 것으로 설명하지 않습니다. REST는 JSON만 허용하는 방식이 아니며 @RestController도 JSON만 반환하도록 제한된 표시는 아닙니다.

보충 근거: [Spring MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html), [응답 본문 처리](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responsebody.html), [GUI 패턴 비교](https://martinfowler.com/eaaDev/uiArchs.html), [표현·도메인·데이터 계층](https://martinfowler.com/bliki/PresentationDomainDataLayering.html).

## MVC와 검증에서 짚을 점

MVC는 일반적인 어노테이션 Controller의 정상 요청을 기준으로 네 단계로 설명합니다.

1. DispatcherServlet은 요청 처리 전체를 조율하고, Controller는 선택된 상품 메서드에서 업무 처리를 시작합니다. 핸들러는 요청 처리 대상이며 이 예에서는 Controller 메서드입니다.
2. 애플리케이션 시작 시 RequestMappingHandlerMapping이 Controller 빈과 매핑 메서드 정보를 등록합니다. 표의 GET /products, GET /products/{id}, POST /products는 이해를 위한 요약이며 내부 구현이 단순한 문자열 표라는 뜻은 아닙니다.
3. GET /products/42가 오면 DispatcherServlet이 HandlerMapping에 문의합니다. HandlerMapping은 등록된 조건에서 GET /products/{id}를 찾아 ProductController 빈과 findById 메서드를 가리키는 정보를 돌려줍니다. 메서드 실행이나 상품 존재 여부 조회는 하지 않습니다. 실제 반환 정보에는 인터셉터를 포함한 실행 체인이 있을 수 있으나 그림에서는 생략합니다.
4. DispatcherServlet이 이 핸들러를 지원하는 HandlerAdapter에 실행을 위임합니다. 어댑터의 인자 해석기가 경로의 42를 long 인자로 준비하고 Controller 메서드를 호출하며, 반환값 처리와 JSON 변환도 연결합니다. 42는 설명용 예시이며 실제 실행에서는 생성된 id를 사용합니다.

요청마다 전체 Controller 클래스를 다시 검색하거나 새 Controller를 만든다고 설명하지 않습니다. HTTP 메서드와 경로 외에 헤더·미디어 타입 등도 매핑 조건이 될 수 있지만 세부 조건 강의는 생략합니다. 서블릿 컨테이너와 Spring의 빈 관리 역할도 구분합니다.

JSON 읽기와 요청 DTO 검증은 Controller 메서드를 실행하기 전에 일어날 수 있습니다. Service·Repository를 거쳐 얻은 결과는 응답 DTO와 메시지 변환기를 통해 JSON 본문으로 나갑니다. MVC의 Model을 Service 하나와 같은 뜻으로 단정하지 않습니다. @Controller도 @ResponseBody를 붙이면 본문을 반환할 수 있고, JSON API도 Spring MVC를 사용합니다. 유효성 검사 PPT는 책 10장 전환·검사 위치와 핵심 규칙·실패 응답 세 장으로 간단히 짚고, 세부 구현은 책을 보며 진행합니다.

입력 형식 검사, 도메인의 유효한 상태, 업무 처리 조건을 구분합니다. 요청 DTO 검사를 통과했다고 도메인의 규칙을 제거하지 않습니다. 이름의 필수 검사와 앞뒤 공백 정리는 별개입니다. 가격 누락과 0원을 구분하려면 요청 DTO는 Integer와 @NotNull·@Min(0)을 사용합니다. @Min만으로 null을 거부한다고 설명하지 않습니다. @NotBlank는 입력값을 trim해서 바꾸는 기능이 아닙니다.

검증 적용 전 build.gradle의 dependencies에 `implementation 'org.springframework.boot:spring-boot-starter-validation'`이 있는지 확인하고, 추가했다면 IDE에서 Gradle 프로젝트를 동기화합니다. 기존 Spring Boot 버전을 유지하며 Spring Boot 3·4의 `jakarta.validation.Valid`와 `jakarta.validation.constraints`를 사용합니다.

## 참고 코드와 응답 범위

기존 `Product`, `ProductRepository`, `MemoryProductRepository`, `ProductService`, 단위·주입/AOP 테스트를 보존합니다. 오늘의 보충 파일은 검증을 적용한 `CreateProductRequest`, `ProductController`, `ApiExceptionHandler`와 기존 `ProductResponse`입니다. 참고 파일 버튼은 마지막 슬라이드에만 배치합니다.

- 생성은 201·Location·상품 JSON, 목록과 단건 조회는 200으로 설명합니다. 생성 결과의 실제 id를 사용하며 id 연속성과 JSON 필드 순서는 가정하지 않습니다.
- 참고 예외 처리기는 요청 DTO 검증·JSON 읽기·도메인 입력 예외를 400, 상품 없음 예외를 404로 정리합니다.
- 이 참고 구현이 모든 경로의 404, 모든 매개변수 타입 오류, 예상하지 못한 500까지 같은 message JSON으로 통일한다고 설명하지 않습니다. 모든 예외를 400으로 바꾸지 않습니다.
- 업무 예외를 HTTP 상태로 바꾸는 것은 애플리케이션의 응답 설계입니다. 프레임워크가 모든 업무 오류를 자동 분류한다고 설명하지 않습니다.
- 메모리 저장소는 서버 재시작 시 초기화됩니다.

## 개인 과제 · 위시리스트 구매 계획

기존 개인 Fork의 `personal-project/`에서 구매할 여러 항목의 총액과 예산, 상태 변경 규칙을 다루는 기능을 추가합니다. 7일의 위시리스트·추천 규칙·테스트는 보존합니다. 새 프로젝트나 DB는 만들지 않으며 실제 결제·재고 처리는 요구하지 않습니다. 사전 단계로 자기 PR의 입력 누락·null·음수·0원 허용, 실제 HTTP 400/404, 도메인 보호와 실패 시 데이터 보존을 점검합니다. 개별 교육생의 이름과 문제를 공용 PPT에 공개하지 않습니다.

1·2단계는 필수이고 3단계는 선택입니다. 수업 중 공통 목표는 1단계 완료이며 2단계의 남은 부분은 과제로 이어갑니다. 마감은 별도 공지하고 임의 날짜를 정하지 않습니다.

### 1단계 · 구매 계획 생성

- 입력은 예산과 선택한 항목 id 목록입니다. 예산 누락·null·음수, null/빈 목록·4개 이상·중복/null id·없는 id를 거부합니다. 항목은 1~3개이며 예산 0과 무료 항목을 허용합니다.
- 가격은 서버의 실제 위시리스트에서 읽고 합계가 예산 이하여야 합니다. 합계는 long 연산으로 계산합니다. 실패하면 구매 계획을 저장하지 않습니다.
- 계획 id는 프로그램이 부여하며 처음 상태는 DRAFT입니다. 예산·선택 항목의 id/이름/가격·총액·남은 예산을 저장하고 조회할 수 있어야 합니다. 없는 계획 id는 명확한 오류로 처리합니다.
- 선택 항목의 이름과 가격은 성공한 생성·수정 당시의 복사본입니다. 이후 원본 항목이 변경·삭제돼도 기존 계획은 바뀌지 않습니다. 확정은 저장된 계획의 금액을 사용하고 현재 위시리스트 가격으로 재계산하지 않습니다.

### 2단계 · 수정·확정·취소

- DRAFT에서만 예산과 항목을 수정할 수 있습니다. 모든 생성 규칙을 다시 확인하고 성공할 때만 새 금액과 현재 항목 스냅샷을 반영합니다.
- DRAFT → CONFIRMED 또는 DRAFT → CANCELLED만 허용합니다. 확정·취소된 계획의 수정, 재확정·재취소, 확정 후 취소, 취소 후 확정은 거부합니다.
- 실패한 수정·상태 변경은 기존 계획의 모든 데이터와 상태를 그대로 유지합니다.

### 3단계 · 최적 조합 추천

- 후보는 최대 20개입니다. 20개를 넘으면 명확하게 거부하고 일부를 몰래 자르지 않습니다. 예산 규칙은 1단계와 같습니다.
- 서로 다른 1~3개 항목 중 예산 이하이면서 합계가 가장 큰 조합을 반환합니다. 가능한 조합이 없으면 빈 결과를 반환합니다. 예산 0과 무료 항목도 유효합니다.
- 예를 들어 6,000원·5,000원·4,000원에서 예산 9,000원이면 5,000원과 4,000원을 골라야 합니다. 같은 총액의 조합을 고르는 결정적인 기준은 직접 정해 README에 적습니다.

Controller는 HTTP 입출력, 구매 계획 Domain은 유효한 상태와 상태 변경 규칙, Service는 항목 조회와 계획 생성·수정의 진행, Repository는 저장·조회를 담당하도록 설계합니다. Repository 인터페이스와 메모리 구현, 생성자 주입을 활용합니다. API 경로와 요청·응답 계약은 교육생이 정해 문서화합니다. 새 프론트엔드는 필수가 아닙니다.

교육생이 정상·실패·경계 조건을 고려해 QA 체크리스트를 직접 만들고 실행합니다. 합계·상태 변경·실패 불변·스냅샷에 의미 있는 테스트를 추가하고 기존 테스트도 유지합니다. README에 설계 이유·API·QA 결과·문제와 수정 기록·단계별 완료/미완료 범위를 적습니다. 정답 알고리즘과 상세 QA 시나리오는 제공하지 않습니다.

기존 구현 브랜치에서 자율 이름의 작업 브랜치를 만들어 개인 origin에 Push합니다. 공용 저장소에 `[11/09][이름] 위시리스트 구매 계획` Issue 1개·PR 1개로 코드·테스트·README를 제출합니다. 검증 보완과 구매 계획을 하나의 개인 과제로 제출하며 검증 전용 중복 PR은 강제하지 않습니다. 원본 main을 base, 개인 Fork 작업 브랜치를 head로 선택하고 이전 PR과 이번 변경 범위를 링크합니다. 리뷰 수정은 같은 브랜치에 Push하고 강사는 병합 없이 PR·Issue를 닫습니다.

## 제출

기존 개인 Fork의 `product-api/`를 이어서 사용합니다. 독립 작업이면 공통 시작점에서, 이전 구현을 확장하면 해당 코드가 있는 작업 브랜치에서 새 브랜치를 만듭니다. 이름은 자율입니다. 조직 원본 `sesac-ddm-4-web/sesac-spring-boot-study`에 `[11/09][이름] 상품 API 검증과 예외 처리` Issue와 PR을 각각 1개 작성하고 코드·README를 함께 제출합니다. PR 본문에는 구현 범위, QA 결과, 관련 Issue `#번호`, 이전 PR 링크와 미완료 범위를 적습니다. 설명만 듣고 파일을 바꾸지 않았다면 학습 기록을 남기고, 변경이 생긴 범위를 추후 제출합니다. 빈 PR은 강제하지 않습니다.

PR의 base repository는 조직 원본, base는 main, head는 본인 Fork의 작업 브랜치입니다. 코드는 개인 origin에 Push합니다. 리뷰 수정도 같은 브랜치에 올리고, 강사가 확인을 마치면 병합 없이 PR과 Issue를 닫습니다. 제출 브랜치는 보존하며 원본 main을 pull해서 이전 개인 구현이 생긴다고 설명하지 않습니다. 라벨·담당자·마일스톤 관리 권한을 교육생에게 요구하지 않습니다. greeting-api/·personal-project/와 기존 루트 README 링크, Wrapper와 실행 파일을 보존하고 build/.gradle/IDE 파일·비밀값은 제외합니다.

## 다음 수업

12일에는 오늘의 검증·실패 응답을 실제 적용 상태에 맞춰 보완하고, 첫 웹 서비스의 요구사항·도메인·계층·API·테스트 설계로 이어갑니다.

## 슬라이드별 진행 메모

### 01. Spring MVC REST 응답 · 유효성 검사

슬라이드의 핵심 개념과 실제 코드를 책에서 연결합니다.

### 02. 수업 내용

요청 주소·쿼리·본문을 받는 방법은 지난 수업에서 다뤘으므로 문법 설명을 반복하지 않습니다. 오늘은 책의 상품 API를 예로 요청 처리의 내부 흐름과 실패 응답을 연결합니다.

### 03. 개인 과제 발표

11명이 각자 특징적인 구현과 고민을 짧게 공유합니다. 추천 정렬·원본 목록 보존·생성자 주입 등 교육생이 선택한 근거를 묻습니다. 이 발표는 지난 시간 과제의 확인이며 새 기능 구현을 요구하지 않습니다.

### 04. Servlet이 하는 일

Servlet은 Jakarta Servlet API의 구성 요소입니다. 서블릿 컨테이너는 초기화 init, 요청 처리 service, 종료 destroy의 수명주기를 관리합니다. HttpServlet의 service는 HTTP 메서드에 맞는 처리로 분기하며 여기서 doGet 등의 구현 실습은 하지 않습니다. DispatcherServlet은 FrameworkServlet과 HttpServletBean을 거쳐 HttpServlet을 상속하므로 Servlet입니다. 일반 어노테이션 Controller는 Servlet 인터페이스를 직접 구현한 객체가 아니라 Spring이 관리하는 빈이고 HandlerAdapter를 통해 메서드가 호출됩니다.

### 05. Tomcat과 Spring 컨테이너

Spring Boot 수업 예제는 내장 Tomcat을 사용합니다. Tomcat은 HTTP 연결과 요청·응답 객체 및 Servlet 실행을 관리하고, Spring 컨테이너는 Controller·Service·Repository 등의 객체를 빈으로 생성하고 의존성을 연결합니다. 역할을 구분한 그림이며 물리 서버 두 대를 뜻하지 않습니다. DispatcherServlet도 Spring Boot 설정에서 빈으로 등록될 수 있으므로 두 컨테이너의 관리 대상이 절대 배타적이라고 설명하지 않습니다. Servlet의 수명주기와 Spring 빈의 수명주기는 역할이 다릅니다.

### 06. Model · View · Controller

Model을 Service 클래스 하나와 일대일 대응시키지 않습니다. 화면을 렌더링하는 전통 MVC와 응답 본문을 쓰는 REST API의 처리 차이는 뒤의 Controller 비교에서 구분합니다. Repository는 저장·조회 책임을 갖습니다.

### 07. MVC · Spring MVC · REST

MVC라는 설계 관점과 Spring MVC라는 웹 프레임워크 이름을 구분합니다. REST는 Spring MVC 대신 고르는 프레임워크 이름이 아닙니다. REST의 전체 제약이나 성숙도 단계는 이번 보충에서 길게 다루지 않고 요청·응답과 자원을 설계하는 관점임을 연결합니다. Spring MVC를 쓰면서 REST 방식의 API를 개발할 수 있습니다.

### 08. MVC와 레이어드 아키텍처

수업 코드의 Controller·Service·Repository는 레이어드 구조의 한 예입니다. 실제 프로젝트의 계층 이름과 개수는 다를 수 있습니다. MVC의 Model은 Service나 Repository 클래스 하나와 같은 뜻이 아니며, 도메인 데이터와 업무 규칙을 포함하는 개념입니다. 계층 간 책임 분리와 의존 방향을 살펴보되 이 표가 모든 아키텍처의 유일한 구성을 뜻하지는 않습니다.

### 09. Spring MVC와 계층 구조 함께 사용

그림의 Controller는 같은 객체이며 Spring MVC와 레이어드 아키텍처 중 하나에만 속하는 것이 아닙니다. DispatcherServlet은 HandlerMapping·HandlerAdapter에 위임해 Controller를 호출하고 응답 처리를 조율합니다. Controller가 업무 처리를 위해 Service를 호출하며, Service가 Repository 인터페이스를 사용합니다. Spring MVC가 Service와 Repository를 자동으로 직접 호출하는 흐름으로 설명하지 않습니다. 이 조합은 오늘 수업의 Spring REST 백엔드 예이며 모든 회사가 동일한 구조라는 통계적 주장을 하지 않습니다. 헥사고날·클린 아키텍처는 내부 의존 관계를 설계하는 다른 관점으로 추가 질문 때만 소개합니다. 그 구조에서도 HTTP 진입점에 Spring MVC를 사용할 수 있습니다.

### 10. MVC · MVP · MVVM

MVC·MVP·MVVM은 화면과 프레젠테이션 로직의 분리를 설명할 때 비교하는 패턴들입니다. 구체적인 변형과 플랫폼에 따라 상호작용 방식은 다르므로 MVP에서는 View와 Model이 언제나 절대 직접 연결되지 않는다는 식의 보편 규칙을 암기시키지 않습니다. MVVM의 바인딩도 해당 플랫폼의 지원이나 구현이 필요하며 특정 프론트엔드 라이브러리를 무조건 MVVM이라고 단정하지 않습니다. 레이어드·헥사고날·클린 아키텍처와 이 세 패턴을 하나의 대체 목록처럼 설명하지 않습니다. 별도 구현 과제는 없습니다.

### 11. DispatcherServlet과 Controller

이후 그림은 일반적인 어노테이션 Controller의 정상 요청을 다룹니다. 서블릿 컨테이너는 예를 들어 내장 Tomcat이며 Spring 컨테이너의 빈 관리와 역할을 구분합니다. 핸들러는 요청 처리 대상의 일반 이름이고, 이 예에서는 Controller 빈과 메서드를 나타내는 HandlerMethod입니다. 모든 HandlerMapping이 Java 메서드만 반환하는 것은 아닙니다. GET /products/42의 42는 설명용 예시이며 실제 실행에서는 생성 결과의 id를 사용합니다. 필터·인터셉터·보안의 세부 체인은 오늘 필수 범위가 아닙니다.

### 12. Controller 메서드의 매핑 등록

RequestMappingHandlerMapping은 초기화 과정에서 어노테이션 Controller의 매핑을 찾아 Controller 빈과 메서드 정보를 등록합니다. 표는 이해를 위한 요약이며 내부 구현이 단순한 문자열 표라는 뜻은 아닙니다. 매핑 조건에는 경로·HTTP 메서드 외에도 params, headers, consumes, produces 등이 있을 수 있으나 오늘은 경로와 메서드에 집중합니다. 같은 경로라도 GET과 POST가 다르면 처리 메서드가 달라질 수 있습니다. 입력 수신 어노테이션 문법은 다시 강의하지 않습니다.

### 13. HandlerMapping으로 담당 메서드 찾기

① 서블릿 컨테이너를 거친 HTTP 요청이 DispatcherServlet에 도착합니다. ② DispatcherServlet이 HandlerMapping에 요청에 맞는 핸들러를 문의합니다. ③ 이 예의 HandlerMapping은 ProductController 빈과 findById 메서드를 가리키는 HandlerMethod를 포함한 실행 체인 정보를 돌려줍니다. 그림에서는 인터셉터 정보를 생략합니다. 경로의 42가 id 위치에 해당한다는 매칭 정보와, 이후 42를 long 인자로 변환해 넣는 과정은 구분합니다. 실제 상품 42의 존재 여부는 Service와 Repository가 확인합니다.

### 14. 요청에서 담당 메서드까지

그림의 ①~③을 문장으로 설명합니다. 실제 반환 형식은 HandlerExecutionChain이며 이 예에는 HandlerMethod가 담깁니다. 여기서는 인터셉터 세부를 생략합니다. 경로와 메서드뿐 아니라 매핑 조건이 더 있을 수 있으나 이미 배운 수신 문법을 반복하지 않습니다. 42는 설명용 값이며 실제 요청에서는 생성 결과의 id를 사용합니다.

### 15. HandlerAdapter로 Controller 호출

④ DispatcherServlet이 핸들러를 지원하는 HandlerAdapter를 선택하고 실행을 요청합니다. 어노테이션 Controller에서는 보통 RequestMappingHandlerAdapter를 사용합니다. ⑤ 이 어댑터의 인자 해석기가 경로의 42를 long 값으로 준비한 뒤 findById(42)를 호출합니다. JSON 본문이 있는 요청은 메시지 변환·검증이 메서드 호출 전에 연결됩니다. ⑥ 메서드는 Service와 Repository를 사용한 결과를 반환하고, 반환값 처리기가 응답 DTO를 메시지 변환기에 전달해 JSON 본문으로 쓸 수 있습니다. Controller가 HTTP 응답을 항상 직접 작성하거나 DispatcherServlet이 JSON을 직접 직렬화한다고 설명하지 않습니다. 그림의 42는 설명용이며 실제 요청에서는 생성된 id를 사용합니다.

### 16. 담당 메서드 실행과 응답

그림의 ④~⑥ 이후 반환값 처리를 문장으로 연결합니다. 일반 어노테이션 Controller의 HandlerAdapter는 RequestMappingHandlerAdapter이며 인자 해석기·반환값 처리기·HttpMessageConverter를 사용합니다. Controller 메서드 진입 전에도 변환·검증이 실패할 수 있습니다. DispatcherServlet은 HandlerExceptionResolver 등에 예외 처리를 위임하고 전역 예외 핸들러가 필요한 응답을 만들 수 있습니다. HTTP 응답을 View로 렌더링하는 경우는 뒤의 HTML·JSON 분기 그림에서 구분합니다.

### 17. JSON 변환과 입력 검증

JSON 변환은 HttpMessageConverter가 맡으며 JSON 변환 라이브러리를 이용합니다. Spring Boot와 Jackson 버전에 따라 구현 클래스가 달라질 수 있으므로 오늘은 역할을 설명합니다. @Valid가 적용된 요청 DTO의 검증은 일반적으로 Controller 메서드 실행 전에 수행됩니다. 로컬 Errors/BindingResult로 처리하는 변형은 오늘 범위 밖입니다.

### 18. 상품 업무 처리

7일 개인 과제의 역할 분리를 공통 상품 API와 연결합니다. 도메인 객체와 Service의 검증은 HTTP 이외의 경로로 생성·호출해도 의미가 있어야 합니다. 생성자 주입과 기존 인터페이스·단위 테스트·AOP 코드는 보존합니다.

### 19. Java 객체가 JSON 응답이 되는 과정

JSON 응답 본문은 직접 문자열을 이어붙여 만드는 방식으로 설명하지 않습니다. @ResponseBody 또는 @RestController의 반환값 처리를 통해 메시지 변환기가 응답 본문을 씁니다. 메시지 변환기의 인코딩·미디어 타입 협상 세부 사항은 추가 질문이 있을 때만 다룹니다.

### 20. REST API도 Spring MVC로 처리

그림은 Controller 반환값이 응답이 되는 두 방식을 비교합니다. 두 경우 모두 DispatcherServlet·HandlerMapping·HandlerAdapter가 요청 처리에 참여합니다. 화면 처리에서는 뷰 이름과 Model로 ViewResolver를 통해 View를 찾고 HTML을 렌더링할 수 있습니다. @ResponseBody나 @RestController의 본문 처리에서는 반환값 처리기와 HttpMessageConverter가 응답 DTO를 JSON 본문으로 씁니다. 따라서 REST API를 만들면 Spring MVC를 사용하지 않는다는 설명은 잘못입니다. JSON을 MVC의 View 객체나 HTML 템플릿과 같은 것으로 맞추지 않습니다. @Controller도 @ResponseBody를 붙이면 본문을 반환하며, @RestController가 항상 JSON만 반환하는 것도 아닙니다. REST가 JSON만 허용하는 것은 아니고, ResponseEntity 없이 응답 DTO를 반환하는 것도 가능합니다. 프론트엔드의 HTML·JavaScript가 별도로 화면을 만들고 API의 JSON을 사용하는 구조와 서버의 View 렌더링을 구분합니다. Spring WebFlux는 다른 웹 처리 기술의 선택지이며, 모든 Spring Boot 프로젝트가 Spring MVC라는 뜻은 아닙니다.

### 21. 요청 DTO · 도메인 · 응답 DTO

새 DTO 작성 실습을 길게 반복하지 않고 교재 9장의 코드와 현재 구현을 대조합니다. DTO가 도메인의 모든 필드를 그대로 받을 필요는 없습니다. 예를 들어 상품 id는 서버가 부여하며 생성 요청의 임의 id를 그대로 신뢰하는 구조로 설명하지 않습니다.

### 22. ResponseEntity의 상태·헤더·본문

교재 상품 추가 Controller와 수업 참고 ProductController를 함께 봅니다. id가 1부터 시작하거나 연속된다고 가정하지 않습니다. ResponseEntity를 사용해야만 모든 JSON 응답이 가능하다고 설명하지 않습니다. 일반 응답 DTO 반환도 가능합니다.

### 23. 정상 응답과 실패 응답 구분

이 표는 오늘 상품 API의 응답 설계 기준입니다. 없는 상품의 404는 해당 예외에 대한 매핑을 구현해야 합니다. 프레임워크가 모든 업무 예외를 알아서 400/404로 분류한다고 설명하지 않습니다. HTTP 메서드 전체와 REST 성숙도는 별도 긴 강의로 확장하지 않고 필요한 질문만 연결합니다.

### 24. 유효성 검사와 예외 처리

교재 10장의 도메인 객체 및 컨트롤러 유효성 검사 추가하기, 전역 예외 핸들러 추가하기, HTTP 응답 상태 코드와 바디를 읽습니다. PPT는 핵심 구분만 짚고 세부 코드와 어노테이션 설정은 책으로 설명합니다. JSON 읽기나 요청 DTO 검증은 Controller 메서드 실행 전에 실패할 수 있습니다. 일반적인 예외는 MethodArgumentNotValidException·HttpMessageNotReadableException이며 모든 검증 경로가 같은 예외를 낸다고 설명하지 않습니다.

### 25. 입력 검증과 업무 규칙

입력 형식 검사와 도메인의 유효한 상태·업무 처리 조건을 구분합니다. @NotBlank는 null·빈 문자열·공백뿐인 문자열을 거부하지만 값을 trim해서 바꾸지는 않습니다. 요청 가격은 Integer로 누락과 명시적인 0을 구분하고 @NotNull·@Min(0)을 함께 사용합니다. @Min만으로 null을 거부한다고 설명하지 않습니다. @Valid가 요청 DTO의 제약을 실행하며 도메인 객체는 HTTP 이외의 경로에서도 자신의 규칙을 지킵니다. 검증 적용 전 dependencies의 implementation "org.springframework.boot:spring-boot-starter-validation"과 Gradle 동기화, jakarta.validation import를 확인합니다. 서비스 메서드 @Validated 등은 필수가 아닙니다.

### 26. 실패 이유에 맞는 응답

교재의 전역 예외 핸들러 부분을 보며 수업 참고 구현의 message 본문을 확인합니다. 요청 DTO 검증·JSON 읽기·수업 도메인의 입력 예외는 400, ProductNotFoundException은 404로 연결합니다. 업무 예외를 HTTP로 매핑하는 것은 애플리케이션 설계이며 프레임워크가 모든 업무 오류를 자동 분류하지 않습니다. 이 참고 핸들러가 모든 경로404·매개변수타입오류·예상하지못한500까지 같은message JSON을 보장하지 않습니다. 모든 IllegalArgumentException이 항상 클라이언트 오류라는 일반 규칙으로 설명하지 않습니다. 500을 catch(Exception)으로 잡아 모두400으로 바꾸지 않습니다. 내부 상세는 서버에서 진단하고 사용자용 오류에는 필요한 정보만 담습니다.

### 27. 위시리스트 구매 계획

PR 정적 검토에서 기본 이름·가격 검증은 이미 대부분 구현되어 있으므로 같은 검증을 처음부터 반복시키지 않습니다. 교육생은 자기 코드의 누락·null 처리와 실제 HTTP 오류 상태, 도메인 규칙 및 실패 후 데이터 보존을 먼저 점검합니다. 학생 이름이나 개별 PR의 결함을 PPT에 공개하지 않습니다. 기존 위시리스트와 추천·테스트는 유지하고 구매 계획 기능을 추가합니다. 새 프로젝트·DB·실제 결제·재고 처리는 필수가 아닙니다. 1·2단계는 필수 과제이며 3단계는 추가 도전입니다. 마감은 별도 공지하며 임의의 날짜를 지정하지 않습니다.

### 28. 구매 계획 생성

id 목록의 각 원소가 null인 경우도 거부합니다. 모든 항목이 실제 존재하는지는 생성과 수정 때 확인합니다. 기존 추천은 개별 항목 가격을 예산과 비교했지만 이 기능은 선택한 항목의 총합을 예산과 비교합니다. 합계는 int로 먼저 더한 뒤 long으로 바꾸지 말고 long 연산으로 계산해 오버플로를 피합니다. 예산 0에서 무료 항목을 선택하는 계획은 유효합니다.

### 29. 구매 계획에 저장할 데이터

계획 목록 또는 단건 조회를 통해 저장한 내용을 확인할 수 있게 합니다. 계획 단건 조회와 수정·상태 변경에서 없는 계획 id는 명확한 오류로 처리합니다. 저장된 항목 정보는 스냅샷이며 원본 객체나 수정 가능한 목록을 그대로 공유하지 않도록 설계합니다. 확정은 계획에 저장한 금액을 기준으로 하며 원본 위시리스트의 현재 가격으로 다시 계산하지 않습니다. 수정 성공 때는 새로 선택한 현재 항목의 정보로 스냅샷을 교체합니다. id가 1부터 연속으로 생성된다는 가정은 하지 않습니다.

### 30. 구매 계획 수정·확정·취소

수정할 때는 예산·id 목록의 1단계 조건을 전부 확인하고 성공할 때만 새 금액과 항목 복사본을 반영합니다. 이미 확정한 계획을 취소하거나 취소한 계획을 확정하는 요청도 거부합니다. 실제 결제·배송·재고 감소·동시 요청 잠금은 요구하지 않습니다. 단순히 성공 응답을 보내는 것으로 끝내지 말고 저장된 상태와 데이터가 맞는지 확인합니다.

### 31. 구매 계획의 책임 분리

기존 위시리스트 기능과 개별 가격 기준 추천을 지우거나 바꾸지 않습니다. 현재 계층 구조와 인터페이스를 활용해 새 기능을 설계합니다. 코드 정답이나 고정 클래스 이름은 제공하지 않으며 상태 표현은 enum 등 의도를 드러내는 방식으로 선택합니다. 금액 합계와 스냅샷, 상태 규칙을 각각 어떤 객체가 지킬지 설명할 수 있어야 합니다. 새 프론트엔드는 필수가 아닙니다.

### 32. 예산을 가장 많이 쓰는 조합 추천

후보 20개를 넘으면 일부를 몰래 잘라 처리하지 않고 명확하게 거부합니다. 동일 항목을 여러 번 고르지 않습니다. 예산 0과 무료 항목도 허용하며, 하나 이상의 유효한 무료 조합이 있으면 추천할 수 있어야 합니다. 같은 총액의 조합은 항목 수·등록 순서·id 등 교육생이 정한 결정적인 기준으로 고르고 기록합니다. 비싼 순으로 단순 선택하는 방법이 항상 최적 조합을 보장하지 않는다는 점을 요구사항 예시로 설명하되 정답 알고리즘 코드는 제공하지 않습니다.

### 33. 구매 계획 QA와 PR 제출

정상·잘못된 입력·경계값·실패 시 데이터 보존을 고려해 교육생이 QA 항목을 직접 설계합니다. 고정된 상세 테스트 시나리오나 정답 체크리스트를 나눠주지 않습니다. 기존 테스트를 유지하면서 새 금액 계산·상태 전이·실패 불변·스냅샷에 의미 있는 테스트를 추가합니다. 1·2단계는 필수, 3단계는 선택이며 실제 완료 범위를 기록합니다. 개인 구현이 있는 브랜치에서 자율 이름의 브랜치를 만들고 개인 origin에 Push합니다. 조직 원본 sesac-ddm-4-web/sesac-spring-boot-study의 main을 base, 개인 Fork 작업 브랜치를 head로 PR을 제출합니다. 리뷰 수정은 같은 브랜치에 Push하고 강사는 병합 없이 PR·Issue를 닫습니다. 기존 검증 보완과 구매 계획 구현을 하나의 개인 과제로 제출하며 검증만을 위한 별도 중복 PR을 강제하지 않습니다.

### 34. 공용 저장소에 학습 결과 제출

조직 원본 https://github.com/sesac-ddm-4-web/sesac-spring-boot-study 에 Issue와 PR을 올립니다. base repository는 조직 원본, base는 main, head는 본인 Fork의 작업 브랜치입니다. 개인 origin에 Push하고 리뷰 수정도 같은 브랜치에 Push합니다. 원본 main에는 교육생 구현을 병합하지 않고 강사가 리뷰 후 PR·Issue를 닫습니다. 작업 브랜치는 보존하며 main을 pull해서 이전 개인 구현이 생긴다고 안내하지 않습니다. 라벨·담당자·마일스톤 관리 권한을 교육생에게 요구하지 않습니다. 실제 코드 변경이 없는 교육생에게 빈 PR을 강제하지 않습니다. greeting-api와 personal-project 및 기존 README 링크, Gradle Wrapper를 보존하고 빌드 결과물·IDE 파일·비밀값은 제외합니다.

### 35. 원본 PR 대상과 리뷰

개인 origin에 Push한 코드가 원본 PR의 head에 표시되는지 확인합니다. 원본 main에 교육생별 구현을 합치지 않습니다. 리뷰 전에 교육생이 PR을 닫거나 직접 병합하도록 안내하지 않습니다. 이전 제출 코드가 함께 포함되면 이전 PR 링크와 이번 변경 범위를 본문에 적습니다.

### 36. REST API 보완과 서비스 설계

12일에는 오늘 다룬 CH10 핵심 내용을 실제 적용 상태에 맞춰 보완하고, 뒤2시간의 첫 웹 서비스 설계로 이어갑니다. 단축 URL·주문 관리 등 교재 과제 기반 설계는 별도 안내를 따릅니다.

### 37. 교재와 보충 자료

교재가 주교재이며 아래 파일은 교재 원문을 복제한 것이 아닌 수업용 독립 참고 구현입니다. 실제 판본과 사용 중인 Spring Boot 버전의 차이를 확인하며 비교합니다. 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.
