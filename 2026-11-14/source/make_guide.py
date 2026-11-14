from pathlib import Path
import json
R = Path(__file__).resolve().parent
meta = json.loads((R / 'metadata-private.json').read_text())
header = '''# 2026-11-14 · 나만의 단축 URL 서비스 · JPA

## 진행

- 오전 3시간: 교재 CH 13을 참고해 나에게 필요한 단축 URL 서비스의 사용자와 목적을 정하고 기본 기능을 구현합니다.
- 오후 3시간: 같은 프로젝트에 필요한 확장 기능 1~2개를 만들고 AI 프론트를 연결·확인합니다.
- 마지막 1~2시간: 상품 예제로 DB 접근 방식, JPA 매핑과 동작을 설명합니다. 코드와 예상 SQL을 함께 읽고 면접 질문의 답을 설명해 봅니다.

오전·오후 모두 하나의 개인 단축 URL 서비스를 개발합니다. 교재의 단축 URL 예제를 참고하되 자신이 실제로 쓸 목적과 기능을 정합니다. 통계·관리자 화면·사용자 지정 주소·만료·태그 검색은 선택 아이디어이며 모두 필수가 아닙니다. 기존 프로젝트는 보존하고 JPA 전환은 필수로 요구하지 않습니다.

백엔드는 최대한 직접 구현하면서 설계·오류 해결 등에 AI 도움을 받을 수 있습니다. 채택한 코드와 동작은 본인이 설명·확인합니다. 프론트는 AI를 활용해 보기 좋게 만들고 실제 API에 연결합니다. 순수 HTML·CSS·JavaScript만 사용하며 외부 라이브러리·CDN은 제외하고 프롬프트는 자율입니다. 직접 QA 체크리스트를 작성하고 README에 목적·구현 현황·확인 결과·AI 도움 범위를 남깁니다.

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
