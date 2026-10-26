from pathlib import Path
import json,re,subprocess,tempfile
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
assert len(slides)==len(meta)==len(private) and 35<=len(slides)<=65
assert sources==SOURCES and len(sources)==3
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
assert doc.xpath('//body/@data-deck-revision')==[DAY+'-v1-curriculum']
titles=[s['title'] for s in meta];chapters=[s['ch'] for s in meta]
practice=next(i for i,s in enumerate(meta) if s['title'].startswith('자율 실습'))
assert not any(d['source'] for d in private[:practice])
# Joining code page text reconstructs each file, including all leading spaces.
for name,source in SOURCES.items():
 pieces=[]
 for slide,record in zip(slides,private):
  if record['source']==name:
   part=slide.xpath('.//pre/code/text()')
   assert len(part)==1
   assert len(part[0].splitlines())<=14
   pieces.append(part[0])
 assert '\n'.join(pieces)==source.rstrip('\n'),name
 assert 'package com.example.product;' in source
 assert not '\t' in source
text=doc.text_content()
for x in ['sesac-spring-boot-study','product-api/','greeting-api','Closes #実際番号' if False else 'Closes #실제번호','Home','01-Setup','02-Architecture','03-API','04-Verification','05-Retrospective','gradle-wrapper.jar','기존','README','Wiki']:
 assert x in text,x
assert 'Initializr 재생성' not in text or '않' in text
if DAY.endswith('09'):
 assert set(SOURCES)=={'CreateProductRequest.java','ProductResponse.java','ProductController.java'}
 assert 'jakarta.validation' not in ''.join(SOURCES.values())
 assert '@Valid' not in SOURCES['ProductController.java']
 assert 'Integer price' in SOURCES['CreateProductRequest.java']
 for x in ['201','Location','빈 목록','id 오름차순','400','404','중간','practice/product-rest','product-api-2026-11-09','필수 Issue 1개','이름 검색','가격 필터']:
  assert x in text,x
 assert titles.index('HTTP 계약을 먼저 정합니다')<practice
 assert titles.index('Java 객체와 JSON의 경계')<practice
 assert titles.index('별도 과제 · 조회 조건 확장')>practice
else:
 assert set(SOURCES)=={'CreateProductRequest.java','ProductController.java','ApiExceptionHandler.java'}
 assert '@Valid @RequestBody' in SOURCES['ProductController.java']
 assert '@NotNull' in SOURCES['CreateProductRequest.java']
 for x in ['400','404','가격 0','불변','멱등','Level 0','Level 1','Level 2','Level 3','가정','교재 근거','short-url/docs/design.md','14일','practice/product-validation','docs/short-url-design','필수 Issue 2개','선택 검색 보존','findAll 검색 코드']:
  assert x in text,x
 assert titles.index('HTTP와 REST를 설명하기')<practice
 assert titles.index('교재 과제 기반 설계 · 2시간')>practice
# Canonical complete reference files match the 7-day source module without executing it.
import ast
module=ast.parse((OUT.parent/'2026-11-07/source/code_examples.py').read_text())
canonical=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCES' for t in n.targets))
if DAY.endswith('12'):
 assert all(v==canonical[k] for k,v in SOURCES.items())
else:
 assert SOURCES['ProductResponse.java']==canonical['ProductResponse.java']
 assert SOURCES['ProductController.java']==canonical['ProductController.java'].replace('import jakarta.validation.Valid;\n','').replace('@Valid @RequestBody','@RequestBody')
# Avoid private notes appearing in shipped HTML; read-only controls only.
assert 'contenteditable=' not in raw and 'localStorage' not in raw
assert (OUT/'INSTRUCTOR.md').exists()
js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: JS syntax check delegated to environment runtime')
print(f'{DAY}: verified {len(slides)} slides; 3 exact source files; ordered curriculum; read-only navigation; stage contracts')
