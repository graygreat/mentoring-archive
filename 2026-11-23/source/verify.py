"""Validate the Nov 23 continuation, concrete examples and personal JPA task."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
from lxml import html
from code_examples import SOURCES

R = Path(__file__).resolve().parent
OUT = R.parent
raw = (OUT / 'index.html').read_text()
doc = html.fromstring(raw)
slide_path = '//section[contains(concat(" ", normalize-space(@class), " "), " slide ")]'
slides = doc.xpath(slide_path)
meta = json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
private = json.loads((R / 'metadata-private.json').read_text())
sources = json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
assert len(slides) == len(meta) == len(private) == 48
assert sources == SOURCES and len(sources) == 6
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

# The new lesson starts where Nov 16 stopped; advanced details follow fundamentals.
titles = [m['title'] for m in meta]
sequence = [
    '객체의 가격과 DB 가격은 별개',
    '왜 Service에 @Transactional을 붙일까?',
    '관리 중인 상품은 save 없이 수정 가능',
    'UPDATE 뒤 예외가 나도 rollback 가능',
    '어떤 예외에서 rollback할까?',
    '같은 객체 안에서 호출하면 새 설정이 적용 안 됨',
    'readOnly는 쓰기 금지 보안 장치가 아님',
    '트랜잭션만으로 동시 수정이 해결되지는 않음',
    '주문 PK와 항목 FK 연결',
    '주문 조회와 항목 접근을 나누어 보기',
    '주문 3개에서 왜 4 SELECT일까?',
    '필요한 항목을 fetch join으로 함께 읽기',
    '나만의 단축 URL 서비스를 JPA로 전환',
    '기존 fork에서 개발하고 공용 저장소로 PR',
    '기존 저장소 인터페이스를 유지할 수 있음',
]
positions = [titles.index(t) for t in sequence]
assert positions == sorted(positions)
assert titles[0] == '트랜잭션과 JPA'
assert '16일 28쪽부터' in slides[0].text_content()
assert private[titles.index('기존 저장소 인터페이스를 유지할 수 있음')]['ch'].startswith('보충')
assert private[titles.index('save가 전달 객체를 항상 관리 상태로 바꿀까?')]['ch'].startswith('보충')

visible = '\n'.join(s.text_content() for s in slides)
assert not re.search(r'Wiki|위키|교시|45분|Closes #|practice/jpa-query-lab|자체.*병합', visible, re.I)
for token in [
    'CH 11', 'JDBC', 'RuntimeException', 'Error', 'rollbackFor', 'rollback-only',
    'org.springframework.transaction.annotation.Transactional', '프록시', 'REQUIRED',
    'readOnly', '자동 복원', 'clear', 'IDENTITY', '외부 API', '동시', 'UNIQUE',
    'LAZY', 'LazyInitializationException', '4 SELECT', '1 SELECT', 'fetch join',
    '3개 주문', '6개', '같은', 'EAGER', 'DTO', '재시작', 'jdbc:h2:file:./data/short-url',
    'spring.jpa.open-in-view=false', 'spring.jpa.hibernate.ddl-auto=update',
    '기존 URL 생성', '고유', '유효성', '없는 코드', 'QA 체크리스트', '새 트랜잭션',
    '1 · 조회', '2 · 변경과 이력', '3 · 동시 요청', '이름 자율',
    'sesac-spring-boot-study', '공용 원본 main', '직접 병합하지 않습니다', 'Issue URL',
    'README', 'gradle-wrapper.jar', 'HTML', 'CSS', 'JavaScript', 'CDN', '프롬프트는 자율',
]:
    assert token in visible, token
assert 'contenteditable=' not in raw and 'localStorage' not in raw

# The reference app is preserved byte-for-byte; teaching snippets have clean whitespace.
for key, source in sources.items():
    assert doc.xpath('//*[@data-source-key=$k]', k=key), key
for label, text in [(k, v) for k, v in sources.items()] + [
    (f'slide-code-{i}', block.text_content())
    for i, block in enumerate(doc.xpath('//section//pre/code'), 1)
]:
    for n, line in enumerate(text.splitlines(), 1):
        assert '\t' not in line and line == line.rstrip(), (label, n, 'whitespace')
        assert (len(line) - len(line.lstrip(' '))) % 4 == 0, (label, n, 'indentation')
for diagram in doc.xpath('//section//*[local-name()="svg"]'):
    assert diagram.get('role') == 'img' and diagram.get('aria-label')
    assert diagram.xpath('./*[local-name()="title"]')
assert len(doc.xpath('//section//*[local-name()="svg"]')) >= 6
assert doc.xpath('//a[@href="assets/order-query-lab.zip"]')
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
print(f'{OUT.name}: {len(slides)} slides; continuation/transaction/JPA/task order verified')
print('Links, source equality, code whitespace, diagrams, metadata and JS syntax valid.')
print('Existing Java/ZIP unchanged. This check does not claim a DB/HTTP run of teaching excerpts.')
