from pathlib import Path
import json
R = Path(__file__).resolve().parent
meta = json.loads((R / 'metadata-private.json').read_text())
header = """# 2026-11-16 · 단축 URL 서비스 발표 · JPA

## 진행

먼저 ‘나만의 단축 URL 서비스 만들기’ 결과를 발표합니다. 서비스의 사용자와 목적, 구현 기능과 실제 동작, 백엔드 구조와 설계 결정, AI 도움을 받은 부분, 해결한 문제와 남은 작업을 설명합니다. 별도 발표용 PPT나 고정 발표 시간은 요구하지 않습니다.

발표 다음에는 14일에 진행하지 못한 JPA 자료를 그대로 이어갑니다. JPA 부분의 제목·본문·코드·표·그림은 14일 자료와 동일합니다. 날짜와 전체 장표 번호만 오늘 자료에 맞춥니다. 기존 작업지와 참고 코드 파일은 보존하지만 오늘 장표에 새로운 실습·제출 요구를 추가하지 않습니다.

## JPA 설명 흐름

상품 객체와 DB 행 → JDBC·SQL Mapper·ORM 비교 → JPA·Hibernate·Spring Data JPA → Entity·Repository·DB 설정 → 영속성 컨텍스트·1차 캐시·변경 감지 → flush·commit·rollback → 코드 결과 예측과 면접 질문 순서입니다.

코드와 예상 SQL, Entity 내부 상태와 DB 값의 차이를 함께 확인합니다. 전체 프로젝트를 새로 구현하거나 단축 URL 서비스를 JPA로 전환하는 것은 오늘 필수 과제로 추가하지 않습니다.

## 장표별 메모

"""
notes = '\n\n'.join(
    f"### {i + 1}. {d['title'].replace('<br>', ' ')}\n\n{d['note'] or '장표의 코드·표·그림과 결과를 함께 확인합니다.'}"
    for i, d in enumerate(meta)
)
(R.parent / 'INSTRUCTOR.md').write_text(header + notes + '\n')
