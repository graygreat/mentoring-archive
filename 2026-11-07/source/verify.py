from pathlib import Path
import json,re,subprocess,tempfile,sys
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
text=(OUT/'index.html').read_text();d=html.fromstring(text)
slides=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(d.xpath('//script[@id="deck-data"]/text()')[0]);sources=json.loads(d.xpath('//script[@id="source-data"]/text()')[0])
assert len(slides)==len(meta)==109
assert sources==SOURCES and len(sources)==12

# Concepts precede all project creation, file writing, and configuration exercises.
titles=[x['title'] for x in meta]
chapters=[x['ch'] for x in meta]
practice_start=titles.index('실습 A · 상품 객체와 저장소')
aop_start=chapters.index('AOP 실습 · 의존성')
b_start=titles.index('실습 B · 상품 API 완성')
c_start=titles.index('실습 C · 검증과 예외 응답')
share_start=titles.index('검증하고 설명하기')
assert practice_start < aop_start < b_start < c_start < share_start
assert titles.index('기본 포트를 바꿔 봅니다') > practice_start
for title in ['실행 준비와 공통 처리','Spring MVC와 REST API',
              '입력 규칙을 요청 DTO에 표시합니다','입력 형식과 업무 규칙을 지킵니다',
              '여러 Controller의 오류 응답을 모읍니다',
              '단위 테스트와 API 확인은 다릅니다','테스트용 객체로 바꿀 수도 있습니다']:
 assert titles.index(title) < practice_start, title
assert not any(x.xpath('./button[@data-source-key]') for x in slides[:practice_start])
assert not any(x['ch'].startswith(('실습 A ·','실습 B ·','실습 C ·','AOP 실습 ·')) for x in meta[share_start:])
assert [x.get('data-index') for x in slides]==[str(i) for i in range(len(slides))]
assert [x.get('data-slide-id') for x in slides]==[f'lesson3-{i}' for i in range(len(slides))]
assert d.xpath('//body/@data-deck-revision')==['2026-11-07-v2-practice-last']

ids=d.xpath('//@id');assert len(ids)==len(set(ids)), 'duplicate HTML/SVG IDs'
assert len(d.xpath('//svg'))==14
assert not d.xpath('//*[@contenteditable]') and 'localStorage' not in text
assert not any('note' in x for x in meta)
assert not re.search('GRAY|강사 시연',text,re.I)
assert all(b.get('data-source-key') in SOURCES for b in d.xpath('//button[@data-source-key]'))
for key,src in sources.items():
 # All lines of every canonical file appear on slide code pages, in order.
 shown='\n'.join(s.xpath('.//pre/code/text()')[0] for s in slides if s.xpath('./button[@data-source-key=$k]',k=key))
 assert re.sub(r'\s+','',src)==re.sub(r'\s+','',shown),key
assert all(len(s.xpath('.//pre/code/text()')[0].splitlines())<=14 for s in slides if s.xpath('./button[@data-source-key]'))
assert 'spring-boot-starter-aspectj' in text and 'spring-boot-starter-validation' in text
assert '@Valid @RequestBody CreateProductRequest request' in SOURCES['ProductController.java']
assert 'private Integer price' in SOURCES['CreateProductRequest.java']
assert 'HttpMessageNotReadableException.class' in SOURCES['ApiExceptionHandler.java']
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
print('PASS: 109 slides, 14 diagrams, 12 full source files, unique IDs, concepts-before-practice order, code-page integrity, read-only publication, JavaScript syntax')
print('Scope: Java core execution verified; actual Spring server and browser rendering are not exercised by this checker.')
