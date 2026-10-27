# 2026-11-16 강사용 가이드 · JPA 첫 저장과 조회 · 4시간

책의 상품 관리 DB 접근 절을 함께 읽습니다. 정확한 페이지와 교재 코드는 실제 책에서 확인합니다. 교재 CH 11의 JDBC와 수업의 JPA는 같은 저장 요구를 다른 방식으로 해결합니다. 제공 Java 코드는 교재 원문이 아닌 수업 독립 예제입니다.

## 오늘 목표와 시간

멘티가 DB 초보임을 전제로 용어를 먼저 암기시키지 않습니다. 노트 3000원 한 개를 객체 → SQL → 행으로 따라간 뒤 도구 이름을 붙입니다. 강사 코딩 시연 없이 짧은 설명 → 질문 → 자율 작업 → 기대 결과 비교로 진행합니다. 각 블록은 집중 45분 + 휴식·정리 15분입니다.

| 블록 | 활동 | 확인 질문 |
|---|---|---|
| 1 | DB 전제 확인 15분 + Entity 매핑·설정 30분 | 행과 열, PK, null을 설명할 수 있는가? |
| 2 | Entity·Repository 작성·저장·조회 45분 | 저장 후 id는 어디서 얻는가? |
| 3 | 조건 검색·테스트 읽기 45분 | 1000원 이하 결과를 실행 전에 예측하는가? |
| 4 | 트랜잭션 첫 관찰·테스트·19일 준비 45분 | flush와 commit, 테스트 DB와 서버 DB를 구분하는가? |

DB 전제가 어려우면 [공통 DB 기초](../shared/db-basics/README.md)와 [작업지](../shared/db-basics/STUDENT-WORKSHEET.md)로 돌아갑니다. 확장 개념을 더 설명하기보다 저장 한 건과 id 조회를 먼저 성공시킵니다. 멘티에게는 [JPA 첫 실습 작업지](BEGINNER-WORKSHEET.md)를 제공합니다.

## 같은 상품의 세 모습

- 요청 DTO: JSON 입력을 받는 모양. `name=노트`, `price=3000`을 받습니다.
- Product: 업무 규칙을 지키는 상품 객체. 기존 서비스가 사용합니다.
- ProductEntity: DB에 저장할 필드와 테이블 매핑을 담는 객체.

옷 비유는 역할을 이해하는 보조 수단으로만 사용합니다. 실제 필드, SQL, 상품 표를 항상 나란히 보여줍니다. 앞으로의 전체 흐름은 JSON → DTO → Product → 19일 Adapter → ProductEntity → Spring Data Repository → Hibernate SQL → products 행입니다. 조회는 Entity → Product → 응답 DTO입니다.

## 두 Repository와 두 DB를 반드시 구분

`ProductRepository`는 Service가 원하는 상품 저장 약속이며 Product를 주고받습니다. 현재 구현은 MemoryProductRepository입니다. `SpringDataProductRepository`는 Entity와 Long id를 다루며 Spring Data가 구현 객체를 제공합니다. 두 인터페이스를 추가하는 것만으로 교체되지 않습니다. 19일 Adapter가 둘을 연결합니다.

| 실행 | 실제 경로와 저장 위치 |
|---|---|
| JPA 테스트 | ProductJpaRepositoryTest → JPA → 독립 메모리 DB. 기본 rollback |
| 오늘 실제 HTTP | Controller → Service → MemoryProductRepository. 서버 종료 시 사라짐 |
| main DB 설정 | `jdbc:h2:file:./data/products`. 19일 API 전환 이후 실제 저장 대상으로 검증 |

테스트 성공을 HTTP 전환 성공으로 발표하지 않습니다. `./data/products`는 product-api 실행 폴더 기준이며 같은 파일 DB를 두 서버에서 열지 않습니다. H2 파일과 비밀값은 Git에서 제외합니다.

## 초보 설명의 정확한 범위

`@Entity`는 관리 대상 클래스 표시, `@Table(name="products")`는 표 이름, `@Id`는 행 식별 키, `@GeneratedValue(IDENTITY)`는 DB에 id 발급을 맡기는 설정입니다. 새 Entity의 Long id는 null이며 저장 이후 반환 객체에서 실제 id를 읽습니다. 1부터 연속이라고 가정하지 않습니다. protected 기본 생성자는 JPA가 객체를 구성하는 입구이고, 업무 생성자는 정상 상품을 만드는 입구입니다.

상품 표를 먼저 읽고 `SELECT ... FROM products WHERE price <= 1000 ORDER BY id`의 결과를 예측합니다. 이어 쿼리 메서드의 Price / LessThanEqual / OrderByIdAsc와 연결합니다. JPQL은 products가 아닌 ProductEntity 클래스와 price 필드를 대상으로 합니다. `:maxPrice`와 `@Param("maxPrice")`는 같은 이름으로 연결하며 사용자 값을 문자열로 이어붙이지 않습니다.

그다음 도구 이름을 정리합니다. JPA는 공통 규칙, Hibernate는 이를 구현해 SQL을 만드는 도구, Spring Data JPA는 Repository 기본 구현을 제공하는 도구, H2는 행을 보관하는 DB입니다.

## 환경과 당일 Java 세 파일

Java 17 / Boot 4.1.2 / Gradle 및 기존 Web·Validation·AspectJ·테스트를 유지합니다. data-jpa, H2 runtime, Boot 4 data-jpa-test만 추가합니다. DataJpaTest 패키지는 `org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest`입니다.

- ProductEntity: id·name·price 매핑과 기존 Product 검증 재사용.
- SpringDataProductRepository: 기본 저장·id 조회, 조건 메서드, JPQL.
- ProductJpaRepositoryTest: 총 4개 테스트. 재조회, 조건 경계·JPQL 비교, 긴 이름 보존, save 없는 변경 감지.

main 설정은 파일 DB / update / open-in-view=false입니다. update는 학습용이고 운영 마이그레이션 전략을 대신하지 않습니다. test 설정은 별도 mem DB / create-drop이며 DataJpaTest의 기본 임베디드 DB 대체 동작도 포함해 격리를 이해합니다. 실행 서버 파일을 삭제해서 테스트를 통과시키지 않습니다.

### 강사 참고: 긴 이름 매핑

기존 Memory 상품 이름에는 길이 상한이 없습니다. 예제의 `@Lob`과 300자 왕복 테스트는 기존 허용 범위가 VARCHAR(255) 때문에 깨지지 않게 보존하는 장치입니다. 기본 수업에서 LOB 타입을 암기시키지 않습니다. id·name·price 저장·조회가 먼저입니다. 운영에서는 이름 길이·검색·정렬·인덱스 요구를 함께 설계합니다.

## 테스트와 트랜잭션을 읽는 방법

첫 테스트를 준비 → 행동 → 기대로 나눠 읽습니다. 노트 생성이 준비, saveAndFlush / clear / findById가 행동, assertEquals가 기대입니다. `assertNotSame`은 저장 객체를 그대로 돌려받지 않았음을 확인합니다. clear 이후 실제 SELECT 로그도 함께 봅니다. SQL 관찰 명령은 `./gradlew test --info --rerun-tasks`입니다. 반복 실행의 UP-TO-DATE 생략을 막으며, 출력이 길면 `build/reports/tests/test/index.html`에서 해당 클래스의 Standard output을 봅니다. 단순 성공 확인은 `./gradlew test`로 충분합니다.

트랜잭션은 한 작업을 묶는 경계입니다. flush는 SQL 전송, commit은 확정, rollback은 취소입니다. 영속 상태는 현재 컨텍스트가 객체를 관리한다는 뜻이며 프로세스 재시작 보존을 뜻하지 않습니다. 재시작 보존은 19일 파일 DB에 연결한 API로 따로 검증합니다. clear는 관리 중인 객체 목록을 비워 다시 읽게 하며 DB 행을 삭제하지 않습니다. 테스트는 기본 rollback이므로 flush 후 조회 성공이 서버 파일 DB 영구 보존을 뜻하지 않습니다.

변경 감지는 트랜잭션 안에서 조회한 관리 객체의 change → flush → clear → 재조회로 관찰합니다. readOnly는 조회 의도와 최적화 힌트이며 보안상 쓰기를 차단하는 장치가 아닙니다. 실제 Service 트랜잭션은 19일에 반영합니다.

기존 ProductServiceTest / ProductCrudTest / ProductWiringTest는 보존합니다. DB 없는 업무 테스트, Spring 연결 테스트, JPA DB 테스트가 증명하는 범위를 구분합니다. 삭제·결과 없음 테스트는 추가 활동이며 학생이 실제 작성한 것만 실행 결과로 기록합니다.

## 관계는 종이 표 두 개 읽기까지만

purchase_orders.id를 order_items.order_id가 참조하는 PK·FK 표를 읽습니다. 주문 A에 노트·펜 두 항목 행이 연결되고 Java에서는 PurchaseOrder.items 목록으로 읽습니다. 공통 DB 연습의 lab_purchase_orders / lab_order_items는 독립 SQL 연습 표이며 23일 JPA 표와 구분합니다. 별도 주문 API를 구현하거나 상품 Entity에 관계를 억지로 추가하지 않습니다. 양방향·cascade·튜닝은 오늘 설명하지 않습니다. 관계 annotation과 LAZY·N+1의 실행 관찰은 23일 최소 주문 관계 실습으로 연결합니다.

## 제출과 19일 준비

저장소 sesac-spring-boot-study / branch practice/product-jpa-basics / 제목 [실습] 상품 Entity와 JPA 저장소. 필수 Issue 1개 + PR 1개. 본인 Assignee, practice 라벨, milestone product-api-2026-11-16. 최신 main → Issue → branch → 작업·검증 → commit/push → base main PR → 자체 확인·병합. Closes #실제번호.

README에 실행 폴더·main/test 설정·테스트 명령을, Wiki Home / 01-Setup / 02-Architecture / 03-API / 04-Verification / 05-Retrospective에 실제 결과를 누적합니다. 03-API는 Memory 계약 유지, 04에는 테스트·SQL 근거, 05에는 질문을 적습니다. 별도 문서 PR은 강제하지 않습니다.

Wrapper jar 예외와 기존 greeting-api를 보존합니다. data/·*.mv.db·*.trace.db·build/·.gradle/·IDE·.env·비밀값을 제외합니다. 19일 출발 상태는 기존 CRUD·테스트 성공, JPA 테스트 성공, 두 DB 구분, 최신 main·실행 명령 확보입니다. 미완료 멘티는 대강용 복구 코드로 합류합니다.

## 검증 기록

verify.py는 HTML·source-data·정확한 코드 공백·14줄 분할·부제목 없음·JS 문법과 초보 작업지 연결을 확인합니다. Java 실제 build·test·HTTP 검증은 루트 통합 기록을 봅니다. 멘티는 자기 실행 결과를 기록해야 합니다.

## 슬라이드별 메모

### 1. 상품 데이터를 Entity와 Repository로

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 2. CH 11의 DB 접근과 JPA를 비교

정확한 페이지와 본문 코드를 자료에서 단정하지 않습니다. 책을 직접 펴서 상품 DB 접근 절을 확인합니다. 교재 JDBC 구현과 수업 JPA 구현을 같은 코드라고 설명하지 않습니다.

### 3. 읽기 → 작성 → 실행 → 설명

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 4. JPA 연습과 API 전환을 구분

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 5. DB 동작을 테스트와 SQL로 설명

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 6. Entity와 저장소의 역할

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 7. 상품 세 개를 표로 읽어보기

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 8. 화면의 값과 업무 객체와 저장 객체

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 9. 오늘은 DB 쪽 연결을 따로 연습

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 10. 입력부터 행으로, 행에서 응답으로

오늘은 Repository 테스트로 가운데 저장·조회를 증명합니다. 실제 HTTP 경로는 Memory입니다. 전체 흐름을 이미 연결한 것으로 설명하지 않습니다.

### 11. Java 필드와 DB 열을 연결하는 객체

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 12. @Id와 @GeneratedValue

DB 생성 id를1부터 연속이라고 가정하지 않습니다. primitive long 대신 Long을 쓰는 새 Entity 상태의 의미를 설명합니다. 기존 도메인Product id와 변환은19일 Adapter에서 다룹니다.

### 13. JPA가 만드는 객체의 입구를 구분

기존 Memory 상품 이름은 길이 상한이 없습니다. 기본 VARCHAR(255)로 전환하면 허용하던 긴 이름이 DB 오류가 되므로 수업 예제는 @Lob으로 매핑하고300자 왕복 테스트로 보존을 확인합니다. 이 선택은 수업 독립 매핑이며 교재 요구가 아닙니다. 운영에서는 실제 이름 길이 정책과 검색·정렬·인덱스 요구를 함께 설계합니다.

### 14. 인터페이스로 제공받는 기본 동작

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 15. id를 추측하지 말고 반환값에서 읽기

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 16. INSERT는 행 추가 · SELECT는 행 읽기

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 17. 이름은 비슷해도 맡은 약속이 다릅니다

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 18. JPA · Hibernate · Spring Data · DB

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 19. 1000원 이하 상품을 id 오름차순으로

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 20. 메서드 이름 또는 JPQL로 전달

전체 메서드 반환 타입과 선언은 뒤의 전체 Repository 파일을 사용합니다. SQL 테이블 products와 JPQL Entity ProductEntity를 구분합니다. :maxPrice와 @Param 이름을 같게 바인딩하며 사용자 값을 문자열로 이어붙이지 않습니다.

### 21. 조회한 Entity의 변경을 언제 반영할까요?

flush는 commit과 다릅니다. 변경 감지는 관리 상태 Entity와 트랜잭션 경계가 전제입니다. 영속 상태는 현재 컨텍스트가 객체를 관리한다는 뜻이며 프로세스 재시작 후 데이터 보존과 다릅니다. 테스트는 기본 롤백이므로 테스트 성공을 실행 서버 DB에 영구 저장했다고 해석하지 않습니다.

### 22. 한 사용자 작업의 경계를 정합니다

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 23. 자율 실습 · JPA 기초

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 24. 기존 프로젝트와 테스트를 보존

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 25. JPA와 H2 의존성을 추가

dependencies 블록 안에 필요한 항목을 합칩니다. Boot4의 JPA 테스트 모듈 및 DataJpaTest 패키지는 제공 예제 기준을 따릅니다. Boot3의 예전 import를 그대로 붙이지 않습니다.

### 26. main은 파일 DB · 테스트는 독립 DB

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 27. 테스트 성공과 API DB 전환은 다릅니다

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 28. 기존 application.properties에 필요한 값 합치기

product-api 폴더에서 실행합니다. 파일 DB는 재시작 보존을 위한 수업 환경이며 운영 DB 설계가 아닙니다. ddl-auto=update는 학습 환경 값이고 운영 마이그레이션 전략을 대신하지 않습니다. DB 비밀번호나 .env는 커밋하지 않습니다.

### 29. 기존 테스트 설정과 충돌 없는지 확인

@DataJpaTest가 임베디드 DB로 대체하는 동작을 포함해 테스트 격리를 확인합니다. main 파일 DB를 지워 테스트를 통과시키지 않습니다.

### 30. 책의 상품 필드를 Entity로 매핑

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 31. ProductEntity.java · 1/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 32. ProductEntity.java · 2/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 33. ProductEntity.java · 3/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 34. Spring Data Repository를 작성

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 35. SpringDataProductRepository.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 36. SpringDataProductRepository.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 37. DB 동작을 독립 테스트로 확인

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 38. 준비 → 행동 → 기대

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 39. ProductJpaRepositoryTest.java · 1/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 40. ProductJpaRepositoryTest.java · 2/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 41. ProductJpaRepositoryTest.java · 3/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 42. ProductJpaRepositoryTest.java · 4/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 43. ProductJpaRepositoryTest.java · 5/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 44. 테스트 결과와 SQL을 함께 읽기

Windows는 .\gradlew.bat test --info --rerun-tasks. 출력이 길면 build/reports/tests/test/index.html의 해당 클래스 Standard output을 확인합니다. ProductWiringTest는 Memory 기반 Service 연결을 계속 확인합니다. JPA 저장소가 추가되어도 API가 자동으로 DB 저장으로 바뀌지 않습니다.

### 45. 세 종류 테스트가 무엇을 증명하나요?

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 46. 관계 읽기와 19일 준비

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 47. 주문 하나에 항목 두 개가 있습니다

상품 수업과 별개의 종이 표 읽기입니다. 공통 DB SQL 연습은 lab_orders / lab_order_items라는 독립 표를 씁니다. 실제 번호를 고정값으로 저장하라는 의미가 아닙니다.

### 48. 표의 여러 항목을 Java 목록으로 표현

양방향·cascade·튜닝을 오늘 추가 설명하지 않습니다. 현재 상품 Entity에 관계를 억지로 추가하지 않습니다.23일 최소 주문 실습의 PurchaseOrder.items와 같은 흐름입니다.

### 49. API는 유지하고 저장소 구현을 바꾸기

19일은 이준형 강사 대강이며 새 개념 강의나 시연 없이 작업지에 따라 진행합니다. 오늘 완료 코드를 출발점으로 쓰고 미완료 학생은 복구용 출발 코드를 사용할 수 있습니다.

### 50. 단축 URL에 AI 프론트 연결

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 51. GitHub 제출

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 52. 필수 Issue 1개 · 병합 PR 1개

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 53. README·Wiki에 실제 증거와 계획을 구분

최신main→Issue→branch→작업·검증→commit/push→PRbase main→자체 확인·병합. Public/main·본인Assignee·practice라벨·milestone product-api-2026-11-16. Wiki 별도 편집과 링크를 PR에 남깁니다. 필수1PR이며 별도 문서PR은 강제하지 않습니다.

### 54. 실행 파일과 학습 기록만 제출

greeting-api/product-api 기존 파일은 보존합니다. H2 파일을 Git에 올리지 않습니다. README에 product-api 폴더에서 실행해야 상대경로가 일정함을 기록합니다.

### 55. 막히면 단계별 확인으로 돌아가기

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 56. 네 가지가 준비됐나요?

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 57. JPA와 Spring Data 공식 문서

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.
