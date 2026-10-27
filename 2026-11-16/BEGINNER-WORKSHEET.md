# 11월 16일 · 상품 한 개로 시작하는 JPA 작업지

목표는 어려운 용어 암기가 아니라 **노트 3000원을 저장하고 다시 읽은 근거를 설명하는 것**입니다. 책에서 상품 DB 접근 절을 읽고 아래 단계마다 멈춰 확인하세요. Java 전체 비교 코드는 [수업 슬라이드](index.html)의 파일 전체 코드 버튼에서 봅니다. 이 작업지는 교재 원문 코드가 아닌 수업 독립 예제 안내입니다.

## 0. 표부터 읽기

[DB 기초 설명](../shared/db-basics/README.md)과 [DB 작업지](../shared/db-basics/STUDENT-WORKSHEET.md)를 먼저 확인합니다.

| id | name | price |
|---|---|---:|
| DB 발급값 A | 노트 | 3000 |
| DB 발급값 B | 무료 | 0 |
| DB 발급값 C | 펜 | 1000 |

- 행 한 개는 상품 한 개, 열은 속성입니다. PK는 행을 구분합니다.
- price <= 1000인 행은 무엇인가요? **무료와 펜**입니다. 1000도 포함합니다.
- 아직 DB가 발급하지 않은 id는 null입니다. 가격 0은 null과 다릅니다.

이 질문이 어렵다면 구현으로 넘어가기 전에 표를 직접 그려 설명합니다.

## 1. 출발 상태와 파일 위치

저장소 `sesac-spring-boot-study`의 최신 main에서 `practice/product-jpa-basics` 브랜치를 만듭니다. 실행 폴더는 항상 `product-api/`입니다. 기존 Java 17·Boot 4.1.2와 CRUD·검증·AOP를 유지합니다.

```sh
cd product-api
./gradlew test
```

Windows PowerShell에서는 `./gradlew.bat test`입니다. 기존 테스트부터 통과해야 새 오류와 기존 오류를 구분할 수 있습니다.

오늘 추가할 파일은 다음과 같습니다.

| 파일 경로 | 역할 |
|---|---|
| `src/main/java/com/example/product/ProductEntity.java` | DB에 저장할 상품 모양 |
| `src/main/java/com/example/product/SpringDataProductRepository.java` | Entity 저장·조회 약속 |
| `src/test/java/com/example/product/ProductJpaRepositoryTest.java` | DB에서 실제 동작하는지 확인 |
| `src/main/resources/application.properties` | 서버 실행용 파일 DB 설정 |
| `src/test/resources/application.properties` | 테스트용 독립 메모리 DB 설정 |

`build.gradle`의 기존 dependencies를 지우지 않고 수업에 제시된 JPA·H2·JPA 테스트 의존성만 합칩니다. 기존 ProductRepository와 MemoryProductRepository도 유지합니다.

## 2. Entity를 표와 연결

책과 슬라이드를 보며 id·name·price를 먼저 적고, 각 필드가 어느 열인지 표시합니다.

| 설정 | 내 말로 설명할 내용 |
|---|---|
| @Entity | JPA가 저장 대상으로 관리하는 클래스 |
| @Table(name = "products") | 연결할 표 이름 |
| @Id | 행을 찾을 식별 키 |
| @GeneratedValue(IDENTITY) | DB에 id 발급을 맡기기 |
| Long id | 저장 전 null, 저장 후 실제 발급값 |
| protected 기본 생성자 | JPA가 객체를 구성할 입구 |

업무 생성자와 change는 기존 Product 검증을 재사용합니다. 입력 DTO는 JSON을 받고, Product는 업무 규칙을 지키며, ProductEntity는 DB 저장을 담당합니다.

완료 확인: Entity 한 개를 만들어도 아직 DB에 저장한 것은 아닙니다. Repository 저장 요청이 필요하다고 설명할 수 있나요?

참고: 비교 코드의 @Lob과 긴 이름 테스트는 기존 이름 허용 범위를 보존하는 항목입니다. 먼저 기본 저장·조회부터 성공시키고 확인합니다.

## 3. 저장 한 건 → 실제 id → 다시 조회

SpringDataProductRepository에서 Entity 타입은 ProductEntity, id 타입은 Long인지 확인합니다. 기존 ProductRepository와 다른 인터페이스입니다.

첫 테스트 `persistAndReloadAfterClear`를 세 부분으로 나눠 읽고 실행합니다.

| 순서 | 코드에서 찾을 동작 | 기대 |
|---|---|---|
| 준비 | 노트 3000원 Entity 생성 | 저장 전 id 없음 |
| 행동 | saveAndFlush → getId | DB가 발급한 실제 id 확보 |
| 행동 | clear → findById(id) | DB에서 새로 읽음 |
| 기대 | assertEquals("노트", found.getName()) | 이름이 노트 |
| 기대 | assertNotSame(saved, found) | 같은 Java 객체를 그대로 받지 않음 |

```sh
./gradlew test --tests '*ProductJpaRepositoryTest.persistAndReloadAfterClear' --info --rerun-tasks
```

같은 테스트를 반복 관찰할 때 `--rerun-tasks`로 UP-TO-DATE 생략을 막습니다. 출력이 길면 `build/reports/tests/test/index.html`에서 해당 테스트 클래스의 **Standard output**을 확인합니다.

IDE 디버거의 `saved.getId()` 또는 임시 출력으로 실제 id를 확인하세요. 1이라고 미리 가정하지 않습니다. SQL 로그에서 INSERT와 SELECT를 찾습니다.

```sql
INSERT INTO products (name, price, id) VALUES (?, ?, default);
SELECT id, name, price FROM products WHERE id = ?;
```

위는 관찰할 SQL의 대표 모양이며 직접 실행할 완성 SQL이 아닙니다. 물음표에는 바인딩 값이 들어갑니다. 실제 Hibernate의 별칭·열 순서는 다를 수 있습니다. 결과 기록에는 자신이 확인한 id와 SQL을 적습니다.

## 4. 1000원 이하 조회

먼저 노트 3000원, 무료 0원, 펜 1000원의 결과를 예측합니다. DB에서 직접 표현하면 다음과 같습니다.

```sql
SELECT id, name, price FROM products
WHERE price <= 1000
ORDER BY id;
```

이 조건을 `findByPriceLessThanEqualOrderByIdAsc(1000)`와 연결합니다. 이어 `findAffordable(1000)`의 @Query를 읽습니다.

- SQL은 `products` 표를 조회합니다.
- JPQL은 `ProductEntity` 클래스와 `p.price` 필드를 조회합니다.
- `:maxPrice`와 `@Param("maxPrice")`가 값을 연결합니다. 문자열로 값을 이어붙이지 않습니다.
- ORDER BY가 있어야 id 오름차순을 기대할 수 있습니다. 기본 findAll의 순서를 가정하지 않습니다.

```sh
./gradlew test --tests '*ProductJpaRepositoryTest.derivedQueryAndJpqlHaveSameBoundary' --info --rerun-tasks
```

완료 확인: 두 방법이 같은 두 상품의 id를 같은 순서로 반환하나요? 1000원이 포함되는 이유를 설명해보세요.

## 5. 변경 감지와 작업 묶음

`managedEntityChangesAreFlushedWithoutSave` 테스트를 읽습니다.

1. 노트 3000원을 저장하고 실제 id를 얻습니다.
2. 관리 목록을 비운 다음 그 id로 조회합니다.
3. 조회한 객체를 공책 2000원으로 변경합니다.
4. flush로 SQL을 보내고 clear 후 다시 읽습니다.
5. `assertEquals(2000, ...)`으로 DB에서 다시 읽은 가격을 확인합니다.

트랜잭션은 작업을 한 묶음으로 다루는 경계입니다. **flush는 전송, commit은 확정, rollback은 취소**입니다. clear는 관리 객체 목록을 비우며 DB 행을 삭제하지 않습니다. 오늘 @DataJpaTest는 기본 rollback이므로 서버 파일 DB에 영구 저장한 증거가 아닙니다. readOnly도 보안상 쓰기를 차단하는 장치는 아닙니다. JPA의 관리 상태(영속 상태)는 현재 영속성 컨텍스트가 객체를 추적한다는 뜻이며, 프로세스 재시작 후 데이터 보존을 뜻하지 않습니다. 재시작 보존은 19일 파일 DB에 연결한 API로 별도 검증합니다.

## 6. 두 DB와 실제 API 확인

| 구분 | 위치 | 오늘 확인할 사실 |
|---|---|---|
| main 설정 | `jdbc:h2:file:./data/products` | 실행 폴더 기준 파일 DB 준비 |
| test 설정 | `jdbc:h2:mem:product-tests;DB_CLOSE_DELAY=-1` | 테스트용 메모리 DB. DataJpaTest는 기본 임베디드 DB 대체도 가능 |
| 실제 HTTP | Service → MemoryProductRepository | 오늘은 여전히 Memory 상품 저장 |

```sh
./gradlew test
./gradlew bootRun
```

기존 API를 POST로 생성하면 응답의 실제 id와 Location을 기록하고, 받은 id로 GET을 확인합니다. JPA 테스트의 id를 HTTP 조회에 사용하지 않습니다. 서로 다른 경로입니다. HTTP가 JPA DB를 사용하도록 연결하는 것은 **19일 Adapter 실습**입니다. 오늘 API 재시작 후 상품이 사라지는 것은 아직 Memory이기 때문입니다.

파일 DB를 두 서버에서 동시에 열지 마세요. H2 파일을 Git에 커밋하지 않습니다.

## 7. 자주 막히는 지점

| 증상 | 먼저 확인 |
|---|---|
| DataJpaTest import 오류 | Boot 4의 `org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest`와 테스트 의존성 |
| Entity 인식 실패 | package com.example.product, @Entity, 파일 위치 |
| 쿼리 생성 오류 | 메서드의 Price와 실제 필드 price, JPQL의 ProductEntity 이름 |
| 메서드 매개변수 오류 | :maxPrice와 @Param("maxPrice") 철자 |
| 저장 후 조회 실패 | 하드코딩한 id 대신 저장 결과 id를 사용했는지 |
| DB 잠김 | 같은 파일 DB를 쓰는 다른 서버를 종료했는지 |
| 테스트 상품이 HTTP에서 안 보임 | 테스트 DB와 HTTP Memory는 별개임 |
| H2 파일이 다른 위치에 생김 | product-api 폴더에서 실행했는지 |

## 8. 제출과 19일 준비

Issue와 PR 제목은 `[실습] 상품 Entity와 JPA 저장소`, 브랜치는 `practice/product-jpa-basics`입니다. 실제 Issue 번호로 `Closes #번호`를 작성합니다.

- 전체 테스트 결과, 첫 저장의 실제 id와 SQL 관찰 기록
- SQL / 쿼리 메서드 / JPQL의 같은 조건 비교
- README의 실행 폴더·main/test 설정·명령
- Wiki의 구조·검증·회고 누적 기록
- API는 아직 Memory이고 19일 Adapter로 전환한다는 설명

`data/`, `*.mv.db`, `*.trace.db`, build·캐시·IDE·비밀값을 제외하고 Wrapper jar 추적 예외는 유지합니다. 기본 동작이 끝나면 선택으로 결과 없음·삭제 테스트를 추가하세요. 실제로 실행한 테스트만 제출 결과에 적습니다.
