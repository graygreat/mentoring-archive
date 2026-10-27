# 11월 23일 DB 표와 SQL 관찰 작업지

4시간, 네 블록마다 45분 활동 + 15분 휴식·정리. 완성 코드를 외우지 않고 **예측 → 실행 → 기록 → 설명**한다. 강사 코딩 시연 없이 [독립 주문 조회 ZIP](assets/order-query-lab.zip)을 사용한다. 책의 전체 주문 관리 API 정답이 아니라 작은 관계 관찰 예제다.

모르는 말은 [DB 기초](../shared/db-basics/README.md)와 [16일 쉬운 작업지](../2026-11-16/BEGINNER-WORKSHEET.md)에서 먼저 확인한다. 실행 폴더는 `order-query-lab`, Windows는 `gradlew.bat`를 사용한다.

## 1블록: 표에서 Java까지

먼저 19일 상품 API에서 노트의 실제 id와 수정 가격이 재시작 후에도 유지되는지 확인한다. 문제가 있으면 요청·응답·DB URL·실행 폴더를 기록하고 후속 질문으로 남긴다.

### 주문 3행과 항목 6행을 읽는다

아래 id는 **설명용 별명**이다. 실제 테스트의 숫자 id를 1부터라고 가정하지 않는다. 같은 열의 A끼리 선을 연결한다.

`purchase_orders`

| id (PK) | label |
|---|---|
| A | 주문 1 |
| B | 주문 2 |
| C | 주문 3 |

`order_items`

| id (PK) | name | order_id (FK) |
|---|---|---|
| i1 | 노트 | A |
| i2 | 펜 | A |
| i3 | 노트 | B |
| i4 | 펜 | B |
| i5 | 노트 | C |
| i6 | 펜 | C |

- [ ] `order_items.order_id → purchase_orders.id` 화살표를 그렸다.
- [ ] PK는 한 행을 구분하고, FK는 연결된 다른 표의 행을 가리킨다고 설명했다.
- [ ] 주문 A의 항목 이름 두 개를 찾았다: `________`.
- [ ] 주문은 3행, 항목은 6행임을 구분했다.

### SQL을 먼저 읽는다

```sql
SELECT id, label FROM purchase_orders WHERE id = ?;
SELECT id, name, order_id FROM order_items WHERE order_id = ?;
```

두 `?`에 같은 주문 id를 넣으면 첫 조회는 주문 하나, 두 번째 조회는 그 주문의 항목들을 가져온다. 아래는 연결된 두 표의 값을 한 결과로 읽는 SQL이다.

```sql
SELECT o.id, o.label, i.name
FROM purchase_orders o
LEFT JOIN order_items i ON i.order_id = o.id
ORDER BY o.id;
```

- 예측: 항목 2개가 있는 주문 하나는 JOIN 결과에서 몇 행인가? `___`.
- 이유: `________`.
- 항목 없는 주문을 남기는 것은 INNER JOIN인가 LEFT JOIN인가? `________`.

이 SQL은 읽기 예시다. 별도 DB를 임의로 만들거나 테스트가 만든 인메모리 DB에 외부 앱으로 접속할 필요는 없다. 실행은 제공 Java 테스트와 그 SQL 로그로 확인한다.

### Java 파일에서 대응 값을 찾는다

`src/main/java/com/example/orderlab/` 아래 파일을 연다.

| DB 값 | Java 위치 | 내가 찾은 줄·뜻 |
|---|---|---|
| purchase_orders 한 행 | PurchaseOrder | |
| 주문명 label | getLabel() | |
| order_id로 이어진 항목들 | getItems() | |
| 항목명 name | OrderItem.getName() | |

왜: Java의 `items`는 표의 한 열이 아니라, FK로 연결한 여러 항목을 나타낸다.

## 2블록: 한 주문의 로딩과 관리 객체 관찰

### LAZY는 언제 필요한가

`PurchaseOrder.java`의 `@OneToMany(fetch = FetchType.LAZY)`를 찾는다. “관계 데이터를 필요할 때 읽는 방식”으로 읽는다. 이 표시만 보고 항상 N+1이라고 결론내리지 않는다.

1. `OrderQueryTest.java`의 `lazyCollectionsProduceOnePlusNQueries`에서 `repository.findAllByOrderByIdAsc()` 다음 줄에 IDE 중단점을 둔다.
2. 테스트를 Debug 실행한다. 목록을 읽은 뒤 로그의 주문 SELECT를 찾는다.
3. 자동으로 관계를 펼치는 IDE 표시가 SQL을 발생시킬 수 있으므로 `items`를 미리 펼치지 않는다.
4. 디버거 평가로 `orders.get(0).getLabel()`을 읽고, 다음으로 `orders.get(0).getItems().size()`를 읽는다.
5. 첫 주문의 항목을 읽을 때 추가 SQL이 있는지 기록한다. 다시 같은 size를 읽으면 어떤가?
6. 디버그로 평가한 작업은 측정에 영향을 줄 수 있다. 기록 후 중단점을 끄고 테스트를 새로 일반 실행해 최종 수를 확인한다.

| 행동 | 예상 SQL | 실제 SQL·이유 |
|---|---|---|
| 주문 목록 조회 | 주문 SELECT | |
| 첫 주문 label | 추가 조회 없음 | |
| 첫 주문 items.size | 항목 SELECT 가능 | |
| 이미 초기화한 같은 items 재접근 | 같은 추가 조회 없음 | |

디버거가 어렵다면 SQL 로그와 코드의 `findAll…`·`getItems().size()` 위치를 대응해 읽는다. 한 주문의 관찰을 마친 뒤 기본 테스트 전체가 모든 주문의 items를 읽는다는 점을 확인한다.

### 같은 id와 같은 객체를 구분한다

```sh
./gradlew test --tests '*PersistenceContextTest' --info --rerun-tasks
```

`--rerun-tasks`는 UP-TO-DATE로 건너뛰지 않고 다시 실행하고, `--info`는 테스트의 표준 출력(SQL 로그)을 콘솔에 보이게 한다. Windows PowerShell에서는 다음처럼 실행한다.

```powershell
.\gradlew.bat test --tests '*PersistenceContextTest' --info --rerun-tasks
```

콘솔이 길면 프로젝트 폴더의 `build/reports/tests/test/index.html`을 브라우저로 연다. Classes 목록에서 `com.example.orderlab.PersistenceContextTest` → **Standard output** 탭을 누른다. 같은 보고서에서 `com.example.orderlab.OrderQueryTest`의 **Standard output**을 열면 SQL과 `lazy-select-count`·`fetch-select-count`를 확인할 수 있다. 보고서는 마지막 테스트 실행 결과로 갱신되므로 필요한 기록을 그때 남긴다.

`sameContextKeepsIdentityAndFlushWritesChanges`를 순서대로 읽는다.

| 행동 | 관리 작업 공간(영속성 컨텍스트) | DB·확인 대상 |
|---|---|---|
| 저장 후 clear | 준비 중 객체 분리 | 저장된 id 유지 |
| first = findById(id) | first 관리 | SELECT로 읽은 값 |
| 같은 id 다시 조회 | 같은 컨텍스트의 같은 객체 | assertSame |
| first.rename("변경") | 관리 객체의 값 변경 | 아직 확정(commit)과 구분 |
| flush | 바뀐 SQL을 DB로 보냄 | UPDATE·롤백 가능 |
| clear | 객체 관리 해제 | DB 행 삭제 아님 |
| 다시 findById(id) | 새 객체로 읽어 관리 | assertNotSame·값은 변경 |

- 예측: clear 뒤에도 id는 같은가? Java 객체 참조도 같은가? `________`.
- 실제 단언 결과: `________`.
- 왜 rename 직후 같은 객체의 값만 보면 DB 반영 증거가 부족한가? `________`.

| 용어 | 쉽게 말하면 | 혼동하면 안 되는 것 |
|---|---|---|
| 영속성 컨텍스트 | 지금 쓰는 Entity를 관리하는 작업 공간 | 모든 요청이 공유하는 전역 창고 아님 |
| 1차 캐시 | 같은 작업 공간에서 같은 id의 관리 객체 재사용 | 다른 컨텍스트까지 같은 객체 보장 아님 |
| flush | 변경 SQL 보내기 | commit(확정) 아님 |
| clear | 관리 객체 분리 | DELETE나 DB 초기화 아님 |
| rollback | 트랜잭션 변경 취소 | flush했어도 취소 가능 |

`uninitializedCollectionCannotLoadAfterContextCloses`는 미초기화 items를 남긴 채 트랜잭션이 끝난 뒤 접근한다. 왜 추가 조회를 할 수 없는지, 이미 읽은 관계라면 같은 상황인지 설명한다. Entity 응답 직렬화·OSIV=true·EAGER 일괄 변경으로 우회하지 않고, 필요한 관계를 Service 트랜잭션 안에서 읽어 DTO로 구성하는 방향을 정리한다.

## 3블록: 3개 주문에서 4회와 1회 비교

### 준비 SQL을 측정에서 빼는 이유

`OrderQueryTest.seedAndClear()`를 읽고 다음 세 줄의 목적을 자기 말로 쓴다.

| 준비 단계 | 왜 필요한가 | 내 설명 |
|---|---|---|
| entityManager.flush() | seed INSERT·관계 설정을 측정 전에 보냄 | |
| entityManager.clear() | 준비하며 남은 관리 객체 재사용을 없앰 | |
| statistics.clear() | 준비 SQL 수를 0으로 다시 셈 | |

`statistics.clear()`는 SQL 통계 숫자만 초기화한다. `entityManager.clear()`는 관리 객체를 분리한다. 어느 것도 DB 행 삭제 명령이 아니다.

### 먼저 SQL 수를 예측한다

| 실행 | 예상 SELECT | 실제 로그·통계 |
|---|---|---|
| 주문 3개 목록 조회 | 1 | |
| 주문 A의 items 읽기 | +1 | |
| 주문 B의 items 읽기 | +1 | |
| 주문 C의 items 읽기 | +1 | |
| 총합 | 4 | |

항목이 6개라서 7회가 되는 것이 아니다. 이 설정에서는 **미초기화 주문별 컬렉션**을 하나씩 조회하므로 목록 1 + 주문 수 3이다.

```sh
./gradlew test --tests '*OrderQueryTest' --info --rerun-tasks
```

PowerShell:

```powershell
.\gradlew.bat test --tests '*OrderQueryTest' --info --rerun-tasks
```

콘솔 또는 `build/reports/tests/test/index.html` → Classes → `com.example.orderlab.OrderQueryTest` → **Standard output**에서 로그를 읽는다.

- [ ] `lazy-select-count=4`와 실제 SELECT를 대응했다.
- [ ] 주문 3개, 항목 6개, 주문명·노트/펜도 확인했다.
- [ ] prepareStatementCount는 원래 모든 준비 SQL 수이며, 여기서는 측정 구간이 SELECT만이라 SELECT 수로 비교함을 확인했다.

### fetch join을 읽기 전에 초안을 적는다

`OrderQueryRepository.findAllWithItems`의 답을 먼저 펼치지 말고 “주문을 읽으며 items도 함께 읽는다”는 요구를 JPQL로 써본다. 책·공식 문서를 참고해도 된다. 초안 `________`.

| 구분 | 이름과 역할 |
|---|---|
| SQL JOIN | DB 표·열 이름으로 행을 연결해 결과 구성 |
| JPQL join | Entity·필드 이름으로 객체 관계 조회 |
| JPQL join fetch | 조회 Entity의 연관 객체·컬렉션도 함께 로딩 |

일반 join이 있다고 items 초기화까지 보장되는 것은 아니다. SQL JOIN이 곧 JPA 객체의 초기화 명령인 것도 아니다. fetch join은 ORM에 필요한 관계를 함께 로딩하라고 명시한다.

참고 구현과 비교한 뒤 같은 데이터를 준비해 개선 테스트를 확인한다.

| 방식 | 주문 수·이름 | 항목 수·이름 | SELECT |
|---|---|---|---|
| 기본 조회 + items 접근 | | | |
| fetch join + 같은 접근 | | | |

완료 기준: 같은 주문 3개·항목 6개·내용을 유지하며 4 → 1. 준비 SQL 제외, clear, 같은 설정과 접근 순서를 유지한다. 배치 페치·캐시·이미 초기화된 관계 등 조건이 다르면 수가 달라질 수 있다.

## 4블록: 설명과 제출

동료에게 다음 질문을 표·코드·SQL 근거를 가리키며 답한다.

1. order_id는 어느 표의 어떤 값을 가리키나?
2. 첫 항목 SELECT는 코드의 어느 행동에서 필요했나?
3. N+1에서 N은 여기서 무엇인가? 왜 4회인가?
4. fetch join 뒤 값도 같은가? 쿼리 수만 줄이고 항목이 빠지지 않았나?
5. flush와 commit, clear와 DELETE의 차이는?
6. “LAZY면 항상 N+1”, “EAGER면 해결”을 왜 단정할 수 없나?

- [ ] 전체 `./gradlew test` 통과.
- [ ] README에 예측·실제 SQL·같은 결과·조건·틀린 예측 수정 기록.
- [ ] 공통 Wiki Home·01-Setup·02-Architecture·03-API·04-Verification·05-Retrospective 누적. 03-API에는 이 랩에 HTTP API 미구현을 표시.
- [ ] `sesac-spring-boot-study` / `practice/jpa-query-lab` / Issue·PR `[실습] 지연 로딩과 N+1 관찰·개선`.
- [ ] PR에 `Closes #실제번호`, Wiki 링크, 테스트·SQL 증거. 자체 확인·병합 후 main pull.
- [ ] Wrapper jar 포함, `!order-query-lab/gradle/wrapper/gradle-wrapper.jar` 유지. build·.gradle·IDE·DB·.env 제외, 중첩 .git 없음.

[단축 URL 별도 과제](../assignments/short-url/)의 생성·복사·이동·오류 화면과 AI 활용·본인 수정을 공유한다. 미완료는 구분해 적는다. 마감은 별도 안내다.

## 막혔을 때

1. 기초 힌트: PK/FK 표에서 한 주문과 항목 두 개를 먼저 연결한다. `getItems()`가 어떤 행을 읽어야 하는지 말한다.
2. 실행 힌트: 테스트 이름·실행 폴더·로그 구간을 확인하고 seed flush → clear → 통계 초기화 순서를 비교한다. 디버거로 미리 펼친 관계가 없는지도 확인한다.
3. 비교 힌트: 예상·실제·첫 다른 SQL을 강사에게 보여주고 해당 참고 메서드만 비교한다. 4나 1을 맞추려고 단언 숫자만 고치지 않는다.

필수 관찰이 끝난 뒤 선택: EntityGraph·배치 조회·컬렉션 fetch join의 페이지네이션 제약. 모든 관계를 무조건 fetch하도록 바꾸지 않는다.
