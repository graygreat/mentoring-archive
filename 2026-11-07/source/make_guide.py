from pathlib import Path
import json
R=Path(__file__).resolve().parent
OUT=R.parent
s=json.loads((R/'metadata-private.json').read_text())
text="""# 2026-11-07 토요일 · 객체 연결과 MVC 진행 참고

## 운영 기준

공식 배정은 핵심 개념 6시간과 MVC 2시간, 총 8시간입니다. 1교시는 수업 45분과 휴식 15분이며 점심은 별도입니다. 교재 1~8장 복습은 5일 앞부분에 먼저 끝내고, 오늘은 필요한 Java와 요청 흐름만 짧게 다시 연결합니다.

책 함께 읽기 → 핵심 질문 → 멘티 구현 → 테스트 → 책과 비교를 반복합니다. 강사 코딩 시연은 하지 않습니다. 파일 전체 코드는 실습 해설·비교용이며 추가 과제의 정답은 제공하지 않습니다. 교재 본문과 수업 보충 코드(예: Map 저장소)의 차이를 확인합니다.

## 교시별 운영

| 시간 | 활동과 실습 | 확인 |
| --- | --- | --- |
| 1 | 책 상품 객체·DI 부분 읽기, 짧은 질문·객체 연결 활동 | 필요한 객체와 역할 설명 |
| 2 | 프로젝트 생성, Product 규칙 직접 구현 | 정상·잘못된 값 비교 |
| 3 | Repository·메모리 저장소 작성 | 저장·조회 결과 |
| 4 | Service·단위 테스트 작성 | 정상·실패 테스트 |
| 5 | 스타터·자동 설정·AOP 짧은 읽기 후 구현 | 프록시·시간 로그 |
| 6 | MVC 책 읽기·요청 흐름 그리기, 계층 책임 점검 | MVC 구조 활동 |
| 7 | 미완성 코드·테스트·구조 활동 보완 | 필수 완료 지점 확인 |
| 8 | 결과 확인·피드백·학습 기록 | 테스트·로그·책과 차이 설명 |

설명·책 읽기·활동 약2시간 / 자율 구현·테스트 약5시간 / 피드백 약1시간의 운영 블록입니다. 각 블록은 활동45분+휴식15분, 점심 별도입니다. 핵심6시간/MVC2시간은 다루는 내용의 배정이며, 설명만 4시간 이어가지 않습니다. MVC는 짧은 읽기뿐 아니라 요청 흐름·계층 분류·완성 코드 책임 점검 활동을 합해 다룹니다. 앞 실습이 막히면 필수 완료 지점을 먼저 완성하고 선택 확장은 뒤로 미룹니다.

## 교재 연결과 진도 경계

- 5일: 교재 1~8장 복습을 먼저 끝내고 Initializr와 간단한 GET을 경험합니다.
- 오늘 9장 일부: 상품 객체·컬렉션·저장과 조회입니다. 교재의 List와 수업 예제의 Map을 비교합니다. 수업 예제는 교재 본문을 재현한 코드가 아닙니다.
- 오늘 12장 일부 선행: 인터페이스·생성자 DI·단위 테스트를 연결합니다. 실제 Memory 구현은 mock이 아닙니다.
- 9일 4시간: 같은 product-api에 Web 의존성·DTO·Controller·JSON/Jackson·정상 요청과 REST 설계를 추가합니다.
- 12일 앞 2시간: 10장과 Validation·오류 응답·실패 사례·면접 포인트를 연결합니다.
- 12일 뒤 2시간: 상품 관리의 남은 CRUD 요구사항·계층·API·테스트를 설계합니다. 단축 URL은 별도 과제로 설계→백엔드→AI 프론트 연결을 진행합니다.
- 14일: 설계한 CRUD 구현·테스트 6시간, JPA 소개 2시간입니다. 교재 11장 DB는 이후 DB/JPA 진도와 연결합니다.

오늘의 MVC는 구조 이해 범위입니다. Controller 작성, Postman, 요청·응답 DTO, 요청 검증 어노테이션과 HTTP 상태 검증은 후속 수업에서 진행합니다. HTML 뷰와 응답 본문은 개념 차이를 구분합니다.

## 작성 파일과 의존성

공통 환경은 Java 17, Spring Boot 4.1.2, Gradle-Groovy, Group com.example, Artifact product, Package com.example.product입니다. Initializr의 선택 의존성은 비워 두고, 기본 starter와 생성된 테스트 의존성·런처·useJUnitPlatform을 유지합니다. AOP 단계에서 spring-boot-starter-aspectj를 추가합니다. Web과 Validation은 각각 9일과 12일에 추가합니다.

메인 소스는 ProductApplication, Product, ProductRepository, MemoryProductRepository, ProductNotFoundException, ProductService, TimingAspect의 7개입니다. 테스트는 ProductServiceTest와 ProductWiringTest입니다. 생성된 ProductApplicationTests도 보존합니다. 전체 소스는 14줄 이하 청크로 나누며 원본 공백을 유지합니다.

ProductServiceTest는 new로 직접 조립하는 단위 테스트 3개입니다. ProductWiringTest는 제공 틀입니다. @Autowired로 Service를 받고 AopUtils.isAopProxy를 확인한 뒤 상품 생성·단건·목록 조회를 검증합니다. @SpringBootTest(webEnvironment=NONE)을 사용하므로 웹 서버 없이 빈 연결과 AOP를 확인하며 이후 Web 의존성이 추가돼도 재사용할 수 있습니다. 실행용 CommandLineRunner나 seed는 추가하지 않습니다.

제공 테스트 4개와 생성된 contextLoads를 보존했다면 총 5개입니다. 기본 starter만 있는 main은 웹 서버를 열지 않고 정상 종료할 수 있습니다. 포트 접속 대신 테스트로 성공을 확인합니다. 0ms 로그도 정상이며, 출력이 숨겨지면 IDE 테스트 콘솔이나 Gradle --info에서 확인합니다.

## 실습과 추가 과제

실습 완료 기준은 생성·목록·단건 조회, 잘못된 이름·가격의 Java 예외, 없는 id의 ProductNotFoundException, 단위 테스트 3개와 주입·AOP 테스트 1개입니다. 없는 상품을 HTTP 404로 응답하는 것은 12일 범위입니다.

과제 1은 가격 0, 이름 공백 정리, null·공백 이름, 실패 후 상태 보존을 테스트하는 기초 과제입니다. 과제 2는 Service.findByMaxPrice(int)의 조건 조회와 경계값 테스트입니다. 상한 0·같은 가격·결과 없음·음수·저장 원본 보존을 확인합니다. 정답 코드를 제공하지 않으며 HTTP 구현은 요구하지 않습니다. 실패 후 id 번호 연속성을 완료 조건으로 두지 않습니다.

추가 과제는 수업 후 별도 수행할 수 있으며 마감은 별도 안내합니다. HTTP 이름 검색·가격 필터·수정·삭제는 후속 REST/CRUD 진도에 연결합니다.

## GitHub 제출

Public 저장소 sesac-spring-boot-study의 main에 greeting-api와 product-api를 누적합니다. 상세 clone·Initializr 복사 절차는 자료에 추가하지 않았습니다. 날짜마다 새 저장소를 만들지 않습니다. Wrapper를 포함하고 build/.gradle/.idea와 비밀값을 제외합니다. 루트 .gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar와 기존 greeting-api 예외를 보존합니다.

필수 Issue·병합 PR은 2개입니다.

- practice/product-core: [실습] 상품 객체·저장소·Service와 테스트
- docs/product-core: [문서] 상품 객체 구조와 테스트 기록

추가 과제는 test/product-boundaries, feature/core-price-filter에서 각각 작업합니다. 수행 과제마다 Issue·병합 PR을 1개씩 추가합니다. 완료 실습을 나중에 기록하면 Issue에 결과 정리임을 명시합니다. 최신 main → Issue·브랜치 → 구현·검증 → PR → 자체 확인·병합 → main pull 순서입니다. 타인 승인은 강제하지 않습니다. Closes에는 실제 Issue 번호를 씁니다. Milestone은 product-core-2026-11-07이며 마감일은 별도 안내 전 미지정입니다.

루트 README는 목차와 기존 프로젝트 링크를 보존합니다. product-api/README는 소개·환경·실행/테스트·구현 현황·객체 기능(API는 9일 예정)·Wiki 링크의 여섯 항목입니다. Wiki는 Home, 01-Setup, 02-Architecture, 03-API, 04-Verification, 05-Retrospective를 재사용하고 프로젝트별 내용을 누적합니다. 03-API에는 오늘 미구현·9일 예정, 04-Verification에는 단위·연결 테스트·AOP 로그·과제 근거를 기록합니다. Wiki는 코드 PR과 별도이므로 문서 PR에 실제 링크와 작성 확인을 남깁니다.

## 검증 범위와 리허설

source/verify.py는 오늘의 소스 9개만 게시되는지, 미래 REST 답안 제외, 목차 순서, 고유 ID, 14줄 소스 청크 공백 완전 일치, Java 코어 실행과 JS 구문을 확인합니다. 별도 리허설에서는 Java 17·Spring Boot 4.1.2에서 기본 starter와 AspectJ만 사용하고 Web·Validation 없이 clean build를 실행해 통과했습니다. 제공 테스트 4개와 Initializr의 contextLoads를 포함한 총 5개 테스트가 통과했습니다. 주입된 Service의 AOP 프록시와 실제 시간 로그도 확인했습니다. 이전 판의 브라우저 점검과 이번 순서 변경은 구분합니다. 최종판의 브라우저 검증은 별도 검수 기록을 따릅니다.

위 결과는 개정된 7일 단계만 따로 실행한 근거입니다. 이전의 전체 상품 API 12파일 리허설에서 확인한 HTTP 성공과 구분합니다. Windows·멘티별 환경과 추가 과제 학생 답안은 별도 확인이 필요합니다.

## 슬라이드별 진행 참고

"""
for i,d in enumerate(s):
 if d['note']:text+=f"### {i+1:02}. {d['title']}\n\n{d['note']}\n\n"
(OUT/'INSTRUCTOR.md').write_text(text)
print('Instructor guide generated')
