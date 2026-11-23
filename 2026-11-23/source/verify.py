"""Verify a progressive, diagram-led Nov 23 lecture and its existing assignment."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
from lxml import html

R = Path(__file__).resolve().parent
OUT = R.parent
raw = (OUT / 'index.html').read_text()
doc = html.fromstring(raw)
slides = doc.xpath('//section[contains(concat(" ", normalize-space(@class), " "), " slide ")]')
meta = json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
private = json.loads((R / 'metadata-private.json').read_text())
sources = json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
assert len(slides) == len(meta) == len(private) == 45
assert sources == {}
assert not doc.xpath('//section//pre | //section//code | //section//*[@data-source-key]')
assert not doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " subtitle ")]')
assert [s.get('data-index') for s in slides] == list(map(str, range(len(slides))))
assert len(set(doc.xpath('//section/@data-slide-id'))) == len(slides)
ids = doc.xpath('//@id')
assert len(ids) == len(set(ids))
for i, (slide, record) in enumerate(zip(slides, meta)):
    assert slide.xpath('./h1')[0].text_content() == re.sub('<[^>]*>', '', record['title'])
    assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
    assert slide.xpath('./footer/span')[0].text_content() == '2026.11.23'
    assert 'note' not in record

titles = [m['title'] for m in meta]
sequence = [
    '객체의 가격과 DB 가격은 별개',
    '가격 변경만 저장되고 이력이 실패한다면?',
    'DB 작업을 하나의 성공·실패 단위로 묶기',
    '함께 성공해야 할 범위를 Service에서 정하기',
    '프록시가 Service 호출 앞뒤를 처리합니다',
    '관리 중인 상품의 변경을 감지하기',
    'flush는 SQL 전달, commit은 변경 확정',
    '같은 UPDATE 뒤에도 두 결과가 가능합니다',
    '어떤 예외에서 rollback할까?',
    '조회인지 변경인지 실제 동작으로 판단하기',
    '객체 변경·SQL 실행·확정을 구분해 볼까?',
    '주문을 볼 때 어떤 데이터까지 필요할까?',
    'PK와 FK로 어느 주문의 항목인지 연결',
    'Java에서는 주문이 항목 목록을 가집니다',
    '항목이 필요해질 때 추가 조회할 수 있음',
    '필요한 값을 Service에서 읽고 DTO로 전달',
    '주문 목록 1회 뒤 항목 조회가 반복됨',
    'fetch join으로 주문과 항목을 함께 읽기',
    '나만의 단축 URL 서비스를 JPA로 전환',
    '기존 fork에서 개발하고 공용 저장소로 PR',
    '같은 객체 안의 호출은 프록시를 다시 지나지 않음',
]
positions = [titles.index(t) for t in sequence]
assert positions == sorted(positions)
assert titles[0] == '트랜잭션과 JPA'
assert '16일 28쪽부터' in slides[0].text_content()
assignment_start = titles.index('나만의 단축 URL 서비스를 JPA로 전환')
assignment_end = titles.index('전환 전후의 차이를 설명하고 제출')
assert all(not p['ch'].startswith('보충') for p in private[:assignment_end + 1])
assert all(p['ch'].startswith('보충') for p in private[assignment_end + 1:-1])
assert titles[-1] == '공식 문서'

# Explain each unfamiliar concept before its detailed operation or caveats.
visible_slides = [s.text_content() for s in slides]
assert '빈은 Spring이 만들고 관리하는 객체' in visible_slides[6]
assert '프록시는 실제 Service 대신 호출' in visible_slides[6]
assert '영속성 컨텍스트는 JPA가 Entity를 관리하는 공간' in visible_slides[7]
assert 'flush는 객체 변경을 SQL로 DB에 동기화' in visible_slides[8]
assert 'DTO는 응답에 필요한 값을 담는 객체' in visible_slides[19]
assert not any('rollback-only' in s for s in visible_slides[:assignment_start])
assert not any('clear' in s for s in visible_slides[:assignment_start])
visible = '\n'.join(visible_slides)
assert not re.search(r'Wiki|위키|교시|45분|Closes #|practice/jpa-query-lab|자체.*병합', visible, re.I)
assert not re.search(r'order-query-lab|ZIP|전체 파일|gradlew test|참고 코드', visible)
for token in [
    'CH 11', 'JDBC', 'RuntimeException', 'Error', 'IOException', 'rollbackFor',
    'rollback-only', '프록시', 'REQUIRED', 'readOnly', '자동 복원', 'clear', 'IDENTITY',
    '외부 API', '동시', 'UNIQUE', 'LAZY', '4 SELECT', '1 SELECT', 'fetch join',
    '3개 주문', '6개', 'EAGER', 'DTO', '재시작', 'open-in-view=false', 'ddl-auto=update',
    '기존 URL 생성', '고유', '유효성', '없는 코드', 'QA 체크리스트', '새 트랜잭션',
    '1 · 조회', '2 · 변경과 이력', '3 · 동시 요청', '이름 자율',
    'sesac-spring-boot-study', '공용 원본 main', '직접 병합하지 않습니다', 'Issue URL',
    'README', 'gradle-wrapper.jar', 'HTML', 'CSS', 'JavaScript', 'CDN', '프롬프트는 자율',
    '원자성', '일관성', '격리성', '지속성',
]:
    assert token in visible, token
assert 'contenteditable=' not in raw and 'localStorage' not in raw

diagrams = doc.xpath('//section//*[local-name()="svg"]')
assert len(diagrams) >= 15
for diagram in diagrams:
    assert diagram.get('role') == 'img' and diagram.get('aria-label')
    assert diagram.xpath('./*[local-name()="title"]')
    for label in diagram.xpath('.//*[local-name()="text"]'):
        assert float(label.get('font-size', '0')) >= 21
expected_topics = {
    'object-db', 'atomicity', 'service-boundary', 'proxy-return', 'dirty-check',
    'flush-commit', 'commit-rollback', 'exception-paths', 'pk-fk', 'object-relation',
    'lazy-timing', 'dto-boundary', 'n-plus-one', 'fetch-one', 'self-call',
}
assert expected_topics <= {d.get('data-diagram-topic') for d in diagrams}
assert doc.xpath('//a[@href="SHORT-URL-JPA-ASSIGNMENT.md"]')
for href in doc.xpath('//a/@href'):
    if href.startswith(('http:', 'https:', '#', 'mailto:')):
        continue
    assert (OUT / href.split('#')[0]).resolve().exists(), href
for name in ['INSTRUCTOR.md', 'BEGINNER-WORKSHEET.md', 'SHORT-URL-JPA-ASSIGNMENT.md']:
    assert (OUT / name).is_file(), name
    assert not re.search(r'Wiki|위키', (OUT / name).read_text(), re.I), name
js = '\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as f:
    f.write(js)
    f.flush()
    result = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
print(f'{OUT.name}: {len(slides)} progressive slides; {len(diagrams)} native diagrams')
print('Definitions, normal-flow order, supplements, assignment, empty sources, links and JS valid.')
print('No lecture code blocks or runnable examples. Existing archive assets are unchanged.')
