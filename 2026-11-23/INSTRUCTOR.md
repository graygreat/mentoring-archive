# 11월 23일 영속성·지연 로딩·N+1

4시간. 책의 상품 관리 JPA 전환을 회고하고, 별도 최소 주문 조회 예제로 영속성과 SQL을 관찰한다. 책 주문 관리의 정답이나 전체 주문 API 구현 과제가 아니다.

## 운영

| 블록 | 45분 활동 | 15분 |
|---|---|---|
| 1 | 19일 결과 확인, 책 저장 계층 비교, 영속성 컨텍스트·동일성 | 휴식 |
| 2 | 변경 감지·flush/clear·준영속·LAZY 실험 | 휴식 |
| 3 | SQL 예측, N+1 재현, fetch join 개선·비교 | 휴식 |
| 4 | 동료/면접 설명, 단축 URL 결과 공유, GitHub | 제출 정리 |

완성 코드를 먼저 읽히기보다 **예측 → 실행 → 결과 비교 → 원인 설명** 순서로 운영한다. 강사 코딩 시연은 없다. 코드가 있는 참고 자료와 새 기능을 요구사항부터 작성하는 과제를 구분한다.

## 출발과 파일

[order-query-lab.zip](assets/order-query-lab.zip)을 별도 `order-query-lab/` 프로젝트로 추가한다. 중첩 .git은 포함하지 않는다. Java 17 이상과 Wrapper 사용. 루트 .gitignore에 `!order-query-lab/gradle/wrapper/gradle-wrapper.jar`를 추가하고 build/.gradle/IDE/.env/DB는 제외한다.

공유 원본 `shared/order_sources.py`의 `ORDER_SOURCES`를 모달에 그대로 표시한다. 앱·PurchaseOrder·OrderItem·OrderQueryRepository·OrderQueryTest·PersistenceContextTest 6개 파일이다. 모달 경로는 com/example/orderlab이다. 참고 ZIP에는 동작하는 개선 코드도 포함되므로 먼저 개선 메서드를 펼치지 않고 직접 작성·비교하도록 안내한다. 필요하면 임시 학습 브랜치에서 fetch 메서드와 대응 개선 테스트를 잠시 치우고 작성한 뒤 복구한다. 메인 결과물이나 기존 데이터를 삭제하지 않는다.

PurchaseOrder → OrderItem은 단방향 @OneToMany LAZY, JoinColumn, Cascade ALL의 최소 관계다. 상품 API의 모델에 관계를 추가하지 않는다. 수업 예제는 상품명 중심의 작은 모델이며 재고·결제·주문 상태 등 책 요구를 구현했다고 주장하지 않는다.

## 실행·완료 기준

```sh
./gradlew test --tests '*PersistenceContextTest'
./gradlew test --tests '*OrderQueryTest'
./gradlew test
```

Windows는 `gradlew.bat` 사용. 실행 폴더는 order-query-lab이다.

PersistenceContextTest:

- 하나의 컨텍스트에서 같은 id를 다시 조회하면 같은 객체 참조인지 확인한다.
- 관리 객체 값을 변경하고 flush → clear → 재조회로 실제 값을 확인한다. flush는 commit이 아니다.
- 별도의 NOT_SUPPORTED 테스트에서 TransactionTemplate의 트랜잭션이 종료된 뒤 미초기화 컬렉션 접근의 LazyInitializationException을 확인한다. 이미 초기화한 관계나 활성 테스트 트랜잭션이면 같은 현상이 재현되지 않을 수 있다.
- 비트랜잭션 테스트가 만든 데이터는 finally에서 별도 트랜잭션으로 정리한다.

OrderQueryTest:

1. 각 테스트에서 주문 3개, 각 항목 2개를 준비한다.
2. seed flush → clear → Hibernate statistics.clear 순서로 측정 전 상태를 맞춘다.
3. 기본 조회와 모든 items 접근으로 SELECT 4회(1+3)를 확인한다.
4. `findAllWithItems`의 left join fetch로 같은 주문·항목을 SELECT 1회로 확인한다.
5. 결과 개수·내용과 측정 범위도 비교한다. 타이밍 수치만으로 결론내리지 않는다.

prepareStatementCount는 모든 prepared statement 수다. 본 실험에서는 seed가 측정 전에 끝나고 측정 구간이 SELECT뿐이라 SELECT 수로 비교할 수 있다. 로그에 다른 SQL이 섞이면 범위를 다시 확인한다. 배치 페치·1차/2차 캐시·쿼리 캐시·미리 초기화된 관계에 따라 숫자가 달라질 수 있으므로 동일 설정을 유지한다.

## 설명할 핵심

- flush는 동기화, clear는 관리 해제, commit은 확정이며 서로 다르다.
- N+1은 LAZY 표시만 보고 단정하지 말고 실제 접근과 SQL로 확인한다. EAGER로 전환한다고 자동 해결되지 않는다.
- Service 트랜잭션 안에서 목적에 맞게 로딩하고 DTO를 구성한다. Entity 직렬화나 OSIV=true 우회는 요구하지 않는다.
- left join은 항목 없는 주문을 포함할 수 있다. 필요하면 별도 선택 테스트를 추가한다.
- 컬렉션 fetch join의 페이지네이션과 복수 컬렉션은 선택 심화다. 모든 관계를 항상 fetch하라고 가르치지 않는다.

면접 활동은 한 문장 정의 + 본인 실험 + 한계 순서로 답하게 한다. 동료에게 SQL 예측을 먼저 말하고 로그로 검증한다.

## 제출

저장소 `sesac-spring-boot-study`, 브랜치 `practice/jpa-query-lab`, Issue/PR `[실습] 지연 로딩과 N+1 관찰·개선`. 필수 Issue 1개·병합 PR 1개. main pull → Issue → 브랜치 → 실험/기록 → test → commit/push → base main PR → 자체 검토·병합 → main pull. 실제 Issue 번호를 `Closes #번호`에 연결한다.

order-query-lab/README에는 실행 조건·데이터 준비·4→1 비교·결과 내용·한계를 기록한다. 공통 Wiki Home, 01-Setup, 02-Architecture, 03-API, 04-Verification, 05-Retrospective에 프로젝트별로 누적한다. 03-API에는 이 랩이 API 구현 프로젝트가 아님을 표시한다. Wiki 링크는 PR에서 확인한다.

별도 [단축 URL 과제](../assignments/short-url/)는 AI 프론트·백엔드 연동을 권장 공유한다. 생성·복사·이동·오류 표시, 프롬프트와 본인 수정, 실제 API 계약을 설명하게 한다. 제출 마감은 별도 안내이며 JPA 랩 필수 완료와 섞지 않는다.
