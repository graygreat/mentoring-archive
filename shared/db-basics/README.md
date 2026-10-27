# 상품 한 개로 시작하는 DB 기초

JPA 전에 필요한 말과 동작을 상품 표로 익힙니다. 교재의 DB 접근 부분과 함께 읽고, 책의 JDBC와 수업의 JPA가 같은 SQL 저장 요구를 서로 다르게 다루는지 비교합니다. 교재 본문·쪽수를 대신하는 자료가 아닙니다.

[화면으로 보기](index.html) · [멘티 작업지](STUDENT-WORKSHEET.md) · [SQL 기본 연습](basics.sql) · [관계·JOIN 연습](relations.sql) · [Gradle 실행 파일](db-basics.gradle)

## 이번 주 순서

- 14일 뒤 2시간: 표·행·열·키·자료형을 읽고 SQL 결과를 예측합니다. 설명보다 표 채우기·짝 설명·수정 전후 비교가 중심입니다.
- 16일: 같은 상품 표를 Entity와 Repository로 저장·조회하고 SQL 로그와 비교합니다. [JPA 초보 작업지](../../2026-11-16/BEGINNER-WORKSHEET.md)를 사용합니다.
- 19일: 이미 만든 부품을 연결해 실제 API 저장소를 바꾸고 재시작 후 같은 id를 확인합니다.
- 23일: 두 표를 FK로 연결해 읽고, SQL JOIN에서 JPA 지연 로딩·N+1 관찰로 확장합니다.

## 1. 먼저 이 표부터 읽습니다

| id | name | price |
|---:|---|---:|
| 101 | 노트 | 3000 |
| 102 | 펜 | 1000 |
| 103 | 무료 | 0 |

표 이름은 `lab_products`. 한 행은 상품 한 개, 열은 상품이 가진 값의 종류입니다. 이름이 같은 상품도 있을 수 있어 id로 구분합니다. 연습표의 101~103은 직접 정한 값이고, JPA API에서는 DB가 발급한 실제 id를 사용합니다.

| 말 | 이 수업에서 확인할 뜻 |
|---|---|
| 데이터베이스(DB) | 관련 데이터를 정해진 구조로 저장해 조회·변경하는 대상 |
| DBMS | DB에 저장·조회 명령을 처리하는 프로그램. 이번 실습은 H2 |
| 테이블·행·열 | 상품 표 / 상품 한 개 / id·이름·가격 같은 항목 |
| 자료형 | id는 BIGINT, 이름은 문자열 VARCHAR, 가격은 정수 INTEGER. 이 예시는 원 단위 정수 가격 |
| PK(기본키) | 한 행을 구분하는 키. 여기서는 id이며 중복·NULL 불가 |
| NULL | 값이 없거나 미정임을 나타냄. 빈 문자열·숫자 0과 다름. `IS NULL`로 비교 |
| 제약 | NOT NULL은 NULL 금지. CHECK(price >= 0)는 음수 금지. 빈 이름 금지는 별도 업무 검증 |
| FK(외래키) | 다른 표의 키를 가리키는 값. 어떤 주문의 항목인지 연결할 때 사용 |
| SQL | DBMS에 조회·저장·수정·삭제 등을 요청하는 언어 |
| 트랜잭션 | 함께 성공해야 하는 DB 작업을 한 묶음으로 처리하는 경계 |

Java 객체는 메모리 안의 값, JSON은 주고받는 표현, DB 행은 저장된 기록입니다. 모양이 비슷해도 같은 물건은 아닙니다. Controller가 JSON을 받았다고 DB에 저장된 것은 아닙니다.

## 2. SQL을 읽고 표가 어떻게 바뀔지 적습니다

| SQL | 읽는 순서 | 예상 |
|---|---|---|
| `INSERT INTO lab_products (id, name, price) VALUES (101, '노트', 3000)` | 어느 표에 어떤 열·값을 넣는가 | 상품 한 행 추가 |
| `SELECT id, name, price FROM lab_products WHERE price <= 1000 ORDER BY id` | 표 → 조건 → 결과 열 → 정렬 | 펜·무료, id 순서 |
| `UPDATE lab_products SET price = 2000 WHERE id = 101` | 대상 id → 바꿀 값 | 101번 가격만 변경 |
| `DELETE FROM lab_products WHERE id = 102` | 대상 id → 행 제거 | 102번만 제거 |

문자열은 작은따옴표, 숫자는 따옴표 없이 씁니다. 세미콜론은 문장 끝입니다. SELECT로 대상을 먼저 확인한 뒤 같은 WHERE로 UPDATE/DELETE를 실행합니다. WHERE를 빠뜨리면 모든 행이 대상이 될 수 있습니다. 이 연습은 앱 DB가 아닌 별도 메모리 DB에서만 실행합니다.

COMMIT은 현재 트랜잭션의 변경을 확정하고 ROLLBACK은 그 트랜잭션의 변경을 되돌립니다. 이미 확정된 과거 변경까지 취소하는 기능은 아닙니다. HTTP 400 응답 자체가 자동으로 DB를 되돌리는 것도 아닙니다. H2의 테이블 생성 같은 DDL에는 암묵적 commit이 있으므로 아래 롤백 실험은 UPDATE만 대상으로 합니다.

## 3. 실행할 때는 자동으로 분리된 연습 DB를 사용합니다

14일에는 종이·화면 예측 활동부터 합니다. 환경 준비로 본 실습이 밀리면 실행은 16일에 이어 확인합니다. H2 콘솔용 서버를 추가로 설치하거나 앱 DB 비밀번호를 바꿀 필요가 없습니다.

1. 위 링크의 `db-basics.gradle`, `basics.sql`, `relations.sql`을 내려받아 본인 `product-api/db-lab/` 폴더에 둡니다.
2. `build.gradle`, `gradlew`가 있는 **product-api 폴더**에서 실행합니다. 기존 Java 17·Gradle Wrapper를 사용합니다. 처음 실행은 Maven Central 의존성 다운로드가 필요합니다.

macOS/Linux:

```sh
./gradlew -I db-lab/db-basics.gradle dbBasics --console=plain
```

Windows PowerShell:

```powershell
.\gradlew.bat -I db-lab/db-basics.gradle dbBasics --console=plain
```

3. `sql>` 입력 위치가 나오면 아래 두 문장을 차례로 입력합니다.

```sql
RUNSCRIPT FROM 'db-lab/basics.sql';
SELECT id, name, price FROM lab_products ORDER BY id;
```

마지막 SELECT의 결과가 `(101, 공책, 1500)`, `(103, 무료, 0)`인지 확인합니다. RUNSCRIPT는 SQL 파일을 실행하며 중간 SELECT 결과를 Shell에 모두 표시하지는 않습니다. 중간 변화를 직접 보려면 새 세션에서 basics.sql을 문장별로 입력합니다. 이때 ROLLBACK 직후 101번 가격은 2000, COMMIT 이후 1500입니다. `exit`로 종료합니다. 새로 실행하면 DB가 비어 있습니다. 같은 세션에서 CREATE TABLE을 다시 실행하면 이미 존재한다는 오류가 나므로 새 세션으로 시작합니다.

관계 연습은 같은 실행 도구에서 다음 명령으로 따로 확인합니다.

```sql
RUNSCRIPT FROM 'db-lab/relations.sql';
SELECT o.id, o.label, i.name
FROM lab_orders o JOIN lab_order_items i ON i.order_id = o.id
ORDER BY o.id, i.id;
```

이 도구는 H2 2.4.240의 `jdbc:h2:mem:db_basics`로 고정되어 있습니다. 파일 DB URL·로그인 입력을 요구하지 않고 앱 설정을 바꾸지 않습니다. COMMIT해도 프로세스가 끝나면 메모리 DB는 없어집니다. 기존 상품 API의 `jdbc:h2:file:./data/products` 파일을 지우거나 접속 URL을 바꿔 해결하지 않습니다.

## 4. SQL과 JPA를 한 줄씩 연결합니다

| 하려는 일 | SQL에서 보는 것 | JPA 수업에서 보는 것 |
|---|---|---|
| 저장 | INSERT와 생성된 행 | `repository.save(new ProductEntity("노트", 3000))` |
| id 조회 | SELECT ... WHERE id = ? | `repository.findById(실제id)` |
| 가격 조건 | WHERE price <= ? ORDER BY id | `findByPriceLessThanEqualOrderByIdAsc(1000)` |
| 수정 | UPDATE와 변경된 행 | 트랜잭션 안에서 조회한 Entity의 `change` 호출 |

이 표는 역할 비교이며 SQL 실행 시점·모양을 그대로 보장하는 표가 아닙니다. 실제 JPA 로그에는 `?` 파라미터와 자동 별칭 등이 보일 수 있습니다. `save`는 새 객체/기존 객체 등에 따라 동작이 달라지고 항상 즉시 INSERT한다는 뜻이 아닙니다. API 요청 전체 연결은 19일에 합니다.

`@Entity`는 JPA 관리 대상 클래스, `@Table(name="products")`는 앱 테이블 이름, `@Id`는 식별자 표시입니다. `lab_products`는 SQL 연습표이고 `products`는 앱의 저장표입니다. JPA는 DB와 SQL을 없애는 도구가 아니라 객체를 통해 DB를 다루도록 돕는 도구입니다.

## 5. 관계는 표 두 개로 먼저 봅니다

주문 201·202·203과 항목 301~306을 만듭니다. `lab_order_items.order_id`가 어느 `lab_orders.id`를 가리키는지 선을 긋습니다. FK는 참조 무결성을 확인하지만 JOIN SQL을 자동 실행하지 않습니다. `relations.sql`의 JOIN은 한 SQL에서 6행을 반환하며 주문 정보는 항목 수만큼 반복됩니다.

23일 JPA 실습에서는 같은 구조를 가진 별도 Entity·표를 사용합니다. SQL JOIN은 결과 행을 결합하는 명령이고, JPQL fetch join은 Entity 연관관계를 함께 가져오는 지시까지 담습니다. 둘을 같은 표현으로 외우지 않고 실제 초기화·SQL 횟수를 관찰합니다.

## 공식 근거

[H2 튜토리얼·Shell](https://www.h2database.com/html/tutorial.html) · [H2 SQL 명령](https://www.h2database.com/html/commands.html) · [Spring Data JPA 시작](https://docs.spring.io/spring-data/jpa/reference/jpa/getting-started.html) · [트랜잭션](https://docs.spring.io/spring-data/jpa/reference/jpa/transactions.html)

## 작성자 실행 확인 · 2026-10-27

Java 17·H2 2.4.240·기존 Gradle Wrapper에서 안내와 동일한 `-I db-lab/db-basics.gradle dbBasics --console=plain` 명령을 실행했습니다. 최종 상품 2행과 관계 JOIN 6행을 확인했습니다. 별도 JDBC 검증으로 PK·NOT NULL·CHECK·FK 거부, 빈 문자열과 NULL 구별, UPDATE의 rollback/commit, 마지막 연결 종료 후 메모리 DB 초기화 등 15개 확인을 통과했습니다. 멘티는 자기 환경에서 예상·실제 결과를 다시 기록합니다.
