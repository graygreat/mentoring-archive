from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
HEADER='''# 2026-11-12 · 교재 CH 11과 DB 연동

## 진행 범위

4시간 동안 교재 CH 11의 DB 사용 웹 애플리케이션, DB 다뤄 보기, 상품 추가, 조회·수정·삭제를 함께 읽습니다. 코드 설명은 책으로 대체하고 교육생이 기존 `product-api/`에 직접 적용합니다. 강사 코딩 시연이나 새 프로젝트 생성은 하지 않습니다. 책에서 사용하는 JDBC 접근 방식을 확인하며 특정 API를 책의 구현이라고 단정하지 않습니다. 이후 `personal-project/` 위시리스트 DB 연동을 필수로 진행하고 완료자는 장바구니 영속화로 확장합니다.

## 설정 확인

기존 Java 17·Spring Boot 4·Gradle 프로젝트를 유지합니다. 필요한 경우 `implementation 'org.springframework.boot:spring-boot-starter-jdbc'`와 `runtimeOnly 'com.h2database:h2'`를 추가하고 버전은 Spring Boot 의존성 관리를 따릅니다. 기존 의존성을 무작정 교체하지 않습니다.

상품 앱은 `jdbc:h2:file:./data/products`, 개인 앱은 `jdbc:h2:file:./data/wishlist`로 분리합니다. Spring Boot 공식 문서의 권장대로 파일 URL에 `;DB_CLOSE_ON_EXIT=FALSE`를 덧붙일 수 있습니다. `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password`를 실제 설정과 맞추고 비밀값은 제출하지 않습니다. 상대 파일 경로는 실행 작업 디렉터리에 따라 달라집니다.

독립 SQL 연습의 `jdbc:h2:mem:db_basics`는 마지막 연결/프로세스 종료 시 사라지는 연습용입니다. 영구 저장 확인은 앱 파일 DB를 같은 URL·작업 디렉터리에서 재시작해 수행합니다. 테스트는 별도 DB를 사용합니다.

책의 테이블 SQL이나 비파괴 `CREATE TABLE IF NOT EXISTS`로 준비합니다. classpath `schema.sql`을 파일 DB에서 자동 실행하려면 `spring.sql.init.mode=always` 등 실행 조건을 확인해야 합니다. 시작할 때 DROP·TRUNCATE하거나 고정 seed를 반복 삽입하지 않습니다. JPA `ddl-auto`를 JDBC 테이블 생성 설정으로 넣지 않습니다.

공식 문서: [Spring Boot SQL](https://docs.spring.io/spring-boot/reference/data/sql.html), [DB 초기화](https://docs.spring.io/spring-boot/how-to/data-initialization.html), [H2 URL](https://h2database.com/html/features.html#database_url).

## 구현과 확인

Repository 인터페이스, Service, Domain, DTO와 HTTP 계약을 유지합니다. 실행 시 Memory/DB 구현 중 하나만 주입되도록 선택합니다. DB가 발급한 키로 생성 결과를 만들고 조회 복원에서도 그 id를 보존합니다. `AtomicLong`이나 `MAX(id)+1`로 DB id를 대신 발급하지 않습니다. 없는 id UPDATE·DELETE는 영향받은 행 수 0을 확인해 404로 변환합니다.

위시리스트의 수동/외부 필드와 저장한 메타데이터를 유지합니다. NULL과 0, 외부 식별자와 로컬 id를 구분합니다. 수동 상품의 이름 중복은 허용하고 name에 새 UNIQUE 제약을 강제하지 않습니다. SQL 입력은 문자열 이어 붙이기 대신 책의 파라미터 바인딩 방식을 따릅니다. 외부 식별자 조합의 UNIQUE 제약과 409 변환을 적용하되 모든 DB 예외를 409로 덮지 않습니다. 목록 순서는 ORDER BY로 명시하고 동률의 등록 순서, 가격 0, 추천·검증·쿠폰 등 기존 동작을 유지합니다. 실패 응답만으로 DB 롤백이 된다고 설명하지 않습니다.

장바구니 확장은 저장된 행 id·수량·이름·단가·재고 복사본을 유지합니다. 원본 변경/삭제가 복사본을 바꾸지 않으며 FK CASCADE로 장바구니를 지우거나 RESTRICT로 원본 삭제를 막지 않도록 설계합니다. 성공 응답뿐 아니라 DB 실제 행과 같은 설정의 재시작 후 동일 id·값도 확인합니다. 쿠폰 선택과 미리보기 상태는 추가 저장하지 않습니다. 여러 쓰기가 하나의 작업을 이루면 중간 실패 시 부분 저장이 남지 않도록 책 수준에서 트랜잭션 범위를 확인합니다.

QA 체크리스트는 교육생이 작성하고 정상·실패·재시작 실제 결과를 기록합니다. Repository 통합 테스트는 별도 DB에서 실행하고 기존 단위 테스트는 유지합니다. 상세 정답 QA 시나리오나 DB 완성 코드는 배포하지 않습니다. 마지막 파일 버튼 3개는 기존 HTTP 검증·예외 처리 보충 코드입니다.

## 제출

공용 `sesac-ddm-4-web/sesac-spring-boot-study`에 Issue 1개·PR 1개, 제목은 `[11/12][이름] 기존 과제 DB 연동`입니다. 이전 구현에서 자율 브랜치로 출발해 개인 Fork의 origin에 Push합니다. base는 조직 원본 main, head는 개인 Fork 작업 브랜치입니다. 이전 PR 링크와 책/개인 과제 실제 변경 범위, 테이블·SQL·설정·QA·테스트·미완료 범위를 기록합니다. 리뷰 수정은 같은 브랜치에 Push하고 강사는 병합 없이 PR·Issue를 닫습니다. 앱 DB 파일·빌드 결과·IDE 파일·비밀값은 제외합니다.

14일은 오전 3시간 단축 URL, 오후 3시간 주문 관리 API 과제 테스트를 개인별로 직접 풀이합니다. 요구사항은 먼저 확인하고 책의 풀이 코드와 완성 예제는 최대한 참고하지 않습니다. 마지막 1~2시간은 ORM·JPA·Spring Data JPA·영속성 컨텍스트의 역할을 소개하고 다음 주로 연결합니다. 기존 DB 연동 결과는 보존하며 두 과제에 JPA 전환을 필수로 추가하지 않습니다.

## 슬라이드별 확인 사항

'''
notes='\n\n'.join(f"### {i+1}. {d['title'].replace('<br>', ' ')}\n\n{d['note'] or '책과 실제 구현을 함께 확인합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(HEADER+notes+'\n')
