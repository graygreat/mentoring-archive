# 2026-11-09 · Spring MVC·REST 응답·유효성 검사

## 진행 기준

오늘 수업은 17:00~18:00과 19:30~21:30으로 총 3시간입니다. 7일 개인 위시리스트 과제를 간단히 발표한 뒤, 교재 9장의 상품 API를 예로 Servlet·Spring MVC 요청 흐름과 HTTP 응답을 설명합니다. 이어서 10장의 유효성 검사·전역 예외 처리·오류 응답을 책과 함께 봅니다. 요청 주소·쿼리·본문을 받는 방법은 이미 배웠으므로 별도 문법 강의를 반복하지 않습니다. 강사 코딩 시연 없이 책의 실제 코드와 교육생의 구현을 읽고 연결합니다.

PPT는 핵심 개념과 흐름 그림, 책에서 볼 부분, 발표·QA·제출 안내를 담습니다. 긴 코드 설명은 책을 중심으로 진행합니다. 정확한 쪽수는 소지한 판본에서 확인합니다. 수업 참고 코드는 교재 원문 복제가 아닌 독립 예제입니다.

첫 시간에는 과제 발표와 공통 질문 정리를 진행합니다. 19:30 이후에는 Servlet·MVC 요청 흐름과 검증 핵심을 약 30~40분 설명한 뒤 외부 상품 연동 구현과 QA에 약 70~80분을 확보하고 제출 안내로 마무리합니다. 수업 중 공통 목표는 1단계이며 필수 2단계의 남은 부분은 과제로 이어갑니다. 이는 강사용 운영 예시이고, 슬라이드에는 고정 교시나 발표 타이머를 두지 않습니다.

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

## 개인 과제 · 외부 상품 연동과 장바구니

기존 개인 Fork의 `personal-project/`에서 상품 검색·찜·장바구니·쿠폰 계산을 구현합니다. 수동 등록·조회·추천과 기존 테스트는 유지합니다. 새 프로젝트·DB·로그인·실제 결제는 요구하지 않습니다. 먼저 자기 PR의 입력 누락·null 처리, HTTP 400/404, 도메인 보호와 실패 후 데이터 보존을 보완합니다. 개별 교육생의 이름이나 결함을 공용 PPT에 공개하지 않습니다.

1·2단계 필수, 3단계 선택입니다. 수업 중 공통 목표는 1단계이며 2단계는 과제로 이어서 완성합니다. 마감은 별도 공지합니다. 외부 HTTP 통신을 처음 접하므로 API 주소·JSON 응답을 먼저 확인하고 기존 계층에 어느 책임을 추가할지 교육생이 정리하게 합니다. 특정 HTTP 클라이언트나 완성 코드는 강제하지 않습니다.

### 외부 API 호출 예시 진행

Spring Boot 4.x·Java 17·Spring Web 기준으로 RestClient를 사용합니다. DummyJsonProduct는 외부 JSON을 받을 record DTO이며 가격은 BigDecimal로 받습니다. record는 값을 묶는 Java 문법이고, @JsonIgnoreProperties(ignoreUnknown = true)는 DTO에 선언하지 않은 외부 필드를 무시하는 설정입니다. Jackson 3에서도 이 어노테이션의 import는 com.fasterxml.jackson.annotation.JsonIgnoreProperties입니다.

DummyJsonClient의 생성자에서 기준 주소 https://dummyjson.com, 연결 제한 3초와 읽기 제한 5초를 설정합니다. get → uri → retrieve → body 호출을 따라 읽으며 body에서 실제 요청과 JSON 변환이 수행됨을 설명합니다. retrieve만 호출하면 네트워크 요청을 마친 것으로 설명하지 않습니다. 기본 4xx·5xx 예외는 외부 404와 그 밖의 장애를 구분하는 데 사용합니다. 빈 응답 본문·변환 실패·통신 장애는502, 외부 상품 없음은404입니다. 오류 본문은 프로젝트의 기존 예외 처리 설정에 따릅니다.

전체 파일 버튼의 세 클래스를 기존 개인 프로젝트에 추가합니다. package는 본인의 SpringBootApplication 클래스와 같은 패키지 또는 하위 패키지로 바꾸고 새 시작 클래스는 만들지 않습니다. 서버를 실행해 GET http://localhost:8080/examples/external-products/1을 요청하면 Controller 생성자에 주입된 DummyJsonClient가 외부 GET을 수행합니다. 포트를 변경했다면 URL도 맞춥니다. 기존 /products 요청과 외부 https://dummyjson.com/products 요청은 서로 다른 서버의 주소입니다.

교육생이 예시를 읽고 자신의 서버로 호출하게 합니다. 강사 시연은 필수가 아닙니다. 이 조회 예시에서 출발해 검색과 목록으로 확장하고, 가져오기 Service에서 저장 전 외부 상품 필드·범위를 검사하며 가격 환산·중복 검사·장바구니는 스스로 구현하게 합니다. HTTP 클라이언트 자체가 과제의 모든 상품 검증까지 대신한다고 설명하지 않습니다. 자동 테스트는 실제 인터넷 대신 외부 Client 대역이나 로컬 서버를 사용합니다.

공식 근거: https://docs.spring.io/spring-framework/reference/integration/rest-clients.html 및 https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/http/client/JdkClientHttpRequestFactory.html.

### 외부 데이터와 가격 기준

[DummyJSON 공식 문서](https://dummyjson.com/docs/products)와 상품 목록·검색·단건 응답을 확인합니다. 필요한 필드는 id·title·price·category·thumbnail·stock입니다. 실제 데이터에는 최소 주문 수량 등 이번 소매 장바구니 규칙과 다른 값도 있으므로 discountPercentage·minimumOrderQuantity는 사용하지 않습니다. 상품 수·id·재고를 고정값으로 가정하지 않습니다. 요청 흐름은 브라우저 → 내 Spring 서버 → DummyJSON이며 내 서버도 외부 호출에서는 클라이언트 역할입니다. 쿠폰·배송비·수량·가격 환산은 API 제공자의 정책이 아닌 과제 규칙입니다. API의 추가·수정·삭제는 영구 저장이 아닌 모의 동작이므로 교육생 데이터는 자신의 메모리 저장소에 둡니다.

가격은 과제용 고정 기준 1 API 가격 단위 = 1,000원으로 변환합니다. 실제 환율이나 API 통화에 대한 단정이 아닙니다. BigDecimal로 곱하고 원 미만 HALF_UP 반올림, 기존 정수 가격 범위 확인, 수량 곱셈·합계는 long 연산으로 처리합니다. 9.99는 9,990원입니다. 외부 stock은 가져온 당시의 참고 값이며 외부에서 차감하거나 예약하지 않습니다.

### 1단계 · 상품 검색과 찜

- Spring 서버가 외부 목록·검색·상세를 호출하고 자체 API로 응답합니다. 목록·검색은 limit 기본10·1~20, skip 기본0·음수 거부입니다. 검색어 누락·공백은400, 검색 결과 없음은200·빈 목록입니다.
- 외부 id만 받아 서버가 상세를 재조회하고 이름·원화 가격·카테고리·이미지·재고를 가져옵니다. 내 id·외부 id·출처를 구분하고 같은 외부 상품의 중복 찜은409로 거부합니다. 품절 상품도 찜은 가능합니다.
- 가져온 값은 저장 시점의 복사본입니다. 자동 동기화는 필수가 아니며 외부 상품의 이름·가격을 임의 요청값으로 수정하는 것은 거부합니다. 수동 등록 상품의 기존 수정 동작은 보존합니다.
- 외부 상품 없음404, 지연·통신 실패502를 구분하고 유한한 연결·응답 대기 시간을 설정합니다. 필수 필드가 없거나 사용할 수 없는 외부 데이터도502로 응답하고 저장하지 않습니다. 외부 실패 시 일부 데이터도 저장되지 않아야 합니다.

### 2단계 · 장바구니와 쿠폰

서버에 메모리 장바구니 하나를 둡니다. 내 항목 id로 추가하고 목록·수량 변경·삭제를 제공합니다. 수량1~5, 최대20종류이며 같은 항목을 추가하면 수량을 합산합니다. 누락·null·0·음수·6 이상 수량은400입니다. 없는 항목404, 합산 수량·재고·종류 수 한도 충돌409입니다. 외부 상품은 저장된 stock을 초과할 수 없고 수동 등록 상품은 외부 재고 제한이 없습니다. 품절 항목은 장바구니에 담을 수 없습니다.

첫 추가 때 이름·가격·재고를 복사하고 이후 같은 항목 추가·수량 변경은 장바구니에 저장한 복사본을 사용합니다. 원본 수정·삭제가 기존 장바구니를 바꾸지 않습니다. 추가는 위시리스트 항목이 있어야 하고, 기존 장바구니 수량 변경·삭제는 장바구니 항목 id로 가능해야 합니다. 삭제 후 다시 담을 때는 그 시점 위시리스트 값을 복사합니다. 모든 조건 확인 후 변경하고 실패하면 모든 기존 값을 유지합니다.

쿠폰은 금액 미리보기 요청의 couponCode로만 받습니다. 생략 시 NONE, null·모르는 코드·사용 조건 불충족은400입니다. 선택 상태·사용 횟수는 저장하지 않으며 장바구니 변경은 쿠폰 조건과 무관합니다. NONE은 할인 없음, PERCENT10은 상품 합계10%·원 미만 버림·최대20,000원, FIXED15000은 할인 전 합계100,000원 이상일 때15,000원 할인입니다. 한 번에 하나만 적용합니다.

상품 합계 → 쿠폰 할인 → 할인 후 상품 금액 → 배송비 → 최종 금액 순서로 계산합니다. 할인 후 금액100,000원 이상은 무료 배송, 미만은5,000원입니다. 빈 장바구니는 NONE만 허용하고 모든 금액이0원입니다. 응답에서 쿠폰 코드·각 금액을 구분하고 실제 결제·재고 차감은 하지 않습니다.

합계110,000원 예시: NONE 최종110,000원, PERCENT10은11,000원 할인 후99,000원+배송5,000원=104,000원, FIXED15000은95,000원+배송5,000원=100,000원입니다. 할인액과 최종 금액을 혼동하지 않도록 설명합니다.

### 3단계 · 쿠폰 추천과 AI 화면

NONE과 사용 가능한 두 쿠폰의 배송비 포함 최종 금액을 비교합니다. 최종 금액이 같으면 NONE → PERCENT10 → FIXED15000 순서입니다. 빈 장바구니는 NONE·0원이며 추천으로 장바구니가 변하지 않습니다.

빠르게 끝냈다면 AI로 검색·찜·장바구니·금액 미리보기 화면을 만듭니다. HTML·CSS·순수 JavaScript만 사용하고 외부 라이브러리와 JS·CSS CDN은 사용하지 않습니다. 상품 이미지는 DummyJSON의 이미지 URL을 사용할 수 있습니다. 프롬프트는 자율이며 화면은 본인 Spring API를 호출합니다. 프론트는 추가 과제입니다.

### 설계·검증·제출

Controller는 HTTP·DTO, Domain은 수량·쿠폰·배송비·금액 규칙, Service는 외부 조회·가져오기와 처리 흐름, Repository는 저장·조회, 별도 외부 API 클라이언트는 통신을 담당합니다. 인터페이스와 메모리 구현, 생성자 주입을 사용하고 API 경로·요청·응답은 직접 설계해 README에 기록합니다. 외부 주소는 고정 DummyJSON이며 임의 URL 입력 기능은 만들지 않습니다.

QA 체크리스트는 직접 만들고 실행합니다. 상세 입력값·정답 시나리오는 제공하지 않습니다. 금액·쿠폰 경계·실패 후 데이터 보존·복사본 보존을 확인하는 의미 있는 테스트를 추가하고 기존 테스트를 유지합니다. 외부 성공·실패는 테스트용 대체 구현으로 재현해 인터넷 응답에 의존하지 않게 합니다. README에 실행법·API·가격/쿠폰/배송비 기준·설계·QA/테스트 결과·수정 기록·단계별 완료/미완료 범위를 기록합니다.

기존 구현에서 자율 이름의 브랜치를 만들어 개인 origin에 Push합니다. 공용 저장소에 `[11/09][이름] 외부 상품 연동과 장바구니` Issue1개·PR1개로 코드·테스트·README를 제출합니다. 검증 보완도 같은 과제에 포함합니다. 조직 main을 base, 개인 Fork 작업 브랜치를 head로 선택하고 이전 PR과 변경 범위를 링크합니다. 리뷰 수정은 같은 브랜치에 Push하고 강사는 병합 없이 PR·Issue를 닫습니다. 제출 브랜치는 보존합니다.

## 제출

기존 개인 Fork의 `product-api/`를 이어서 사용합니다. 독립 작업이면 공통 시작점에서, 이전 구현을 확장하면 해당 코드가 있는 작업 브랜치에서 새 브랜치를 만듭니다. 이름은 자율입니다. 조직 원본 `sesac-ddm-4-web/sesac-spring-boot-study`에 `[11/09][이름] 상품 API 검증과 예외 처리` Issue와 PR을 각각 1개 작성하고 코드·README를 함께 제출합니다. PR 본문에는 구현 범위, QA 결과, 관련 Issue `#번호`, 이전 PR 링크와 미완료 범위를 적습니다. 설명만 듣고 파일을 바꾸지 않았다면 학습 기록을 남기고, 변경이 생긴 범위를 추후 제출합니다. 빈 PR은 강제하지 않습니다.

PR의 base repository는 조직 원본, base는 main, head는 본인 Fork의 작업 브랜치입니다. 코드는 개인 origin에 Push합니다. 리뷰 수정도 같은 브랜치에 올리고, 강사가 확인을 마치면 병합 없이 PR과 Issue를 닫습니다. 제출 브랜치는 보존하며 원본 main을 pull해서 이전 개인 구현이 생긴다고 설명하지 않습니다. 라벨·담당자·마일스톤 관리 권한을 교육생에게 요구하지 않습니다. greeting-api/·personal-project/와 기존 루트 README 링크, Wrapper와 실행 파일을 보존하고 build/.gradle/IDE 파일·비밀값은 제외합니다.

## 다음 수업

다음 수업인 11월 12일에는 교재 11장 「상품 관리 애플리케이션에 데이터베이스 연동하기」를 진행합니다. 메모리 저장과 DB 저장의 차이, 테이블·행·열·기본키와 SQL을 먼저 짚고 상품 추가·조회·수정·삭제를 데이터베이스에 연결합니다. Controller·Service·Repository의 역할을 유지하며 저장소 접근이 어떻게 달라지는지 책 코드로 확인합니다. DB가 데이터를 유지하는지는 실제 저장 설정에 따라 다르므로 메모리 DB와 영구 저장을 구분합니다.

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

### 27. 외부 상품 연동과 장바구니

기존 위시리스트에 외부 상품 가져오기와 장바구니를 추가하는 확장 과제입니다. 별도 새 프로젝트·DB·실제 결제·재고 예약은 요구하지 않습니다. 먼저 자기 PR의 입력 누락/null 처리, 실제 400/404 응답, 도메인 규칙과 실패 시 데이터 보존을 보완합니다. 1·2단계는 필수, 3단계는 선택이며 마감은 별도로 공지합니다. 교육생 이름이나 개별 코드 문제를 공용 PPT에 표시하지 않습니다.

### 28. DummyJSON 상품 검색과 조회

공식 문서 https://dummyjson.com/docs/products 에서 목록·검색·상품 상세 응답을 확인합니다. Spring 서버도 외부 API에 HTTP 요청을 보낼 때는 클라이언트입니다. 브라우저가 DummyJSON을 직접 호출하는 대신 본인 Spring 서버의 검색·가져오기 API를 사용하도록 연결합니다. HTTP 클라이언트 종류와 내부 API 경로는 교육생이 정하되 연결·응답 시간 제한을 설정합니다. 외부 데이터와 id별 값은 바뀔 수 있으므로 특정 상품 id의 제목·가격·재고를 고정값으로 채점하지 않습니다. 이 과제는 실제 쇼핑몰이나 실시간 가격 변동 알림 기능이 아닙니다.

### 29. 외부 호출 예제 준비

각 파일 이름 버튼에서 package·import·오류 처리까지 포함한 전체 코드를 확인합니다. package com.example.product는 예시이므로 자신의 @SpringBootApplication 클래스가 있는 패키지와 같거나 그 하위로 세 파일 모두 수정합니다. Spring Boot 4와 Java 17, Spring Web를 기준으로 합니다. 프로젝트에 이미 존재하는 Application 클래스나 기존 API를 삭제하지 않습니다. 이 세 파일은 외부 상세 조회 연결 예시이며 검색·목록·위시리스트 저장·환산·장바구니의 완성 답안은 아닙니다.

### 30. JSON 응답을 담는 DTO

파일 전체 코드 버튼에 package와 import가 있습니다. record는 Java 17에서 사용할 수 있는 데이터 운반용 클래스 문법으로, 생성자와 id(), title(), price() 같은 접근자를 자동으로 제공합니다. DTO 필드 이름은 외부 JSON 키와 맞춥니다. DummyJSON 응답에는 discountPercentage 등 더 많은 필드가 있어도 ignoreUnknown=true로 무시합니다. 가격을 받은 직후 아직 수업용 원화 환산이 된 값은 아닙니다. 환산·검증·저장은 이후 과제로 구현합니다.

### 31. RestClient로 GET 요청

전체 DummyJsonClient에는 @Component, RestClient 생성, 기준 주소 https://dummyjson.com, 연결 제한 3초와 응답 제한 5초가 포함되어 있습니다. 생성자의 JDK HttpClient와 JdkClientHttpRequestFactory는 유한한 시간 제한을 설정하기 위한 구성입니다. findById는 양수가 아닌 id를 400으로 거부하고 외부 404를 404, 다른 외부 오류·네트워크 장애·시간 초과·빈 본문을 502로 바꿉니다. 여기서는 핵심 4줄을 먼저 읽고 나머지 설정·예외 처리는 전체 코드와 함께 봅니다. RestClient가 응답 JSON을 읽는 작업과 내 Controller가 DTO를 JSON 응답으로 쓰는 작업은 서로 다른 HTTP 통신입니다.

### 32. 내 서버에서 외부 상품 조회

전체 ExternalProductExampleController에는 @RestController와 @RequestMapping("/examples/external-products"), DummyJsonClient를 받는 생성자가 있습니다. Spring이 Client 빈을 Controller 생성자에 주입합니다. localhost 주소를 열면 내 서버가 외부 API를 호출하고, 외부 JSON을 DTO로 읽은 뒤 자신의 JSON 응답을 반환합니다. 브라우저에서 dummyjson.com/products/1을 직접 여는 것은 외부 서버에 바로 요청하는 것이므로 이 예제의 내 Controller와 Client를 거치지 않습니다. 외부 상품의 실제 제목·가격·재고는 바뀔 수 있으므로 특정 값이 고정되어 있다고 가정하지 않습니다. 현재 예제는 외부 상세 조회만 제공하며 내 위시리스트에 저장하지 않습니다.

### 33. 외부 상품을 내 위시리스트에 저장

사용자가 보낸 임의의 상품 이름·가격·재고를 신뢰하지 않고 외부 상세 응답에서 읽습니다. 외부 데이터의 식별자는 sourceType과 externalId로 보존하고, 로컬 항목 id는 프로그램이 부여합니다. 외부 id와 로컬 id가 우연히 같아도 같은 의미로 취급하지 않습니다. 가져온 항목의 이름·가격은 읽기 전용이며 수동 등록 상품은 기존 기능대로 수정할 수 있습니다. 원본 외부 가격이나 재고가 이후 변해도 저장한 위시리스트 값을 자동으로 바꾸지 않습니다. 재고가 0인 상품은 관심 목록에 보관할 수 있지만 장바구니에는 담을 수 없습니다. 가져오기에 실패하면 항목을 일부만 저장하지 않습니다.

### 34. 외부 가격을 수업용 원화로 환산

double로 곱해 소수점 오차를 만든 뒤 형변환하지 않도록 주의합니다. JSON 숫자를 BigDecimal로 읽거나 원래 소수 표현을 보존하는 방식으로 변환합니다. 실제 외부 가격 단위의 통화를 단정하거나 환율 API를 새로 연결하지 않습니다. 외부 discountPercentage는 반영하지 않습니다. 생성·합산 과정에서 정수 오버플로가 발생하지 않도록 금액 연산 타입을 확인하고, 처리할 수 없는 외부 응답은 저장 전에 거부합니다. 특정 외부 상품이 항상 price 9.99라고 가정하지 않습니다.

### 35. 장바구니에 상품 담기

외부 상품의 수량 제한은 1~5와 저장된 재고 중 더 작은 한도를 따릅니다. 예를 들어 stock이 2인 외부 상품은 수량 3으로 담지 못합니다. 이미 있는 항목의 중복 추가도 합산 후 수량과 처음 복사한 stock을 기준으로 검사합니다. stock 0이면 장바구니 추가를 거부합니다. 수동 상품은 stock 제한만 없고 공통 수량 1~5 및 최대 20종 제한은 적용합니다. 기존 줄에 대한 추가는 상품 종류 수를 늘리지 않습니다. 외부 minimumOrderQuantity는 과제 규칙에 적용하지 않습니다.

### 36. 장바구니 조회·수량 변경·삭제

장바구니 조회에서 행 id, 원본 로컬 id, 이름·단가·수량과 계산에 필요한 값을 확인할 수 있게 합니다. 외부 상품 정보는 실시간 동기화하지 않습니다. 같은 로컬 상품을 다시 추가할 때도 기존 장바구니 줄의 복사본을 덮어쓰지 않습니다. 단, 추가 요청 자체는 원본 로컬 위시리스트 항목이 실제로 존재해야 합니다. 원본이 삭제된 뒤 기존 줄의 수량을 바꾸는 것은 장바구니 행 id로 처리하므로 허용합니다. 행을 삭제한 뒤 다시 추가하려면 원본이 존재해야 하며 그 시점의 값을 복사합니다. 조회 응답이나 수정 가능한 참조를 통해 저장 데이터가 외부에서 바뀌지 않게 설계합니다.

### 37. 쿠폰 할인 규칙

PERCENT10 할인은 원 단위 정수에서 소수 부분을 버리고 20,000원 상한을 적용합니다. FIXED15000의 사용 조건은 할인 전 상품 합계이며, 배송비 무료 조건은 다음 페이지의 할인 후 금액 기준입니다. 요청 코드가 알 수 없거나 사용 조건을 만족하지 않으면 400으로 거부하고 장바구니는 변경하지 않습니다. 할인 후 금액은 상품 합계에서 할인을 뺀 값이며 최종 금액은 할인 후 금액에 배송비를 더한 값입니다. 미리보기는 요청마다 받은 couponCode로 계산하는 기능이며 선택 쿠폰을 상태로 저장하지 않습니다.

### 38. 배송비와 최종 금액

금액 계산은 상품별 단가×수량을 합쳐 subtotal을 만들고, 쿠폰 할인 discount를 계산해 discountedSubtotal=subtotal-discount, 마지막에 shipping을 더해 finalAmount를 계산합니다. 무료배송 경계는 원래 상품 합계가 아니라 할인 후 금액입니다. 예시의 PERCENT10은 99,000원에 배송비 5,000원을 더하고 FIXED15000은 95,000원에 5,000원을 더합니다. 빈 장바구니에서 배송비 5,000원을 붙이지 않으며 NONE 이외 쿠폰 요청은 400으로 거부합니다. 이 표는 계산 요구사항 예시이고 학생용 상세 QA 체크리스트를 대신하지 않습니다.

### 39. 실패 응답과 데이터 보존

입력 수량 0·음수·누락 등 입력 형식과 범위 오류는 400, 이미 담긴 수량과 합쳤을 때 5를 넘거나 재고를 초과하는 등 상태·재고 충돌은 409로 구분합니다. 최대 20종을 넘기는 추가도 409입니다. 외부 API 자체가 상품 없음으로 응답하면 404, 연결 장애나 시간 초과 등으로 정상 상세 값을 얻지 못하면 502로 구분합니다. 예외를 모두 400으로 덮지 않습니다. 무한 대기하지 않도록 HTTP 클라이언트의 연결·응답 시간 제한을 유한하게 설정합니다. 모든 검사를 통과한 뒤 저장 상태에 반영하며 일부 필드나 수량만 먼저 바꾸지 않습니다.

### 40. 외부 호출과 업무 규칙 분리

HTTP 클라이언트 종류는 공식 API 문서와 사용 중인 Spring 버전의 문서를 보고 자율적으로 선택합니다. 프론트엔드는 외부 DummyJSON 주소가 아니라 본인 Spring 서버의 API를 호출합니다. 외부 클라이언트의 입출력과 예외를 애플리케이션 규칙에 맞게 다루고, 외부 상품 DTO와 내부 위시리스트·장바구니 객체를 구분합니다. 기존 클래스 이름이나 패키지를 모두 바꾸도록 강제하지 않고 현재 구조를 확장합니다. 새 외부 라이브러리나 DB는 필수가 아닙니다.

### 41. 최저 금액 쿠폰과 AI 화면

사용할 수 없는 쿠폰은 비교 후보에서 제외하고 NONE을 반드시 포함합니다. 쿠폰 추천 결과는 쿠폰 코드와 금액 근거를 반환하되 장바구니나 선택 쿠폰을 저장하지 않습니다. 빈 장바구니는 NONE과 금액 0이 추천됩니다. 추가 기능을 완료한 교육생은 검색·가져오기·장바구니·금액 미리보기 화면을 만들 수 있습니다. AI가 작성한 화면도 직접 실행하고 자신의 서버와 연동한 동작을 설명해야 합니다. 외부 라이브러리와 JavaScript·CSS CDN은 사용하지 않습니다. DummyJSON thumbnail의 상품 이미지 URL은 사용할 수 있습니다. 별도 AI 프롬프트 예시는 제공하지 않으며 화면 구성과 프롬프트는 자율입니다. 프론트엔드는 선택 과제입니다.

### 42. 설계 확인 체크리스트

발표와 PR 작성 전 본인 코드에서 각 항목의 위치와 동작 근거를 확인합니다. 단순히 체크 표시만 채우는 대신 실제 구현과 테스트 결과로 설명합니다. 외부 Client 대역은 고정 응답·실패를 돌려주는 가짜 구현이나 모의 객체를 뜻하며 자동 테스트에서 실제 외부 네트워크를 호출하지 않습니다. 기존 테스트를 삭제해 새 테스트만 통과시키지 않습니다.

### 43. 장바구니 QA와 PR 제출

정상·잘못된 입력·경계 조건·외부 장애·실패 후 데이터 보존·장바구니 복사본 보존을 고려해 교육생이 QA 체크리스트를 직접 작성합니다. 상세 정답 시나리오를 배포하지 않습니다. 기존 테스트를 보존하고 할인·배송비 계산, 수량·재고 규칙, 실패 시 변경 없음, 복사본 유지에 의미 있는 테스트를 추가합니다. 자동 테스트에서는 별도 외부 Client를 대역으로 바꿔 실제 외부 네트워크를 호출하지 않습니다. 1·2단계는 필수, 3단계는 선택이며 실제 완료 범위를 적습니다. 기존 구현 브랜치에서 자율 이름의 브랜치를 만들고 개인 origin에 Push합니다. 조직 원본 sesac-ddm-4-web/sesac-spring-boot-study의 main을 base, 개인 Fork 작업 브랜치를 head로 PR을 제출합니다. 리뷰 수정은 같은 브랜치에 Push하고 강사는 병합 없이 PR·Issue를 닫습니다. 사전 검증 보완과 새 기능을 하나의 개인 과제로 제출하며 유효성 검사 전용 중복 PR을 강제하지 않습니다.

### 44. 공용 저장소에 학습 결과 제출

조직 원본 https://github.com/sesac-ddm-4-web/sesac-spring-boot-study 에 Issue와 PR을 올립니다. base repository는 조직 원본, base는 main, head는 본인 Fork의 작업 브랜치입니다. 개인 origin에 Push하고 리뷰 수정도 같은 브랜치에 Push합니다. 원본 main에는 교육생 구현을 병합하지 않고 강사가 리뷰 후 PR·Issue를 닫습니다. 작업 브랜치는 보존하며 main을 pull해서 이전 개인 구현이 생긴다고 안내하지 않습니다. 라벨·담당자·마일스톤 관리 권한을 교육생에게 요구하지 않습니다. 실제 코드 변경이 없는 교육생에게 빈 PR을 강제하지 않습니다. greeting-api와 personal-project 및 기존 README 링크, Gradle Wrapper를 보존하고 빌드 결과물·IDE 파일·비밀값은 제외합니다.

### 45. 원본 PR 대상과 리뷰

개인 origin에 Push한 코드가 원본 PR의 head에 표시되는지 확인합니다. 원본 main에 교육생별 구현을 합치지 않습니다. 리뷰 전에 교육생이 PR을 닫거나 직접 병합하도록 안내하지 않습니다. 이전 제출 코드가 함께 포함되면 이전 PR 링크와 이번 변경 범위를 본문에 적습니다.

### 46. 데이터베이스 연동

다음 수업인 11월 12일에는 교재 CHAPTER 11 상품 관리 애플리케이션에 데이터베이스 연동하기를 진행합니다. 데이터베이스를 사용하는 웹 애플리케이션, 데이터베이스 다뤄 보기, 상품 추가 기능 구현하기, 상품 조회/수정/삭제 구현하기 순서로 책과 기존 상품 API를 연결합니다. DB 기본 용어와 간단한 SQL부터 설명하고 메모리 저장소의 데이터 접근 코드를 DB에 연결합니다. 영구 저장은 실제 저장 설정을 전제로 설명하며 메모리 DB도 서버를 끄면 데이터가 사라질 수 있음을 구분합니다. 구체적인 DB 제품·라이브러리·설정은 교재와 기존 프로젝트 버전에 맞춥니다.

### 47. 교재와 보충 자료

교재가 주교재이며 아래 파일은 교재 원문을 복제한 것이 아닌 수업용 독립 참고 구현입니다. 실제 판본과 사용 중인 Spring Boot 버전의 차이를 확인하며 비교합니다. 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.
