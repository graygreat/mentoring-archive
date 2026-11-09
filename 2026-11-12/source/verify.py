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
assert 22<=len(slides)<=25
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

assert set(SOURCES)=={'CreateProductRequest.java','ProductController.java','ApiExceptionHandler.java'}
assert '@Valid @RequestBody' in SOURCES['ProductController.java'] and '@NotNull' in SOURCES['CreateProductRequest.java']
for token in ['CH 11','JDBC','H2','NULL','가격 0','ORDER BY','CREATE TABLE IF NOT EXISTS','AtomicLong','MAX(id)+1','404','409','UNIQUE','트랜잭션','재시작','Repository','personal-project/','[11/12][이름] 기존 과제 DB 연동','Issue 1개·PR 1개']:
 assert token in visible,token
titles=[x['title'] for x in meta]
assert titles.index('책에서 함께 읽을 부분')<titles.index('상품 API를 DB에 연결')<titles.index('과제')<titles.index('기존 위시리스트를 DB에 저장')
assert titles.count('과제')==1
for token in ['교시','45분','practice/product-validation','docs/product-crud-design','Closes #','필수 Issue 2개','자가 병합']:
 assert token not in visible,token
assert 'HTTP 검증·예외 처리 보충 코드' in slides[-1].text_content()
module=ast.parse((OUT.parent/'2026-11-07/source/code_examples.py').read_text())
canonical=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCES' for t in n.targets))
assert all(v==canonical[k] for k,v in SOURCES.items())
assert 'jdbc:h2:file:./data/products' in visible and 'jdbc:h2:file:./data/wishlist' in visible
assert 'jdbc:h2:mem:db_basics' in visible

js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: root should check navigation JavaScript syntax')
print(f'{DAY}: {len(slides)} book-led slides; canonical source-data and whitespace intact; chapter/work/completion flow; read-only navigation verified')
