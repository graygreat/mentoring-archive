# 2026-11-07 토요일 · 객체 연결과 MVC 진행 참고

## 운영 기준

공식 배정은 핵심 개념 6시간과 MVC 2시간, 총 8시간입니다. 1교시는 수업 45분과 휴식 15분이며 점심은 별도입니다. 교재 1~8장 복습은 5일 앞부분에 먼저 끝내고, 오늘은 필요한 Java와 요청 흐름만 짧게 다시 연결합니다.

개념은 먼저 설명하고 실습은 후반에 모읍니다. 코딩 시연 없이 요구사항 안내 → 멘티 자율 구현 → 결과 확인·피드백으로 진행합니다. 파일 전체 코드는 실습 해설·비교용이며, 실습과 정답 없는 추가 과제를 구분합니다. 강사와 동시에 타이핑하거나 완성 프로젝트를 받아 실행하는 방식은 전제하지 않습니다.

## 교시별 배분

| 교시 | 공식 배정 | 중심 내용 | 순수 수업 |
| --- | --- | --- | --- |
| 1 | 핵심 개념 | 교재 연결, IoC·DI·컨테이너·빈·생성자 주입 | 45분 |
| 2 | 핵심 개념 | 스코프·공유 상태·스타터·자동 설정·AOP | 45분 |
| 3 | MVC | 서버·클라이언트, MVC, DispatcherServlet과 핸들러 연결 | 45분 |
| 4 | MVC | 계층별 책임, 화면/본문 응답, 흐름 그리기 | 45분 |
| 5 | 핵심 개념 적용 | Initializr·Product·저장소 계약과 구현 | 45분 |
| 6 | 핵심 개념 적용 | Service·Java 예외·단위 테스트 | 45분 |
| 7 | 핵심 개념 적용 | AOP 의존성·TimingAspect·제공 연결 테스트 | 45분 |
| 8 | 핵심 개념 적용 | 자율 실습 마무리 20분 + 결과 피드백 25분 | 45분 |

핵심 개념과 그 적용은 6교시, MVC는 2교시입니다. 실제 진행 순서는 핵심 개념 2교시 → MVC 2교시 → 실습·피드백 4교시입니다. 설명·구조 활동 180분, 자율 실습 155분, 피드백 25분으로 총 360분입니다. GitHub 문서와 추가 과제는 수업 후 정리하도록 안내합니다.

## 교재 연결과 진도 경계

- 5일: 교재 1~8장 복습을 먼저 끝내고 Initializr와 간단한 GET을 경험합니다.
- 오늘 9장 일부: 상품 객체·컬렉션·저장과 조회입니다. 교재의 List와 수업 예제의 Map을 비교합니다. 수업 예제는 교재 본문을 재현한 코드가 아닙니다.
- 오늘 12장 일부 선행: 인터페이스·생성자 DI·단위 테스트를 연결합니다. 실제 Memory 구현은 mock이 아닙니다.
- 9일 4시간: 같은 product-api에 Web 의존성·DTO·Controller·JSON/Jackson·정상 요청과 REST 설계를 추가합니다.
- 12일 앞 2시간: 10장과 Validation·오류 응답·실패 사례·면접 포인트를 연결합니다.
- 12일 뒤 2시간: 13/14장 문제 중 단축 URL을 공통 문제로 사용해 요구사항·도메인·API·테스트를 설계합니다. 주문 관리는 비교·확장용입니다.
- 14일: 설계한 CRUD 구현·테스트 6시간, JPA 소개 2시간입니다. 교재 11장 DB는 이후 DB/JPA 진도와 연결합니다.

오늘의 MVC는 구조 이해 범위입니다. Controller 작성, Postman, 요청·응답 DTO, 요청 검증 어노테이션과 HTTP 상태 검증은 후속 수업에서 진행합니다. HTML 뷰와 응답 본문은 개념 차이를 구분합니다.

## 작성 파일과 의존성

공통 환경은 Java 17, Spring Boot 4.1.2, Gradle-Groovy, Group com.example, Artifact product, Package com.example.product입니다. Initializr의 선택 의존성은 비워 두고, 기본 starter와 생성된 테스트 의존성·런처·useJUnitPlatform을 유지합니다. AOP 단계에서 spring-boot-starter-aspectj를 추가합니다. Web과 Validation은 각각 9일과 12일에 추가합니다.

메인 소스는 ProductApplication, Product, ProductRepository, MemoryProductRepository, ProductNotFoundException, ProductService, TimingAspect의 7개입니다. 테스트는 ProductServiceTest와 ProductWiringTest입니다. 생성된 ProductApplicationTests도 보존합니다. 전체 소스는 14줄 이하 청크로 나누며 원본 공백을 유지합니다.

ProductServiceTest는 new로 직접 조립하는 단위 테스트 3개입니다. ProductWiringTest는 제공 틀입니다. @Autowired로 Service를 받고 AopUtils.isAopProxy를 확인한 뒤 상품 생성·단건·목록 조회를 검증합니다. @SpringBootTest(webEnvironment=NONE)을 사용하므로 웹 서버 없이 빈 연결과 AOP를 확인하며 이후 Web 의존성이 추가돼도 재사용할 수 있습니다. 실행용 CommandLineRunner나 seed는 추가하지 않습니다.

제공 테스트 4개와 생성된 contextLoads를 보존했다면 총 5개입니다. 기본 starter만 있는 main은 웹 서버를 열지 않고 정상 종료할 수 있습니다. 포트 접속 대신 테스트로 성공을 확인합니다. 0ms 로그도 정상이며, 출력이 숨겨지면 IDE 테스트 콘솔이나 Gradle --info에서 확인합니다.

## 실습과 추가 과제

실습 완료 기준은 생성·목록·단건 조회, 잘못된 이름·가격의 Java 예외, 없는 id의 ProductNotFoundException, 단위 테스트 3개와 주입·AOP 테스트 1개입니다. 없는 상품을 HTTP 404로 응답하는 것은 12일 범위입니다.

과제 1은 가격 0, 이름 공백 정리, null·공백 이름, 실패 후 상태 보존을 테스트하는 기초 과제입니다. 과제 2는 Service.findByMaxPrice(int)의 조건 조회와 경계값 테스트입니다. 상한 0·같은 가격·결과 없음·음수·저장 원본 보존을 확인합니다. 정답 코드를 제공하지 않으며 HTTP 구현은 요구하지 않습니다. 실패 후 id 번호 연속성을 완료 조건으로 두지 않습니다.

추가 과제는 수업 후 별도 수행할 수 있으며 마감은 별도 안내합니다. HTTP 이름 검색·가격 필터·수정·삭제는 후속 REST/CRUD 진도에 연결합니다.

## GitHub 제출

Public 저장소 sesac-spring-boot-study의 main에 greeting-api와 product-api를 누적합니다. 상세 clone·Initializr 복사 절차는 자료에 추가하지 않았습니다. 날짜마다 새 저장소를 만들지 않습니다. Wrapper를 포함하고 build/.gradle/.idea와 비밀값을 제외합니다. 루트 .gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar와 기존 greeting-api 예외를 보존합니다.

필수 Issue·병합 PR은 2개입니다.

- practice/product-core: [실습] 상품 객체·저장소·Service와 테스트
- docs/product-core: [문서] 상품 객체 구조와 테스트 기록

추가 과제는 test/product-boundaries, feature/core-price-filter에서 각각 작업합니다. 수행 과제마다 Issue·병합 PR을 1개씩 추가합니다. 완료 실습을 나중에 기록하면 Issue에 결과 정리임을 명시합니다. 최신 main → Issue·브랜치 → 구현·검증 → PR → 자체 확인·병합 → main pull 순서입니다. 타인 승인은 강제하지 않습니다. Closes에는 실제 Issue 번호를 씁니다. Milestone은 product-core-2026-11-07이며 마감일은 별도 안내 전 미지정입니다.

루트 README는 목차와 기존 프로젝트 링크를 보존합니다. product-api/README는 소개·환경·실행/테스트·구현 현황·객체 기능(API는 9일 예정)·Wiki 링크의 여섯 항목입니다. Wiki는 Home, 01-Setup, 02-Architecture, 03-API, 04-Verification, 05-Retrospective를 재사용하고 프로젝트별 내용을 누적합니다. 03-API에는 오늘 미구현·9일 예정, 04-Verification에는 단위·연결 테스트·AOP 로그·과제 근거를 기록합니다. Wiki는 코드 PR과 별도이므로 문서 PR에 실제 링크와 작성 확인을 남깁니다.

## 검증 범위와 리허설

source/verify.py는 오늘의 소스 9개만 게시되는지, 미래 REST 답안 제외, 목차 순서, 고유 ID, 14줄 소스 청크 공백 완전 일치, Java 코어 실행과 JS 구문을 확인합니다. 별도 리허설에서는 Java 17·Spring Boot 4.1.2에서 기본 starter와 AspectJ만 사용하고 Web·Validation 없이 clean build를 실행해 통과했습니다. 제공 테스트 4개와 Initializr의 contextLoads를 포함한 총 5개 테스트가 통과했습니다. 주입된 Service의 AOP 프록시와 실제 시간 로그도 확인했습니다. 브라우저에서는 97장 전체의 콘텐츠 경계를 검사해 넘침 0건을 확인했으며 코드 화면도 시각적으로 확인했습니다.

위 결과는 개정된 7일 단계만 따로 실행한 근거입니다. 이전의 전체 상품 API 12파일 리허설에서 확인한 HTTP 성공과 구분합니다. Windows·멘티별 환경과 추가 과제 학생 답안은 별도 확인이 필요합니다.

## 슬라이드별 진행 참고

### 02. 개념 전체 → 자율 실습 → 피드백

공식 배정은 핵심 개념 6시간과 MVC 2시간입니다. 실제 진행은 핵심 개념 2교시 → MVC 2교시 → 핵심 개념 적용 실습·피드백 4교시로 모아 운영합니다. 각 교시는 수업 45분 + 휴식 15분, 점심 별도입니다. 시연 없이 요구사항 안내 → 멘티 구현 → 결과 확인·피드백으로 진행합니다.

### 03. 이번 주 교재를 나누어 봅니다

책의 장 순서를 모두 오늘 끝낸다는 뜻이 아닙니다. 같은 상품 프로젝트를 단계별로 확장합니다. 책 9장 List와 수업 Map을 구분하고, 12장의 객체지향·테스트 일부를 먼저 연결합니다. 책 11장 DB는 이후 DB/JPA 진도와 연결합니다.

### 04. List로 관리한 상품을 Map으로

교재 예제를 그대로 옮긴 코드가 아닙니다. 같은 요구를 다른 자료구조로 표현한 독립 예제입니다. List가 틀린 구현이라는 뜻은 아닙니다.

### 05. 오늘은 객체와 테스트를 완성합니다

HTTP 서버나 Controller 없이 완료할 수 있습니다. Java 예외와 HTTP 상태 코드는 구분합니다. 오늘의 없는 상품 처리는 ProductNotFoundException 발생까지입니다.

### 06. 실습 예제와 별도 과제는 다릅니다

강사의 코딩 시연은 하지 않습니다. 완성 예제는 비교·해설 자료이며 직접 작성할 파일 범위를 표시합니다. 막히면 힌트를 주고 여러 명의 공통 오류만 짧게 설명합니다.

### 08. 직접 만들기와 전달받기

생성자 주입은 일반 Java에서도 가능합니다. Spring은 이를 컨테이너의 빈 생성·연결에 적용합니다.

### 16. @Bean은 메서드의 반환 객체를 등록

이 코드를 추가하려면 MemoryProductRepository의 @Repository를 제거해야 같은 역할을 이중 등록하지 않습니다. Configuration과 Bean의 import는 org.springframework.context.annotation입니다. 이 예시는 필수 프로젝트에 작성하지 않습니다.

### 17. 등록 · 범위 · 타입을 확인합니다

Qualifier나 Primary는 후보를 의도적으로 여러 개 사용할 때 확장합니다. 초반에는 후보를 하나로 유지합니다. 빈 이름 암기보다 오류 메시지의 required type과 후보 수를 읽게 합니다.

### 18. 여러 요청이 Service 하나를 공유합니다

JVM 전체에 모든 클래스 객체가 하나라는 뜻이 아닙니다. 컨테이너가 다르거나 같은 클래스의 빈 정의가 여러 개면 객체도 달라질 수 있습니다. 요청 스코프 등은 이름만 소개하고 구현하지 않습니다.

### 19. 요청별 값은 지역 변수로 다룹니다

Repository의 저장소는 의도적으로 공유하는 상태입니다. 공유 상태와 요청별 임시 값을 구분합니다. 이번 메모리 구현은 ConcurrentHashMap과 AtomicLong을 사용하되 트랜잭션이나 영속성을 제공하지 않습니다.

### 20. IoC와 DI를 자신의 코드로 설명

예시 답변: ProductService가 ProductRepository에 의존하며 Spring이 구현 빈을 전달합니다. 인터페이스를 기준으로 받으므로 Service를 유지하면서 저장 구현이나 테스트용 객체를 바꿀 수 있습니다.

### 22. 함께 사용하는 라이브러리 묶음

스타터는 의존성 묶음입니다. 클래스가 생기는 것과 빈이 등록되는 것은 다릅니다. Web 스타터와 Validation은 9일·12일에 필요해질 때 추가합니다.

### 28. 프록시를 통과하는 호출을 비교

개념 설명 뒤 집중 실습에서 프로젝트와 Aspect를 작성하고, 제공된 Spring 연결 테스트로 적용을 확인합니다. 이 표는 Spring의 기본 프록시 기반 AOP에 대한 설명이며 AspectJ weaving까지 일반화하지 않습니다. final/private 제약은 질문이 나오면 설명합니다.

### 29. 자동 설정과 AOP를 설명해 봅시다

답변은 정의 암기보다 오늘의 dependencies·TimingAspect·주입 코드를 근거로 하게 합니다. DI와 AOP는 서로 다른 개념이며 DI 자체가 모든 메서드 호출을 가로채는 것은 아닙니다.

### 32. 연결·업무·저장 책임을 구분합니다

DispatcherServlet이 모든 업무와 저장을 직접 수행하지 않습니다. Service와 Repository는 애플리케이션이 설계하는 역할입니다.

### 34. DispatcherServlet이 흐름을 조율합니다

DispatcherServlet은 프런트 컨트롤러입니다. HandlerMapping에서 담당 핸들러 정보를 찾고 HandlerAdapter에 실행을 위임합니다. 상세 확장점 구현은 하지 않습니다.

### 37. HTML 화면과 응답 본문

일반적인 Controller의 뷰 반환과 본문 반환을 개념적으로 구분합니다. 템플릿 설정이나 반환값 처리 코드까지 구현시키지 않습니다.

### 39. 상품 요청 흐름을 말로 그려봅니다

코딩 시연이나 새 Controller 작성 없이 진행하는 구조 활동입니다. MVC 2교시 안에서 개념 설명·책 코드 읽기·질문·이 활동을 함께 진행합니다.

### 41. 테스트용 구현으로 바꿀 수 있습니다

Memory 구현 자체는 mock이 아닙니다. 인터페이스와 생성자 DI 덕분에 이후 fake 또는 mock으로 바꿀 수 있다는 연결까지만 합니다.

### 43. Initializr에서 본인 프로젝트 생성

리허설 기준 공통 4.1.2를 사용하고 미리보기는 제외합니다. Spring Boot 4.x Java 17 조건과 starter 이름은 공식 문서 기준입니다. 시작 클래스명은 ProductApplication으로 생성됩니다. AOP 의존성은 뒤에서 한 줄 추가합니다.

### 44. 파일은 모두 같은 패키지에서 시작

첫 실습은 프로젝트 생성과 객체 연결에 집중합니다. 요청 DTO·Controller는9일, 검증과 예외 응답은12일에 추가합니다. 새 파일 생성 시 package와 class 틀이 이미 있으면 참고 코드로 전체를 교체하거나 중복 부분을 제거합니다.

### 45. 기본 실행·테스트 의존성을 유지

이 부분만으로 build.gradle 전체를 덮어쓰지 않습니다. 생성된 테스트 런처 의존성 등도 유지합니다. 오늘은 Web·Validation 선택이 필요하지 않습니다. 테스트 의존성과 JUnit Platform 설정을 삭제하지 않습니다.

### 46. ProductApplication.java · 1/1

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 48. Product.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 49. Product.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 51. ProductRepository.java · 1/1

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 52. id를 키로 상품을 찾습니다

고급 동시성 알고리즘을 가르치는 시간이 아닙니다. 빈에서 공유하는 저장 상태를 다루기 위한 도구의 역할만 설명합니다. 단일 JVM 학습용 메모리 저장소이며 재시작하면 데이터와 번호가 초기화됩니다. 여러 연산을 묶은 트랜잭션은 제공하지 않습니다.

### 53. MemoryProductRepository.java · 1/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 54. MemoryProductRepository.java · 2/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 55. MemoryProductRepository.java · 3/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 56. 정렬해서 목록을 반환합니다

교재 3장의 모던 Java 복습과 연결합니다. 메서드 참조 Product::getId는 각 상품의 id를 정렬 기준으로 읽는 표현입니다. Stream 전체 API를 설명하지 않습니다. 반환 목록은 수정용 저장소가 아니라 조회 결과입니다.

### 57. ProductNotFoundException.java · 1/1

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 58. ProductService.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 59. ProductService.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 60. 웹 없이 객체 연결부터 확인

서버 포트나 URL 호출은 오늘의 완료 기준이 아닙니다. 기본 스타터만 사용한 main은 웹 서버를 열지 않고 정상 종료할 수 있습니다. 다음 단위 테스트로 객체 기능을 직접 확인합니다.

### 61. Spring 없이도 Service를 사용할 수 있습니다

이 코드는 관계를 읽는 짧은 예시이며 시작 클래스 main에 무조건 붙이라는 의미가 아닙니다. 다음 테스트 파일에서 실제로 실행합니다. 앞에서 배운 대로 plain new 객체에는 Spring AOP가 적용되지 않는다는 점을 연결합니다.

### 62. ProductServiceTest.java · 1/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 63. ProductServiceTest.java · 2/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 64. ProductServiceTest.java · 3/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 65. 정상 · 잘못된 값 · 없는 상품

서버와 DB를 실행하는 테스트가 아닙니다. 테스트마다 새 테스트 인스턴스와 저장소를 사용합니다. 테스트 통과는 HTTP 매핑이나 AOP 적용까지 증명하지 않습니다. Wrapper 실행 권한이 없으면 bash ./gradlew test로도 실행할 수 있습니다.

### 66. Spring Boot 4.x의 스타터 추가

Spring Boot 4에서 예전 spring-boot-starter-aop 이름은 spring-boot-starter-aspectj로 변경되었습니다. 이 수업에서는 Boot 자동 설정을 사용하므로 @EnableAspectJAutoProxy를 별도로 추가하지 않습니다. 공식 AOP 문서와 마이그레이션 가이드를 확인했습니다.

### 67. TimingAspect.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 68. TimingAspect.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 69. proceed()가 원래 메서드를 실행합니다

실행 시간은 짧으면 0ms가 나올 수 있습니다. 0ms 자체가 AOP 실패가 아닙니다. return 값을 전달하고 예외를 삼키지 않는 구조를 설명합니다.

### 70. Spring이 주입한 Service를 테스트에서 호출

새 Controller나 실행용 seed를 추가하지 않습니다. 제공 테스트는 웹 환경 없이 Spring 컨텍스트에서 빈을 주입합니다. 뒤 수업에 Web 의존성이 추가되어도 그대로 재사용할 수 있습니다. SpringBootTest는 SpringBootTest.WebEnvironment.NONE을 사용합니다.

### 71. ProductWiringTest.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 72. ProductWiringTest.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 73. 단위 테스트와 주입 테스트를 비교

Initializr 기본 contextLoads 테스트를 유지했다면 전체5개입니다. 예제4개는 ProductServiceTest3개와 ProductWiringTest1개입니다. 로그가 안 보이면 IDE 테스트 콘솔 또는 Gradle --info로 확인합니다. 단위 테스트 new 호출에는 AOP 로그가 없고, 주입된 Service에는 나타납니다. 숫자0ms도 정상입니다.

### 76. 화면으로 결과와 구조를 설명

마지막 교시 안에서 자율 실습 마무리 20분과 피드백 25분을 운영합니다. 시연 없이 멘티 실행 결과로 확인하며, 모든 팀의 발표를 길게 반복하지 않습니다.

### 80. 상품 규칙의 경계값 테스트 추가

기존 테스트를 삭제하지 않습니다. 각 테스트는 새 저장소에서 시작하고 기대값과 실제값을 assert로 비교합니다. 실패 후 번호 연속성은 요구하지 않습니다. HTTP나 검증 어노테이션은 사용하지 않습니다.

### 81. Service에 가격 상한 조회 추가

메서드 이름은 상품 id 조회와 구분합니다. 기존 findAll 결과를 조건으로 조회하되 저장소를 덮어쓰지 않습니다. Repository 계약 변경은 필수가 아닙니다. 상한 0 · 동일 가격 · 결과 없음 · 음수 · 조회 전후 원본 보존을 테스트합니다. HTTP 검색은 9일 이후 별도 과제입니다.

### 82. 새 기능을 테스트와 함께 설명

추가 과제는 실습 코드에 없는 구현입니다. 수업시간 안에 두 과제의 완료를 강제하지 않으며 마감은 별도 안내합니다. API 이름 검색·수정·삭제는 후속 범위입니다.

### 84. Spring 학습용 저장소 하나를 계속 사용

저장소 생성/clone 상세 절차는 수업 슬라이드에 추가하지 않습니다. 기존 greeting-api,Issue,PR,Wiki는 유지합니다. GitHub Free의 Public 저장소 Wiki기능을 확인합니다.

### 85. product-api/에 오늘의 파일을 보관

Wrapper jar는 실행에 필요합니다. 루트Java.gitignore의 *.jar에 대한 예외를 유지하고 greeting-api의 예외도 보존합니다. 프로젝트 내부의 별도.git은 복사하지 않습니다. 비밀값 포함 여부를 확인합니다.

### 88. 매 단계 최신 main에서 시작합니다

완료한 실습을 사후정리하는 경우 Issue에 완료결과정리임을 명시합니다. 본인이 자체확인 후 병합할 수 있습니다. Wiki는 코드PR에 자동포함되지 않으므로 문서PR에서 Wiki링크와작성확인을 남깁니다.

### 91. Issue 연결 후 자체 확인하고 병합

Issue와PR제목은같게사용합니다. 커밋은 feat:·test:·docs:·fix:로 목적을 표시하며 최소개수나 타인승인은강제하지않습니다. main직접push대신교육용PR흐름으로제출합니다.

### 92. 프로젝트 README 여섯 항목

greeting-api등기존루트README링크를보존합니다. docs/product-core PR에두README변경과Wiki작성확인을기록합니다. 웹없는main정상종료와실제테스트명령을구분해적습니다.

### 94. 구현한 범위와 근거를 정확히 기록

Wiki는GitHubWiki화면에작성하며일반코드PR과별도입니다.6페이지기존섹션보존,문서PR에Wiki링크와작성확인을포함합니다.

### 95. 필수 실습·문서를 링크로 제출

12일설계는docs/short-url-design로이어갑니다.오늘REST나오류응답을미리구현하도록요구하지않습니다.마감은별도공지전미지정입니다.

