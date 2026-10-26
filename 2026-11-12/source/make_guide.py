from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
header='''# 2026-11-12 강사용 가이드 · REST 실습2시간 + 서비스 설계2시간

## 진행 원칙과 시간표

기존 product-api에 검증/예외를 추가하고, 교재 문제를 바탕으로 새 기능을 설계합니다. 강사 구현 시연 없이 개념 → 자율 실습 → 검증/피드백. 4블록 총240분:

1. 검증·예외와 HTTP 메서드/상태/멱등성/REST 성숙도 45분 + 휴식15분.
2. 멘티 오류 실습·정상 회귀·결과 설명45분 + 정리/휴식15분.
3. 교재 CH13 읽기10분, 요구20분, 도메인10분, 점검5분 + 휴식15분.
4. API15분, 테스트15분, 동료설명10분, 수정5분, 제출정리15분.

앞120분은 CH10 검증·예외 실습, 뒤120분은 CH13 설계입니다. CH14 주문관리는 공통 설계를 마친 뒤 선택 설계입니다. 교재 부록B의 테스트 풀이 흐름을 연결합니다. 1~8장 복습은5일, CH12 객체지향·테스트는7일 선행, CH11 DB/JDBC 방식은 이후 JPA와 구분합니다.

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

## 교재 기반 설계

책 CH13의 과제·테스트 제시를 학생이 직접 읽고 설계합니다. 자료는 원문을 복제하거나 미확인 세부 정책을 책의 요구라고 단정하지 않습니다. 단축 코드 길이, 중복, 통계, 만료 등은 교재 명시 여부를 확인합니다. 미지정 정책은 질문 또는 가정으로 표시합니다. 단축URL이 전체CRUD/모든JSON이어야 한다고 강요하지 않습니다. 리다이렉션 요구라면 상태/Location을 설계합니다.

필수 산출물 `short-url/docs/design.md`:

1. 요구사항: 필수/선택/가정 및 교재 근거(장·절/페이지).
2. 사용자 시나리오.
3. 도메인 규칙·계층별 책임.
4. API표: 메서드/경로/헤더·경로·본문/정상·실패 응답.
5. 테스트: 정상·실패·경계값, 준비/실행/기대 결과.
6. 구현 순서·미해결 질문·동료 피드백과 반영.

오늘 새 Java프로젝트/DB/JPA 구현은 필수가 아닙니다. 해설은 독립 설계 뒤 비교합니다. 선택 CH14 주문관리도 실제 교재 요구를 읽고 같은 틀로 `order-api/docs/design.md`에 설계하며 재고·결제 등을 임의 필수화하지 않습니다.

## GitHub 제출

sesac-spring-boot-study 재사용, greeting-api/product-api 보존. 필수 Issue2개와 병합 PR2개:

| 브랜치 | Issue·PR 제목 |
|---|---|
| practice/product-validation | [실습] 상품 API 검증과 예외 응답 |
| docs/short-url-design | [설계] 단축 URL 요구사항과 API 설계 |

본인 Assignee, milestone product-api-2026-11-12(마감미지정), 검증작업 practice/docs, 설계작업 assignment/docs 라벨. 최신 main→Issue→branch→작업/검증/문서→commit/push→PR(base main)→자체확인/병합. Closes는 실제 Issue번호. 별도 문서PR 강제 안 함. Wiki 변경은 코드PR에 자동포함되지 않으므로 별도 편집 후 링크/체크를 남김.

루트README에 프로젝트·설계 링크. product-api/README는 소개/실제환경/실행·테스트/현황/API/Wiki 여섯항목. Wiki Home/01-Setup/02-Architecture/03-API/04-Verification/05-Retrospective에 프로젝트·날짜별 누적, 기존 내용 보존. 단축URL은 실행 결과 대신 설계 계획이라고 표시. 오류가 없었다면 헷갈린 점의 원인/해결/배운 점을 회고.

실제 수행한 정상/오류 기대·실제, 테스트, AOP, Issue/PR링크 기록. Public/main 및 Issues/Wiki 유지. Wrapper jar와 루트 .gitignore의 product-api/greeting-api 예외 유지. build/.gradle/IDE파일/.env·비밀값 제외. short-url은 설계문서만 있으며14일 프로젝트 추가 때 Wrapper도 포함.

최종 제출: 저장소URL, WikiHomeURL, 필수PR2개, 선택 수행 여부.14일 첫6시간은 설계 기반 최소 기능→실패 처리→테스트·피드백, 뒤2시간은 ORM/JPA 개념 진입. CH11 JDBC 방식과 동일 구현이라고 설명하지 않습니다.

## 실행 리허설 근거 · 2026-10-26

Java 17 / Spring Boot 4.1.2에서 실제 단계별 증분 구성을 실행 검증했습니다. 7일(core+AspectJ) → 9일(+Web MVC) → 12일(+Validation) 순서로 clean build 및 JUnit 테스트 5개가 각 단계에서 통과했습니다. 오늘 단계는 정상 7개 + 오류 9개 + 실패 후 저장 상태 불변 1개와 AOP 로그를 확인했습니다. 검증 환경의 결과이며 멘티는 자기 환경에서도 다시 실행하고 실제 결과를 기록합니다. 루트 통합 리허설 기록을 참조합니다.

## 슬라이드별 강사 메모

'''
notes='\n\n'.join(f"### {i+1}. {d['title'].replace('<br>',' ')}\n\n{d['note'] or '질문·산출물·완료 기준을 확인하고 멘티의 근거와 결과를 피드백합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(header+notes+'\n')
print('Created INSTRUCTOR.md')
