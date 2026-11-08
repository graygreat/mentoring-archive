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
assert 20<=len(slides)<=34
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
assert 'personal-project/' in visible and '위시리스트 유효성 검사' in visible
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

assert set(SOURCES)=={'CreateProductRequest.java','ProductResponse.java','ProductController.java','ApiExceptionHandler.java'}
assert '@Valid @RequestBody' in SOURCES['ProductController.java']
assert 'Integer price' in SOURCES['CreateProductRequest.java']
for token in ['CH 09','CH 10','CH 11','발표','MVC','DispatcherServlet','HandlerMapping','HandlerAdapter','메시지 변환기','JSON','201','Location','400','404','500','QA','체크리스트','README','Fork','compare across forks','@NotBlank','@NotNull','@Min','@Valid']:
 assert token in visible,token
titles=[x['title'] for x in meta]
assert '상품 API의 응답 코드 읽기' not in titles
for token in ['교시','45분','practice/product-rest','Closes #','병합 PR','@RequestParam','@PathVariable']:
 assert token not in visible,token
assert titles.index('개인 과제 발표')<titles.index('DispatcherServlet과 Controller')<titles.index('QA 체크리스트 작성과 실행')
assert len(doc.xpath('//section//svg'))>=2
module=ast.parse((OUT.parent/'2026-11-07/source/code_examples.py').read_text())
canonical=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCES' for t in n.targets))
assert SOURCES['ProductResponse.java']==canonical['ProductResponse.java']
validation_module=ast.parse((OUT.parent/'2026-11-12/source/code_examples.py').read_text())
validation=next(ast.literal_eval(n.value) for n in validation_module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCES' for t in n.targets))
for key in validation:
 assert SOURCES[key]==validation[key],key

js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: root should check navigation JavaScript syntax')
print(f'{DAY}: {len(slides)} book-led slides; canonical validation source-data; MVC, response, QA and submission coverage; read-only navigation verified')
