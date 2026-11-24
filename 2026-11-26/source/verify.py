"""Validate Nov 26 association and security teaching material."""
from pathlib import Path
import json,re,subprocess,tempfile
from lxml import html
R=Path(__file__).resolve().parent
OUT=R.parent
raw=(OUT/'index.html').read_text()
doc=html.fromstring(raw)
slides=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
private=json.loads((R/'metadata-private.json').read_text())
assert len(slides)==len(meta)==len(private)
assert len(slides) == 34
assert json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])=={}
assert not doc.xpath('//section//*[@data-source-key]')
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
ids=doc.xpath('//@id');assert len(ids)==len(set(ids))
for i,(slide,record) in enumerate(zip(slides,meta)):
    assert slide.xpath('./h1')[0].text_content()==re.sub('<[^>]*>','',record['title'])
    assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
    assert slide.xpath('./footer/span')[0].text_content()=='2026.11.26'
    assert 'note' not in record
visible='\n'.join(s.text_content() for s in slides)
assert not re.search(r'Wiki|위키|교시|45분|Closes #|필수 과제',visible,re.I)
for token in ['AppUser','ShortLink','owner_id','mappedBy','ManyToOne','OneToMany',
              'OneToOne','ShortLinkTag','UNIQUE','LAZY','DTO','인증','인가',
              'DispatcherServlet','세션','BCryptPasswordEncoder','matches',
              'CSRF','302','401','403','PR','자율 학습']:
    assert token in visible,token
assert 'WebSecurityConfigurerAdapter' not in raw
assert not re.search(r'csrf\s*\([^)]*disable|NoOpPasswordEncoder',raw)
assert 'contenteditable=' not in raw and 'localStorage' not in raw
titles=[m['title'] for m in meta]
assert len(doc.xpath('//svg[@data-diagram-topic="many-to-many"]'))==1
assert '과제' in private[-1]['ch']
assert 'PR' in slides[-1].text_content()
assert 'LinkFolder' not in visible and '모음함' not in visible
assert '스터디' in visible
expected=['PK는 내 행의 번호, FK는 연결할 행의 번호',
          '두 링크가 같은 사용자 객체를 참조',
          'owner 객체 참조와 owner_id 컬럼 연결',
          'mappedBy에는 owner_id가 아닌 owner',
          'FK를 갱신하는 기준은 ShortLink.owner',
          '목록에 넣기와 FK 변경은 다른 동작',
          '인증과 인가','기본 로그인부터 단계적으로 학습']
positions=[titles.index(t) for t in expected]
assert positions==sorted(positions)
assert titles.index('기본 로그인부터 단계적으로 학습')-titles.index('관계 정보와 접근 권한은 별개')<=8
assignment=titles.index('스터디 모집·모임 관리 서비스')
assert len(slides)-assignment==3
assert not doc.xpath('//svg[@data-diagram-topic="study-project"]')
assignment_text='\n'.join(x.text_content() for x in slides[assignment:])
for token in ['일대일','다대일','규칙','트랜잭션','PR']:
    assert token in assignment_text,token
for token in ['MemberProfile','StudyMember','StudyMeeting','LEADER','ACTIVE','WITHDRAWN','joinedAt','409']:
    assert token not in assignment_text,token
assert not any(x.xpath('.//pre') for x in slides[assignment:])
# Optional security study and the JPA assignment must remain distinct.
assert any('자율 학습' in m['ch'] or '자율 학습' in m['title'] for m in meta)
keys=[]
for block in doc.xpath('//section//pre'):
    keys.append(block.get('data-code-key'))
    for line in block.text_content().splitlines():
        assert '\t' not in line and line==line.rstrip(),line
        assert (len(line)-len(line.lstrip(' ')))%4==0,line
assert all(keys) and len(keys)==len(set(keys))
assert 'link-owner' in keys
assert 'Objects.requireNonNull(owner)' in visible
assert not {'security-chain-1','security-chain-2','user-details-service','csrf-fetch'} & set(keys)
svgs=doc.xpath('//section//*[local-name()="svg"]')
assert len(svgs)>=10
for s in svgs:
    assert s.get('role')=='img' and s.get('aria-label')
    assert s.xpath('./*[local-name()="title"]')
    for t in s.xpath('.//*[local-name()="text"]'):
        assert float(t.get('font-size',0))>=21
for href in doc.xpath('//a/@href'):
    if href.startswith(('http:','https:','#','mailto:')):continue
    assert (OUT/href.split('#')[0]).resolve().exists(),href
for name in ['UNDERSTANDING-WORKSHEET.md']:
    assert (OUT/name).is_file(),name
js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
    f.write(js);f.flush()
    r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
    assert r.returncode==0,r.stderr
print(f'{OUT.name}: {len(slides)} slides, {len(svgs)} diagrams, {len(keys)} short code blocks')
print('Association/security order, safe policy, ownership checks, metadata, links, whitespace and JS verified.')
print('Teaching fragments are not a complete application; runtime verification is a separate check.')
