# 11월 19일 상품 API JPA 전환

4시간 · 이준형 강사 대강. [진행표](HANDOFF.md)와 [학생 작업지](STUDENT-WORKSHEET.md)를 중심으로 운영한다. 설명·시연 대신 단계별 결과 확인을 한다.

## 책과 오늘의 범위

상품 관리 애플리케이션이 공통 수업 프로젝트다. 책의 데이터 접근 절을 함께 읽되 책의 JDBC 구현과 수업의 JPA 구현을 구분한다. 본문 페이지나 책의 정확한 메서드명은 임의 지정하지 않는다. 출발은 16일 완료 상태이며, 오늘은 14일의 CRUD 계약을 그대로 둔 채 저장소를 교체한다.

필수 산출물: JPA adapter 연결, Service 트랜잭션, 회귀 테스트, 파일 DB 재시작 보존, README/Wiki 및 병합 PR 1개. 단축 URL은 별도 과제다.

## 참고 구현의 사용

완성 참고 구현은 슬라이드 뒤쪽 **강사 참고 구현**의 파일 버튼으로 확인한다. 학습자 작업지를 먼저 수행한 후 3단계 힌트에서 비교한다. 참고 파일은 `shared/product_sources.py`의 `DAY19_SOURCES`를 그대로 사용하며 4개다.

- `MemoryProductRepository.java`: 구현은 남기고 `@Repository` 등록 제거.
- `JpaProductRepository.java`: ProductRepository 구현, SpringDataProductRepository 위임, Entity→Product 변환, id 오름차순, 수정/삭제의 없는 id 계약 유지.
- `ProductService.java`: 클래스 `@Transactional`, 조회 메서드 `readOnly=true`. create/update는 Repository 호출 전에 `new Product(...)`로 기존 도메인 검증을 수행한다. Repository 프록시 안에서 발생한 입력 오류가 다른 데이터 접근 예외로 변환되어 400 계약을 깨지 않도록 검증 경계를 유지한다.
- `ProductJpaMigrationTest.java`: Service 호출의 수정 커밋, 잘못된 수정 뒤 기존 값 유지, 삭제 후 없는 id 예외 확인. SpringBootTest에는 바깥 테스트 트랜잭션을 붙이지 않아 Service 트랜잭션 경계를 확인한다.

Entity와 Spring Data Repository는 16일 출발 코드에 이미 존재한다. ProductEntity.name의 `@Lob`는 기존 API에서 허용하던 긴 이름을 기본 문자열 컬럼 길이 때문에 거부하지 않도록 적용한 학습용 매핑이다. 새로운 이름 길이 제한을 몰래 추가하지 않는다. 모든 문자열에 @Lob를 일반화하지 말고 실제 DB의 타입·조회 특성과 요구사항에 맞춰 판단한다. 긴 이름 저장·재조회는 ProductJpaRepositoryTest로 확인한다. `ProductController`, DTO, 예외 처리기를 JPA Entity 반환으로 바꾸지 않는다. 구현체 빈을 둘 다 등록한 채 @Primary로 숨기지 않는다.

실행 설정은 `jdbc:h2:file:./data/products`, `ddl-auto=update`, `open-in-view=false`. 테스트는 별도 인메모리 DB와 `create-drop`. 로컬 학습용 설정이다. DB 파일은 Git 추적에서 제외한다.

## 확인 순서

1. product-api 폴더에서 `./gradlew test`를 실행한다.
2. `./gradlew bootRun`으로 앱 하나만 실행한다.
3. POST 201의 실제 id·Location을 보관하고 GET/PUT/DELETE를 확인한다. 수정 200, 삭제 204, 없는 상품 404가 기준이다.
4. blank/negative/missing/null/bad JSON 400 및 실패 뒤 데이터 불변을 확인한다.
5. 별도 상품을 생성·수정해 실제 id와 값을 기록하고 정상 종료한다.
6. 같은 작업 폴더와 설정으로 재실행해 같은 id·값을 조회한다.
7. 테스트 DB가 아니라 실행용 파일 DB에서 보존됐음을 학생이 설명하게 한다.

정확한 실행 검증 결과는 저장소 전체 통합 검수에서 확인한다. 이 문서는 테스트 성공을 전제로 미리 완료를 주장하지 않는다.

## GitHub

`sesac-spring-boot-study` / `practice/product-jpa-migration` / `[실습] 상품 API 데이터 접근 JPA 전환`. 필수 Issue 1개·병합 PR 1개. README·테스트·재시작 증거·Wiki 여섯 페이지의 관련 갱신을 같은 작업에 포함한다. PR `Closes #실제번호`. Wiki는 코드 PR과 별도 저장되므로 링크 확인이 필요하다.

## 23일로 인계

학생별 완료 여부, 재현 가능한 오류, 구현체 선택/트랜잭션/테스트 격리 질문을 기록한다. 23일은 독립 주문 관계 예제로 지연 로딩과 N+1을 관찰하므로 상품 API에 관계를 덧붙이지 않는다.

## 초보 진행 보완

[DB 기초](../shared/db-basics/README.md) → [16일 쉬운 작업지](../2026-11-16/BEGINNER-WORKSHEET.md) → [19일 작업지](STUDENT-WORKSHEET.md)의 A~E 순서로 연결한다. HANDOFF의 초기 5분 진단은 1교시 안에 포함한다. 새 개념 강의는 추가하지 않는다.

Repository 두 종류는 기존 Product 업무 계약과 Entity용 Spring Data 도구로 구분한다. 노트 3000을 저장하고 실제 id의 가격을 3500으로 바꾼 뒤 SQL 로그·행 값·재시작 조회까지 같은 사례로 추적한다. API 정상 응답만으로 JPA 사용을 증명했다고 판정하지 않는다.
