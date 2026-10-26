from pathlib import Path
import json,re,subprocess,tempfile,sys
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
text=(OUT/'index.html').read_text();d=html.fromstring(text)
slides=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(d.xpath('//script[@id="deck-data"]/text()')[0]);sources=json.loads(d.xpath('//script[@id="source-data"]/text()')[0])
expected_keys={'ProductApplication.java','Product.java','ProductRepository.java','MemoryProductRepository.java','ProductNotFoundException.java','ProductService.java','ProductServiceTest.java','TimingAspect.java','ProductWiringTest.java'}
assert len(slides)==len(meta) and len(slides)>75
assert sources=={k:SOURCES[k] for k in expected_keys}
assert not any(k in sources for k in ['ProductController.java','CreateProductRequest.java','ProductResponse.java','ApiExceptionHandler.java'])
titles=[x['title'] for x in meta]
practice_start=titles.index('집중 실습 · 상품 객체와 저장소')
share_start=titles.index('검증하고 설명하기')
assignment_start=titles.index('별도 과제 · 객체와 테스트 확장')
for title in ['객체를 연결하는 Spring','실행 준비와 공통 처리','서버·클라이언트와 MVC','테스트 범위를 나눕니다']:
 assert titles.index(title)<practice_start,title
assert practice_start < share_start < assignment_start
assert not any(s.xpath('./button[@data-source-key]') for s in slides[:practice_start])
assert not any(s.xpath('./button[@data-source-key]') for s in slides[share_start:])
assert [x.get('data-index') for x in slides]==[str(i) for i in range(len(slides))]
assert [x.get('data-slide-id') for x in slides]==[f'lesson3-{i}' for i in range(len(slides))]
assert d.xpath('//body/@data-deck-revision')==['2026-11-07-v6-staged-core']
visible='\n'.join(s.text_content() for s in slides)
for excluded in ['@RequestBody','ResponseEntity','@RestController','@Valid','HTTP/1.1 201','PUT /products','DELETE /products','GET /products?','server.port=8081','spring-boot-starter-webmvc','spring-boot-starter-validation']:
 assert excluded not in visible,excluded
for required in ['1~8장','DispatcherServlet','HandlerMapping','HandlerAdapter','@Controller','@Service','@Repository','Model','View','List','Map','SpringBootTest','AopUtils','0ms','sesac-spring-boot-study','product-api/README.md','practice/product-core','docs/product-core','test/product-boundaries','feature/core-price-filter','Issue 2개 · 병합 PR 2개','Home','01-Setup','02-Architecture','03-API','04-Verification','05-Retrospective','!product-api/gradle/wrapper/gradle-wrapper.jar','Closes #12','Public / main','main pull']:
 assert required in visible,required
assert 'CommandLineRunner' not in text
assert not d.xpath('//*[@contenteditable]') and 'localStorage' not in text
assert not any('note' in x for x in meta)
assert not d.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
assert '교재 CH 09 · 12 일부 선행 · 1~8장 복습은 5일에' not in text
ids=d.xpath('//@id');assert len(ids)==len(set(ids))
file_page_count=0
for key,src in sources.items():
 lines=src.splitlines()
 expected=['\n'.join(lines[i:i+14]) for i in range(0,len(lines),14)]
 pages=[s for s in slides if s.xpath('./button[@data-source-key=$k]',k=key)]
 actual=[s.xpath('.//pre/code')[0].text_content() for s in pages]
 assert actual==expected,f'{key}: exact-whitespace source mismatch'
 assert '\n'.join(actual)=='\n'.join(lines),f'{key}: reconstruction'
 file_page_count+=len(pages)
 for n,line in enumerate(lines,1):
  assert '\t' not in line and line==line.rstrip(),f'{key}:{n}: whitespace'
  assert (len(line)-len(line.lstrip(' ')))%4==0,f'{key}:{n}: indentation'
for n,block in enumerate(d.xpath('//pre/code'),1):
 snippet=block.text_content()
 for line_no,line in enumerate(snippet.splitlines(),1):
  assert '\t' not in line and line==line.rstrip(),f'block{n}:{line_no}: whitespace'
  if re.search(r'public |private |return |new |@(?:Configuration|SpringBootTest)|long started|try \{',snippet):
   assert (len(line)-len(line.lstrip(' ')))%4==0,f'block{n}:{line_no}: indentation'
product_pages=[s for s in slides if s.xpath('./button[@data-source-key="Product.java"]')]
assert product_pages[1].xpath('.//pre/code')[0].text_content().startswith('        this.id = id;')
assert 'spring-boot-starter-aspectj' in visible
assert 'webEnvironment = SpringBootTest.WebEnvironment.NONE' in sources['ProductWiringTest.java']
assert 'AopUtils.isAopProxy(service)' in sources['ProductWiringTest.java']
# Execute the actual domain/repository/service logic independently of Spring.
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);classes=root/'classes';classes.mkdir()
 core=['Product.java','ProductRepository.java','MemoryProductRepository.java','ProductNotFoundException.java','ProductService.java']
 for key in core:
  source=re.sub(r'import org\.springframework\.stereotype\.[^;]+;','',SOURCES[key])
  source=re.sub(r'@(Service|Repository)\s*','',source)
  (root/key).write_text(source)
 (root/'Check.java').write_text('''package com.example.product;
import java.util.*;
import java.util.concurrent.*;
public class Check {
 static void ok(boolean value) { if (!value) throw new AssertionError(); }
 static void invalid(Runnable action) {
  try { action.run(); throw new AssertionError("expected invalid input"); }
  catch (IllegalArgumentException expected) {}
 }
 public static void main(String[] args) throws Exception {
  ProductRepository repo = new MemoryProductRepository();
  ProductService service = new ProductService(repo);
  ok(service.findAll().isEmpty());
  Product a = service.create("  노트  ",3000);
  Product b = service.create("무료 샘플",0);
  ok(a.getName().equals("노트") && b.getPrice()==0);
  ok(service.findById(a.getId()).getId()==a.getId());
  ok(service.findAll().size()==2);
  invalid(() -> service.create(null,1));
  invalid(() -> service.create("  ",1));
  invalid(() -> service.create("노트",-1));
  ok(service.findAll().size()==2);
  try { service.findById(999999); throw new AssertionError(); }
  catch (ProductNotFoundException expected) {}
  ok(new ProductService(repo).findAll().size()==2);
  ok(new ProductService(new MemoryProductRepository()).findAll().isEmpty());
  ExecutorService pool=Executors.newFixedThreadPool(4);
  List<Callable<Product>> jobs=new ArrayList<>();
  for (int i=0;i<100;i++) jobs.add(() -> service.create("펜",100));
  List<Future<Product>> results=pool.invokeAll(jobs);pool.shutdown();
  Set<Long> ids=new HashSet<>();
  for(Future<Product> r:results) ok(ids.add(r.get().getId()));
  ok(service.findAll().size()==102);
  long prev=0;
  for(Product p:service.findAll()){ok(p.getId()>prev);prev=p.getId();}
  System.out.println("PASS: actual Java core logic, invalid values, missing id, DI isolation, unique IDs and sorted results");
 }
}''')
 subprocess.run(['java','-m','jdk.compiler/com.sun.tools.javac.Main','-encoding','UTF-8','-d',str(classes),*[str(p) for p in root.glob('*.java')]],check=True)
 subprocess.run(['java','-cp',str(classes),'com.example.product.Check'],check=True)
subprocess.run(['node','--check',str(R/'engine.js')],check=True)
print(f'PASS: {len(slides)} slides, {len(sources)} stage-specific Java files, {file_page_count} exact-whitespace code pages; concepts precede practice; no future REST answer code; unique IDs; GitHub scope; JavaScript syntax')
print('Scope: independent Java core execution verified. Spring integration/AOP and visual layout require the separate rehearsal/browser checks.')
