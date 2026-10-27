# 11월 19일 상품 API JPA 전환 작업지

수업 4시간. 45분 작업과 확인 뒤 15분 휴식 또는 정리한다. 강사 시연 없이 책의 상품 관리와 16일 코드를 보며 직접 구현한다. 이 문서에는 완성 구현을 싣지 않는다.

## 준비

- `sesac-spring-boot-study`의 기존 `product-api`를 사용한다. 현재 작업을 commit하고 main을 갱신한다.
- 책의 상품 관리 데이터 접근·저장소 부분을 읽고 본인 판본의 절과 페이지를 기록한다. 책 JDBC와 수업 JPA는 구현 방식이 다르다.
- 16일 완료 상태: `ProductEntity`, `SpringDataProductRepository`, JPA 저장소 테스트가 존재한다. **HTTP API는 아직 MemoryProductRepository를 사용한다.**
- 출발 상태가 없다면 [복구용 출발 ZIP](assets/product-api-start.zip)을 별도 임시 폴더에서 열어 비교한다. 기존 프로젝트·DB 파일을 덮어쓰거나 삭제하지 않는다. 사용한 복구 범위를 기록한다.
- product-api 폴더에서 `./gradlew test`를 실행한다. Windows는 `gradlew.bat test`. Java 17 이상과 기존 Gradle Wrapper를 사용한다.

## 1교시: 출발 상태와 변경 계획

- [ ] 기존 테스트 통과 결과를 기록했다.
- [ ] POST·GET·PUT·DELETE API 계약과 400/404 응답을 확인했다.
- [ ] ProductService가 ProductRepository 인터페이스를 주입받음을 찾았다.
- [ ] 현재 등록된 구현체가 MemoryProductRepository임을 찾았다.
- [ ] Controller/DTO를 바꾸지 않고 저장소를 교체할 계획을 적었다.

완료 확인: 호출 흐름과 변경할 파일을 강사에게 설명한다. 출발 테스트 실패를 새 구현 문제와 섞지 않는다.

## 2교시: adapter·빈·트랜잭션 연결

- [ ] `JpaProductRepository`가 기존 `ProductRepository`의 모든 메서드를 구현한다.
- [ ] 생성자로 `SpringDataProductRepository`를 주입한다.
- [ ] 저장 시 DB가 부여한 실제 id를 반환한다.
- [ ] Entity와 Product 사이를 변환하고 목록의 id 오름차순을 유지한다.
- [ ] 수정·삭제의 없는 id 처리를 기존 인터페이스 계약대로 반환한다.
- [ ] Memory 클래스는 보존하되 `@Repository` 등록은 제거했다.
- [ ] Jpa 구현체만 `@Repository`로 등록했다.
- [ ] ProductService의 쓰기 업무는 `@Transactional`, 조회는 `readOnly=true`로 경계를 둔다.
- [ ] 기존 Controller·DTO·예외 처리기를 유지했다.
- [ ] create/update의 도메인 검증이 Repository 호출 전에 수행되어 입력 오류의 기존 예외 계약을 유지한다.
- [ ] 기존 API의 긴 이름도 저장할 수 있도록 16일 Entity의 name 매핑과 긴 이름 재조회 테스트를 보존했다.

실행 DB는 16일과 같은 `jdbc:h2:file:./data/products`, `ddl-auto=update`, `open-in-view=false`를 사용한다. 프로젝트 폴더와 DB 경로를 기록한다. 로컬 학습용 설정이며 운영 설정으로 제시하지 않는다.

테스트 DB는 `src/test/resources/application.properties`의 별도 인메모리 DB와 `create-drop`을 사용한다. 실행용 파일 DB를 테스트에 공유하지 않는다.

완료 확인: 저장소 구현체가 하나만 주입되고, 실행 로그에서 파일 DB 연결을 확인한다.

## 3교시: CRUD·실패 회귀

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
