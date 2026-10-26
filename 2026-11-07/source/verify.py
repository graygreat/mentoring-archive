from pathlib import Path
import json,re,subprocess,tempfile,sys
from lxml import html
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
text=(OUT/'index.html').read_text();d=html.fromstring(text)
slides=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
meta=json.loads(d.xpath('//script[@id="deck-data"]/text()')[0]);sources=json.loads(d.xpath('//script[@id="source-data"]/text()')[0])
assert len(slides)==len(meta)==115
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
assert d.xpath('//body/@data-deck-revision')==['2026-11-07-v3-assignments']
# Independent assignments follow wrap-up and precede references, without answer files.
assignment_start=titles.index('별도 과제 · 상품 API 확장')
assert share_start < titles.index('요청 하나로 오늘 배운 것을 연결') < assignment_start
assert assignment_start < titles.index('교재와 공식 문서')
assignments=slides[assignment_start:-1]
assert len(assignments)==8
assert not any(x.xpath('./button[@data-source-key]') for x in assignments)
assert not any(x['ch'].startswith('빠른 팀') for x in meta)
assignment_text='\n'.join(x.text_content() for x in assignments)
for requirement in ['필수 1~2단계','도전 3~4단계','GET /products?name=노트',
                    'GET /products?maxPrice=5000','PUT /products/{id}','DELETE /products/{id}',
                    '200 + []','id 오름차순','두 조건을 모두 만족','204 · 응답 본문 없음',
                    '400 응답','404 응답','기존 이름·가격·id 유지','테스트 코드']:
 assert requirement in assignment_text,requirement
assert not re.search(r'public class|private final|@RestController',assignment_text)


ids=d.xpath('//@id');assert len(ids)==len(set(ids)), 'duplicate HTML/SVG IDs'
assert len(d.xpath('//svg'))==14
assert not d.xpath('//*[@contenteditable]') and 'localStorage' not in text
assert not any('note' in x for x in meta)
assert not re.search('GRAY|강사 시연',text,re.I)
assert all(b.get('data-source-key') in SOURCES for b in d.xpath('//button[@data-source-key]'))
file_page_count=0
for key,src in sources.items():
 # Compare each chunk verbatim: whitespace normalization hid broken continuation indents.
 lines=src.splitlines()
 expected=['\n'.join(lines[i:i+14]) for i in range(0,len(lines),14)]
 pages=[s for s in slides if s.xpath('./button[@data-source-key=$k]',k=key)]
 shown=[s.xpath('.//pre/code')[0].text_content() for s in pages]
 assert len(shown)==len(expected),f'{key}: file page count'
 for n,(actual,wanted) in enumerate(zip(shown,expected),1):
  assert actual==wanted,f'{key} page {n}: source whitespace mismatch'
 assert '\n'.join(shown)=='\n'.join(lines),f'{key}: full source reconstruction'
 file_page_count+=len(pages)
 # Canonical Java examples use four-space indentation and no tabs/trailing spaces.
 for n,line in enumerate(lines,1):
  assert '\t' not in line and line==line.rstrip(),f'{key}:{n}: whitespace'
  assert (len(line)-len(line.lstrip(' ')))%4==0,f'{key}:{n}: indentation'
assert file_page_count==25
# Audit all displayed blocks, including ordinary snippets and command/HTTP examples.
# Folder listings intentionally use two-space indentation; Java snippets use four.
java_snippet_markers=r'public |private |return |new |@(?:Configuration|RestController|PostMapping)|long started|try \{'
for n,block in enumerate(d.xpath('//pre/code'),1):
 snippet=block.text_content()
 for line_no,line in enumerate(snippet.splitlines(),1):
  assert '\t' not in line and line==line.rstrip(),f'code block {n}:{line_no}: whitespace'
  if re.search(java_snippet_markers,snippet):
   assert (len(line)-len(line.lstrip(' ')))%4==0,f'Java block {n}:{line_no}: indentation'
# Regression: Product's second page begins inside its constructor, eight spaces deep.
product_pages=[s for s in slides if s.xpath('./button[@data-source-key="Product.java"]')]
assert product_pages[1].xpath('.//pre/code')[0].text_content().startswith('        this.id = id;')
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
print('PASS: 115 slides, 14 diagrams, 12 full source files, unique IDs, concepts-before-practice order, 25 exact-whitespace code pages, all snippet whitespace, read-only publication, JavaScript syntax')
print('Scope: Java core execution verified; actual Spring server and browser rendering are not exercised by this checker.')
