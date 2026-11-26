"""Check the case-based JPA and security-concept lesson structure."""
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
assert len(slides)==38
assert json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])=={}
assert not doc.xpath('//section//*[@data-source-key]')
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
ids=doc.xpath('//@id');assert len(ids)==len(set(ids))
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
for i,(slide,record) in enumerate(zip(slides,meta)):
    assert slide.xpath('./h1')[0].text_content()==re.sub('<[^>]*>','',record['title'])
    assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
    assert slide.xpath('./footer/span')[0].text_content()=='2026.11.26'
    assert 'note' not in record
visible='\n'.join(s.text_content() for s in slides)
assert not re.search(r'Wiki|위키|교시|45분|Closes #',visible,re.I)
for stale in ['ShortLink','AppUser','ShortLinkTag','owner_id','/api/links','단축 URL']:
    assert stale not in visible,stale
for token in ['ManyToOne','OneToMany','OneToOne','ManyToMany','JoinTable','JoinColumn',
              'mappedBy','StudyMember','UNIQUE','LAZY','DTO','인증','인가','SSO','IdP',
              'SecurityFilterChain','DispatcherServlet','HandlerInterceptor',
              '세션','쿠키','preHandle','postHandle','afterCompletion']:
    assert token in visible,token
# Each mapping has a distinct, contiguous case section.
case_order=['ManyToOne','OneToMany','OneToOne','ManyToMany']
case_positions=[]
for case in case_order:
    positions=[i for i,m in enumerate(meta) if case in m['ch']]
    assert len(positions)>=2,case
    assert positions==list(range(min(positions),max(positions)+1)),case
    case_positions.append(min(positions))
assert case_positions==sorted(case_positions)
# The simplified security section follows the object-design section.
assert meta[9]['title']=='모임의 소속 설정과 스터디 목록 추가'
assert [m['title'] for m in meta[27:35]]==[
    '인증과 인가','쿠키와 세션으로 로그인 상태 이어가기',
    'Filter는 요청·응답을 처리하는 중간 단계',
    'Filter와 HandlerInterceptor의 실행 위치','HandlerInterceptor의 세 가지 시점',
    'Spring Security의 요청 확인 순서','SSO는 여러 서비스의 반복 로그인을 줄입니다',
    'Security는 기본 로그인부터 직접 학습']
for removed in ['DelegatingFilterProxy','FilterChainProxy','SecurityContext','PasswordEncoder','CSRF','JWT','OAuth 2.0','OIDC']:
    assert removed not in visible,removed
assert 'WebSecurityConfigurerAdapter' not in raw
assert not re.search(r'csrf\s*\([^)]*disable|NoOpPasswordEncoder',raw)
assert 'contenteditable=' not in raw and 'localStorage' not in raw
assignment=next(i for i,m in enumerate(meta) if m['title']=='스터디 모집·모임 관리 서비스')
assert len(slides)-assignment==3
assignment_text='\n'.join(x.text_content() for x in slides[assignment:])
for token in ['일대일','다대일','규칙','트랜잭션','PR']:
    assert token in assignment_text,token
for token in ['MemberProfile','StudyMember','StudyMeeting','LEADER','WITHDRAWN','joinedAt','409']:
    assert token not in assignment_text,token
assert all('과제' in m['ch'] for m in meta[assignment:])
assert not any(x.xpath('.//pre') for x in slides[assignment:])
assert any('자율 학습' in m['ch'] or '자율 학습' in m['title'] for m in meta)
keys=[]
for block in doc.xpath('//section//pre'):
    keys.append(block.get('data-code-key'))
    for line in block.text_content().splitlines():
        assert '\t' not in line and line==line.rstrip(),line
        assert (len(line)-len(line.lstrip(' ')))%4==0,line
assert all(keys) and len(keys)==len(set(keys))
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
assert (OUT/'UNDERSTANDING-WORKSHEET.md').is_file()
readme=(OUT.parent/'README.md').read_text()
assert '| 2026-11-26 |' in readme
assert '[수업 자료](./2026-11-26/index.html)' in readme
js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
    f.write(js);f.flush()
    result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
print(f'{OUT.name}: {len(slides)} slides, {len(svgs)} diagrams, {len(keys)} code blocks')
print('Four case sections, security concepts, open project brief, README, links, whitespace and JS verified.')
print('Code fragments are not a complete application; semantic and runtime checks are separate.')
