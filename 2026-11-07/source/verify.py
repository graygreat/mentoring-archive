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
assert 16 <= len(slides) <= 24 and len(slides)==len(meta)
assert sources=={k:SOURCES[k] for k in expected_keys}
assert not any(k in sources for k in ['ProductController.java','CreateProductRequest.java','ProductResponse.java','ApiExceptionHandler.java'])
assert [x.get('data-index') for x in slides]==[str(i) for i in range(len(slides))]
assert [x.get('data-slide-id') for x in slides]==[f'lesson3-{i}' for i in range(len(slides))]
assert d.xpath('//body/@data-deck-revision')==['2026-11-07-v7-book-led']
titles=[x['title'] for x in meta]
assert titles.index('CH 09 · 상품 객체와 저장·조회') < titles.index('CH 12 · 추상화와 테스트 일부') < titles.index('개인 프로젝트 · 나만의 소장품 관리')
assert not any(s.xpath('.//pre') for s in slides)
source_buttons=d.xpath('//button[@data-source-key]')
assert len(source_buttons)==len(expected_keys)
assert {b.get('data-source-key') for b in source_buttons}==expected_keys
assert slides[-1].xpath('.//div[@class="inline-list"]/button[@type="button"]')==source_buttons
visible='\n'.join(s.text_content() for s in slides)
for excluded in ['@RequestBody','ResponseEntity','@RestController','@Valid','HTTP/1.1 201','PUT /products','DELETE /products','spring-boot-starter-webmvc','spring-boot-starter-validation']:
 assert excluded not in visible,excluded
for required in ['CH 09','CH 12','product-api/','personal-project/','CollectionItem','id, name, price','Repository','Service','최소 3개','105분','75분','휴식·정리 15분','앞 5명','뒤 6명','36분','9분','11명','발표 4분 + 질문 2분','DispatcherServlet','AOP','assignment/personal-core','practice/product-core','docs/product-core','sesac-spring-boot-study']:
 assert required in visible,required
assert 'Wiki' not in visible and '위키' not in visible
assert 45*2+15==105
assert 11*(4+2)+9==75
assert 105+75+4*15==4*60
assert 'CommandLineRunner' not in text
assert not d.xpath('//*[@contenteditable]') and 'localStorage' not in text
assert not any('note' in x for x in meta)
assert not d.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')
ids=d.xpath('//@id');assert len(ids)==len(set(ids))
for key,source in sources.items():
 for n,line in enumerate(source.splitlines(),1):
  assert '\t' not in line and line==line.rstrip(),f'{key}:{n}: whitespace'
  assert (len(line)-len(line.lstrip(' ')))%4==0,f'{key}:{n}: indentation'
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
print(f'PASS: {len(slides)} book-led slides; {len(sources)} unchanged stage-specific Java files; core behavior, time allocation, project boundary, IDs and JavaScript syntax')
print('Scope: independent Java core execution verified. Student personal projects and final browser layout are checked separately.')
