from pathlib import Path
import json
R = Path(__file__).resolve().parent
meta = json.loads((R / 'metadata-private.json').read_text())
header = """# 2026-11-16 · 단축 URL 서비스 발표 · JPA

## 진행

먼저 ‘나만의 단축 URL 서비스 만들기’ 결과를 발표합니다. 서비스의 사용자와 목적, 구현 기능과 실제 동작, 백엔드 구조와 설계 결정, AI 도움을 받은 부분, 해결한 문제와 남은 작업을 설명합니다. 별도 발표용 PPT나 고정 발표 시간은 요구하지 않습니다.

발표 다음에는 14일에 진행하지 못한 JPA 자료를 이어갑니다. JPA·Hibernate·Spring Data JPA의 역할 설명을 구체화하고, 각 역할의 상품 조회 예제와 다른 JPA 구현체의 관계를 추가합니다. 학습 순서 그림, Entity와 표의 대응, 첫 저장·조회 예제, 영속성 컨텍스트와 DB의 차이를 보충합니다. 변경 감지 원리와 트랜잭션 기본 의미를 설명한 뒤 가격 수정 코드를 읽습니다. Repository 어댑터·persist와 merge·고급 트랜잭션 주의사항은 본문 정리 뒤 보충으로 모읍니다. 기존 작업지와 참고 코드 파일은 보존하지만 오늘 장표에 새로운 실습·제출 요구를 추가하지 않습니다.

## JPA 설명 흐름

학습 순서와 네 가지 질문 → 상품 객체와 DB 행 → JDBC·SQL Mapper·ORM 비교 → JPA·Hibernate·Spring Data JPA → Entity·표의 대응 → Repository·DB 설정과 첫 저장·조회 → 영속성 컨텍스트와 DB의 차이·1차 캐시·변경 감지 → 트랜잭션 기본과 가격 수정 코드 → flush·commit·rollback → 코드 결과 예측과 면접 질문 → 정리 → 보충 자료 순서입니다.

코드와 예상 SQL, Entity 내부 상태와 DB 값의 차이를 함께 확인합니다. 전체 프로젝트를 새로 구현하거나 단축 URL 서비스를 JPA로 전환하는 것은 오늘 필수 과제로 추가하지 않습니다.

## 오늘의 핵심과 보충

오늘은 역할 구분, 객체와 표의 매핑, 저장·조회·변경과 실제 SQL, 관리 상태와 트랜잭션 경계를 연결해 설명할 수 있으면 됩니다. 같은 키보드 상품을 예제로 사용하며 조회 당시 값·현재 객체 값·DB 값을 구분합니다. 저장 반환값의 실제 ID를 사용하고, save 호출과 commit을 동일하게 설명하지 않습니다.

본문 정리 뒤에 모은 보충 자료는 기존 Repository 연결, persist·merge 상세, 트랜잭션의 체크 예외·자기 호출·readOnly 주의사항입니다. 질문과 남은 시간에 따라 읽습니다. 이 내용을 모두 암기하는 것을 오늘의 완료 기준으로 삼지 않습니다. 관계·지연 로딩·N+1의 구현은 후속 수업에서 다룹니다.

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
