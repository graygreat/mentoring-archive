from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
header='''# 2026-11-09 강사용 가이드 · REST API 4시간

## 진행 원칙

7일 `product-api`를 그대로 확장합니다. Java 17, Spring Boot 4.1.2, Gradle 설정과 코어·AOP·기존 테스트를 유지합니다. Initializr 재생성이나 별도 Git 저장소 생성은 하지 않습니다. 책 CH09 관련 절 함께 읽기→핵심 질문→직접 작성→Postman/테스트→책과 비교를 반복합니다. 강사 코딩 시연은 하지 않습니다. 정확한 쪽수와 절은 실제 판본에서 확인합니다. 전체 코드는 실습 참고이며 선택 과제의 정답은 제공하지 않습니다.

## 시간 배분

- 1블록 45분 + 휴식 15분: MVC 복습, 자원·URI·메서드·상태와 입력 위치.
- 2블록 45분 + 휴식 15분: DTO, Jackson 메시지 변환, ResponseEntity, Postman 읽기.
- 3블록 45분 + 휴식 15분: 멘티가 DTO 두 개와 Controller 구현.
- 4블록 45분 + 정리 15분: 정상 요청, 기존 테스트·AOP 확인, 설명·GitHub 제출 안내.

배정 240분 안에서 휴식을 조정하며 선택 과제로 수업 시간을 늘리지 않습니다.

## 교재 연결

CH 09 상품 관리, 부록 A API 요청 도구를 함께 봅니다. CH 07~08의 JSON·HTTP는 재연결하며 1~8장 전체 복습은 5일에서 마칩니다. CH 12의 추상화·단위 테스트는 7일 선행입니다. CH 10 입력 검증·예외 응답은 12일로 이연합니다. CH 11 DB/JDBC 예제와 이후 JPA 방식은 구분합니다. 본문 복제 대신 책의 관련 예제를 읽고 자체 예제와 비교합니다.

## 단계별 코드 계약

7일의 코어 8파일과 `ProductWiringTest.java`를 유지합니다. Wiring 테스트의 `@SpringBootTest(webEnvironment=NONE)`도 유지합니다. 기존 `ProductServiceTest`는 일반 Java 객체 테스트이므로 AOP가 적용되지 않는 것이 정상입니다.

오늘 `source-data`는 당일 추가 3파일만 포함합니다.

1. `CreateProductRequest.java`: name/Integer price, getter/setter, 검증 어노테이션 없음.
2. `ProductResponse.java`: id/name/price를 공개하는 응답 DTO.
3. `ProductController.java`: 생성·목록·단건, 아직 @Valid 없음.

build.gradle의 기존 dependencies에 `implementation 'org.springframework.boot:spring-boot-starter-webmvc'`만 추가합니다. 기존 AspectJ와 테스트를 제거하지 않습니다. 전체 코드 버튼의 파일을 `src/main/java/com/example/product/`에 각각 작성합니다. 매 코드 페이지는 원본을 14줄씩 분할하며 첫 줄 공백도 보존합니다.

## 필수 실행 확인

`product-api/`에서 `./gradlew test`, `./gradlew bootRun`. Windows PowerShell은 `.\\gradlew.bat test` / `.\\gradlew.bat bootRun`. 서버 포트 변경 시 모든 URL에 같은 포트 사용. 재시작하면 메모리 데이터가 사라집니다.

새 서버에서 GET 목록 200 + [], POST 노트 3000으로 201·Location·응답 JSON, 응답의 실제 id 단건 조회 200, 펜 생성 후 id 오름차순 목록, JSON Content-Type, Service AOP 로그를 확인합니다. JSON 속성 순서와 연속 id는 강제하지 않습니다. 0ms 시간 로그도 정상입니다.

9일의 없는 상품은 ProductNotFoundException이 아직 HTTP에 매핑되지 않아 500일 수 있습니다. 404·검증 400·공통 오류 JSON은 12일 완료 기준입니다. 오늘 완성된 오류 계약으로 기록하지 않습니다.

Postman에서 Body/raw/JSON과 Content-Type을 확인합니다. Desktop 앱·Agent 또는 curl로 로컬 서버에 연결합니다. macOS/Linux curl 예제와 Windows JSON 파일 + curl.exe 대안을 구분합니다.

## 별도 과제

이름 부분검색 → 가격 상한·복합조건 순으로 선택 확장합니다. 검색어 strip, 영문 대소문자 구분, 미지정/공백은 전체, id 오름차순, 빈 결과 200+[], 원본 저장 데이터 불변. 가격은 0과 상한값 포함 경계를 검사합니다. 음수/문자 가격 400은 12일 이후 범위입니다. 정답 코드는 제공하지 않습니다. 수정·삭제는 14일 CRUD 구현과 연결합니다. 현재 비교 슬라이드에 Map.of 표현을 직접 제공하며 DTO와 비교합니다. 두 프로젝트 수정은 강제하지 않습니다.

## GitHub 제출

`sesac-spring-boot-study`의 Public/main, Issues/Wiki 설정을 유지합니다. 필수 Issue 1개와 병합 PR 1개:

- branch: `practice/product-rest`
- title: `[실습] 상품 생성·조회 REST API`
- labels: `practice`, `docs`; assignee 본인
- milestone: `product-api-2026-11-09`, 마감 미지정

최신 main → Issue → branch → 코드/테스트/문서 → commit/push → PR(base main) → 자체 확인/병합 → 다음 main pull. 관련 Issue는 실제 번호로 Closes 연결. 선택 과제는 feature/name-search 및 feature/price-filter에 각각 Issue/PR을 추가합니다.

product-api/README.md 여섯 항목은 소개, 실제 개발 환경, 실행·테스트, 구현 현황, API, Wiki 링크입니다. 루트 README 목차·greeting-api를 보존합니다. Wiki Home/01-Setup/02-Architecture/03-API/04-Verification/05-Retrospective에 프로젝트별로 누적합니다. 코드 PR에 Wiki가 자동 포함되지 않으므로 별도 편집하고 링크/완료 확인을 PR에 남깁니다. 별도 docs PR은 요구하지 않습니다.

Wrapper jar 포함: 루트 .gitignore의 `!product-api/gradle/wrapper/gradle-wrapper.jar` 및 기존 greeting-api 예외 보존. build/.gradle/IDE파일/.env·비밀값 제외. 저장소 URL, Wiki Home URL, 필수 PR1개와 선택 수행 여부 제출.

## 다음 시간

12일 앞2시간 CH10 검증/예외 및 HTTP·REST 면접 연결. 뒤2시간 CH13 단축 URL 공통 설계, CH14 주문관리 선택. 14일 직접 구현6시간과 JPA2시간으로 이어집니다.

## 실행 리허설 근거 · 2026-10-26

Java 17 / Spring Boot 4.1.2에서 실제 단계별 증분 구성을 실행 검증했습니다. 7일(core+AspectJ) → 9일(+Web MVC) → 12일(+Validation) 순서로 clean build 및 JUnit 테스트 5개가 각 단계에서 통과했습니다. 오늘 단계는 정상 HTTP 7개 확인과 AOP 로그를 확인했습니다. 검증 환경의 결과이며 멘티는 자기 환경에서도 다시 실행하고 실제 결과를 기록합니다. 루트 통합 리허설 기록을 참조합니다.

## 슬라이드별 강사 메모

'''
notes='\n\n'.join(f"### {i+1}. {d['title'].replace('<br>',' ')}\n\n{d['note'] or '슬라이드의 질문과 완료 기준을 확인하고 멘티가 자신의 코드·결과로 설명하게 합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(header+notes+'\n')
print('Created INSTRUCTOR.md')
