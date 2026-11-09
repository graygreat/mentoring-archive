from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
HEADER='''# 2026-11-09 · Spring MVC·REST 응답·유효성 검사

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

12일에는 오늘의 검증·실패 응답을 실제 적용 상태에 맞춰 보완하고, 첫 웹 서비스의 요구사항·도메인·계층·API·테스트 설계로 이어갑니다.

## 슬라이드별 진행 메모

'''
notes='\n\n'.join(f"### {i+1:02}. {d['title'].replace('<br>',' ')}\n\n{d['note'] or '슬라이드의 핵심 개념과 실제 코드를 책에서 연결합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(HEADER+notes+'\n')
print('Instructor guide generated')
