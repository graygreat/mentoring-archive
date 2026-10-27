# 2026-11-16 강사용 가이드 · 상품 Entity와 JPA 저장소 4시간

책의 상품 관리 DB 접근 절을 읽으며 JPA 기본기를 연습합니다. 교재 CH11의 JDBC와 수업의 JPA는 같은 저장 요구를 서로 다른 방식으로 해결합니다. 책 본문 미확인 페이지·메서드·정책을 만들어 적지 않습니다. 수업 코드는 독립 예제입니다.

## 시간과 진행

각 블록은 집중45분+휴식·정리15분, 총4시간입니다. 강사 구현 시연 없이 읽기→핵심질문→자율작성→테스트→비교를 반복합니다.

1. 교재 DB 흐름10 / Entity·id 개념15 / Gradle·DB 설정20.
2. Entity·Repository 자율 구현35 / 매핑 점검10.
3. DB 테스트 작성·실행30 / SQL 관찰·변경감지15.
4. 단방향 관계 읽기10 /19일 전환 계획10 / 미완료보완·문서15 / 결과 공유10.

오늘은 Entity·Repository·DB 테스트 연습입니다. ProductService가 사용하는 실제 API 저장소는 Memory입니다. JPA 추가만으로 기존 API가 DB 저장으로 바뀌었다고 안내하지 않습니다.19일 이준형 강사 대강에서 Adapter를 연결하며 실제 API를 전환합니다.

## 실행 환경과 설정

기존 Java17/Boot4.1.2/Gradle을 유지합니다. 기존 dependencies에 data-jpa, H2 runtime, Boot4 data-jpa-test 모듈만 추가합니다. Web MVC·Validation·AspectJ·기존 테스트를 삭제하지 않습니다. DataJpaTest 패키지는 org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest입니다.

src/main/resources/application.properties는 jdbc:h2:file:./data/products, ddl-auto=update, open-in-view=false입니다. product-api 디렉터리에서 실행하여 상대경로를 일관되게 유지합니다. 같은 파일을 여러 실행 서버에서 동시에 열지 않습니다. update는 학습용이며 운영 스키마 변경 전략을 대신하지 않습니다.

src/test/resources/application.properties는 별도 mem DB/create-drop을 사용합니다. @DataJpaTest는 테스트 슬라이스·트랜잭션·기본롤백 및 임베디드DB 대체 동작을 이해하며 사용합니다. 실행 서버DB와 테스트DB는 서로 다릅니다. 테스트 통과가 main 파일DB에 데이터가 남았다는 증거는 아닙니다. 파일DB의 재시작 보존은19일 API 전환 뒤 확인합니다.

## 당일 세 Java 파일

- ProductEntity: DB매핑·id자동생성·보호된기본생성자. change는 기존 Product 검증을 재사용하여 정상값만 필드에 반영합니다. 도메인Product와 Entity는 분리합니다.
- SpringDataProductRepository: JpaRepository 기본동작, id정렬, 가격상한 쿼리메서드와 @Query JPQL을 비교합니다.
- ProductJpaRepositoryTest: 총 4개 테스트로 clear 뒤 재조회,300자 긴 이름 보존,조건 경계·JPQL 비교,save 호출 없는 변경감지를 검증합니다.

상품 name은 @Lob으로 매핑해 기존 Memory에서 허용하던 긴 이름이 기본 VARCHAR(255) 때문에 저장 오류로 바뀌지 않도록 합니다.300자 왕복 테스트가 이 계약을 검증합니다. 이는 독립 수업 예제의 매핑 선택이며 운영에서는 이름 길이 정책과 인덱스 요구를 함께 설계합니다.

기존 ProductServiceTest/ProductCrudTest/ProductWiringTest는 유지합니다. source-data는 위 세 파일만이며 전체누적프로젝트는 다른날 자료와 공통canonical을 합칩니다. 기본 findAll의 정렬·고정id·연속id를 가정하지 않습니다. JPQL은 Entity와 속성을 조회하며 사용자값 문자열 이어붙이기 대신 바인딩합니다.

수업 예제에는 삭제/결과없음 테스트를 추가 활동으로 제시합니다. 학생이 실제로 추가한 테스트만 수행 결과에 포함합니다. 기존예제에 없는 테스트를 이미 제공된 것으로 말하지 않습니다.

## 트랜잭션과 SQL 질문

관리상태Entity 조회→change→flush→clear→재조회 흐름으로 변경감지를 관찰합니다. flush는 commit이 아닙니다. EntityManager.clear는1차캐시를 비워 재조회 근거를 만듭니다. 원래 Entity와 재조회 객체가 다른 인스턴스인지 확인합니다.

Service 트랜잭션은 사용자 작업의 조회·규칙·변경을 묶는 경계입니다. readOnly는 의도와최적화 힌트이며 보안상 쓰기 차단을 보장하는 장치가 아닙니다. 실제 ProductService @Transactional과 Adapter는19일에 반영하므로 오늘 단위테스트의 new Service와 JPA 변경감지를 혼동하지 않습니다.

## 단방향 관계 읽기

별도 개념 예로 Order→Member 한개의 관계를 읽습니다. 여러주문이 한회원에 연결되고 외래키는 orders.member_id입니다. @ManyToOne/@JoinColumn 역할을 설명합니다. ManyToOne 기본fetch는EAGER이며 LAZY를 명시하는 의도만 소개합니다. LAZY가 단일SQL이나 N+1제거를 자동보장한다고 설명하지 않습니다. 주문전체구현·양방향·cascade는 오늘필수아님,23일 별도 작은주문랩에서 실행합니다.

##19일 준비

14일 Memory CRUD정상·오류/기존테스트,16일 JPA테스트,main/test 설정,최신main과실행명령을 확보합니다. ProductRepository 인터페이스는 유지하고 Memory 빈을 JPA Adapter로 바꾸는 지점을 문서화합니다. 미완료학생은19일 복구용출발코드로 합류할 수 있도록 완료여부를 표시합니다.

## GitHub 제출

sesac-spring-boot-study / branch practice/product-jpa-basics / 제목 [실습] 상품 Entity와 JPA 저장소. 필수 Issue1개+PR1개, 본인Assignee·practice라벨·milestone product-api-2026-11-16. 최신main→Issue→branch→작업·검증→commit/push→base main PR→자체확인·병합, Closes #실제번호.

product-api/README에 실행위치·설정·테스트·현황 기재. Wiki Home/01-Setup/02-Architecture/03-API/04-Verification/05-Retrospective에 날짜별누적.03-API는Memory계약유지,04에는실제SQL·테스트,05에는JDBC/JPA차이·질문 기록. Wiki는별도편집후PR에링크남김. 별도문서PR강제없음.

Wrapper jar예외·기존greeting-api보존. data/·*.mv.db·*.trace.db·build/·.gradle/·IDE·.env·비밀값은Git제외. rootREADME에프로젝트/Wiki링크유지. 단축URL+AI프론트는별도과제안내이며필수공통수업코드를대신하지않습니다.

## 검증 기록의 범위

verify.py는HTML/source-data/코드공백/14줄분할/부제목없음/JS문법을검증합니다. Java실제build·test·HTTP검증은루트통합검증기록을확인합니다. 멘티는자기환경에서실제결과를다시기록합니다.

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

### 7. Product와 ProductEntity는 책임이 다릅니다

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 8. @Id와 @GeneratedValue

DB 생성 id를1부터 연속이라고 가정하지 않습니다. primitive long 대신 Long을 쓰는 새 Entity 상태의 의미를 설명합니다. 기존 도메인Product id와 변환은19일 Adapter에서 다룹니다.

### 9. JPA가 만드는 객체의 입구를 구분

기존 Memory 상품 이름은 길이 상한이 없습니다. 기본 VARCHAR(255)로 전환하면 허용하던 긴 이름이 DB 오류가 되므로 수업 예제는 @Lob으로 매핑하고300자 왕복 테스트로 보존을 확인합니다. 이 선택은 수업 독립 매핑이며 교재 요구가 아닙니다. 운영에서는 실제 이름 길이 정책과 검색·정렬·인덱스 요구를 함께 설계합니다.

### 10. 인터페이스로 제공받는 기본 동작

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 11. 쿼리 메서드와 JPQL을 구분

문자열로 사용자 값을 이어붙이지 않습니다. 가격 조건이 수업 메서드명과 어떻게 연결되는지 소스를 읽습니다. JPQL이 SQL과 모양은 비슷해도 테이블 질의와 동일하지 않음을 설명합니다.

### 12. 조회한 Entity의 변경을 언제 반영할까요?

flush는 commit과 다릅니다. 변경 감지는 관리 상태 Entity와 트랜잭션 경계가 전제입니다. 테스트는 기본 롤백이므로 테스트 성공을 실행 서버 DB에 영구 저장했다고 해석하지 않습니다.

### 13. 한 사용자 작업의 경계를 정합니다

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 14. 자율 실습 · JPA 기초

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 15. 기존 프로젝트와 테스트를 보존

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 16. JPA와 H2 의존성을 추가

dependencies 블록 안에 필요한 항목을 합칩니다. Boot4의 JPA 테스트 모듈 및 DataJpaTest 패키지는 제공 예제 기준을 따릅니다. Boot3의 예전 import를 그대로 붙이지 않습니다.

### 17. main은 파일 DB · 테스트는 독립 DB

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 18. 기존 application.properties에 필요한 값 합치기

product-api 폴더에서 실행합니다. 파일 DB는 재시작 보존을 위한 수업 환경이며 운영 DB 설계가 아닙니다. ddl-auto=update는 학습 환경 값이고 운영 마이그레이션 전략을 대신하지 않습니다. DB 비밀번호나 .env는 커밋하지 않습니다.

### 19. 기존 테스트 설정과 충돌 없는지 확인

@DataJpaTest가 임베디드 DB로 대체하는 동작을 포함해 테스트 격리를 확인합니다. main 파일 DB를 지워 테스트를 통과시키지 않습니다.

### 20. 책의 상품 필드를 Entity로 매핑

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 21. ProductEntity.java · 1/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 22. ProductEntity.java · 2/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 23. ProductEntity.java · 3/3

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 24. Spring Data Repository를 작성

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 25. SpringDataProductRepository.java · 1/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 26. SpringDataProductRepository.java · 2/2

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 27. DB 동작을 독립 테스트로 확인

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 28. ProductJpaRepositoryTest.java · 1/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 29. ProductJpaRepositoryTest.java · 2/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 30. ProductJpaRepositoryTest.java · 3/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 31. ProductJpaRepositoryTest.java · 4/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 32. ProductJpaRepositoryTest.java · 5/5

전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.

### 33. 테스트 결과와 SQL을 함께 읽기

Windows는 .\gradlew.bat test. ProductWiringTest는 Memory 기반 Service 연결을 계속 확인합니다. JPA 저장소가 추가되어도 API가 자동으로 DB 저장으로 바뀌지 않습니다.

### 34. 세 종류 테스트가 무엇을 증명하나요?

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 35. 관계 읽기와 19일 준비

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 36. 주문은 회원을 참조할 수 있습니다

상품 관리와 별개인 작은 관계 읽기 활동입니다. 주문·회원 전체 CRUD나 실제 교재의 필수 정책으로 오해하지 않게 합니다.23일 별도 최소 주문 예제로 지연 로딩·N+1을 실행합니다.

### 37. 객체 참조와 외래 키를 나란히

@ManyToOne의 기본 fetch는 EAGER입니다. LAZY를 명시하는 이유와 프록시·접근 시점의 상세 동작은23일 실습으로 연결합니다. LAZY를 적으면 언제나 단일 SQL이 보장된다고 말하지 않습니다.

### 38. API는 유지하고 저장소 구현을 바꾸기

19일은 이준형 강사 대강이며 새 개념 강의나 시연 없이 작업지에 따라 진행합니다. 오늘 완료 코드를 출발점으로 쓰고 미완료 학생은 복구용 출발 코드를 사용할 수 있습니다.

### 39. 단축 URL에 AI 프론트 연결

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 40. GitHub 제출

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 41. 필수 Issue 1개 · 병합 PR 1개

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 42. README·Wiki에 실제 증거와 계획을 구분

최신main→Issue→branch→작업·검증→commit/push→PRbase main→자체 확인·병합. Public/main·본인Assignee·practice라벨·milestone product-api-2026-11-16. Wiki 별도 편집과 링크를 PR에 남깁니다. 필수1PR이며 별도 문서PR은 강제하지 않습니다.

### 43. 실행 파일과 학습 기록만 제출

greeting-api/product-api 기존 파일은 보존합니다. H2 파일을 Git에 올리지 않습니다. README에 product-api 폴더에서 실행해야 상대경로가 일정함을 기록합니다.

### 44. 네 가지가 준비됐나요?

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.

### 45. JPA와 Spring Data 공식 문서

읽을 범위·자율 작업·기대 결과를 확인하고 멘티가 실제 실행 근거를 설명하도록 합니다.
