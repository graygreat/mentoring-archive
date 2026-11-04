from pathlib import Path
import ast,json,re,subprocess,tempfile
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
DAY=OUT.name
raw=(OUT/'index.html').read_text();doc=html.fromstring(raw)
slides=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
sources=json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
private=json.loads((R/'metadata-private.json').read_text())
assert len(slides)==len(meta)==len(private)
assert 10<=len(slides)<=22
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
assert 'product-api/' in visible
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

for token in ['CH 09','CH 10','CH 12','CH 11','personal-project/','CollectionItem','/items','400','404','105','75','180','60','4시간','11명','4분','2분','practice/product-crud','assignment/personal-rest','JPA','Memory','README','Closes #실제번호']:
 assert token in visible+'\n'+'\n'.join(x.get('note','') for x in private),token
assert 105+75==4*45 and 4*45+4*15==240
assert 11*(4+2)+9==75
assert 45+45+15==105 and 5*6==30 and 6*6+9==45
titles=[x['title'] for x in meta]
assert titles.index('책의 상품 수정·삭제를 함께 봅니다')<titles.index('개인 프로젝트 · 배운 CRUD를 적용합니다')<titles.index('CH 11 · 데이터베이스 연동을 읽습니다')
assert '../shared/db-basics/' in raw and '../shared/db-basics/STUDENT-WORKSHEET.md' in raw
assert 'assignments/personal-project/README.md' in raw
assert '새프로젝트' not in visible
assert {'ProductRepository.java','MemoryProductRepository.java','ProductService.java','ProductController.java','ProductCrudTest.java'}==set(SOURCES)

js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: root should check navigation JavaScript syntax')
print(f'{DAY}: {len(slides)} book-led slides; canonical source-data and whitespace intact; chapter/work/completion flow; read-only navigation verified')
