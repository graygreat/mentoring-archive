# 멘토링 수업 자료

Spring Boot & AI 과정의 수업 자료를 모아두는 저장소입니다.

## 수업 자료

| 날짜 | 배정 시간 | 주제와 교재 연결 | HTML |
| --- | --- | --- | --- |
| 2026-11-02 | 기존 일정 | OT · Git · GitHub 협업 · Java 팀 실습 | [수업 자료](./2026-11-02/index.html) |
| 2026-11-05 | 4시간 | 교재 1~8장 선행 복습 → Initializr·프로젝트 구조·Gradle → 인사 API 단순 GET | [수업 자료](./2026-11-05/index.html) |
| 2026-11-07 | 핵심 개념 6시간 + MVC 2시간 | 9장 구조·12장 객체/테스트 일부: IoC/DI·빈·자동 설정·AOP·MVC → 상품 객체·Repository·Service·테스트 | [수업 자료](./2026-11-07/index.html) |
| 2026-11-09 | 4시간 | 9장·부록 A, 7~8장 재연결: REST 설계·DTO·JSON·상품 생성/조회·Postman | [수업 자료](./2026-11-09/index.html) |
| 2026-11-12 | REST 실습 2시간 + 서비스 설계 2시간 | 10장 검증·예외·400/404·면접 → 13장 단축 URL 공통 설계, 14장 주문 관리 선택 확장 | [수업 자료](./2026-11-12/index.html) |

다음 일정인 11월 14일은 12일 설계를 바탕으로 CRUD 구현·테스트 6시간, JPA 입문 2시간입니다. 교재 11장 DB 연동은 이후 DB·JPA 진도에 연결하되 JDBC 기반 접근과 JPA를 구분해 설명합니다.

## 진행 기준

- 이론을 먼저 다룬 뒤 실습을 후반에 모읍니다. 시연 없이 요구사항 안내 → 멘티 자율 구현 → 결과 확인·피드백으로 진행합니다.
- 5일은 책을 펴고 1~8장 복습을 먼저 약 60~90분 안에 진행합니다. 1~2장은 역할과 경험을 짧게 회상하고 3장은 객체·생성자·컬렉션·예외, 4~8장은 요청 흐름을 중심으로 질문합니다. 남은 시간에 프로젝트 생성·구조·Gradle과 단순 GET을 구현합니다.
- 복습 연결 질문: 브라우저 요청 → 헤더·본문 → 서버 → 응답 상태·JSON → 화면을 하나의 사례로 설명할 수 있는가? 9장 이후에는 이 요청을 계층 구조와 API로 확장합니다.
- 7일 운영은 핵심 개념 이론 2시간 → MVC 이론 2시간 → 상품 객체·저장소·Service·단위 테스트·AOP 자율 실습 4시간입니다. 필수 완료 기준은 Java 동작·테스트·빈과 AOP 확인이며, REST API 완성을 요구하지 않습니다.
- 9일에는 기존 상품 기능에 HTTP 입구를 추가해 정상 응답을 확인합니다. 12일 앞부분에서 실패 응답을 완성하고, 뒷부분에서 책의 과제 요구사항을 분석해 14일 구현용 설계서와 테스트 시나리오를 작성합니다.
- 단축 URL은 공통 설계 과제입니다. 주문 관리는 추가 선택으로 두고, 교재 해설은 직접 설계한 뒤 비교합니다. 교재 본문은 수업 중 책에서 확인하며 자료에 본문을 전재하지 않습니다.
- JSON 응답 추가 과제는 9일, 입력 검증 추가 과제는 12일로 이동했습니다. 5일에는 인사 API 실습과 문서 Issue·병합 PR 각 2개만 요구합니다.
- 개인 학습 저장소는 `sesac-spring-boot-study`를 계속 사용합니다. `greeting-api/`, `product-api/`와 루트 README·공통 Wiki에 프로젝트별 결과를 누적합니다.

교재 연결 범위는 [출판사 제공 목차](https://www.yes24.com/product/goods/124434554)를 참고합니다.

진행 참고: [7일 운영 가이드](./2026-11-07/INSTRUCTOR.md) · [9일 운영 가이드](./2026-11-09/INSTRUCTOR.md) · [12일 운영 가이드](./2026-11-12/INSTRUCTOR.md)

## GitHub Pages

아래 주소에서 수업 자료를 볼 수 있습니다.

- 자료 목록: https://graygreat.github.io/mentoring-archive/
- 11월 2일 수업: https://graygreat.github.io/mentoring-archive/2026-11-02/
- 11월 5일 수업: https://graygreat.github.io/mentoring-archive/2026-11-05/
- 11월 7일 수업: https://graygreat.github.io/mentoring-archive/2026-11-07/
- 11월 9일 수업: https://graygreat.github.io/mentoring-archive/2026-11-09/
- 11월 12일 수업: https://graygreat.github.io/mentoring-archive/2026-11-12/

최초 설정: **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**

HTML을 그대로 게시하며 별도의 빌드나 설치는 필요 없습니다.

## 사용법

- 방향키: 슬라이드 이동
- O: 목차
- F: 전체 화면

공개 페이지는 열람 전용입니다. 편집 및 강사 메모 기능은 포함하지 않습니다.
