from pathlib import Path
import json,re,subprocess,tempfile
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
raw=(OUT/'index.html').read_text();doc=html.fromstring(raw)
slides=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
sources=json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
private=json.loads((R/'metadata-private.json').read_text())
assert len(slides)==len(meta)==len(private)
assert 8 <= len(slides) <= 16
assert sources==SOURCES
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
ids=doc.xpath('//@id');assert len(ids)==len(set(ids))
for i,(slide,record) in enumerate(zip(slides,meta)):
 title=slide.xpath('./h1')[0].text_content()
 assert title==re.sub('<[^>]*>','',record['title'])
 assert f'{i+1:02} / {len(slides):02}' in slide.text_content()
 assert not slide.xpath('.//pre'), 'Code belongs in the book/worksheet/reference viewer, not lecture slides'
for key,source in sources.items():
 assert doc.xpath('//*[@data-source-key=$k]',k=key),key
 for n,line in enumerate(source.splitlines(),1):
  assert '\t' not in line and line==line.rstrip(),f'{key}:{n}: whitespace'
  assert (len(line)-len(line.lstrip(' ')))%4==0,f'{key}:{n}: indentation'
text='\n'.join(s.text_content() for s in slides)
assert not re.search(r'Wiki|위키',text,re.I)
for token in ['CH 11','JDBC','JPA','작업지','sesac-spring-boot-study','README','Closes #실제번호','gradle-wrapper.jar']:
 assert token in text,token
assert 'contenteditable=' not in raw and 'localStorage' not in raw
assert (OUT/'INSTRUCTOR.md').exists()
for name in ['INSTRUCTOR.md','BEGINNER-WORKSHEET.md','STUDENT-WORKSHEET.md','HANDOFF.md']:
 p=OUT/name
 if p.exists():assert not re.search(r'Wiki|위키',p.read_text(),re.I),name
for href in doc.xpath('//a/@href'):
 if href.startswith(('http:','https:','#','mailto:')):continue
 target=(OUT/href.split('#')[0]).resolve()
 assert target.exists(),href
if OUT.name.endswith('16'):
 assert len(sources)==3
 for token in ['Memory','19일','flush','clear','rollback','BEGINNER-WORKSHEET.md']:
  assert token in text or token in raw,token
 worksheet=(OUT/'BEGINNER-WORKSHEET.md').read_text()
 for token in ['ProductEntity','SpringDataProductRepository','price <= 1000','실제 id','rollback','Memory','19일']:
  assert token in worksheet,token
elif OUT.name.endswith('19'):
 assert len(sources)==4
 for token in ['이준형','STUDENT-WORKSHEET.md','HANDOFF.md','실제 id','재시작','400','404','practice/product-jpa-migration','open-in-view=false','jdbc:h2:file:./data/products']:
  assert token in text or token in raw,token
 assert doc.xpath('//a[@href="assets/product-api-start.zip"]')
 assert (OUT/'assets'/'product-api-start.zip').is_file()
else:
 assert len(sources)==6
 for token in ['3개 주문','4 SELECT','1 SELECT','flush','clear','practice/jpa-query-lab','order-query-lab','EntityGraph','CDN','HTML','CSS','JavaScript']:
  assert token in text,token
 assert doc.xpath('//a[@href="assets/order-query-lab.zip"]')
 assert (OUT/'assets'/'order-query-lab.zip').is_file()
js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('Node unavailable; root must check JS syntax')
print(OUT.name,len(slides),'book-led slides;',len(sources),'exact source references; links/metadata/indentation/JS valid')
print('Scope: lecture navigation/worksheets checked. Existing Java and ZIP files are unchanged; DB and HTTP execution are not rerun for this prose change.')
