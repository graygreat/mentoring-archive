from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
header='''# 2026-11-12 강사용 가이드 · REST 실습2시간 + 서비스 설계2시간

## 진행 원칙과 시간표

기존 product-api에 검증/예외를 추가하고, 책의 상품 관리 앱에서 남은 CRUD 기능을 설계합니다. 강사 구현 시연 없이 개념 → 자율 실습 → 검증/피드백. 4블록 총240분:

1. 검증·예외와 HTTP 메서드/상태/멱등성/REST 성숙도 45분 + 휴식15분.
2. 멘티 오류 실습·정상 회귀·결과 설명45분 + 정리/휴식15분.
3. 교재 상품 CRUD 읽기10분, 요구20분, 도메인10분, 점검5분 + 휴식15분.
4. API15분, 테스트15분, 동료설명10분, 수정5분, 제출정리15분.

앞120분은 CH10 검증·예외 실습, 뒤120분은 상품 CRUD 설계입니다. 단축 URL과 주문 전체 구현은 별도 과제입니다. 교재 부록B의 테스트 풀이 흐름을 연결합니다. 1~8장 복습은5일, CH12 객체지향·테스트는7일 선행, CH11 DB/JDBC 방식은 이후 JPA와 구분합니다.

## 단계 코드 계약

Java17/Boot4.1.2/기존 Gradle 및 코어/AOP/ServiceTest/ProductWiringTest 유지. 기존 dependencies 안에 validation 스타터만 추가:

`implementation 'org.springframework.boot:spring-boot-starter-validation'`

당일 source-data는3파일: CreateProductRequest, ProductController, ApiExceptionHandler. DTO는 제약 추가, Controller는 @Valid import/생성 요청 매개변수 추가, Handler는 신규. ProductResponse와 나머지 파일은9일/7일 자료에 있습니다.

**이름·가격 검색 선택 과제를 구현한 학생은 Controller 전체 예제로 덮어쓰지 않습니다.** 전체 예제는 기본 생성·조회 기준입니다. 기존 Controller에 `import jakarta.validation.Valid;`와 생성 요청의 `@Valid`만 반영하고 기존 findAll 검색 코드를 유지합니다. DTO는 제약을 반영하고 Handler는 새로 추가합니다. 동일 이름의 클래스를 중복 생성하지 않습니다.

DTO 검증과 Product 도메인 규칙은 함께 유지합니다. Integer price의 null은 @NotNull로 거부하며 @Min만으로는 부족합니다. 메시지 변환 실패/DTO 검증 실패/도메인 규칙 실패를 구분합니다. 모든 예외를 무조건400으로 바꾸지 않습니다. 제공 처리기의 범위는 ProductNotFoundException, MethodArgumentNotValidException, HttpMessageNotReadableException, IllegalArgumentException입니다. 숫자가 아닌 경로 id 등은 다른 기본 오류 응답일 수 있으므로 동일 message를 보장한다고 말하지 않습니다.

## 실행과 검증

product-api/에서 ./gradlew test 및 ./gradlew bootRun. Windows는 .\\gradlew.bat test / .\\gradlew.bat bootRun. 서버 재시작·포트 일치 확인.

- 새 서버 빈 목록200+[], 정상 생성201/Location/JSON, 실제 id조회200.
- 가격0 정상, 이름 앞뒤 공백 strip 후201.
- 공백/빈/누락/null 이름, 음수/누락/null 가격 각각400.
- 가격문자 abc와 깨진JSON 각각400, message 확인.
- 없는 숫자id404+message. 현재 목록에 없는 id를 선택.
- 각 실패 전후 목록 개수와 기존 값 불변. id 연속성은 강제하지 않음.
- 기존 단위·Wiring 테스트와 AOP 시간 로그 확인.

현재 비교 슬라이드에 ResponseStatusException 한 줄 예시를 직접 제공합니다. greeting-api 추가 수정은 필수가 아닙니다. 선택 이름·가격 검색을 구현했다면 음수/문자가격400과 원본 불변도 추가 확인합니다.

HTTP 면접 설명: GET 안전·멱등, POST는 일반적 멱등 보장 없음, PUT/DELETE 멱등. 재삭제404여도 최종 상태가 같을 수 있습니다. REST 성숙도0/1/2/3는 토론 틀로 소개하며 오늘 구현은Level2 범위입니다. JSON만으로 REST 판단하지 않음, Level3 하이퍼미디어 구현은 요구하지 않음.

## 상품 CRUD 설계 · 뒤 2시간

수업 공통 프로젝트는 책의 상품 관리 애플리케이션입니다. CH09 남은 CRUD 요구와 CH10 검증, CH12 테스트 관련 절을 함께 읽습니다. 페이지·세부 정책은 실제 판본에서 확인합니다. 슬라이드는 길 안내와 보충 예제이며 본문이나 교재 정답 코드를 전재하지 않습니다. 생성·조회는 그대로 보존하고 수정·삭제를 설계합니다. 새 프로젝트는 만들지 않습니다.

1. 상품 수정·삭제의 필수/선택/가정, 교재 근거.
2. 사용자 시나리오와 Product·Controller·Service·Repository 책임.
3. 기존 생성·조회와 연결한 API표: 메서드/경로/입력/성공/실패.
4. PUT 전체 교체 또는 PATCH 부분 변경의 선택 근거, DELETE 후 응답과 재삭제 정책.
5. 정상·없는 id·잘못된 입력·경계값·실패 후 상태 보존 테스트.
6. 구현 순서·동료 피드백·미정 질문.

필수 문서는 product-api/docs/crud-design.md입니다. 뒤 첫 블록은 책 읽기10분·요구20분·도메인10분·점검5분+휴식15분, 둘째 블록은 API15분·테스트15분·동료검토10분·수정5분+정리15분으로 운영합니다. 책의 예제와 수업 보충 코드를 비교하고 왜 다른지 기록합니다.

단축 URL은 별도 과제입니다. [과제 안내](../assignments/short-url/index.html)에 설계→백엔드 직접 구현→AI 프론트→테스트·Git 제출을 안내했습니다. 메모리 저장+AI 화면 연결은 필수, DB 전환은 선택, 마감은 별도 공지입니다. 주문 전체 API도 선택입니다. 23일 주문 최소 예제는 JPA 관계·N+1 공통 실습용이며 전체 주문 과제와 구분합니다.

## GitHub 제출

Public 저장소 sesac-spring-boot-study의 main을 계속 사용합니다. 필수 Issue2개와 병합 PR2개:

| 브랜치 | Issue·PR 제목 |
|---|---|
| practice/product-validation | [실습] 상품 API 검증과 예외 응답 |
| docs/product-crud-design | [설계] 상품 CRUD 요구사항과 테스트 설계 |

Assignee 본인, milestone product-api-2026-11-12(마감 별도), 라벨 practice/docs. 최신 main→Issue→branch→구현/설계/검증→commit/push→PR(base main, Closes 실제번호)→자체확인/병합→main pull. 별도 문서PR은 추가로 요구하지 않습니다.

product-api/README에 소개·실제 환경·실행/테스트·현황·API·Wiki 링크를 누적합니다. 루트README에 기존 프로젝트와 CRUD 설계 링크를 보존합니다. Wiki Home/01-Setup/02-Architecture/03-API/04-Verification/05-Retrospective는 같은 여섯 페이지를 프로젝트·날짜별로 누적합니다. Wiki는 별도 저장소이므로 코드PR과 자동 동기화되지 않습니다. 편집 후 PR에 실제 링크·작성 확인을 남깁니다.

검증된 API와 아직 구현 전인 수정·삭제 계획을 구분합니다. Wrapper와 기존 greeting-api/product-api를 보존합니다. build/.gradle/.idea/.env·비밀값과 중첩 .git은 제외합니다. 루트 .gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar와 greeting-api 예외를 유지합니다.

최종 제출: 저장소URL·WikiHomeURL·필수PR2개·실제 검증 기록·CRUD 설계 문서. 14일 앞6시간은 책을 보며 상품 CRUD 구현·테스트, 뒤2시간은 JPA 입문·매핑 활동입니다. 교재11장 JDBC와 JPA를 같은 구현이라고 설명하지 않습니다.

## 실행 리허설 근거 · 2026-10-26

Java 17 / Spring Boot 4.1.2에서 실제 단계별 증분 구성을 실행 검증했습니다. 7일(core+AspectJ) → 9일(+Web MVC) → 12일(+Validation) 순서로 clean build 및 JUnit 테스트 5개가 각 단계에서 통과했습니다. 오늘 단계는 정상 7개 + 오류 9개 + 실패 후 저장 상태 불변 1개와 AOP 로그를 확인했습니다. 검증 환경의 결과이며 멘티는 자기 환경에서도 다시 실행하고 실제 결과를 기록합니다. 루트 통합 리허설 기록을 참조합니다.

## 슬라이드별 강사 메모

'''
notes='\n\n'.join(f"### {i+1}. {d['title'].replace('<br>',' ')}\n\n{d['note'] or '질문·산출물·완료 기준을 확인하고 멘티의 근거와 결과를 피드백합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(header+notes+'\n')
print('Created INSTRUCTOR.md')
