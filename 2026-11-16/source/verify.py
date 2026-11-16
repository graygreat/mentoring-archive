from pathlib import Path
import json, re, subprocess, tempfile
from lxml import html
R = Path(__file__).resolve().parent
OUT = R.parent
raw = (OUT / 'index.html').read_text()
doc = html.fromstring(raw)
slide_path = '//section[contains(concat(" ", normalize-space(@class), " "), " slide ")]'
slides = doc.xpath(slide_path)
meta = json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
private = json.loads((R / 'metadata-private.json').read_text())
assert len(slides) == len(meta) == len(private) == 40
assert meta[0] == {'ch': '발표', 'title': '나만의 단축 URL 서비스 만들기'}
assert len(slides[0].xpath('.//ol/li')) == 4
assert meta[1]['title'] == 'Spring Data JPA와 DB 연동'
assert json.loads(doc.xpath('//script[@id="source-data"]/text()')[0]) == {}
assert not doc.xpath('//section//button[@data-source-key]')
assert [s.get('data-index') for s in slides] == list(map(str, range(len(slides))))
assert len(set(doc.xpath('//section/@data-slide-id'))) == len(slides)
ids = doc.xpath('//@id')
assert len(ids) == len(set(ids))
assert not doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " subtitle ")]')
assert 'contenteditable=' not in raw and 'localStorage' not in raw
for i, (slide, item) in enumerate(zip(slides, meta)):
    assert slide.xpath('./h1')[0].text_content() == re.sub('<[^>]+>', '', item['title'])
    assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
    assert slide.xpath('./footer/span')[0].text_content() == '2026.11.16'
    assert 'note' not in item
# Preserve the carried-over lesson apart from the clarified roles summary.
previous = html.fromstring((OUT.parent / '2026-11-14/index.html').read_text())
previous_slides = previous.xpath(slide_path)
previous_meta = json.loads(previous.xpath('//script[@id="deck-data"]/text()')[0])
start = next(i for i, item in enumerate(previous_meta) if item['title'] == 'Spring Data JPA와 DB 연동')
baseline = previous_meta[start:]
originals = {item['title']: slide for item, slide in zip(baseline, previous_slides[start:])}
carried = [item for item in meta[1:] if item['title'] in originals]
assert {item['title'] for item in carried} == {item['title'] for item in baseline}
moved_title = '조회한 상품을 트랜잭션 안에서 수정'
assert [item['title'] for item in carried if item['title'] != moved_title] == [item['title'] for item in baseline if item['title'] != moved_title]
assert len(meta) - 1 - len(carried) == 8
titles = [item['title'] for item in meta]
assert titles.index('어떻게 UPDATE가 나갈까?') < titles.index(moved_title) < titles.index('SQL 전달과 변경 확정은 다르다')
optional_titles = {'직접 만든 Repository는 어디에 남을까?', 'save는 무엇을 할까?', '왜 Service에 @Transactional을 붙일까?'}
for item in meta:
    if item['title'] in optional_titles:
        assert item['ch'].startswith('보충'), item['title']

def comparable(element):
    text = html.tostring(element, encoding='unicode')
    return re.sub(r'arrow-\d+', 'arrow-normalized', text)

for copied, item in zip(slides[1:], meta[1:]):
    if item['title'] not in originals or item['title'] == '세 가지 이름의 역할':
        continue
    original = originals[item['title']]
    assert copied.get('class') == original.get('class')
    selectors = ['./h1', './div[@class="content"]']
    if item['title'] not in optional_titles:
        selectors.append('./div[@class="topline"]')
    for selector in selectors:
        assert comparable(copied.xpath(selector)[0]) == comparable(original.xpath(selector)[0])
visible = '\n'.join(s.text_content() for s in slides)
assert not re.search(r'wiki|위키|교시|45분|Closes #|병합 PR', visible, re.I)
for token in ['발표', 'AI 도움', 'ORM', 'SQL Mapper', 'JPA', 'Hibernate', 'Spring Data JPA',
              'EclipseLink', 'OpenJPA', 'EntityManager', 'JpaRepository', '영속성 컨텍스트', '스냅샷', '변경 감지', 'flush', 'commit', 'rollback', '면접']:
    assert token in visible, token
for block in doc.xpath('//section//pre/code'):
    text = block.text_content()
    assert '\t' not in text
    for line in text.splitlines():
        assert line == line.rstrip()
        assert (len(line) - len(line.lstrip(' '))) % 4 == 0, line
for diagram in doc.xpath('//section//*[local-name()="svg"]'):
    assert diagram.get('role') == 'img' and diagram.get('aria-label')
    assert diagram.xpath('./*[local-name()="title"]')
for href in doc.xpath('//a/@href'):
    if href.startswith(('http:', 'https:', '#', 'mailto:')):
        continue
    assert (OUT / href.split('#')[0]).resolve().exists(), href
assert (OUT / 'INSTRUCTOR.md').exists()
js = '\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as f:
    f.write(js)
    f.flush()
    result = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
print(f'{OUT.name}: 40 slides; beginner roadmap, mapping, save and persistence visuals; original teaching content and navigation verified')
