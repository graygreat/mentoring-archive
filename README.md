# 멘토링 수업 자료

Spring Boot & AI 과정의 수업 자료를 모아두는 저장소입니다.

## 수업 자료

| 날짜 | 배정 시간 | 주제와 교재 연결 | HTML |
| --- | --- | --- | --- |
| 2026-11-02 | 기존 일정 | OT · Git · GitHub 협업 · Java 팀 실습 | [수업 자료](./2026-11-02/index.html) |
| 2026-11-05 | 4시간 | 교재 1~8장 선행 복습 → Initializr·프로젝트 구조·Gradle → 인사 API 단순 GET | [수업 자료](./2026-11-05/index.html) |
| 2026-11-07 | 핵심 개념 6시간 + MVC 2시간 | 책 9·12장 일부와 MVC 읽기 → 개인 소장품 코어·테스트·발표 | [수업 자료](./2026-11-07/index.html) |
| 2026-11-09 | 4시간 | 9장·부록 A, 7~8장 재연결: REST 설계·DTO·JSON·상품 생성/조회·Postman | [수업 자료](./2026-11-09/index.html) |
| 2026-11-12 | REST 실습 2시간 + 서비스 설계 2시간 | 10장 검증·예외·400/404·면접 → 상품 남은 CRUD 요구·계층·API·테스트 설계 | [수업 자료](./2026-11-12/index.html) |
| 2026-11-14 | 상품 CRUD 6시간 + DB 기초·JPA 맛보기 2시간 | 책 상품 CRUD → 개인 소장품 REST CRUD·발표 → 상품 표·SQL·객체 매핑 | [수업 자료](./2026-11-14/index.html) |
| 2026-11-16 | 4시간 | SQL과 객체 비교 → Entity·ID·Repository → 기본 트랜잭션·쿼리 단계 실습 | [수업 자료](./2026-11-16/index.html) |
| 2026-11-19 | 4시간 · 이준형 강사 대강 | 사전 점검·작업지·오류 힌트로 상품 저장소 JPA 전환·API/DB 보존 검증 | [수업 자료](./2026-11-19/index.html) |
| 2026-11-23 | 4시간 | SQL을 보며 영속성·트랜잭션 복습 → 관계·지연 로딩·N+1 관찰/개선 | [수업 자료](./2026-11-23/index.html) |

## 진행 기준

- 7일부터 수업의 중심은 책의 상품 관리 애플리케이션입니다. 책 함께 읽기 → 핵심 질문 → 멘티 직접 구현 → 테스트 → 책과 비교를 반복합니다. PPT는 장·활동 전환, 과제와 완료 기준을 안내하고 긴 개념 설명과 코드 전체는 책·보충 자료로 확인합니다. 강사 코딩 시연은 하지 않습니다.
- 책의 관련 절을 실제 판본에서 확인합니다. 확인되지 않은 쪽수나 세부 규칙을 책의 요구사항으로 적지 않습니다. 수업 보충 예제(예: Map 저장소)와 교재 원본의 차이를 구분합니다.
- 5일에는 책1~8장 복습을 약60~90분 먼저 진행하고 Initializr·프로젝트 구조·Gradle·단순 GET을 구현합니다.
- 7일 토요일 8교시는 책·공통 프로젝트 4교시와 개인 프로젝트·발표 4교시로 진행합니다. 개인 과제는 객체·메모리 저장소·Service·생성자 DI와 테스트까지이며 Controller/HTTP는 요구하지 않습니다.
- 14일 토요일 8교시는 책의 상품 CRUD 2교시 → 개인 프로젝트 REST CRUD·발표 4교시 → DB 기초·JPA 입문 2교시로 진행합니다. 앞 6교시의 CRUD 학습과 뒤 2교시 DB 배정을 유지합니다. 개인 프로젝트에 JPA·DB를 붙이는 것은 필수가 아닙니다.
- 주말 개인 활동 4교시는 구현·준비 105분 + 발표·질문 75분 + 휴식·정리 60분입니다. 11명 모두 발표 4분·질문 2분(66분), 공통 피드백 9분을 사용합니다. 매 교시는 활동 45분+휴식·정리 15분, 점심 별도입니다. 발표용 PPT 없이 코드·테스트·실행 결과를 보여줍니다.
- [주말 개인 프로젝트 안내](./assignments/personal-project/README.md): 개인 저장소의 `personal-project/`에서 소장품 관리를 구현합니다. 7일 코어와 테스트 → 14일 같은 프로젝트의 REST CRUD로 확장합니다. 공통 교재 프로젝트 `product-api/`는 이후 진도를 위해 별도로 보존합니다.
- 12일 뒤2시간은 상품 CRUD 설계, 14일 구현, 16일 SQL→Entity→Repository 단계 실습, 19일 상품 저장소 JPA 전환, 23일 SQL을 보며 관계·성능 확인으로 연결합니다. 교재11장의 JDBC 방식과 JPA 접근은 비교해 설명합니다.
- 19일은 새 개념 설명 없이 작업지·출발 코드·단계별 확인·오류 힌트로 진행합니다. 23일 주문 최소 예제는 관계·지연 로딩·N+1 공통 실습이며 주문 전체 API 구현과 구분합니다.
- [단축 URL 별도 과제](./assignments/short-url/index.html): 책 요구 분석→메모리 백엔드 직접 구현→AI로 HTML/CSS/JS 프론트 생성·연결→테스트·Git 제출. DB 전환과 주문 전체 API는 선택입니다. 마감은 별도 공지입니다.
- 실습은 책과 참고 코드를 보고 구현하고, 추가 과제는 정답 코드 없이 적용합니다. 필수 완료 지점과 선택 확장을 나눕니다.
- 개인 Public 저장소 `sesac-spring-boot-study`를 계속 사용하며 `greeting-api/`, `product-api/`, `personal-project/`, `short-url/`와 README에 결과를 누적합니다. Issue·PR에 실제 검증 결과를 적고, 기존 프로젝트를 지우거나 중첩 `.git`을 만들지 않습니다.

교재 연결 범위는 [출판사 제공 목차](https://www.yes24.com/product/goods/124434554)를 참고합니다.

진행 참고: [7일 운영 가이드](./2026-11-07/INSTRUCTOR.md) · [9일 운영 가이드](./2026-11-09/INSTRUCTOR.md) · [12일 운영 가이드](./2026-11-12/INSTRUCTOR.md) · [14일](./2026-11-14/INSTRUCTOR.md) · [16일](./2026-11-16/INSTRUCTOR.md) · [19일 대강](./2026-11-19/INSTRUCTOR.md) · [23일](./2026-11-23/INSTRUCTOR.md)

DB 입문: [용어·SQL 안내](./shared/db-basics/) · [상품 표·SQL 예상 작업지](./shared/db-basics/STUDENT-WORKSHEET.md)

실행 검증: [날짜별 예제와 검증 기록](./shared/README.md) · 대강 준비: [19일 진행표](./2026-11-19/HANDOFF.md) · [멘티 작업지](./2026-11-19/STUDENT-WORKSHEET.md)

## GitHub Pages

아래 주소에서 수업 자료를 볼 수 있습니다.

- 자료 목록: https://graygreat.github.io/mentoring-archive/
- 11월 2일 수업: https://graygreat.github.io/mentoring-archive/2026-11-02/
- 11월 5일 수업: https://graygreat.github.io/mentoring-archive/2026-11-05/
- 11월 7일 수업: https://graygreat.github.io/mentoring-archive/2026-11-07/
- 11월 9일 수업: https://graygreat.github.io/mentoring-archive/2026-11-09/
- 11월 12일 수업: https://graygreat.github.io/mentoring-archive/2026-11-12/
- 11월 14일 수업: https://graygreat.github.io/mentoring-archive/2026-11-14/
- 11월 16일 수업: https://graygreat.github.io/mentoring-archive/2026-11-16/
- 11월 19일 수업: https://graygreat.github.io/mentoring-archive/2026-11-19/
- 11월 23일 수업: https://graygreat.github.io/mentoring-archive/2026-11-23/

최초 설정: **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**

HTML을 그대로 게시하며 별도의 빌드나 설치는 필요 없습니다.

## 자료 목록 공개 일정

홈의 자료 목록은 브라우저에서 **한국시간(Asia/Seoul)** 날짜를 확인해 수업일에 자동 공개하며, 이전 자료는 계속 표시합니다. 열린 페이지도 1분마다, 다시 활성화될 때 날짜를 확인합니다.

- `index.html`의 각 자료 `<section>`에서 `data-release-date="2026-11-05"`로 공개일을 지정합니다.
- `data-published="true"`인 자료만 공개합니다. 일시 보류하려면 `"false"`로 바꾸고 배포하며, 다시 `"true"`로 바꾸면 지정일 이후 표시됩니다.
- 자료 카드는 처음에는 `hidden` 상태이며 JavaScript가 날짜를 확인한 뒤 표시합니다. JavaScript를 끄면 목록은 표시되지 않습니다.
- 이 기능은 **홈 목록 노출 제어**입니다. 공개 저장소의 파일과 개별 자료 URL에 대한 직접 접근을 차단하지 않습니다. 브라우저의 시계가 잘못 설정되어 있으면 공개 시점도 달라질 수 있습니다.

검증: `node --test tests/release-schedule.test.cjs`

## 사용법

- 방향키: 슬라이드 이동
- O: 목차
- F: 전체 화면

공개 페이지는 열람 전용입니다. 편집 및 강사 메모 기능은 포함하지 않습니다.
