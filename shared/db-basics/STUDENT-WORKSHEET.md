# DB 기초 · 멘티 작업지

[DB 안내](index.html) · [SQL 파일](basics.sql) · [관계 SQL](relations.sql)

상품 관리의 공통 Java 코드를 바꾸기 전에 작성합니다. 한 항목마다 **예상 → 실행/표 채우기 → 실제 → 이유**를 기록합니다. 14일에는 1~4번 표 활동을 우선하고, SQL 실행은 준비 상태에 따라 16일에 이어 확인합니다.

## 1. 표 읽기 · 10분

| id | name | price |
|---:|---|---:|
| 101 | 노트 | 3000 |
| 102 | 펜 | 1000 |
| 103 | 무료 | 0 |

- [ ] 표 이름·열 세 개·행 세 개를 각각 가리킬 수 있다.
- [ ] 102번 상품의 이름과 가격을 말할 수 있다.
- [ ] 이름이 같은 상품 두 개를 id로 구분할 수 있다.
- [ ] `0`, `NULL`, 빈 문자열이 같은 값인지 설명했다.

질문: 이 표에 `(101, 새 상품, 500)`을 추가하면 왜 안 될까요? `name NOT NULL`이면 공백 이름도 자동 거부될까요?

| 질문 | 내 예상 | 확인한 이유 |
|---|---|---|
| id가 중복되면? | | |
| name이 NULL이면? | | |
| name이 빈 문자열이면? | | |
| price가 0이면? | | |

## 2. 조건 조회 · 10분

```sql
SELECT id, name, price FROM lab_products
WHERE price <= 1000 ORDER BY id;
```

- [ ] 결과의 행 개수와 순서를 먼저 적었다.
- [ ] `<=`를 `<`로 바꾸면 무엇이 달라지는지 설명했다.
- [ ] 결과가 없을 때 표가 삭제되는 것이 아님을 설명했다.

## 3. 수정·삭제 · 10분

아직 실행하지 말고 위의 초기 표를 종이에 복사해 변경합니다.

```sql
UPDATE lab_products SET price = 2000 WHERE id = 101;
DELETE FROM lab_products WHERE id = 102;
```

| 확인 | 내 기록 |
|---|---|
| UPDATE 직후 101번 행 | |
| UPDATE에 영향받지 않은 행 | |
| DELETE 이후 남은 id | |
| WHERE가 없다면 영향받을 범위 | |

실행할 때는 같은 WHERE의 SELECT로 대상을 먼저 확인합니다. 앱 DB에 위 SQL을 붙여넣지 않습니다.

## 4. 한 묶음의 변경 · 10분

`basics.sql`의 트랜잭션 구간을 읽습니다.

- [ ] 2000→900으로 바꾼 뒤 ROLLBACK하면 왜 2000인지 적었다.
- [ ] 1500으로 바꾼 뒤 COMMIT하면 해당 트랜잭션의 변경이 확정됨을 설명했다.
- [ ] 메모리 DB에서는 COMMIT해도 프로세스 종료 후 사라진다는 점을 적었다.
- [ ] HTTP 400과 DB ROLLBACK이 서로 다른 역할임을 설명했다.

## 5. 독립 DB에서 실제 확인 · 15~20분

[안내의 실행 순서](README.md)를 따라 `db-basics.gradle`, `basics.sql`, `relations.sql`을 본인 `product-api/db-lab/`에 둡니다. 기존 Gradle Wrapper로 독립 H2 메모리 SQL Shell을 엽니다.

```sh
./gradlew -I db-lab/db-basics.gradle dbBasics --console=plain
```

Windows PowerShell:

```powershell
.\gradlew.bat -I db-lab/db-basics.gradle dbBasics --console=plain
```

`sql>`에서:

```sql
RUNSCRIPT FROM 'db-lab/basics.sql';
SELECT id, name, price FROM lab_products ORDER BY id;
```

- [ ] 두 행: 101·공책·1500, 103·무료·0을 확인했다.
- [ ] RUNSCRIPT가 중간 SELECT를 모두 출력하지 않음을 알고, 최종 SELECT를 별도로 실행했다.
- [ ] `exit` 후 도구를 다시 열면 연습표가 없는 것을 확인했다.
- [ ] 내 앱의 `data/`를 삭제하지 않았고 app datasource 설정도 바꾸지 않았다.

문장별 변화는 새 세션에서 basics.sql을 한 문장씩 입력해 비교합니다. 여러 줄 SQL은 마지막에 세미콜론을 붙입니다.

## 6. 두 표의 관계 · 23일 준비 10분

`relations.sql`에서 주문 201의 항목을 찾고 `order_id → id`로 선을 긋습니다.

- [ ] 한 주문이 항목 둘을 가질 수 있음을 표로 설명했다.
- [ ] 존재하지 않는 주문을 가리키는 FK가 왜 문제인지 설명했다.
- [ ] FK가 있다고 조회가 자동 JOIN되는 것은 아님을 설명했다.
- [ ] JOIN 한 SQL이 주문 3개·항목 6개를 6행으로 보여주는 이유를 적었다.

## 7. JPA로 연결 · 16일 사용

| DB에서 본 것 | JPA 수업 코드에서 찾을 것 | 찾은 파일/메서드 |
|---|---|---|
| products 테이블 | @Table(name = "products") | |
| 한 행의 식별자 | @Id, 저장 후 실제 getId() | |
| 한 행 저장 | new ProductEntity("노트", 3000), save | |
| id 조건 조회 | findById(실제 id) | |
| 가격 상한 조회 | findByPriceLessThanEqualOrderByIdAsc | |

이 연습표 `lab_products`를 앱 Entity의 `products`로 이름 바꾸지 않습니다. [16일 초보 작업지](../../2026-11-16/BEGINNER-WORKSHEET.md)로 이어갑니다.

## 막히면 이 순서로 확인

| 증상 | 먼저 확인 |
|---|---|
| Gradle 파일을 못 찾음 | product-api 폴더, db-lab 파일 위치, `-I` 경로 |
| 의존성 다운로드 실패 | 네트워크/프록시. 표 예측부터 진행하고 강사에게 공유 |
| SQL 문장이 끝나지 않음 | 마지막 세미콜론, 문자열 작은따옴표 |
| 테이블이 없다고 나옴 | 같은 SQL Shell 세션에서 CREATE/RUNSCRIPT를 했는지 |
| 테이블이 이미 존재함 | 같은 세션에서 스크립트를 반복했는지. 도구 종료 후 새 세션 |
| 중복 키 오류 | 같은 PK id로 INSERT했는지. 기존 행을 지우기 전에 의도 확인 |
| 앱 재시작 후 내 연습표가 안 보임 | 별도 메모리 DB가 맞음. 앱 파일 DB와 공유하지 않음 |

기록은 `product-api/docs/db-basics.md`에 예측·실제·틀렸던 이유를 적고 기존 실습 PR에 포함합니다. 별도 필수 PR을 추가하지 않습니다.
