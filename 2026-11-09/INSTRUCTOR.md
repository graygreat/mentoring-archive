# 2026-11-09 · 교재와 함께 상품 REST API 만들기

## 진행 기준

4교시 × 60분이며 각 교시는 활동45분과 휴식·정리15분입니다. 책 CH 09의 상품 구조·추가·DTO·조회 부분을 함께 읽고, 부록 A에서 Postman 사용 부분을 확인합니다. 정확한 쪽수는 소지한 판본에서 표시합니다. PPT는 책을 대신하지 않고 챕터 전환과 멘티 작업 범위만 안내합니다. 강사 코딩 시연은 하지 않습니다.

1. 책에서 요청 DTO·도메인·응답 DTO와 생성/조회 흐름 찾기.
2. 기존 `product-api/`에 세 파일을 직접 작성.
3. 서버를 실행한 뒤 Postman으로 실제 상태·헤더·본문 비교.
4. 오류 보완과 README·Issue·PR 제출.

## 유지할 코드 계약

7일 `Product`, `ProductRepository`, `MemoryProductRepository`, `ProductService`, 기존 단위·주입/AOP 테스트를 보존합니다. 오늘 참고 소스는 `CreateProductRequest`, `ProductResponse`, `ProductController`입니다. 교재 원문 복제 코드가 아닌 독립 수업 예제입니다. price는 Integer이며 아직 `@Valid`나 예외 처리기를 넣지 않습니다. 없는 상품·잘못된 입력의 400/404 통일은12일에 합니다.

- 생성201 + Location + 상품JSON, 목록200 + 빈목록[] + id오름차순, 실제 생성id 단건200을 확인합니다.
- 재시작하면 메모리 저장소가 초기화됩니다. id연속성과JSON속성순서를가정하지않습니다.
- Test 후 bootRun을실행하고서버터미널을유지합니다. Windows는gradlew.bat입니다.

## 제출

`sesac-spring-boot-study / product-api/`, `practice/product-rest`, `[실습] 상품 생성·조회 REST API`로 필수Issue1개·병합PR1개를제출합니다. 본인Assignee,practice/docs라벨,milestone `product-api-2026-11-09`. README에 실제 API 결과를 기록하고 `Closes #실제번호`를 사용합니다. 기존 greeting-api와루트README링크,GradleWrapper/JAR예외를보존합니다. build/.gradle/IDE/.env/비밀값은제외합니다. 선택검색과제는완료한경우만각각Issue·PR을추가합니다.

## 슬라이드별 진행 메모

### 1. 책의 상품 기능을 HTTP로 연결합니다

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 2. 책을 읽고, 작성하고, 요청합니다

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 3. 교재 CH 09를 펼칩니다

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 4. 상품 추가와 조회를 찾아봅시다

교재 CH 09의 실제 소제목을 기준으로 찾습니다. 사용 판본의 쪽수를 각자 표시합니다. 수정·삭제 구현은14일 범위입니다. 공통 수업 프로젝트product-api는7일코어와테스트를그대로유지합니다.

### 5. 요청값과 상품 객체는 무엇이 다른가요?

DTO·도메인 차이는 책의 해당 코드를 함께 보며 설명합니다. PPT에서 같은 코드를 다시 강의하지 않습니다. CreateProductRequest·ProductResponse·ProductController 세 파일을 작성하며 기존Service/Repository계약은보존합니다.

### 6. 기존 product-api에 세 파일 추가

책을 보면서 직접 작성합니다. 제공 source-data는 독립 참고 코드이며 교재 원문이 아닙니다. price는 Integer로 유지해12일누락/null검증으로이어갑니다. 오늘@RequestBody정상요청만, @Valid와예외처리기는12일입니다.

### 7. 정상 요청 세 가지를 확인합니다

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 8. 부록 A · Postman으로 확인합니다

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 9. 서버를 만든 뒤 실제 요청을 보냅니다

명령은 ./gradlew test 뒤 ./gradlew bootRun입니다. Windows는 .\gradlew.bat test / bootRun을사용합니다. 실행중인터미널을유지하고다른작업시새터미널을사용합니다. id=1을가정하지않고POST반환값을사용합니다. JSON속성순서는검증하지않습니다. AOP0ms도정상입니다.

### 10. 책의 요청 하나를 내 코드로 설명합니다

동작근거는실제실행화면으로확인합니다. 아직없는상품/잘못된값에대한오류응답은중간구현입니다. 오늘400·404를완료했다고요구하지않고12일CH10에서통일합니다.

### 11. 목록 조회에 조건을 추가합니다

쿼리 매개변수는 name과 maxPrice입니다. GET /products?name=노트&maxPrice=3000으로 두 조건을 함께 적용합니다. 선택브랜치 feature/name-search / feature/price-filter,제목[과제 1] 상품 이름 검색 / [과제 2] 가격 조건 검색. 단계마다Issue와PR추가,assignment라벨. 미완료선택과제를필수로강제하지않습니다.

### 12. 오늘 필수 Issue 1개 · 병합 PR 1개

본인Assignee,practice·docs라벨,milestone product-api-2026-11-09. main pull→Issue→branch→구현검증→commit/push→PR자체확인병합. 기존greeting-api와루트README링크를유지합니다. src·Gradle설정·Wrapper와gradle-wrapper.jar포함,build/.gradle/IDE/.env비밀값제외. 루트.gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar 보존. 별도문서PR강제없음.

### 13. 12일에는 실패 응답과 CRUD 설계

해당 장을 책에서 함께 읽고, 안내된 작업과 실제 완료 결과를 확인합니다.

### 14. 교재와 보충 자료

 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.
