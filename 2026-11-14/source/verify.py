from pathlib import Path
import ast,json,re,subprocess,tempfile
from lxml import html
SOURCES = {}
R=Path(__file__).resolve().parent
OUT=R.parent
DAY=OUT.name
raw=(OUT/'index.html').read_text();doc=html.fromstring(raw)
slides=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
sources=json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
private=json.loads((R/'metadata-private.json').read_text())
assert len(slides)==len(meta)==len(private)
assert 25<=len(slides)<=35
assert sources==SOURCES
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
assert not doc.xpath('//section//pre')
buttons=doc.xpath('//section//button[@data-source-key]')
assert {b.get('data-source-key') for b in buttons}==set(sources)
assert len(buttons)==len(sources)
assert all(b.get('type')=='button' for b in buttons)
assert all(b in slides[-1].xpath('.//button[@data-source-key]') for b in buttons)
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
visible='\n'.join(s.text_content() for s in slides)
assert not re.search(r'wiki|위키',visible,re.I)
assert '책' in visible and 'README' in visible and 'sesac-spring-boot-study' in visible
assert 'short-url/' in visible and 'order-api/' in visible
assert 'contenteditable=' not in raw and 'localStorage' not in raw
for name,source in sources.items():
 assert 'package com.example.product;' in source
 assert '\t' not in source
 for n,line in enumerate(source.splitlines(),1):
  assert line==line.rstrip(),f'{name}:{n}: trailing spaces'
  assert (len(line)-len(line.lstrip(' ')))%4==0,f'{name}:{n}: indentation'
assert (OUT/'INSTRUCTOR.md').exists()
ids=doc.xpath('//@id');assert len(ids)==len(set(ids))
for i,(slide,item) in enumerate(zip(slides,meta)):
 title=slide.xpath('./h1')[0].text_content()
 assert title==re.sub('<[^>]+>','',item['title'])
 assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
assert not any('note' in item for item in meta)

for token in ['CH 13','CH 14','오전 · 3시간','오후 · 3시간','1~2시간','8글자','새로운 키','컬렉션','자동화 테스트','POST /orders','PATCH /orders/{orderId}/cancel','CREATED','500','404','모든 상품 재고 유지','orderedProducts','totalPrice','amount','SHIPPING','COMPLETED','CANCELED','주문 시점','ORM','JPA','Hibernate','Spring Data JPA','영속성 컨텍스트','1차 캐시','변경 감지','flush','commit','rollback','브랜치 이름은 자율','개인 Fork','병합 없이','HTML','CSS','JavaScript','CDN']:
 assert token in visible+'\n'+'\n'.join(x.get('note','') for x in private),token
combined=visible+'\n'+'\n'.join(x.get('note','') for x in private)+(OUT/'INSTRUCTOR.md').read_text()
for removed in ['교시','45분','150분','14-2/','상품 CRUD · 개인 REST 프로젝트']:
 assert removed not in combined,removed
assert not doc.xpath('//section//button[@data-source-key]')
assert not sources
assert 'https://github.com/lleellee0/java-for-backend/tree/main/14-1' in raw
assert not doc.xpath('//a[contains(@href,"/14-2")]')
titles=[x['title'] for x in meta]
assert titles.index('CH 13 · 단축 URL 서비스 개발')<titles.index('CH 14 · 주문 관리 API 서버 개발')<titles.index('Spring Data JPA와 DB 연동')

js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: root should check navigation JavaScript syntax')
print(f'{DAY}: {len(slides)} independent task slides; book contracts and JPA introduction; read-only navigation verified')
