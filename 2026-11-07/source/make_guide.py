from pathlib import Path
import json
R=Path(__file__).resolve().parent
OUT=R.parent
s=json.loads((R/'metadata-private.json').read_text())
text='''# 2026-11-07 토요일 · 진행 참고

## 운영 기준

- 총 8시간은 휴식 포함, 45분 수업 8회와 15분 휴식 8회 기준입니다. 점심은 별도라는 가정입니다.
- 순수 수업 360분 중 개념·코드 읽기 180분, 실습 155분, 발표·공유 25분으로 구성합니다.
- 학생용 슬라이드에는 강의 시간을 표시하지 않았습니다. 아래 배분은 진행자가 조정할 참고입니다.
- 개념 설명을 모두 마친 뒤 후반부에 실습을 모아서 진행합니다. 실습 A → 포트 설정 확인 → AOP 작성 → 실습 B → 실습 C 순서로 같은 프로젝트를 완성한 뒤 발표합니다.
- 슬라이드 코드는 여러 장으로 나누었습니다. `파일 전체 코드`에서 package·import·중괄호를 포함한 전체 예제를 확인할 수 있습니다. 다운로드할 완성 프로젝트는 제공하지 않습니다.

## 교시별 배분

| 교시 | 중심 내용 | 개념·설명 | 실습 | 발표 |
| --- | --- | ---: | ---: | ---: |
| 1 | 교재 연결, IoC/DI, 컨테이너와 빈 | 45분 | 0분 | 0분 |
| 2 | 스타터·자동 설정·AOP 개념과 프록시 | 45분 | 0분 | 0분 |
| 3 | MVC 흐름, REST 설계, DTO·HTTP 응답 | 45분 | 0분 | 0분 |
| 4 | 검증·예외 응답, 테스트 범위·모킹 개념 | 45분 | 0분 | 0분 |
| 5 | 실습 A: 프로젝트·객체 연결·단위 테스트 | 0분 | 45분 | 0분 |
| 6 | 포트 설정·AOP 작성, 실습 B: DTO·Controller | 0분 | 45분 | 0분 |
| 7 | 실습 B: API 요청, 실습 C: 예외 처리·검증 | 0분 | 45분 | 0분 |
| 8 | 실습 C 결과 확인, 발표·정리 | 0분 | 20분 | 25분 |
| 합계 | | 180분 | 155분 | 25분 |

실습과 발표 합계는 180분입니다. 팀 수가 많으면 팀별로 한 가지 성공 요청과 한 가지 오류, 객체 연결 한 부분을 공유하게 하며 전체 발표 시간은 유지합니다.

## 교재 병행

- **9장 중심:** List로 시작한 상품 관리에서 Map 기반 메모리 저장으로 확장합니다. 생성·목록·단건 조회는 필수, 이름 검색·가격 필터는 수업 이후 필수 과제, 수정·삭제는 도전 과제입니다.
- **10장 연결:** DTO 제약, Domain 규칙, 전역 예외 핸들러, 201·200·400·404를 직접 확인합니다.
- **12장 일부:** 인터페이스, 생성자 DI, Service 단위 테스트를 다룹니다. 현재 테스트는 실제 메모리 저장소를 사용합니다. Mockito 사용은 필수가 아닙니다.
- **11장 이후:** 메모리 데이터 유실을 확인한 뒤 DB 저장 필요성으로 연결합니다. 13·14장 전체 과제는 이번 범위에서 제외합니다.
- 교재 본문을 재현한 자료가 아니라 제공된 목차에 맞춘 독립적인 예제와 설명입니다.

## 실습 진행 기준

개념 구간에서는 코드와 요청 흐름을 읽고 설명합니다. 프로젝트 생성, 설정 변경, Java 파일 작성과 실행은 모두 실습 A 이후에 진행합니다. 슬라이드 순서와 시간표 모두 이 기준을 따릅니다.

### 실습 A

같은 패키지에 상품 객체, 저장소 인터페이스와 메모리 구현체, 없는 상품 예외, Service를 만듭니다. `ProductServiceTest`는 서버 없이 실행하는 테스트입니다. `@SpringBootTest`나 DB 연결은 사용하지 않습니다.

- 생성 성공, 잘못된 가격, 없는 id 테스트 통과를 확인합니다.
- 인터페이스를 주입받는 생성자를 찾고, 실제 연결되는 구현체를 설명하게 합니다.
- 아직 Controller가 없으므로 `/products`의 404를 실습 실패로 판단하지 않습니다.

### 포트 설정·AOP

실습 A의 실행 확인 뒤 `server.port=8081`로 변경·재시작해 보고, 뒤의 API 요청을 위해 8080으로 되돌립니다. Boot 4.x에서는 `spring-boot-starter-aspectj`를 추가합니다. `TimingAspect`를 작성하되 `proceed()`와 `finally`의 의미를 먼저 읽습니다. HTTP를 통한 Service 호출 뒤 콘솔 로그를 확인합니다. 순수 Java 테스트의 `new ProductService(...)`에는 프록시가 없다는 점을 비교합니다.

### 실습 B·C

Request DTO·Response DTO·Controller·전역 예외 핸들러를 같은 프로젝트에 추가합니다. 검증 어노테이션을 포함한 최종 코드가 제공되므로, API의 정상 요청부터 확인하고 검증·예외 처리 단계에서 앞서 배운 규칙과 실제 응답을 연결합니다. 모든 파일이 완성되기 전에는 중간 단계 오류가 있을 수 있습니다.

- `POST /products`: 201, Location, 생성 응답의 id 확인
- `GET /products`: 200과 배열, 비어 있으면 `[]`
- `GET /products/{id}`: 생성 응답의 실제 id로 조회
- 공백 이름·음수 가격·빠진 가격·문자열 가격: 각각 400, 목록 수 불변
- 존재하지 않는 id: 404와 오류 JSON
- 앞뒤 공백이 있는 정상 이름: 201, 공백이 제거된 이름
- 서버를 다시 시작하면 메모리 저장 상품과 번호가 초기화됨

브라우저 주소창은 GET 확인에 사용합니다. POST는 사용 가능한 API 도구 또는 슬라이드의 JSON 파일 기반 curl 명령을 사용합니다. 프로젝트에 파일을 새로 추가하거나 바꾼 뒤 저장·재시작합니다. 같은 서버를 두 번 실행하지 않습니다.

## 속도 조절

- 환경 설정이 지연되면 짝과 한 화면에서 원인을 확인하고 역할을 교대합니다.
- 시간이 부족하면 AOP 코드 작성 분량을 줄이고 흐름 관찰에 집중합니다. 필수 API와 400·404, 발표는 유지합니다.
- 시간이 남는 팀은 실습 결과와 발표 설명을 보완합니다. 별도 과제는 수업 이후 수행하며 DB 설치로 범위를 넓히지 않습니다.
- 파일 단위 코드를 여러 페이지에서 연결할 때 클래스나 메서드를 중복 작성하지 않도록 확인합니다.

## 별도 과제 운영

- 실습과 발표·정리를 마친 뒤 과제 섹션을 안내합니다. 기존 8시간 수업의 실습 배분은 늘리지 않습니다.
- 필수 1단계는 이름 부분 일치 검색, 필수 2단계는 가격 상한 필터와 이름 조건의 AND 결합입니다. 검색어 미지정·공백, 무결과, 상한 경계값, 잘못된 숫자 조건도 확인합니다.
- 도전 3단계는 이름·가격 전체 수정입니다. id·목록 개수를 유지하고, 실패 요청 뒤 기존 값이 보존되어야 합니다. 도전 4단계는 삭제와 204 빈 본문, 후속 조회·재삭제의 404를 확인합니다.
- 같은 프로젝트를 단계적으로 확장하고 기존 POST·GET·400·404 동작을 회귀 테스트합니다. 정답 코드와 구현 시연 없이 요구사항 안내 → 질문 → 결과 피드백으로 진행합니다.
- GitHub 저장소·Wiki·병합 PR로 실습과 과제를 제출받습니다. 성공·실패 요청 결과, 단계별 테스트와 설명을 확인하며 마감을 임의로 정하지 않습니다.

## GitHub 제출 운영 규칙

- Spring 학습 내내 재사용할 개인별 본인 계정의 Public 저장소 이름은 `sesac-spring-boot-study`, 설명은 `Spring Boot 학습 실습 및 과제 기록`, 기본 브랜치는 `main`입니다. Issues와 Wiki를 활성화합니다. 각자 계정이므로 같은 이름이 가능합니다. 진행자가 대신 저장소·Issue를 생성하지 않습니다.
- 기존 학습 저장소를 재사용합니다. 날짜별 이름이면 sesac-spring-boot-study로 이름을 변경하며 추가 새 저장소를 만들 의무는 없습니다. 저장소가 없을 때만 README와 Java .gitignore로 main을 초기화합니다. Settings → Features에서 Issues·Wiki를 확인합니다. 처음 접근은 clone, 이미 작업 중이면 최신 main을 pull합니다. practice/product-api에서 product-api/ 안에 실습 파일을 복사하며 기존 .git 폴더는 복사하지 않습니다. greeting-api/ 등 기존 프로젝트와 기록을 보존합니다. 기존 루트의 Java 프로젝트는 해당 프로젝트 폴더로 옮겨 완료 실습 PR에서 함께 정리할 수 있고 별도 PR을 강제하지 않습니다. 완료한 실습은 결과 정리 Issue를 만들고 `practice/product-api`에서 코드·실행 파일·테스트를 추가하여 PR로 제출합니다. 실습 전에 Issue를 작성했던 것처럼 기록하지 않습니다.
- 실습 이후 모든 단계는 Issue 생성 → 최신 main에서 지정 브랜치 생성 → 구현·테스트 → commit·push → main 대상 PR → 자체 확인·병합 → 로컬 main pull 순서입니다. 기능 코드를 main에 직접 push하지 않습니다. 타인 승인은 필수가 아니며 최소 커밋 개수도 강제하지 않습니다. 메시지는 목적에 맞게 `feat:`, `test:`, `docs:`, `fix:`를 사용합니다.

| 브랜치 | Issue와 PR의 동일 제목 |
| --- | --- |
| practice/product-api | [실습] 상품 API 기본 기능 구현 |
| feature/name-search | [과제 1] 상품 이름 검색 |
| feature/price-filter | [과제 2] 가격 조건 검색 |
| feature/update-product | [과제 3] 상품 수정 |
| feature/delete-product | [과제 4] 상품 삭제 |
| docs/product-api | [문서] 상품 API README와 Wiki 정리 |

- 라벨 `practice`, `assignment`, `docs`, `bug`를 생성합니다. 실습·과제·문서에 해당 라벨을 붙이고 bug는 오류 수정에 사용합니다. milestone은 `product-api-2026-11-07`, 마감일은 미지정이며 assignee는 본인입니다.
- Issue 본문 제목은 **목표 / 구현할 일 체크리스트 / 완료 기준 / 검증 결과(기대·실제) / 관련 PR**입니다. PR 본문 제목은 **변경 내용 / 검증 결과 / 관련 Issue**이며 `Closes #실제번호`로 연결합니다. 번호는 실제 자동 발급 번호로 바꿉니다. 기본 브랜치 main에 병합하여 Issue가 닫혔는지 확인합니다.
- 필수 실습·과제 1·과제 2·문서는 Issue 4개와 병합 PR 4개입니다. 도전 3·4는 수행한 경우 각각 Issue·PR 1개씩 더하여 모두 수행하면 각각 6개입니다. 미수행 도전의 Issue 생성 의무는 없습니다. 필요에 따른 버그 Issue는 별도입니다.
- 루트 README는 프로젝트 목록·각 폴더 README 링크·Wiki 링크를 담는 공통 목차입니다. `product-api/README.md`의 고정 섹션은 **프로젝트 소개 / 개발 환경(Java·실제 Boot) / 실행·테스트 방법 / 구현 현황(실습·1~4, 필수·도전) / API 목록 / Wiki 링크**입니다. 문서 브랜치 PR에 README와 Wiki 링크·작성 확인을 포함합니다.

| Wiki 고정 페이지 | 필수 내용 |
| --- | --- |
| Home | 공통 목차와 프로젝트별 링크 |
| 01-Setup | 실제 JDK·Boot, 실행·테스트 명령, 포트 |
| 02-Architecture | Controller-Service-Repository, DI 역할, AOP |
| 03-API | 구현 API의 메서드·경로·요청·응답·상태 |
| 04-Verification | 실습 201·200·400·404, AOP 로그, 각 단계 성공·실패 기대/실제, 테스트 결과, Issue·PR 링크 |
| 05-Retrospective | 해결 오류 최소 1개(없으면 가장 헷갈린 점), 원인·해결·배운 점 |

- 기존 여섯 Wiki 페이지를 유지하며 각 페이지에 greeting-api/product-api 등 프로젝트별 섹션을 누적하고 기존 내용을 덮어쓰지 않습니다. Wiki가 없을 때만 GitHub Wiki 화면에서 Home부터 생성합니다. 일반 코드 PR에 자동 포함되지 않으므로 링크가 실제 열리고 여섯 페이지가 있는지 별도 확인합니다. GitHub Free의 Public 저장소에서도 Wiki를 사용할 수 있습니다.
- 실행·테스트는 `product-api/` 폴더에서 진행합니다. 원래 실습 명령은 이 폴더에서 실행합니다. 이 폴더 안의 제출 파일은 `src`, `build.gradle`, `settings.gradle`, `gradlew`, `gradlew.bat`, `gradle/wrapper`이며 생성된 wrapper jar도 포함합니다. GitHub Java .gitignore의 `*.jar` 규칙으로 누락되지 않도록 `!product-api/gradle/wrapper/gradle-wrapper.jar` 예외를 저장소 루트 .gitignore에 추가·확인하며 기존 greeting-api wrapper 예외도 유지합니다. build/와 .gradle/ 패턴은 하위 프로젝트에도 적용합니다. Initializr .gitignore를 복사할 때도 wrapper 예외를 유지합니다. `.gitignore`에서 `build/`, `.gradle/`, `.idea/`, `*.iml`, `.env` 등을 제외하고 비밀값이 없는지 확인합니다.
- 최종 제출은 **저장소 URL + Wiki Home URL + 필수 병합 PR 4개 링크 + 도전 구현 여부와 해당 PR 링크**입니다. main의 product-api/에서 실습과 필수 1·2가 실행되고 기존 POST·GET·400·404가 유지되어야 합니다.
- 제출 절차는 시연 없이 안내·질문·결과 피드백으로 진행합니다. 기존 8시간 실습 배분을 늘리지 않으며 별도 마감일을 임의로 설정하지 않습니다.
- README에도 아래 공식 문서 두 링크를 넣습니다. 공식 근거: [Wiki](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis), [PR과 Issue 연결](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

## 발표 평가

완성 화면만 보지 않고 (1) 기대값과 실제 HTTP 결과, (2) DI로 연결되는 객체, (3) 입력 검증과 예외 응답, (4) 해결한 오류와 근거를 확인합니다. 발표용 별도 PPT는 만들지 않습니다.

## 검증 범위

`verify.py`는 슬라이드와 전체 코드의 일치, 고유 HTML/SVG id, 개념→실습 순서와 집중 실습의 연속성, 읽기 전용 게시, JavaScript 구문을 검사합니다. 실제 Java Domain·Repository·Service의 정상/실패 처리, 객체 주입과 저장소 분리, 병렬 생성 시 id 중복 여부도 실행 확인합니다.

자동 검사에는 실제 Spring 서버 실행과 브라우저 렌더링이 포함되지 않습니다. 별도 과제 구간과 GitHub 제출 안내 15장은 브라우저에서 내용과 화면 잘림을 확인했습니다. JUnit·HTTP 바인딩·AOP를 실제 Spring 환경에서 검증한 결과로 해석하면 안 됩니다. 수업 환경에서 공통 Boot 버전과 JDK를 맞추고 요청 확인표를 한 번 실행하는 것이 최종 리허설입니다.

## 슬라이드별 진행 참고

'''
for i,d in enumerate(s):
 if d['note']:text+=f"### {i+1:02}. {d['title']}\n\n{d['note']}\n\n"
(OUT/'INSTRUCTOR.md').write_text(text)
print('Instructor guide generated')
