from pathlib import Path
import json
R = Path(__file__).resolve().parent
meta = json.loads((R / 'metadata-private.json').read_text())
header = """# 2026-11-16 · 단축 URL 서비스 발표 · JPA

## 진행

먼저 ‘나만의 단축 URL 서비스 만들기’ 결과를 발표합니다. 서비스의 사용자와 목적, 구현 기능과 실제 동작, 백엔드 구조와 설계 결정, AI 도움을 받은 부분, 해결한 문제와 남은 작업을 설명합니다. 별도 발표용 PPT나 고정 발표 시간은 요구하지 않습니다.

발표 다음에는 14일에 진행하지 못한 JPA 자료를 이어갑니다. JPA·Hibernate·Spring Data JPA의 역할 설명을 구체화하고, 각 역할의 상품 조회 예제와 다른 JPA 구현체의 관계를 추가합니다. 그 밖의 기존 JPA 설명은 유지합니다. 기존 작업지와 참고 코드 파일은 보존하지만 오늘 장표에 새로운 실습·제출 요구를 추가하지 않습니다.

## JPA 설명 흐름

상품 객체와 DB 행 → JDBC·SQL Mapper·ORM 비교 → JPA·Hibernate·Spring Data JPA → Entity·Repository·DB 설정 → 영속성 컨텍스트·1차 캐시·변경 감지 → flush·commit·rollback → 코드 결과 예측과 면접 질문 순서입니다.

코드와 예상 SQL, Entity 내부 상태와 DB 값의 차이를 함께 확인합니다. 전체 프로젝트를 새로 구현하거나 단축 URL 서비스를 JPA로 전환하는 것은 오늘 필수 과제로 추가하지 않습니다.

## 세 가지 역할 설명

JPA는 객체 저장·조회·관리의 표준과 API이며, EntityManager 등의 실제 구현은 Hibernate 같은 JPA 구현체가 제공합니다. Spring Data JPA는 이를 이용하는 Repository의 반복 구현을 줄입니다. ProductEntity의 같은 ID 조회로 각 역할을 연결하고 EntityManager와 Hibernate를 별도 서비스 두 개처럼 설명하지 않습니다.

EclipseLink와 Apache OpenJPA도 JPA 구현체입니다. 표준 API를 사용하면 교체 영향을 줄일 수 있지만 설정·지원 표준 버전·생성 SQL·구현체 전용 기능을 확인하고 테스트해야 합니다. 이 수업에서는 Hibernate를 사용하며 다른 구현체 설치를 실습 과제로 추가하지 않습니다.

## 장표별 메모

"""
notes = '\n\n'.join(
    f"### {i + 1}. {d['title'].replace('<br>', ' ')}\n\n{d['note'] or '장표의 코드·표·그림과 결과를 함께 확인합니다.'}"
    for i, d in enumerate(meta)
)
(R.parent / 'INSTRUCTOR.md').write_text(header + notes + '\n')
