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
assert len(slides)==len(meta)==len(private)==49
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
for token in ['AppUser','ShortLink','owner_id','mappedBy','연관관계 주인','ManyToOne','OneToMany',
              'orphanRemoval','REMOVE','LAZY','DTO','인증','인가','SecurityFilterChain',
              'DispatcherServlet','JSESSIONID','UserDetailsService','passwordHash','BCryptPasswordEncoder',
              'matches','hasRole','ROLE_ADMIN','Authentication','findByIdAndOwnerId','404','302','401','403',
              'CSRF','CORS','POST /logout','same-origin','headerName','프롬프트']:
    if token=='프롬프트':
        continue
    assert token in visible,token
assert 'WebSecurityConfigurerAdapter' not in raw
assert not re.search(r'csrf\s*\([^)]*disable|NoOpPasswordEncoder',raw)
assert 'contenteditable=' not in raw and 'localStorage' not in raw
expected=[
 'owner_id로 어느 사용자의 링크인지 연결',
 '링크 객체가 사용자 객체를 참조',
 'FK를 AppUser 참조에 매핑하기',
 '사용자에서도 링크로 탐색하려면?',
 'mappedBy는 반대쪽 필드 이름',
 'FK를 갱신하는 기준은 ShortLink.owner',
 '관계가 있다고 접근 권한까지 검사되지는 않음',
 '인증과 인가는 다른 질문',
 'Security 필터가 Controller보다 먼저 검사',
 'URL별 접근 규칙 지정하기',
 '링크 ID와 현재 사용자 ID를 함께 조회',
 '쿠키가 자동으로 따라가는 요청 주의',
]
titles=[m['title'] for m in meta]
indexes=[titles.index(t) for t in expected];assert indexes==sorted(indexes)
assert private[-1]['ch']=='선택 적용'
assert titles[-2]=='연관관계·인증·요청 인가 참고'
assert len(slides[-1].xpath('.//ol/li'))==3
keys=[]
for block in doc.xpath('//section//pre'):
    keys.append(block.get('data-code-key'))
    for line in block.text_content().splitlines():
        assert '\t' not in line and line==line.rstrip(),line
        assert (len(line)-len(line.lstrip(' ')))%4==0,line
assert all(keys) and len(keys)==len(set(keys))
assert {'security-chain-1','security-chain-2','password-encoder','ownership-query','csrf-fetch'}<=set(keys)
for fragment in ['.anyRequest().denyAll()', '.formLogin(', '.logout(', '.roles(user.getRole())',
                 'Objects.requireNonNull(owner)', 'findByIdAndOwnerId(linkId, user.getId())']:
    assert fragment in visible,fragment
svgs=doc.xpath('//section//*[local-name()="svg"]')
assert len(svgs)>=12
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
