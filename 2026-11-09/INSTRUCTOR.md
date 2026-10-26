# 2026-11-09 강사용 가이드 · REST API 4시간

## 진행 원칙

7일 `product-api`를 그대로 확장합니다. Java 17, Spring Boot 4.1.2, Gradle 설정과 코어·AOP·기존 테스트를 유지합니다. Initializr 재생성이나 별도 Git 저장소 생성은 하지 않습니다. 시연 없이 개념 설명 → 요구사항 안내 → 멘티 자율 구현 → 결과 피드백으로 운영합니다. 전체 코드는 실습 참고이며 선택 과제의 정답은 제공하지 않습니다.

## 시간 배분

- 1블록 45분 + 휴식 15분: MVC 복습, 자원·URI·메서드·상태와 입력 위치.
- 2블록 45분 + 휴식 15분: DTO, Jackson 메시지 변환, ResponseEntity, Postman 읽기.
- 3블록 45분 + 휴식 15분: 멘티가 DTO 두 개와 Controller 구현.
- 4블록 45분 + 정리 15분: 정상 요청, 기존 테스트·AOP 확인, 설명·GitHub 제출 안내.

배정 240분 안에서 휴식을 조정하며 선택 과제로 수업 시간을 늘리지 않습니다.

## 교재 연결

CH 09 상품 관리, 부록 A API 요청 도구를 함께 봅니다. CH 07~08의 JSON·HTTP는 재연결하며 1~8장 전체 복습은 5일에서 마칩니다. CH 12의 추상화·단위 테스트는 7일 선행입니다. CH 10 입력 검증·예외 응답은 12일로 이연합니다. CH 11 DB/JDBC 예제와 이후 JPA 방식은 구분합니다. 본문 복제 대신 책의 관련 예제를 읽고 자체 예제와 비교합니다.

## 단계별 코드 계약

7일의 코어 8파일과 `ProductWiringTest.java`를 유지합니다. Wiring 테스트의 `@SpringBootTest(webEnvironment=NONE)`도 유지합니다. 기존 `ProductServiceTest`는 일반 Java 객체 테스트이므로 AOP가 적용되지 않는 것이 정상입니다.

오늘 `source-data`는 당일 추가 3파일만 포함합니다.

1. `CreateProductRequest.java`: name/Integer price, getter/setter, 검증 어노테이션 없음.
2. `ProductResponse.java`: id/name/price를 공개하는 응답 DTO.
3. `ProductController.java`: 생성·목록·단건, 아직 @Valid 없음.

build.gradle의 기존 dependencies에 `implementation 'org.springframework.boot:spring-boot-starter-webmvc'`만 추가합니다. 기존 AspectJ와 테스트를 제거하지 않습니다. 전체 코드 버튼의 파일을 `src/main/java/com/example/product/`에 각각 작성합니다. 매 코드 페이지는 원본을 14줄씩 분할하며 첫 줄 공백도 보존합니다.

## 필수 실행 확인

`product-api/`에서 `./gradlew test`, `./gradlew bootRun`. Windows PowerShell은 `.\gradlew.bat test` / `.\gradlew.bat bootRun`. 서버 포트 변경 시 모든 URL에 같은 포트 사용. 재시작하면 메모리 데이터가 사라집니다.

새 서버에서 GET 목록 200 + [], POST 노트 3000으로 201·Location·응답 JSON, 응답의 실제 id 단건 조회 200, 펜 생성 후 id 오름차순 목록, JSON Content-Type, Service AOP 로그를 확인합니다. JSON 속성 순서와 연속 id는 강제하지 않습니다. 0ms 시간 로그도 정상입니다.

9일의 없는 상품은 ProductNotFoundException이 아직 HTTP에 매핑되지 않아 500일 수 있습니다. 404·검증 400·공통 오류 JSON은 12일 완료 기준입니다. 오늘 완성된 오류 계약으로 기록하지 않습니다.

Postman에서 Body/raw/JSON과 Content-Type을 확인합니다. Desktop 앱·Agent 또는 curl로 로컬 서버에 연결합니다. macOS/Linux curl 예제와 Windows JSON 파일 + curl.exe 대안을 구분합니다.

## 별도 과제

이름 부분검색 → 가격 상한·복합조건 순으로 선택 확장합니다. 검색어 strip, 영문 대소문자 구분, 미지정/공백은 전체, id 오름차순, 빈 결과 200+[], 원본 저장 데이터 불변. 가격은 0과 상한값 포함 경계를 검사합니다. 음수/문자 가격 400은 12일 이후 범위입니다. 정답 코드는 제공하지 않습니다. 수정·삭제는 14일 CRUD 구현과 연결합니다. 현재 비교 슬라이드에 Map.of 표현을 직접 제공하며 DTO와 비교합니다. 두 프로젝트 수정은 강제하지 않습니다.

## GitHub 제출

`sesac-spring-boot-study`의 Public/main, Issues/Wiki 설정을 유지합니다. 필수 Issue 1개와 병합 PR 1개:

- branch: `practice/product-rest`
- title: `[실습] 상품 생성·조회 REST API`
- labels: `practice`, `docs`; assignee 본인
- milestone: `product-api-2026-11-09`, 마감 미지정

최신 main → Issue → branch → 코드/테스트/문서 → commit/push → PR(base main) → 자체 확인/병합 → 다음 main pull. 관련 Issue는 실제 번호로 Closes 연결. 선택 과제는 feature/name-search 및 feature/price-filter에 각각 Issue/PR을 추가합니다.

product-api/README.md 여섯 항목은 소개, 실제 개발 환경, 실행·테스트, 구현 현황, API, Wiki 링크입니다. 루트 README 목차·greeting-api를 보존합니다. Wiki Home/01-Setup/02-Architecture/03-API/04-Verification/05-Retrospective에 프로젝트별로 누적합니다. 코드 PR에 Wiki가 자동 포함되지 않으므로 별도 편집하고 링크/완료 확인을 PR에 남깁니다. 별도 docs PR은 요구하지 않습니다.

Wrapper jar 포함: 루트 .gitignore의 `!product-api/gradle/wrapper/gradle-wrapper.jar` 및 기존 greeting-api 예외 보존. build/.gradle/IDE파일/.env·비밀값 제외. 저장소 URL, Wiki Home URL, 필수 PR1개와 선택 수행 여부 제출.

## 다음 시간

12일 앞2시간 CH10 검증/예외 및 HTTP·REST 면접 연결. 뒤2시간 CH13 단축 URL 공통 설계, CH14 주문관리 선택. 14일 직접 구현6시간과 JPA2시간으로 이어집니다.

## 실행 리허설 근거 · 2026-10-26

Java 17 / Spring Boot 4.1.2에서 실제 단계별 증분 구성을 실행 검증했습니다. 7일(core+AspectJ) → 9일(+Web MVC) → 12일(+Validation) 순서로 clean build 및 JUnit 테스트 5개가 각 단계에서 통과했습니다. 오늘 단계는 정상 HTTP 7개 확인과 AOP 로그를 확인했습니다. 검증 환경의 결과이며 멘티는 자기 환경에서도 다시 실행하고 실제 결과를 기록합니다. 루트 통합 리허설 기록을 참조합니다.

## 슬라이드별 강사 메모

### 1. 상품 기능을 REST API로 연결하기

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 2. 객체에서 HTTP로 한 단계 확장

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 3. 오늘은 정상 요청 세 가지를 완성

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 4. 같은 개념을 책과 프로젝트에서 찾기

교재 본문을 복제하지 않습니다. 지정한 장에서 관련 예제를 함께 읽고 자체 상품 예제와 비교합니다. CH 12 추상화·테스트는 7일에 선행했고 CH 11 DB 연결은 이후 다룹니다. JDBC 교재 예제와 이후 JPA를 같은 구현이라고 설명하지 않습니다.

### 5. 개념 먼저 · 구현은 멘티가 직접

4시간 배정: 1블록 REST/MVC·HTTP 복습, 2블록 DTO/JSON/응답 설명, 3블록 자율 구현, 4블록 요청 검증·질문·기록. 각 블록 45분+휴식15분을 기본으로 총 240분 안에 운영합니다. 강사 구현 시연 없이 요구사항 안내→자율 구현→결과 피드백. 참고 완성 코드는 실습용이며 별도 과제의 정답은 제공하지 않습니다.

### 6. HTTP 계약을 먼저 정합니다

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 7. DispatcherServlet이 요청을 조율

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 8. HTTP 처리를 Service에 넣지 않습니다

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 9. 동작보다 자원을 URI로 표현

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 10. 요청의 의도를 메서드로 구분

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 11. 정상과 실패를 구분하는 약속

9일에는 예외 처리기를 아직 작성하지 않으므로 없는 상품 조회를 404로 보장하지 않습니다. ProductNotFoundException은 상태 매핑 전에는 500이 될 수 있습니다. 실패 응답의 통일은 12일 실습 완료 기준입니다.

### 12. 경로 · 쿼리 · 본문을 구분

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 13. Java 객체와 JSON의 경계

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 14. 화면 이름과 응답 본문을 구분

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 15. 입력 형식을 별도의 객체로 정의

오늘의 DTO는 아직 검증 어노테이션이 없습니다. price는 Integer로 유지하여 12일에 누락/null을 명시적으로 검증합니다. 9일 필수 검증은 정상 요청만 다룹니다.

### 16. 입력 · 업무 · 출력의 책임을 구분

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 17. 문자열과 객체 사이를 메시지 변환기가 연결

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 18. 요청 setter · 응답 getter를 읽기

이 설명은 오늘 제공하는 JavaBean 형태의 DTO에 대한 것입니다. Jackson이 모든 경우에 setter를 강제한다거나 record를 사용할 수 없다고 일반화하지 않습니다.

### 19. ResponseEntity는 상태 · 헤더 · 본문

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 20. 조회 결과가 없어도 요청은 성공

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 21. Postman에서 요청과 응답을 나누어 읽기

Postman UI는 버전에 따라 위치가 다를 수 있습니다. 동일한 메서드/URL/헤더/본문을 보내는 것이 핵심입니다. 웹 버전에서 로컬 서버 연결이 막히면 Desktop 앱/Agent 또는 curl 대안을 사용합니다.

### 22. 자율 실습 · 상품 REST API

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 23. 기존 프로젝트가 먼저 통과해야 합니다

기존 테스트 명령은 ./gradlew test이며 Windows PowerShell은 .\gradlew.bat test입니다. 실패가 남아 있으면 HTTP 코드를 붙이기 전에 원인을 먼저 해결합니다. 이전 파일 참고: ../2026-11-07/. 새 Initializr 프로젝트를 받거나 중첩 git init을 하지 않습니다.

### 24. Web MVC 스타터만 추가

7일의 Java 17 · Spring Boot 4.1.2 · Gradle 구성을 유지합니다. 오늘 validation 스타터는 추가하지 않습니다. 기존 dependencies 블록을 통째로 바꾸지 않습니다.

### 25. 새로 작성할 파일은 세 개

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 26. CreateProductRequest.java · 1/1

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 27. ProductResponse.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 28. ProductResponse.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 29. ProductController.java · 1/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 30. ProductController.java · 2/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 31. ProductController.java · 3/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 32. 테스트를 확인한 뒤 서버 실행

Windows PowerShell: .\gradlew.bat test / .\gradlew.bat bootRun. IDE에서 main을 실행해도 됩니다. 포트 충돌이면 기존 서버를 종료하거나 application.properties의 server.port를 변경하고 모든 요청 URL에 같은 포트를 사용합니다. 재시작하면 메모리 상품이 초기화됩니다.

### 33. 빈 목록을 먼저 조회

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 34. 상품을 생성하고 실제 id 기록

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 35. 생성한 id로 단건 조회

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 36. 상품 두 개와 목록 순서 확인

Spring MVC Controller에 주입된 Service도 7일에 확인한 프록시를 사용합니다. 0ms 로그도 정상일 수 있으며 메서드 실행 시간을 정밀 성능 지표로 사용하지 않습니다.

### 37. Postman과 같은 요청을 curl로 확인

Windows PowerShell은 curl 별칭 차이가 있으므로 Postman을 우선 사용하거나 curl.exe와 JSON 파일을 사용합니다. JSON을 UTF-8 product.json으로 저장한 뒤 curl.exe -i -X POST http://localhost:8080/products -H "Content-Type: application/json" --data-binary "@product.json"으로 보낼 수 있습니다. 파일 경로와 포트를 실제 환경에 맞춥니다.

### 38. 실패 응답 완성은 12일에 이어갑니다

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 39. 요청 한 개의 왕복을 설명하기

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 40. 별도 과제 · 조회 조건 확장

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 41. 기존 목록 API에 조건 하나 추가

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 42. 이름과 가격 조건을 누적 적용

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 43. Map 응답과 DTO 응답을 비교

5일에서 옮긴 JSON 추가 과제의 연결 읽기입니다. 기존 greeting-api는 보존합니다. PUT·DELETE는 14일 CRUD 구현과 통합하며 오늘 별도 필수 과제로 부과하지 않습니다.

### 44. GitHub 제출

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 45. 오늘 필수 Issue 1개 · 병합 PR 1개

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 46. 이전 수업 결과 위에서 시작

코드 PR에 Wiki 변경이 자동 포함되지는 않습니다. Wiki는 별도 편집하고 PR에 URL과 완료 체크를 남깁니다. 문서만의 추가 PR은 강제하지 않습니다. 타인 승인 대신 자체 검증 후 병합할 수 있습니다. 선택 과제는 feature/name-search / [과제 1] 상품 이름 검색, feature/price-filter / [과제 2] 가격 조건 검색으로 각각 Issue·PR을 추가하며 assignment 라벨을 사용합니다. 마감일은 별도 안내 전 지정하지 않습니다.

### 47. 실행에 필요한 파일과 기존 기록 보존

기존 greeting-api와 그 Wrapper 예외도 보존합니다. 저장소는 Public / main · Issues와 Wiki 활성화. 이미 만들어 둔 저장소를 재사용합니다. Initializr로 새로 받지 않고 product-api에 누적합니다.

### 48. 프로젝트 문서에 여섯 항목 갱신

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 49. 기존 여섯 페이지에 product-api 기록 누적

각 페이지 기존 greeting-api 및 7일 product-api 내용을 보존합니다. 결과는 기대와 실제를 나눠 기록하고 Issue·PR 링크를 포함합니다. 미구현 400/404를 완료했다고 쓰지 않습니다.

### 50. 저장소 · Wiki · 병합 PR 링크 제출

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 51. 정상 동작에서 실패 계약으로 확장

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.

### 52. 교재와 공식 문서

슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.
