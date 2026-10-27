# 멘토링 수업 자료

Spring Boot & AI 과정의 수업 자료를 모아두는 저장소입니다.

## 수업 자료

| 날짜 | 배정 시간 | 주제와 교재 연결 | HTML |
| --- | --- | --- | --- |
| 2026-11-02 | 기존 일정 | OT · Git · GitHub 협업 · Java 팀 실습 | [수업 자료](./2026-11-02/index.html) |
| 2026-11-05 | 4시간 | 교재 1~8장 선행 복습 → Initializr·프로젝트 구조·Gradle → 인사 API 단순 GET | [수업 자료](./2026-11-05/index.html) |
| 2026-11-07 | 핵심 개념 6시간 + MVC 2시간 | 9장 구조·12장 객체/테스트 일부: IoC/DI·빈·자동 설정·AOP·MVC → 상품 객체·Repository·Service·테스트 | [수업 자료](./2026-11-07/index.html) |
| 2026-11-09 | 4시간 | 9장·부록 A, 7~8장 재연결: REST 설계·DTO·JSON·상품 생성/조회·Postman | [수업 자료](./2026-11-09/index.html) |
| 2026-11-12 | REST 실습 2시간 + 서비스 설계 2시간 | 10장 검증·예외·400/404·면접 → 상품 남은 CRUD 요구·계층·API·테스트 설계 | [수업 자료](./2026-11-12/index.html) |
| 2026-11-14 | 상품 CRUD 6시간 + JPA 입문 2시간 | 책 상품 관리의 남은 CRUD 직접 개발·테스트 → ORM·Entity 매핑 활동 | [수업 자료](./2026-11-14/index.html) |
| 2026-11-16 | 4시간 | 상품 관리 기반 Entity·Repository·트랜잭션·쿼리 메서드·JPQL·연관관계 | [수업 자료](./2026-11-16/index.html) |
| 2026-11-19 | 4시간 · 이준형 강사 대강 | 작업지에 따라 상품 저장소 JPA 전환·API 회귀·DB 보존 검증 | [수업 자료](./2026-11-19/index.html) |
| 2026-11-23 | 4시간 | 전환 피드백·영속성 컨텍스트·지연 로딩·주문 최소 예제 N+1 재현/개선 | [수업 자료](./2026-11-23/index.html) |

## 진행 기준

- 수업의 중심은 책의 상품 관리 애플리케이션입니다. 책 함께 읽기 → 핵심 질문 → 멘티 직접 구현 → 테스트 → 책과 비교를 반복합니다. 강사 코딩 시연은 하지 않습니다.
- 책의 관련 절을 실제 판본에서 확인합니다. 확인되지 않은 쪽수나 세부 규칙을 책의 요구사항으로 적지 않습니다. 수업 보충 예제(예: Map 저장소)와 교재 원본의 차이를 구분합니다.
- 5일에는 책1~8장 복습을 약60~90분 먼저 진행하고 Initializr·프로젝트 구조·Gradle·단순 GET을 구현합니다.
- 7일 토요일8시간은 설명·책 읽기·활동 약2시간 / 자율 실습5시간 / 피드백1시간의 운영 블록입니다. 짧은 설명과 직접 구현을 번갈아 진행하며 Controller/HTTP 구현은9일 이후입니다.
- 14일 토요일8시간은 설명·활동1.5시간 / 자율 실습5.5시간 / 결과 확인1시간의 운영 블록입니다. 앞6시간 상품 CRUD·테스트, 뒤2시간 JPA 입문·Entity 매핑 활동으로 구분합니다. 주말은 매시간 활동45분+휴식15분, 점심 별도입니다.
- 12일 뒤2시간은 상품 CRUD 설계, 14일 구현, 16일 JPA 기초, 19일 상품 저장소 JPA 전환, 23일 회귀·심화 확인으로 연결합니다. 교재11장의 JDBC 방식과 JPA 접근은 비교해 설명합니다.
- 19일은 새 개념 설명 없이 작업지·출발 코드·단계별 확인·오류 힌트로 진행합니다. 23일 주문 최소 예제는 관계·지연 로딩·N+1 공통 실습이며 주문 전체 API 구현과 구분합니다.
- [단축 URL 별도 과제](./assignments/short-url/index.html): 책 요구 분석→메모리 백엔드 직접 구현→AI로 HTML/CSS/JS 프론트 생성·연결→테스트·Git 제출. DB 전환과 주문 전체 API는 선택입니다. 마감은 별도 공지입니다.
- 실습은 책과 참고 코드를 보고 구현하고, 추가 과제는 정답 코드 없이 적용합니다. 필수 완료 지점과 선택 확장을 나눕니다.
- 개인 Public 저장소 sesac-spring-boot-study를 계속 사용하며 greeting-api/product-api/short-url, 루트README, 공통Wiki6페이지에 결과를 누적합니다. 기존 프로젝트를 지우지 않고 중첩.git은 만들지 않습니다.

교재 연결 범위는 [출판사 제공 목차](https://www.yes24.com/product/goods/124434554)를 참고합니다.

진행 참고: [7일 운영 가이드](./2026-11-07/INSTRUCTOR.md) · [9일 운영 가이드](./2026-11-09/INSTRUCTOR.md) · [12일 운영 가이드](./2026-11-12/INSTRUCTOR.md) · [14일](./2026-11-14/INSTRUCTOR.md) · [16일](./2026-11-16/INSTRUCTOR.md) · [19일 대강](./2026-11-19/INSTRUCTOR.md) · [23일](./2026-11-23/INSTRUCTOR.md)

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

## 사용법

- 방향키: 슬라이드 이동
- O: 목차
- F: 전체 화면

공개 페이지는 열람 전용입니다. 편집 및 강사 메모 기능은 포함하지 않습니다.
