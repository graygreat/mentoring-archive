"""Verify a progressive, diagram-led Nov 23 lecture and its existing assignment."""
from pathlib import Path
import json
import hashlib
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
assert len(slides) == len(meta) == len(private) == 48
assert sources == {}
assert not doc.xpath('//section//*[@data-source-key]')
assert len(doc.xpath('//section//pre/code')) >= 10
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
    '같은 객체 안의 호출은 프록시를 다시 지나지 않음',
]
positions = [titles.index(t) for t in sequence]
assert positions == sorted(positions)
assert titles[0] == '트랜잭션과 JPA'
assert '16일 28쪽부터' in slides[0].text_content()
assignment_start = titles.index('나만의 단축 URL 서비스를 JPA로 전환')
assignment_end = assignment_start
assert assignment_start == 32
assert len(slides[assignment_start].xpath('.//ol/li')) == 3
assert all(not p['ch'].startswith('보충') for p in private[:assignment_end + 1])
assert all(p['ch'].startswith('보충') for p in private[assignment_end + 1:-1])
assert titles[-1] == '공식 문서'

# Explain each unfamiliar concept before its detailed operation or caveats.
visible_slides = [s.text_content() for s in slides]
assert '빈은 Spring이 만들고 관리하는 객체' in visible_slides[6]
assert '프록시는 실제 Service 대신 호출' in visible_slides[6]
assert '영속성 컨텍스트는 JPA가 Entity를 관리하는 공간' in visible_slides[7]
assert 'flush는 객체 변경을 SQL로 DB에 동기화' in visible_slides[8]
assert 'DTO는 응답에 필요한 값을 담는 객체' in visible_slides[titles.index('필요한 값을 Service에서 읽고 DTO로 전달')]
assert not any('rollback-only' in s for s in visible_slides[:assignment_start])
assert not any('clear' in s for s in visible_slides[:assignment_start])
visible = '\n'.join(visible_slides)
assert not re.search(r'Wiki|위키|교시|45분|Closes #|practice/jpa-query-lab|자체.*병합', visible, re.I)
assert not re.search(r'order-query-lab|ZIP|전체 파일|gradlew test|참고 코드', visible)
for token in [
    'CH 11', 'JDBC', 'RuntimeException', 'Error', 'IOException', 'rollbackFor',
    'rollback-only', '프록시', 'REQUIRED', 'readOnly', '자동 복원', 'clear', 'IDENTITY',
    '외부 API', '동시', 'UNIQUE', 'LAZY', '4 SELECT', '1 SELECT', 'fetch join',
    '3개 주문', '6개', 'EAGER', 'DTO', '원자성', '일관성', '격리성', '지속성',
]:
    assert token in visible, token
assignment = slides[assignment_start].text_content()
for token in ['기존에 만든 단축 URL 서비스', 'JPA로 바꾸기', '트랜잭션 범위', 'PR description', '어디에 왜', '신경 썼는지']:
    assert token in assignment, token
assert not re.search(r'QA|체크리스트|Issue|재시작|추가 과제|CDN|브랜치', assignment)

# Existing lecture, diagrams, supplements and the one-slide assignment stay intact.
def content_signature(slide):
    return [slide.get('class'), *[
        re.sub(r'arrow-\d+', 'arrow-normalized', html.tostring(slide.xpath(selector)[0], encoding='unicode'))
        for selector in ['./div[@class="topline"]', './h1', './div[@class="content"]']
    ]]
original_titles = ['트랜잭션과 JPA', '오늘 다룰 내용', '객체의 가격과 DB 가격은 별개', '가격 변경만 저장되고 이력이 실패한다면?', 'DB 작업을 하나의 성공·실패 단위로 묶기', '함께 성공해야 할 범위를 Service에서 정하기', '프록시가 Service 호출 앞뒤를 처리합니다', '관리 중인 상품의 변경을 감지하기', 'flush는 SQL 전달, commit은 변경 확정', '같은 UPDATE 뒤에도 두 결과가 가능합니다', 'save 직후 INSERT가 보여도 commit은 별개', '어떤 예외에서 rollback할까?', '실패를 밖으로 전달하는지 확인하기', '조회인지 변경인지 실제 동작으로 판단하기', '객체 변경·SQL 실행·확정을 구분해 볼까?', '주문을 볼 때 어떤 데이터까지 필요할까?', 'PK와 FK로 어느 주문의 항목인지 연결', 'Java에서는 주문이 항목 목록을 가집니다', '항목이 필요해질 때 추가 조회할 수 있음', '필요한 값을 Service에서 읽고 DTO로 전달', '주문 목록 1회 뒤 항목 조회가 반복됨', 'fetch join으로 주문과 항목을 함께 읽기', 'SQL을 줄여도 같은 데이터여야 합니다', '객체·트랜잭션·관계 조회를 연결하기', '나만의 단축 URL 서비스를 JPA로 전환', '같은 객체 안의 호출은 프록시를 다시 지나지 않음', '기존 트랜잭션이 있으면 함께 참여', '이미 취소 표시된 트랜잭션은 정상 확정 불가', '동시 요청과 외부 처리는 별도 대책이 필요', 'clear는 DB 데이터를 삭제하지 않습니다', '트랜잭션의 네 가지 특성', '기존 저장소 인터페이스를 유지할 수 있음', 'save 반환값과 원본 객체를 구분하기', '공식 문서']
preserved = [content_signature(slides[titles.index(title)]) for title in original_titles]
assert hashlib.sha256(json.dumps(preserved, ensure_ascii=False).encode()).hexdigest() == '59a300e18125c44e30a2380b7acbbc5b49cf9df94b8579ef63fc0493005af53d', 'Existing lecture or simple assignment changed'
assert [title for title in titles if title in original_titles] == original_titles
# Short diagnostic snippets are now requested; full source archives remain absent.
for block in doc.xpath('//section//pre/code'):
    for line in block.text_content().splitlines():
        assert '\t' not in line and line == line.rstrip(), line
        assert (len(line) - len(line.lstrip(' '))) % 4 == 0, line
for title in [
    'items와 order_id를 코드로 연결',
    '어느 줄에서 항목 SELECT가 나갈까?',
    'Service 밖에서 처음 items를 읽으면?',
    '조회 트랜잭션 안에서 DTO 값 만들기',
    '반복문이 주문별 SELECT를 추가합니다',
    '필요한 관계를 fetch join으로 지정하기',
]:
    assert titles.index(title) < assignment_start, title
for title in [
    '주문 페이지를 JOIN 결과 행으로 자르면?',
    'DB만 바뀌고 관리 객체는 옛값일 수 있음',
    '두 요청의 증가가 한 번으로 덮일 수 있음',
]:
    assert private[titles.index(title)]['ch'].startswith('보충'), title
for token in ['LazyInitializationException', 'open-in-view=false', 'getItems().size()',
              'left join fetch o.items', '@Version', 'Pageable', 'executeUpdate()',
              'entityManager.clear()', 'SQL 로그', '새 트랜잭션', 'findIdPage(Pageable pageable)',
              'findWithItemsByIds', 'countQuery', 'where o.id in :ids']:
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
    'lazy-closed', 'collection-page', 'bulk-stale', 'lost-update',
}
assert expected_topics <= {d.get('data-diagram-topic') for d in diagrams}
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
print('Short issue snippets are included; full runnable archives remain outside the lecture.')
