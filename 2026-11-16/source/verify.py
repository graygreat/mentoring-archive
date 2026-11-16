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
assert len(slides) == len(meta) == len(private) == 41
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
# Preserve carried-over content except the explicitly approved flow clarifications.
previous = html.fromstring((OUT.parent / '2026-11-14/index.html').read_text())
previous_slides = previous.xpath(slide_path)
previous_meta = json.loads(previous.xpath('//script[@id="deck-data"]/text()')[0])
start = next(i for i, item in enumerate(previous_meta) if item['title'] == 'Spring Data JPA와 DB 연동')
baseline = previous_meta[start:]
originals = {item['title']: slide for item, slide in zip(baseline, previous_slides[start:])}
carried = [item for item in meta[1:] if item['title'] in originals]
assert {item['title'] for item in carried} == {item['title'] for item in baseline}
moved_title = '조회한 상품을 트랜잭션 안에서 수정'
reordered_titles = {moved_title, '직접 만든 Repository는 어디에 남을까?', 'save는 무엇을 할까?', '왜 Service에 @Transactional을 붙일까?'}
assert [item['title'] for item in carried if item['title'] not in reordered_titles] == [item['title'] for item in baseline if item['title'] not in reordered_titles]
assert len(meta) - 1 - len(carried) == 9
titles = [item['title'] for item in meta]
assert titles.index('어떻게 UPDATE가 나갈까?') < titles.index('왜 Service에 @Transactional을 붙일까?') < titles.index(moved_title) < titles.index('SQL 전달과 변경 확정은 다르다')
optional_titles = {'직접 만든 Repository는 어디에 남을까?', 'save는 무엇을 할까?', '트랜잭션 설정에서 주의할 점'}
assert titles[-5:] == ['상품 가격 변경 과정을 연결하기', '직접 만든 Repository는 어디에 남을까?', 'save는 무엇을 할까?', '트랜잭션 설정에서 주의할 점', 'JPA · MyBatis 공식 문서']
assert titles[titles.index('저장한 상품의 실제 id로 다시 조회') + 1] == '조회한 객체를 관리하는 작업 공간'
assert not meta[titles.index('왜 Service에 @Transactional을 붙일까?')]['ch'].startswith('보충')
assert all(meta[titles.index(t)]['ch'].startswith('보충') for t in optional_titles)
for item in meta:
    if item['title'] in optional_titles:
        assert item['ch'].startswith('보충'), item['title']

approved_transitions = {
    '같은 가격 변경을 두 방식으로 구현': ('두 방식 모두 UPDATE SQL로 DB 값을 바꿉니다.<br>지금은 작성 방식만 비교합니다. 관리 상태·트랜잭션·변경 감지는 뒤에서 설명합니다.', '두 방식 모두 UPDATE SQL로 DB 값을 바꿉니다.<br>JPA의 SQL 예: UPDATE products SET ... price = ? ... WHERE id = ?'),
    '같은 객체와 조회 당시 값을 함께 관리': ('현재 값과 조회 당시 값을 비교할 수 있습니다.<br>다음으로 이 차이를 이용한 변경 감지가 어떻게 UPDATE로 이어지는지 봅니다.', '현재 값과 조회 당시 값의 차이를 보고 UPDATE가 필요한지 판단합니다.'),
    moved_title: ('별도 save 없이 변경 감지로 가격 변경을 반영할 수 있습니다.<br>이제 실제 UPDATE가 실행되는 시점과 변경이 확정되는 시점을 구분합니다.', '별도 save 호출 없이도 변경 감지를 통해 가격 변경을 DB에 반영할 수 있습니다.'),
}

def comparable(element):
    text = html.tostring(element, encoding='unicode')
    return re.sub(r'arrow-\d+', 'arrow-normalized', text)

for copied, item in zip(slides[1:], meta[1:]):
    if item['title'] not in originals or item['title'] in {'세 가지 이름의 역할', '왜 Service에 @Transactional을 붙일까?'}:
        continue
    original = originals[item['title']]
    assert copied.get('class') == original.get('class')
    selectors = ['./h1', './div[@class="content"]']
    if item['title'] not in optional_titles:
        selectors.append('./div[@class="topline"]')
    for selector in selectors:
        actual = comparable(copied.xpath(selector)[0])
        if selector == './div[@class="content"]' and item['title'] in approved_transitions:
            changed, previous = approved_transitions[item['title']]
            assert changed in actual, item['title']
            actual = actual.replace(changed, previous)
        assert actual == comparable(original.xpath(selector)[0]), (item['title'], selector)
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
print(f'{OUT.name}: 41 slides; transaction basics before update, supplements after summary; preserved teaching content and navigation verified')
