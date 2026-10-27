# 11월 19일 상품 API JPA 전환 작업지

수업 4시간. 45분 작업과 확인 뒤 15분 휴식 또는 정리한다. 강사 시연 없이 책의 상품 관리와 16일 코드를 보며 직접 구현한다. 이 문서에는 완성 구현을 싣지 않는다.

## 준비

- `sesac-spring-boot-study`의 기존 `product-api`를 사용한다. 현재 작업을 commit하고 main을 갱신한다.
- 책의 상품 관리 데이터 접근·저장소 부분을 읽고 본인 판본의 절과 페이지를 기록한다. 책 JDBC와 수업 JPA는 구현 방식이 다르다.
- 16일 완료 상태: `ProductEntity`, `SpringDataProductRepository`, JPA 저장소 테스트가 존재한다. **HTTP API는 아직 MemoryProductRepository를 사용한다.**
- 출발 상태가 없다면 [복구용 출발 ZIP](assets/product-api-start.zip)을 별도 임시 폴더에서 열어 비교한다. 기존 프로젝트·DB 파일을 덮어쓰거나 삭제하지 않는다. 사용한 복구 범위를 기록한다.
- product-api 폴더에서 `./gradlew test`를 실행한다. Windows는 `gradlew.bat test`. Java 17 이상과 기존 Gradle Wrapper를 사용한다.

## 모르는 단어가 있으면 먼저 확인

[DB 기초](../shared/db-basics/README.md)와 [16일 쉬운 작업지](../2026-11-16/BEGINNER-WORKSHEET.md)에서 표·행·열·PK·Entity를 복습한다. 새 개념을 배우는 날이 아니라 작은 연결을 완성하는 날이다.

| 단어 | 이 작업에서의 뜻 |
|---|---|
| Entity | `products` 표의 한 행과 연결하는 `ProductEntity` 객체 |
| 빈 등록 | Spring이 만들어 주입할 객체라고 표시하는 것 |
| 영속 상태 | Entity가 영속성 컨텍스트에서 관리되는 상태. 재시작 후 보존은 DB 설정과 별개다. |
| adapter | 기존 계약을 다른 저장 도구에 연결하는 `JpaProductRepository` |
| 트랜잭션 | 한 업무의 DB 변경을 함께 확정하거나 취소하는 범위 |
| flush | 바뀐 값을 SQL로 DB에 보내는 것. commit(확정)과 다르다. |
| readOnly | 조회 업무라는 힌트. 쓰기를 무조건 막는 장치는 아니다. |

## 1교시: 출발 상태와 변경 계획

- [ ] 기존 테스트 통과 결과를 기록했다.
- [ ] POST·GET·PUT·DELETE API 계약과 400/404 응답을 확인했다.
- [ ] ProductService가 ProductRepository 인터페이스를 주입받음을 찾았다.
- [ ] 현재 등록된 구현체가 MemoryProductRepository임을 찾았다.
- [ ] Controller/DTO를 바꾸지 않고 저장소를 교체할 계획을 적었다.

완료 확인: 호출 흐름과 변경할 파일을 강사에게 설명한다. 출발 테스트 실패를 새 구현 문제와 섞지 않는다.

## 2교시: 작은 연결 다섯 개

### A. 파일과 계약을 찾는다

왜: Service 코드를 DB 도구에 직접 묶지 않고 기존 API의 동작을 유지하기 위해서다.

1. `src/main/java/com/example/product/ProductService.java`에서 생성자 인자의 타입을 찾는다. 답: `________`.
2. `ProductRepository.java`를 열고 메서드의 입력·반환 타입을 적는다.
3. `SpringDataProductRepository.java`를 연다. `JpaRepository<ProductEntity, Long>`에서 저장하는 객체 타입과 id 타입을 표시한다.

| 이름 | 누가 호출하나? | 주고받는 값 |
|---|---|---|
| ProductRepository | ProductService | Product · 기존 업무 계약 |
| SpringDataProductRepository | JpaProductRepository | ProductEntity · Spring Data가 제공하는 DB 도구 |
| JpaProductRepository | Service에서 기존 계약으로 호출 | 두 계약을 연결하고 값을 변환 |

말로 확인: “Service → ProductRepository의 Jpa 구현체 → Spring Data 도구 → DB”를 설명한다. 두 인터페이스가 같은 역할이라고 설명하지 않는다.

### B. 메서드를 하나씩 맞춘다

수정 위치: `JpaProductRepository.java`를 만들고 기존 `ProductRepository`를 구현한다. 생성자로 `SpringDataProductRepository`를 받는다. 완성 코드를 먼저 복사하지 말고 표에서 짝을 찾는다.

| 기존 메서드 | 연결할 도구와 행동 | 확인 |
|---|---|---|
| save(name, price) | 새 Entity → data.save → 반환 Entity.toProduct | DB 생성 id가 Product에 있나? |
| findAll() | findAllByOrderByIdAsc → 각각 toProduct | 기존 id 오름차순인가? |
| findById(id) | findById → Optional 안 Entity를 Product로 변환 | 없으면 빈 Optional인가? |
| update(id, name, price) | 먼저 Entity 조회 → 있으면 change → toProduct | 같은 id인가? 없으면 빈 Optional인가? |
| delete(id) | 먼저 조회 → 있으면 delete | 성공 true / 없으면 false인가? |

등록 흐름에 `name=노트`, `price=3000`을 직접 넣어 읽는다.

| 단계 | id | name | price |
|---|---|---|---|
| POST 입력 | 없음 | 노트 | 3000 |
| 새 ProductEntity | DB에 맡김 | 노트 | 3000 |
| data.save 반환 | 실제 생성값 | 노트 | 3000 |
| toProduct 반환 | 같은 생성값 | 노트 | 3000 |

왜 변환하나: DB용 Entity를 기존 업무용 Product로 돌려주면 Service·DTO·Controller의 계약을 보존할 수 있다. id=1을 지정하거나 새로운 임의 id를 만들지 않는다.

### C. Spring에 연결할 구현체 하나를 고른다

수정 위치: `MemoryProductRepository.java`와 `JpaProductRepository.java`의 클래스 선언 위.

- [ ] Memory 클래스와 구현은 남기고 `@Repository` 등록만 제거한다.
- [ ] Jpa 구현체에 `@Repository`를 붙인다.
- [ ] Service의 생성자 타입은 `ProductRepository` 그대로 둔다.

왜: 둘 다 등록하면 주입 후보가 둘이라 시작 오류가 난다. 두 빈을 그대로 둔 채 `@Primary`로 가리는 해결은 이번 실습에서 사용하지 않는다.

### D. Service 업무 단위를 묶는다

수정 위치: `ProductService.java`. 쓰기 업무에 `@Transactional`, 조회에 `@Transactional(readOnly = true)`를 적용한다. 예시 구현은 클래스 쓰기 기본 설정 + 조회 메서드 재정의 방식이다.

왜: 수정은 “Entity 찾기 → 값 변경 → 업무 정상 종료 시 반영”을 하나로 묶어야 한다. 예외가 나면 트랜잭션을 취소할 수 있다. readOnly는 조회 의도를 알리며 데이터베이스 쓰기 금지를 보장하는 장치가 아니다.

- [ ] create/update는 Repository 호출 전 기존 도메인 검증을 유지한다.
- [ ] 입력 오류의 기존 400 계약을 유지한다.
- [ ] `ProductEntity.name`의 긴 이름 매핑과 긴 이름 저장 테스트를 보존한다.
- [ ] Controller·DTO·예외 처리기를 바꾸지 않는다.

### E. 앱 DB와 테스트 DB를 구분한다

| 위치 | URL·용도 | 확인 |
|---|---|---|
| src/main/resources/application.properties | `jdbc:h2:file:./data/products` · 앱 파일 DB | 같은 product-api 폴더에서 실행 |
| src/test/resources/application.properties | 별도 `jdbc:h2:mem:…` · 테스트 DB | create-drop·롤백으로 테스트 격리 |

앱은 `ddl-auto=update`, `open-in-view=false`를 유지한다. `./data`는 실행 폴더 기준이다. 현재 폴더 `________`, 실제 DB 파일 경로 `________`를 적는다. 로컬 학습용 설정이며 운영 정책은 별도다.

**출발 코드에 Entity와 JPA Repository가 있다는 사실만으로 API가 JPA를 쓴다고 결론내리지 않는다.** POST 때의 INSERT·GET 때의 SELECT 로그와 4교시 재시작 보존을 함께 확인한다. main에서 `spring.jpa.show-sql=true`가 켜져 있는지 확인한다. 로그의 실제 수·순서는 flush 시점 등에 따라 다를 수 있다.

완료 확인: `./gradlew test` 후 앱을 시작해 구현체 중복 오류가 없고 파일 DB를 연결했는지 확인한다. DB 잠금은 중복 실행을 종료하고, 보존 실패는 URL·현재 폴더·DDL을 비교한다. **DB 파일을 지워서 해결하지 않는다.**

## 3교시: CRUD·실패 회귀

먼저 정상 사례 하나를 예측한다. POST `{"name":"노트","price":3000}` → 201의 실제 id 기록 → PUT 같은 id에 `{"name":"노트","price":3500}` → GET 같은 id에 3500. INSERT로 한 행이 추가되고, PUT은 같은 행을 바꿔야 한다. 실행한 요청·SQL 종류·행의 값·응답을 나란히 적는다.

| 행동 | 예상 | 실제 SQL·응답·행 값 |
|---|---|---|
| POST 노트 3000 | INSERT · 새 행 · 201 | |
| GET 실제 id | SELECT · 노트 3000 · 200 | |
| PUT 같은 id 3500 | 조회/UPDATE · 같은 행 · 200 | |
| GET 같은 id | 노트 3500 · 200 | |
| 실패 요청 | 400/404 · 기존 행과 값 유지 | |

다음 표를 실제 실행 결과로 채운다. `{id}`는 POST 응답에서 받은 실제 id다. 임의로 1이라고 가정하지 않는다.

| 확인 | 기대 | 실제·근거 |
|---|---|---|
| POST 정상 | 201, Location, 실제 id | |
| GET 목록 | 200, id 오름차순 | |
| GET 생성 id | 200, 생성 값 | |
| PUT 생성 id | 200, 같은 id·수정 값 | |
| 공백 이름·음수·누락/null 가격 | 400, 데이터 불변 | |
| 잘못된 JSON·가격 타입 | 400, 데이터 불변 | |
| 없는 id 조회·수정·삭제 | 404, 데이터 불변 | |
| trim 이름·가격 0 | 정상 처리 | |
| DELETE 생성 id | 204, 이후 조회 404 | |

- [ ] 실패 전후 GET 목록의 값과 개수를 비교했다.
- [ ] ProductServiceTest·ProductCrudTest·ProductJpaRepositoryTest 등 기존 테스트가 통과했다.
- [ ] JPA Service 수준에서 수정 반영과 잘못된 수정 뒤 데이터 보존을 확인하는 테스트를 추가했다.
- [ ] 테스트는 각자 데이터를 만들고 실제 id를 사용하며 다른 테스트 실행 순서에 의존하지 않는다.

## 4교시: 재시작·문서·제출

재시작 검사용 상품은 삭제하지 말고 별도로 생성한다.

1. 생성 응답의 id, 이름, 가격을 기록한다.
2. 값을 수정하고 같은 id로 다시 조회한다.
3. 애플리케이션을 정상 종료한다.
4. 같은 폴더·같은 설정으로 다시 실행한다.
5. 같은 id 조회가 200이고 수정 값이 유지되는지 확인한다.
6. 필요한 확인 후에만 본인이 만든 실습 상품을 정리한다.

- [ ] 실행 DB 파일이 `data/`에 있고 재시작 후 데이터가 남았다.
- [ ] README에 실행·DB 경로·테스트·현재 API를 적었다.
- [ ] Wiki의 Home, 01-Setup, 02-Architecture, 03-API, 04-Verification, 05-Retrospective에 기존 내용을 보존하며 누적했다.
- [ ] DB 파일·build·.gradle·IDE·.env를 Git에서 제외했다.
- [ ] Gradle Wrapper jar를 포함했다. 루트 ignore의 `!product-api/gradle/wrapper/gradle-wrapper.jar`를 확인했다.

저장소 `sesac-spring-boot-study`, 브랜치 `practice/product-jpa-migration`, Issue/PR 제목 **`[실습] 상품 API 데이터 접근 JPA 전환`**. 필수 Issue 1개와 병합 PR 1개다. main pull → Issue → 브랜치 → 작업·검증 → commit/push → base main PR → 자체 확인·병합 → main pull 순서로 진행한다. PR에는 `Closes #실제번호`, 테스트·HTTP·재시작 증거와 Wiki 링크를 넣는다. Wiki는 별도로 편집한다.

## 막힐 때 사용하는 힌트

| 단계 | 먼저 확인할 일 |
|---|---|
| 1 | 오류의 첫 원인, 파일 경로, 메서드 시그니처, 주입 타입을 확인한다. |
| 2 | 빈 두 개 등록, Entity 변환, Service 트랜잭션, DB URL·실행 폴더를 확인한다. |
| 3 | 재현 방법과 시도한 수정을 강사에게 설명한 뒤 참고 구현과 차이를 비교한다. |

DB 잠금은 실행 중인 다른 앱부터 확인한다. 보존 실패는 DB URL·작업 폴더·DDL 설정부터 비교한다. 오류를 해결하려고 기존 DB 파일을 무작정 지우지 않는다.

필수 완료 후 선택: 저장소 구현체 계약 테스트 비교, 읽기 전용 트랜잭션 설명, [단축 URL 별도 과제](../assignments/short-url/)의 DB 전환 계획. 단축 URL DB 전환은 필수 제출 범위와 구분한다.
