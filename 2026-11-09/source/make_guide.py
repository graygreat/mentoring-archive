from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
HEADER='''# 2026-11-09 · Spring MVC·REST 응답·유효성 검사

## 진행 기준

오늘은 4시간입니다. 7일 개인 위시리스트 과제를 간단히 발표한 뒤, 교재 9장의 상품 API를 예로 Spring MVC 요청 흐름과 HTTP 응답을 설명합니다. 이어서 10장의 유효성 검사·전역 예외 처리·오류 응답을 책과 함께 봅니다. 요청 주소·쿼리·본문을 받는 방법은 이미 배웠으므로 별도 문법 강의를 반복하지 않습니다. 강사 코딩 시연 없이 책의 실제 코드와 교육생의 구현을 읽고 연결합니다.

PPT는 핵심 개념과 흐름 그림, 책에서 볼 부분, 발표·QA·제출 안내를 담습니다. 긴 코드 설명은 책을 중심으로 진행합니다. 정확한 쪽수는 소지한 판본에서 확인합니다. 수업 참고 코드는 교재 원문 복제가 아닌 독립 예제입니다.

운영 시간의 예시는 발표 35분, MVC 흐름 45분, REST 응답 35분, 검증·예외 처리 60분, QA 30분, 정리 또는 DB 도입 15분, 중간 휴식 여유 20분입니다. 이는 강사용 참고이며 발표 상황과 이해도에 맞춰 조정합니다. 정해진 교시나 발표 타이머를 슬라이드에 두지 않습니다.

## 발표와 책 연결

- 11명 모두 자신이 구현한 기능, Domain·Service·Repository 역할, 직접 정한 규칙이나 해결한 문제 한 가지를 공유합니다. 별도 발표용 PPT를 요구하지 않습니다.
- 9장에서는 상품 추가·조회 Controller, 요청 DTO·도메인·응답 DTO와 상태·헤더·본문을 정하는 부분을 찾습니다. 이미 배운 입력 수신 어노테이션은 따로 재강의하지 않습니다.
- 상품 API가 아직 없다면 생성·조회 연결을 먼저 마칩니다. 미완료 교육생에게 검증까지 전부 완료했다고 기록하게 하지 않습니다.
- 10장은 도메인/Controller 검증, 전역 예외 핸들러, HTTP 응답 상태와 바디 순서로 읽습니다.

## MVC와 검증에서 짚을 점

DispatcherServlet은 요청을 받아 HandlerMapping으로 담당 처리기를 찾고 HandlerAdapter에 실행을 위임하는 조율자입니다. JSON 읽기와 요청 DTO 검증은 Controller 메서드를 실행하기 전에 일어날 수 있습니다. Service·Repository를 거쳐 얻은 결과는 응답 DTO와 메시지 변환기를 통해 JSON 본문으로 나갑니다. MVC의 Model을 Service 하나와 같은 뜻으로 단정하지 않습니다. @Controller도 @ResponseBody를 붙이면 본문을 반환할 수 있고, JSON API도 Spring MVC를 사용합니다.

입력 형식 검사, 도메인의 유효한 상태, 업무 처리 조건을 구분합니다. 요청 DTO 검사를 통과했다고 도메인의 규칙을 제거하지 않습니다. 이름의 필수 검사와 앞뒤 공백 정리는 별개입니다. 가격 누락과 0원을 구분하려면 요청 DTO는 Integer와 @NotNull·@Min(0)을 사용합니다. @Min만으로 null을 거부한다고 설명하지 않습니다. @NotBlank는 입력값을 trim해서 바꾸는 기능이 아닙니다.

검증 적용 전 build.gradle의 dependencies에 `implementation 'org.springframework.boot:spring-boot-starter-validation'`이 있는지 확인하고, 추가했다면 IDE에서 Gradle 프로젝트를 동기화합니다. 기존 Spring Boot 버전을 유지하며 Spring Boot 3·4의 `jakarta.validation.Valid`와 `jakarta.validation.constraints`를 사용합니다.

## 참고 코드와 응답 범위

기존 `Product`, `ProductRepository`, `MemoryProductRepository`, `ProductService`, 단위·주입/AOP 테스트를 보존합니다. 오늘의 보충 파일은 검증을 적용한 `CreateProductRequest`, `ProductController`, `ApiExceptionHandler`와 기존 `ProductResponse`입니다. 참고 파일 버튼은 마지막 슬라이드에만 배치합니다.

- 생성은 201·Location·상품 JSON, 목록과 단건 조회는 200으로 설명합니다. 생성 결과의 실제 id를 사용하며 id 연속성과 JSON 필드 순서는 가정하지 않습니다.
- 참고 예외 처리기는 요청 DTO 검증·JSON 읽기·도메인 입력 예외를 400, 상품 없음 예외를 404로 정리합니다.
- 이 참고 구현이 모든 경로의 404, 모든 매개변수 타입 오류, 예상하지 못한 500까지 같은 message JSON으로 통일한다고 설명하지 않습니다. 모든 예외를 400으로 바꾸지 않습니다.
- 업무 예외를 HTTP 상태로 바꾸는 것은 애플리케이션의 응답 설계입니다. 프레임워크가 모든 업무 오류를 자동 분류한다고 설명하지 않습니다.
- 메모리 저장소는 서버 재시작 시 초기화됩니다.

## QA 활동

수업 중에는 새 프로젝트를 만들지 않고 기존 `product-api/`에 책의 검증·예외 처리를 적용한 범위를 확인합니다. 정상 동작, 잘못된 입력, 경계 조건, 실패 시 데이터 보존을 고려해 교육생이 직접 QA 체크리스트를 만듭니다. 사전 조건·입력·기대 결과·실제 결과·통과 여부를 적고, 실행 후 문제를 수정해 다시 확인합니다. 상세 입력값과 정답 시나리오를 배포하지 않습니다. 개인 과제는 아래의 기존 위시리스트 검증 보완으로 별도 안내합니다.

Postman 또는 현재 사용할 수 있는 클라이언트로 실행합니다. 먼저 기존 테스트를 실행하고 서버를 시작합니다. 서버 터미널을 유지하며 Windows에서는 gradlew.bat을 사용합니다. 기존 테스트는 보존하되 새로운 테스트 코드 작성은 오늘의 짧은 QA 활동에서 필수로 요구하지 않습니다. README에는 실제 완료한 범위와 미완료 부분을 구분해 기록합니다.

## 개인 과제 · 위시리스트 유효성 검사

7일에 작성한 개인 Fork의 `personal-project/`에 오늘 배운 검증 책임 분리를 적용합니다. 기존 검증을 중복해서 다시 만들지 않고 빠진 조건과 검사 위치를 보완합니다.

- 이름의 null·빈 문자열·공백 거부와 앞뒤 공백 제거, 0 이상의 가격과 무료 항목 허용을 유지합니다.
- 음수 예산을 거부하고 없는 id는 예외로 구분합니다. 실패 뒤에는 기존 데이터가 유지되어야 합니다.
- Domain·Service 검증은 필수입니다. HTTP API가 이미 있다면 요청 DTO의 @NotBlank, Integer 가격의 @NotNull·@Min(0), Controller 인자의 @Valid와 적절한 400·404 실패 응답도 적용합니다. 새 HTTP API 구현은 요구하지 않습니다.
- 추천 규칙과 기존 테스트는 유지합니다. 정상·잘못된 입력·경계 조건·데이터 보존을 고려해 직접 QA 체크리스트를 작성하고 실행합니다. README에 검증 위치와 이유, 실제 결과·문제·수정 결과·남은 문제를 적습니다.
- 수업 중 상품 API 작업과 별도로 공용 저장소에 `[11/09][이름] 위시리스트 유효성 검사` Issue 1개·PR 1개를 제출합니다. 기존 개인 구현 브랜치에서 새 자율 브랜치로 이어가고 코드와 README를 함께 올립니다. 원본 main 대상·개인 Fork head·같은 브랜치 리뷰 수정·강사의 병합 없는 종료 규칙을 그대로 사용합니다.

## 시간 여유가 있을 때의 11장

MVC·검증의 이해도가 충분하고 시간이 남으면 11장 1~2절에서 메모리와 DB 저장의 차이, 테이블·행·열·기본키, 간단한 SQL을 소개합니다. DB 연결 및 전체 CRUD, JPA·Entity·N+1은 오늘 완료 목표가 아닙니다. 교재의 JDBC 접근과 뒤에 진행할 JPA 접근을 구분합니다. DB의 영구 저장은 실제 저장 설정을 전제로 설명합니다.

## 제출

기존 개인 Fork의 `product-api/`를 이어서 사용합니다. 독립 작업이면 공통 시작점에서, 이전 구현을 확장하면 해당 코드가 있는 작업 브랜치에서 새 브랜치를 만듭니다. 이름은 자율입니다. 조직 원본 `sesac-ddm-4-web/sesac-spring-boot-study`에 `[11/09][이름] 상품 API 검증과 예외 처리` Issue와 PR을 각각 1개 작성하고 코드·README를 함께 제출합니다. PR 본문에는 구현 범위, QA 결과, 관련 Issue `#번호`, 이전 PR 링크와 미완료 범위를 적습니다. 설명만 듣고 파일을 바꾸지 않았다면 학습 기록을 남기고, 변경이 생긴 범위를 추후 제출합니다. 빈 PR은 강제하지 않습니다.

PR의 base repository는 조직 원본, base는 main, head는 본인 Fork의 작업 브랜치입니다. 코드는 개인 origin에 Push합니다. 리뷰 수정도 같은 브랜치에 올리고, 강사가 확인을 마치면 병합 없이 PR과 Issue를 닫습니다. 제출 브랜치는 보존하며 원본 main을 pull해서 이전 개인 구현이 생긴다고 설명하지 않습니다. 라벨·담당자·마일스톤 관리 권한을 교육생에게 요구하지 않습니다. greeting-api/·personal-project/와 기존 루트 README 링크, Wrapper와 실행 파일을 보존하고 build/.gradle/IDE 파일·비밀값은 제외합니다.

## 다음 수업

12일에는 오늘의 검증·실패 응답을 실제 적용 상태에 맞춰 보완하고, 첫 웹 서비스의 요구사항·도메인·계층·API·테스트 설계로 이어갑니다.

## 슬라이드별 진행 메모

'''
notes='\n\n'.join(f"### {i+1:02}. {d['title'].replace('<br>',' ')}\n\n{d['note'] or '슬라이드의 핵심 개념과 실제 코드를 책에서 연결합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(HEADER+notes+'\n')
print('Instructor guide generated')
