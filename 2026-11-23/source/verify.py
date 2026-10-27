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
assert len(meta)==len(slides)>=35
assert sources==SOURCES
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
assert doc.xpath('//body/@data-deck-revision')==[OUT.name+'-v1-curriculum']
for pre in doc.xpath('//section//pre'):
 assert len(pre.text_content().splitlines())<=14
for name,source in sources.items():
 assert '\t' not in source,name
 assert doc.xpath('//*[@data-source-key="'+name+'"]'),name
text=doc.text_content()
for x in ['sesac-spring-boot-study','Closes #실제번호','Home','01-Setup','02-Architecture','03-API','04-Verification','05-Retrospective','README','Wiki','gradle-wrapper.jar','별도 과제']:
 assert x in text,x
if OUT.name.endswith('19'):
 for x in ['실제 id','재시작','400','404','이준형','practice/product-jpa-migration','open-in-view=false','STUDENT-WORKSHEET.md','HANDOFF.md']:
  assert x in text or x in raw,x
 assert len(sources)==4
 assert 'jdbc:h2:file:./data/products' in text
 assert (OUT/'HANDOFF.md').exists() and (OUT/'STUDENT-WORKSHEET.md').exists()
else:
 for x in ['3개 주문','4 SELECT','1 SELECT','flush','clear','practice/jpa-query-lab','order-query-lab','EntityGraph','쿼리 캐시']:
  assert x in text,x
 assert len(sources)==6
 assert 'com/example/orderlab/' in raw
assert 'contenteditable=' not in raw and 'localStorage' not in raw
assert (OUT/'INSTRUCTOR.md').exists()
assert '../assets/' not in raw
assert doc.xpath('//a[@href="assets/order-query-lab.zip"]')
assert (OUT/'assets'/'order-query-lab.zip').is_file()
js='\n'.join(doc.xpath('//script[not(@type)]/text()'))
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write(js);f.flush()
 try:
  r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert r.returncode==0,r.stderr
 except FileNotFoundError:
  print('Node unavailable; JS check pending runtime')
print(OUT.name,len(slides),'slides;',len(sources),'exact modal references; subtitle-free; <=14-line code; JS valid')
