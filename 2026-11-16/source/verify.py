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
assert len(slides) == len(meta) == len(private) == 32
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
# Copying the previous JPA lesson must preserve its actual teaching content.
previous = html.fromstring((OUT.parent / '2026-11-14/index.html').read_text())
previous_slides = previous.xpath(slide_path)
previous_meta = json.loads(previous.xpath('//script[@id="deck-data"]/text()')[0])
start = next(i for i, item in enumerate(previous_meta) if item['title'] == 'Spring Data JPA와 DB 연동')
assert meta[1:] == previous_meta[start:]
assert len(previous_slides[start:]) == 31
for copied, original in zip(slides[1:], previous_slides[start:]):
    assert copied.get('class') == original.get('class')
    for selector in ['./h1', './div[@class="content"]', './div[@class="topline"]']:
        assert html.tostring(copied.xpath(selector)[0]) == html.tostring(original.xpath(selector)[0])
visible = '\n'.join(s.text_content() for s in slides)
assert not re.search(r'wiki|위키|교시|45분|Closes #|병합 PR', visible, re.I)
for token in ['발표', 'AI 도움', 'ORM', 'SQL Mapper', 'JPA', 'Hibernate', 'Spring Data JPA',
              '영속성 컨텍스트', '스냅샷', '변경 감지', 'flush', 'commit', 'rollback', '면접']:
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
print(f'{OUT.name}: 32 slides; one presentation slide + 31 unchanged November 14 JPA slides; navigation verified')
