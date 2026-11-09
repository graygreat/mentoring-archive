from pathlib import Path
import json
R=Path(__file__).resolve().parent
meta=json.loads((R/'metadata-private.json').read_text())
HEADER='''# 2026-11-14 · 상품 CRUD · 개인 REST 프로젝트 · DB 기초

## 진행 내용

- CH 09·10·12의 상품 수정·삭제, 검증·예외, 테스트를 교재로 설명합니다.
- 12일 DB에 연결한 공통 `product-api/`의 미완료 수정·삭제를 보완하고 기존 테스트를 확인합니다.
- 개인 `personal-project/`의 DB 저장을 유지하며 위시리스트 REST CRUD와 미완료 기능을 보완합니다.
- 결과를 발표하고 다른 교육생과 코드·테스트를 확인합니다.
- 12일 CH 11의 DB 연결과 SQL을 복습하고 JPA 보충 자료와 비교합니다.

개인 구현 및 준비는 150분입니다. 발표용 PPT는 요구하지 않으며 코드·테스트·실제 요청 결과를 보여줍니다. 미완료자는 완성한 범위와 막힌 지점, 다음 작업을 설명합니다.

## 공통 프로젝트

9·12일의 `product-api/`와 DB 저장을 유지합니다. 12일 README에 적은 완료·미완료 범위를 출발점으로 삼습니다. 마지막의 Memory 참고 코드는 구조 비교용이며 자신의 JDBC DB 구현을 덮어쓰지 않습니다. PUT은 유효한 수정 200과 기존 id 유지, DELETE는 성공 204와 본문 없음을 확인합니다. 없는 id는 404, 잘못된 입력은 400입니다. 실패 후 원본 값이 보존되는지 확인합니다. 기존 ProductServiceTest·ProductWiringTest와 생성·조회 API는 보존하고 ProductCrudTest를 추가합니다. 공통 프로젝트는 19일 JPA 전환에서 계속 사용합니다.

## 개인 과제 · 위시리스트와 예산 추천

7·9일에 만든 `CollectionItem(id, name, price)`와 Service, 12일에 연결한 DB Repository를 이어 사용합니다. DB 연결 미완료자는 저장·조회부터 보완하며 메모리 저장소로 되돌리지 않습니다. 외부 상품 메타데이터·이름과 가격의 읽기 전용 규칙·장바구니 복사본을 보존합니다. 책·게임·장비처럼 본인이 선택한 주제를 유지합니다. 이름은 앞뒤 공백을 제거하고 누락·빈 이름·공백뿐인 이름은 거부합니다. 가격은 정수 0 이상이며 0원을 허용합니다. 프로그램이 부여한 실제 id로 단건을 조회하고 없는 id는 찾을 수 없는 상황으로 구분합니다.

기존 예산 추천은 각 후보의 개별 가격이 예산 이하인 항목을 가격 오름차순, 같은 가격이면 등록 순으로 최대 3개 반환합니다. 결과가 없으면 빈 목록, 예산 0이면 무료 항목을 포함하고 음수 예산은 거부합니다. 조회 후 저장 데이터가 바뀌지 않아야 합니다.

개인 API는 다음 기준을 적용합니다.

| 요청 | 결과 |
| --- | --- |
| POST /items | 201, id·name·price 응답, Location |
| GET /items | 200, 목록, 비어 있으면 [] |
| GET /items/{id} | 200, 실제 생성 id의 항목 / 없는 id 404 |
| PUT /items/{id} | 200, 변경된 같은 id / 입력 400·없는 id 404 |
| DELETE /items/{id} | 204, 본문 없음 / 없는 id 404 |

요청은 name·price를 사용합니다. 가격 누락·null·음수와 빈 이름은 400입니다. 없는 id와 잘못된 입력은 따로 확인합니다. 실패한 등록·수정 뒤 저장 값이 보존되는지 테스트합니다. 7일 코어 테스트 최소 4개를 유지하고 수정·삭제·실패 보존 사례를 추가합니다. 미완료 교육생은 등록·조회 한 경로부터 복구하고 실제 진행 상황을 발표할 수 있습니다. 12일 위시리스트 DB 연동과 재시작 보존은 유지합니다. JPA·프론트는 개인 기본 과제의 필수가 아닙니다. 수동 등록 항목의 수정 계약과 외부 상품의 이름·가격 읽기 전용 규칙을 구분합니다.

## 이론 적용과 추가 과제

Domain의 규칙, Controller 입력·응답과 Service 업무의 구분, Repository 인터페이스·DB 구현, 생성자 주입, 독립적인 단위 테스트와 Spring 연결 확인을 코드에서 찾습니다. 다른 교육생과 정상·실패 결과를 확인합니다. 추가 AOP를 구현했다면 업무 코드와 공통 로그가 분리되고 주입된 객체 호출에 적용되는지도 봅니다.

완료한 교육생은 이름 검색·즐겨찾기·구매 완료 상태를 추가할 수 있습니다. 기존 추천을 HTTP로 제공하려면 `GET /items/recommendations?budget=5000` 같은 경로를 추가하고 정상 200·음수 예산 400을 확인합니다. 이는 선택 구현입니다.

AI 프론트는 순수 HTML·CSS·JavaScript로 목록·등록·예산 입력·추천 결과를 만듭니다. 외부 라이브러리·CDN은 사용하지 않고 프롬프트는 자율입니다. 실제 API를 fetch로 호출하여 정상·실패 응답과 화면 반영을 확인합니다. 샘플 데이터만 사용하는 화면은 실제 연동과 구분해 표시합니다. 백엔드 핵심 로직은 직접 작성합니다.

## DB 기초와 JPA 보충

12일 DB 연결 결과와 SQL을 복습하며 기존 CRUD 학습과 DB/JPA 입문의 내용 배정을 유지합니다. CH 11은 JDBC 기반 접근이고 JPA는 이를 바탕으로 한 수업 보충입니다. `shared/db-basics/`와 작업지에서 DB·DBMS·H2, 행·열·PK·NULL, SELECT·WHERE·ORDER BY, UPDATE·DELETE, COMMIT·ROLLBACK을 읽고 예상 결과를 적습니다. HTTP 400만으로 DB 롤백이 보장되지 않고 이미 COMMIT한 변경을 나중 ROLLBACK으로 되돌릴 수 없음을 확인합니다.

`@Entity`는 표와 연결할 클래스, `@Id`는 기본 키 필드입니다. Product 도메인과 Entity를 구분하고 `product-api/docs/jpa-mapping.md`에 상품 표·예상 SQL·객체 필드의 대응을 적습니다. 실행 가능한 Entity·Repository는 16일에, 공통 API의 JPA 전환은 19일에 이어갑니다.

## 제출

기존 개인 Fork의 `sesac-spring-boot-study`를 사용하고 브랜치 이름은 각자 정합니다. 개인 origin에 Push하고 공용 저장소에 Issue·PR을 제출합니다. 원본 main을 base, 개인 Fork 작업 브랜치를 head로 선택하며 공통 실습과 개인 적용의 변경 범위·실제 테스트 결과·관련 Issue #번호를 적습니다. 리뷰 수정은 같은 브랜치에 Push하고 강사가 확인 후 병합 없이 PR·Issue를 닫습니다. 각 README에 환경·실행 방법·완료 기능·실제 결과를 기록합니다. 루트 README의 다른 프로젝트 링크와 기존 greeting-api는 보존합니다. src·Gradle 설정·Wrapper·gradle-wrapper.jar를 포함하고 build/.gradle/IDE/.env/비밀값은 제외합니다.

## 슬라이드별 진행 메모

'''
notes='\n\n'.join(f"### {i+1}. {d['title'].replace('<br>', ' ')}\n\n{d['note'] or '교재와 PPT에 적힌 작업을 확인하고 실제 완료 결과를 설명합니다.'}" for i,d in enumerate(meta))
(R.parent/'INSTRUCTOR.md').write_text(HEADER+notes+'\n')
