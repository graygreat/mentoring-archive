# 단축 URL 웹 서비스 별도 과제

수업의 공통 프로젝트는 책의 상품 관리 앱입니다. 이 과제는 배운 계층·REST·검증·테스트를 새 문제에 스스로 적용하는 작업입니다. 백엔드 정답 코드는 제공하지 않습니다. 프론트는 AI를 활용합니다. 마감은 별도 공지입니다. 로컬 학습 환경에서 진행하며 공개 배포·악용 방지 정책은 별도 확장으로 다룹니다.

[과제 안내](./index.html) · [설계 템플릿](./templates/design.md) · [검증 템플릿](./templates/verification.md) · [AI 프롬프트](./templates/ai-prompts.md) · [프로젝트 README 틀](./templates/project-readme.md)

## 단계와 범위

| 단계 | 권장 시점 | 필수 결과 |
| --- | --- | --- |
| 1. 설계 | 12일 이후 | 책 CH13 요구 확인, 필수·선택·가정, API·화면·테스트 설계 |
| 2. 백엔드 | 14일 상품 CRUD 학습 후 | 메모리 저장, 생성·원본 이동, 정상·실패·경계 테스트 |
| 3. AI 프론트 | 백엔드 완료 후, 16일 전후 권장 | HTML/CSS/JavaScript 화면 생성·실제 API 연결 |
| 4. 통합·제출 | 23일 결과 공유 전 권장 | 실제 화면·HTTP·테스트 결과, AI 기록, Issue·PR·Wiki |

권장 시점은 마감이 아닙니다. 과제는 수업 시간 전체를 대체하지 않으며, 수업 중 상품 관리의 필수 완료 지점부터 마칩니다. DB/JPA 전환, 배포, 통계·만료·사용자 계정·주문 전체 API는 선택입니다.

## 책 요구와 수업 과제의 구분

책 CH13의 실제 문제와 테스트 제시 부분을 읽고 장·절/본인 판본의 페이지를 기록합니다. 이 안내는 책 본문의 정책이나 정답을 전재하지 않습니다. 코드 길이, 중복 URL, 충돌 처리, 만료, 조회수 등의 세부 조건은 책을 확인합니다. 명시되지 않은 내용은 본인 가정으로 표시합니다.

수업 과제로 추가하는 필수는 **AI 프론트 연결·실제 검증·Git 기록**입니다. URL 입력→생성 결과와 복사→단축 링크 클릭→원본 이동의 사용자 흐름을 완성합니다. 생성 API의 경로·필드명·상태·본문은 본인이 설계하며 프론트와 정확히 일치시킵니다. 단축 URL에 불필요한 전체 CRUD를 강제하지 않습니다.

## 구현 완료 기준

- 원본 URL을 입력해 단축 URL을 생성하고 브라우저에서 실제 원본으로 이동한다.
- 메모리 저장소는 프로세스 재시작 시 초기화된다. 초기화를 결함으로 보고 DB를 필수 구현하지 않는다.
- 입력 URL은 http/https 스킴의 절대 주소로 제한한다(수업 권장 정책). javascript/data/file 스킴은 거부하고 프론트 링크도 같은 정책으로 확인한다.
- 백엔드는 원본 페이지 내용을 다운로드할 필요가 없다. 미리보기·메타데이터 수집은 과제 범위에 넣지 않는다.
- 생성 응답의 Location이 가리키는 곳과 원본 이동 응답의 Location을 구분한다. 원본 이동은 설계한 3xx와 원본 주소 Location을 실제로 확인한다.
- 빈 값·잘못된 주소·없는 코드·충돌/중복 정책을 테스트한다. 구현하지 않은 선택 기능은 검증 완료로 기록하지 않는다.
- 프론트는 입력/버튼/생성 결과/복사/이동 링크/로딩/오류 메시지를 갖춘다. 성공·실패 뒤 버튼 상태가 복구된다.
- `src/main/resources/static/index.html`과 필요한 CSS/JS를 사용한다. Spring Boot가 제공하는 같은 origin에서 상대 경로로 API를 호출한다.
- 서버를 실행한 `http://localhost:실제포트/`로 접근한다. HTML을 파일로 직접 열거나 별도 개발 서버를 띄우지 않는다.
- 사용자 URL·오류 메시지는 textContent 등 텍스트로 표시한다. innerHTML로 주입하지 않는다. 복사는 HTTPS/localhost 환경에서 확인하고 실패 시 선택해서 복사할 안내를 제공한다.

## AI 사용 범위

프론트 생성과 프론트 오류 해결에 AI를 활용합니다. 백엔드 구현 답안 전체를 AI에 대신 작성시키는 과제가 아닙니다. 프롬프트에는 실제 API 명세만 넣고 비밀값·개인정보를 넣지 않습니다.

AI 초안에서 API 경로·메서드·JSON 필드·상태 처리·링크를 멘티가 확인하고 수정합니다. 요청/응답 흐름을 설명할 수 있어야 합니다. [프롬프트 템플릿](./templates/ai-prompts.md)을 본인 명세로 채워 사용하고 프롬프트·수정 이유·검증을 `short-url/docs/ai-log.md`에 남깁니다.

## GitHub 제출 규칙

저장소 `sesac-spring-boot-study` (Description `Spring Boot 학습 실습 및 과제 기록`, Public/main)를 재사용합니다. `short-url/`에 별도 프로젝트를 두고 IDE·Gradle은 그 폴더에서 실행합니다. 기존 greeting-api/product-api와 문서를 보존합니다. 프로젝트 안에 중첩 .git을 복사하지 않습니다.

| 순서 | 브랜치 | Issue·PR 제목 | 라벨 |
| --- | --- | --- | --- |
| 1 | docs/short-url-design | [과제 1] 단축 URL 요구사항과 API·화면 설계 | assignment, docs |
| 2 | feature/short-url-core | [과제 2] 단축 URL 백엔드와 테스트 | assignment |
| 3 | feature/short-url-ai-ui | [과제 3] AI 프론트 연결과 통합 검증 | assignment, docs |
| 선택 | feature/short-url-jpa | [선택] 단축 URL JPA 저장소 전환 | assignment |

필수 Issue3개·병합 PR3개. Assignee 본인, milestone `short-url-assignment`(마감 미설정). bug 라벨은 실제 결함이 있을 때만 추가합니다. 최신main pull→Issue→브랜치→작업/검증/문서→commit/push→base main PR→자체검토/병합→main pull. PR 본문에는 변경 내용·기대/실제 검증·AI 활용 여부·`Closes #실제Issue번호`를 씁니다.

프로젝트에는 src/build.gradle/settings.gradle/gradlew/gradlew.bat/gradle/wrapper(gradle-wrapper.jar 포함)를 커밋합니다. build/.gradle/.idea/*.iml/.env·비밀값·로컬DB파일은 제외합니다. 루트 Java .gitignore가 *.jar를 제외하면 `!short-url/gradle/wrapper/gradle-wrapper.jar` 예외를 추가하고 기존 두 프로젝트의 예외도 유지합니다. 기존 디렉터리 무시 규칙으로 상위 폴더 전체가 제외됐다면 해당 규칙도 함께 점검합니다.

루트 README에 프로젝트 링크를 추가하고 `short-url/README.md`에는 소개·실제 환경·실행/테스트·구현 현황·API·Wiki를 기록합니다. 기존 공통 Wiki **Home / 01-Setup / 02-Architecture / 03-API / 04-Verification / 05-Retrospective**에 short-url 섹션을 누적합니다. Wiki 수정은 코드PR에 자동 포함되지 않으므로 실제 Wiki 링크·작성 확인을 PR에 남깁니다.

최종 제출: 저장소URL·프로젝트README·WikiHome·필수PR3개·설계/검증/AI 기록·화면 증거. 코드 캡처만으로 완료 처리하지 않고 실행 가능한 코드와 테스트를 포함합니다.
