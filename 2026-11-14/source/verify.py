from pathlib import Path
import json,re,subprocess,tempfile
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
raw=(R.parent/'index.html').read_text();doc=html.fromstring(raw)
slides=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(doc.xpath('//script[@id="deck-data"]/text()')[0])
sources=json.loads(doc.xpath('//script[@id="source-data"]/text()')[0])
private=json.loads((R/'metadata-private.json').read_text())
assert len(slides)==len(meta)==len(private)
assert len(slides)>=35
assert sources==SOURCES
assert not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert len(set(doc.xpath('//section/@data-slide-id')))==len(slides)
assert [s.get('data-index') for s in slides]==list(map(str,range(len(slides))))
for key,source in SOURCES.items():
 pieces=[]
 for slide,record in zip(slides,private):
  if record['source']==key:
   code=slide.xpath('.//pre/code/text()')
   assert len(code)==1 and len(code[0].splitlines())<=14
   pieces.append(code[0])
 assert '\n'.join(pieces)==source.rstrip('\n'),key
 assert '\t' not in source
text=doc.text_content()
for token in ['sesac-spring-boot-study','Closes #실제번호','Home','01-Setup','02-Architecture','03-API','04-Verification','05-Retrospective','gradle-wrapper.jar','메모리' if False else 'Memory','../assignments/short-url/']:
 assert token in (raw if token.startswith('../') else text),token
assert 'contenteditable=' not in raw and 'localStorage' not in raw
assert (R.parent/'INSTRUCTOR.md').exists()
with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
 f.write('\n'.join(doc.xpath('//script[not(@type)]/text()')));f.flush()
 try:
  result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
  assert result.returncode==0,result.stderr
 except FileNotFoundError:
  print('node unavailable: root should check JS syntax')
print(R.parent.name, len(slides), 'slides verified; exact whitespace; date sources; no subtitles')
