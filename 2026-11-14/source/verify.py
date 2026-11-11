from pathlib import Path
import json, re, subprocess, tempfile
from lxml import html
R = Path(__file__).resolve().parent
OUT = R.parent
raw = (OUT / 'index.html').read_text()
doc = html.fromstring(raw)
slides = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta = json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
private = json.loads((R / 'metadata-private.json').read_text())
assert len(slides) == len(meta) == len(private)
assert 20 <= len(slides) <= 40
assert [s.get('data-index') for s in slides] == list(map(str, range(len(slides))))
assert len(set(doc.xpath('//section/@data-slide-id'))) == len(slides)
ids = doc.xpath('//@id')
assert len(ids) == len(set(ids))
assert json.loads(doc.xpath('//script[@id="source-data"]/text()')[0]) == {}
assert not doc.xpath('//section//button[@data-source-key]')
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert 'contenteditable=' not in raw and 'localStorage' not in raw
visible = '\n'.join(s.text_content() for s in slides)
assert not re.search(r'wiki|위키|교시|45분', visible, re.I)
for i, (slide, item) in enumerate(zip(slides, meta)):
    assert slide.xpath('./h1')[0].text_content() == re.sub('<[^>]+>', '', item['title'])
    assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
    assert 'note' not in item
# Tasks use only chapter landing pages; requirements remain in the textbook.
for chapter in ['CH 13', 'CH 14']:
    assert sum(chapter in x['title'] for x in meta) == 1
for removed in ['구현할 API 5개', '주문 데이터 형식', '구현 체크리스트', '8글자', '모든 상품 재고 유지']:
    assert removed not in visible, removed
for token in ['JDBC', 'SQL Mapper', 'MyBatis', 'ORM', 'JPA', 'Hibernate', 'Spring Data JPA',
              'EntityManager', '영속성 컨텍스트', '1차 캐시', '변경 감지', 'flush', 'commit',
              'rollback', '@Entity', '@Id', '@Transactional', 'merge', 'persist', '면접']:
    assert token in visible, token
code_blocks = doc.xpath('//section//pre/code')
assert len(code_blocks) >= 5
for block in code_blocks:
    text = block.text_content()
    assert '\t' not in text
    for line in text.splitlines():
        assert line == line.rstrip()
        assert (len(line) - len(line.lstrip(' '))) % 4 == 0, line
assert (OUT / 'INSTRUCTOR.md').exists()
js = '\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as f:
    f.write(js)
    f.flush()
    result = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
print(f'{OUT.name}: {len(slides)} slides; two task landing pages; concrete JPA code and interview content; navigation verified')
