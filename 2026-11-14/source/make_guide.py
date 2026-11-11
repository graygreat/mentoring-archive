from pathlib import Path
import json
R = Path(__file__).resolve().parent
meta = json.loads((R / 'metadata-private.json').read_text())
header = '''# 2026-11-14 · 단축 URL · 주문 관리 API · JPA

## 진행

- 오전 3시간: 교재 CH 13 단축 URL 과제 테스트. 문제를 함께 확인하고 풀이 코드를 최대한 보지 않고 개인별로 구현합니다.
- 오후 3시간: 교재 CH 14 주문 관리 API 서버 과제 테스트. 책과 시작 코드를 사용합니다.
- 마지막 1~2시간: 상품 예제로 DB 접근 방식, JPA 매핑과 동작을 설명합니다. 코드와 예상 SQL을 함께 읽고 면접 질문의 답을 설명해 봅니다.

과제 장표는 각 장의 메인 페이지만 둡니다. 세부 문제 설명은 교재로 진행하며 기존 과제 안내와 학생 프로젝트는 유지합니다. 두 과제의 JPA 전환은 필수가 아닙니다.

## JPA 설명 흐름

JDBC → SQL Mapper와 ORM 비교 → JPA·Hibernate·Spring Data JPA 구분 → Entity·Repository·DB 설정 → 트랜잭션 안의 조회·변경 → 영속성 컨텍스트·1차 캐시·변경 감지 → flush·commit·rollback → save와 Entity 상태 → 면접 질문으로 확인 순서입니다.

자료의 짧은 코드는 개념 설명을 위한 발췌입니다. SQL은 예상 형태이며 DB·Hibernate 설정에 따라 달라질 수 있습니다. 기존 JDBC 연결을 지우거나 과제 전체를 JPA로 바꾸게 하지 않습니다. 실제 프로젝트 적용과 테스트는 16일에 이어갑니다. 관계·지연 로딩·N+1은 후속 수업과 연결하는 예고 수준으로 다룹니다.

## 보충 장표 사용

MyBatis와 JPA의 같은 가격 변경 예제를 비교합니다. 기존 Repository와 Spring Data Repository 사이의 역할을 구분하고, 영속성 컨텍스트 안의 현재 객체·조회 당시 상태와 DB 행을 함께 확인합니다. 수정·flush·commit·rollback의 각 시점에서 Java 값과 DB 값을 예상합니다. 마지막 코드 결과 예측 문제는 먼저 이유를 설명하게 한 뒤 해설을 확인합니다. Entity와 요청·응답 DTO의 역할도 구분합니다.

## 장표별 메모

'''
notes = '\n\n'.join(
    f"### {i + 1}. {d['title'].replace('<br>', ' ')}\n\n{d['note'] or '장표의 코드·표·그림과 결과를 함께 확인합니다.'}"
    for i, d in enumerate(meta)
)
(R.parent / 'INSTRUCTOR.md').write_text(header + notes + '\n')
