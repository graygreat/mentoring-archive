from pathlib import Path
import html,json,re,textwrap
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
S=[]
def esc(s):return html.escape(str(s))
def code(s,*,preserve_whitespace=False):
 # File continuations retain their original indentation, including the first line.
 rendered=s if preserve_whitespace else textwrap.dedent(s).strip('\n')
 return '<pre><code>'+esc(rendered)+'</code></pre>'
def call(s):return '<div class="callout">'+s+'</div>'
def table(rows):return '<table class="lesson-table">'+''.join('<tr>'+''.join(f'<{("th" if i==0 else "td")}>{x}</{("th" if i==0 else "td")}>' for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
def steps(*xs):return '<ol class="steps">'+''.join('<li>'+x+'</li>' for x in xs)+'</ol>'
def cards(*xs):return '<div class="cols'+(' three' if len(xs)==3 else '')+'">'+''.join('<div class="card"><div class="eyebrow">'+a+'</div><h3>'+b+'</h3><p>'+c+'</p></div>' for a,b,c in xs)+'</div>'
def add(ch,title,body='',sub='',note='',kind='',source=None):S.append(dict(ch=ch,title=title,body=body,sub=sub,note=note,kind=kind,source=source))
def section(n,title,sub):add(title,title,'<div class="section-number">'+n+'</div>',sub,kind='section')
def filepages(ch,key,goal):
 lines=SOURCES[key].splitlines();chunks=[lines[i:i+14] for i in range(0,len(lines),14)]
 for i,chunk in enumerate(chunks):
  add(ch,key+f' · {i+1}/{len(chunks)}',code('\n'.join(chunk),preserve_whitespace=True),f'{goal} · '+('파일 처음부터 작성' if i==0 else '앞 코드 바로 다음 줄에 이어 작성'),note='전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.',kind='code-slide file-slide',source=key)
# SVG diagrams are native vector drawings; no external image or font dependency.
_diagram_id=0
def svg(title,inner,h=300):
 global _diagram_id
 _diagram_id+=1
 return '<svg class="diagram" viewBox="0 0 1148 '+str(h)+'" role="img" aria-label="'+esc(title)+'"><title>'+esc(title)+'</title><defs><marker id="arrow-'+str(_diagram_id)+'" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9" fill="none" stroke="#087f5b" stroke-width="1.5"/></marker></defs>'+inner.replace('url(#arrow)',f'url(#arrow-{_diagram_id})')+'</svg>'
def box(x,y,w,h,title,sub='',fill='#edf5ee'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#9fbea9" stroke-width="2"/><text x="{x+w/2}" y="{y+45}" text-anchor="middle" fill="#16251f" font-size="25" font-weight="700">{esc(title)}</text>'+('' if not sub else f'<text x="{x+w/2}" y="{y+81}" text-anchor="middle" fill="#52665a" font-size="19">{esc(sub)}</text>')
def arrow(x1,y1,x2,y2,label=''):
 return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'+('' if not label else f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-14}" text-anchor="middle" fill="#087f5b" font-size="17">{esc(label)}</text>')
def linear(title,nodes):
 n=len(nodes);gap=38;w=(1148-gap*(n-1))/n;inner=''
 for i,(name,desc) in enumerate(nodes):
  x=i*(w+gap);inner+=box(x,75,w,120,name,desc)
  if i<n-1:inner+=arrow(x+w+5,135,x+w+gap-7,135)
 return svg(title,inner)
def container():
 inner='<rect x="18" y="10" width="1112" height="270" rx="18" fill="#f3f7ee" stroke="#087f5b" stroke-width="2" stroke-dasharray="8 5"/><text x="45" y="48" fill="#087f5b" font-size="23" font-weight="700">Spring 컨테이너 · 객체를 만들고 연결하는 곳</text>'
 inner+=box(62,100,290,125,'Controller 빈','요청 받기')+box(430,100,290,125,'Service 빈','업무 진행')+box(798,100,290,125,'Repository 빈','상품 저장·조회')+arrow(362,162,420,162)+arrow(730,162,788,162)
 return svg('Spring 컨테이너 안에서 Controller, Service, Repository 빈의 의존성이 연결됩니다',inner)
def singleton():
 return svg('여러 요청이 하나의 Service 빈을 공유합니다',box(18,20,260,105,'요청 A','상품 목록 조회')+box(18,160,260,105,'요청 B','상품 생성')+box(550,90,420,125,'ProductService 빈 하나','요청마다 새로 만들지 않음')+arrow(290,74,538,130)+arrow(290,214,538,160))
def mvc():
 inner=box(5,20,235,110,'브라우저·도구','HTTP 요청')+box(300,20,250,110,'DispatcherServlet','요청 처리 조율')+box(610,20,240,110,'HandlerAdapter','메서드 호출 지원')+box(910,20,233,110,'Controller','Java 메서드 실행')
 inner+=arrow(250,75,290,75)+arrow(560,75,600,75)+arrow(860,75,900,75)+box(290,185,270,105,'HandlerMapping','담당 핸들러 찾기')+arrow(425,140,425,175,'조회')
 return svg('DispatcherServlet이 HandlerMapping으로 담당 핸들러를 찾고 HandlerAdapter로 Controller 호출을 위임합니다',inner,310)
def proxy():return linear('호출이 프록시를 지나 실제 Service로 전달되고 공통 처리가 앞뒤에서 실행됩니다',[('호출하는 코드','Service를 사용'),('프록시','공통 처리 → 위임'),('실제 Service','상품 업무 처리')])
add('책과 함께 · 4시간','책의 상품 기능을<br>HTTP로 연결합니다','<div class="cover-bottom"><strong>CH 09 · 상품 관리 애플리케이션</strong><span>기존 product-api → 생성·조회 API → Postman 확인</span></div>',kind='cover')
add('오늘의 진행','책을 읽고, 작성하고, 요청합니다',table([['교시','함께 할 일'],['1','CH 09 · 상품 구조와 DTO 읽기'],['2','생성·조회 코드를 책에서 찾아 직접 작성'],['3','부록 A · Postman으로 요청·응답 확인'],['4','오류 보완 · 설명 · README와 PR 제출']])+call('매 교시 45분 활동 + 15분 휴식·정리 · 강사 코딩 시연 없음'))
section('01','교재 CH 09를 펼칩니다','')
add('읽을 곳','상품 추가와 조회를 찾아봅시다',steps('데이터 구조 정의하기 → 상품 추가 구현 및 프로젝트 구조','DTO와 getter, setter → 상품 조회 부분','책에서 입력·업무 처리·저장을 맡는 클래스를 표시'),note='교재 CH 09의 실제 소제목을 기준으로 찾습니다. 사용 판본의 쪽수를 각자 표시합니다. 수정·삭제 구현은14일 범위입니다. 공통 수업 프로젝트product-api는7일코어와테스트를그대로유지합니다.')
add('책을 보며 질문','요청값과 상품 객체는 무엇이 다른가요?',steps('요청의 name·price는 어떤 객체가 받나요?','상품 id는 누가 정하고 어디에 담나요?','저장한 Product를 어떤 응답 객체로 바꾸나요?'),note='DTO·도메인 차이는 책의 해당 코드를 함께 보며 설명합니다. PPT에서 같은 코드를 다시 강의하지 않습니다. CreateProductRequest·ProductResponse·ProductController 세 파일을 작성하며 기존Service/Repository계약은보존합니다.')
add('직접 작성','기존 product-api에 세 파일 추가',table([['작성할 파일','책과 비교할 책임'],['CreateProductRequest','name · price 입력'],['ProductResponse','id · name · price 응답'],['ProductController','생성·목록·단건 요청을 기존 Service에 연결']])+call('Initializr로 새로 만들지 않습니다. 기존 단위 테스트와 AOP를 보존합니다.'),note='책을 보면서 직접 작성합니다. 제공 source-data는 독립 참고 코드이며 교재 원문이 아닙니다. price는 Integer로 유지해12일누락/null검증으로이어갑니다. 오늘@RequestBody정상요청만, @Valid와예외처리기는12일입니다.')
add('완료 기준','정상 요청 세 가지를 확인합니다',table([['요청','확인할 결과'],['POST /products','201 · Location · 생성한 상품 JSON'],['GET /products','200 · 빈 목록 [] · id 오름차순'],['GET /products/{id}','POST로 받은 실제 id · 200 · 같은 상품']])+call('메모리 저장소이므로 서버를 재시작하면 상품은 초기화됩니다.'))
section('02','부록 A · Postman으로 확인합니다','')
add('실행 순서','서버를 만든 뒤 실제 요청을 보냅니다',steps('product-api/에서 기존 테스트 실행 → 서버 시작','빈 목록 조회 → 상품 두 개 생성','생성한 실제 id와 Location 기록 → 단건·목록 조회','상태·헤더·본문을 기대값과 비교'),note='명령은 ./gradlew test 뒤 ./gradlew bootRun입니다. Windows는 .\\gradlew.bat test / bootRun을사용합니다. 실행중인터미널을유지하고다른작업시새터미널을사용합니다. id=1을가정하지않고POST반환값을사용합니다. JSON속성순서는검증하지않습니다. AOP0ms도정상입니다.')
add('질문과 확인','책의 요청 하나를 내 코드로 설명합니다',steps('JSON → 요청 DTO → Service 호출 위치 찾기','201과 Location을 정한 코드 찾기','Postman 응답과 테스트 결과를 각각 보여주기'),note='동작근거는실제실행화면으로확인합니다. 아직없는상품/잘못된값에대한오류응답은중간구현입니다. 오늘400·404를완료했다고요구하지않고12일CH10에서통일합니다.')
add('선택 과제','목록 조회에 조건을 추가합니다',table([['기능','수업에서 정한 기준'],['이름 검색','앞뒤 공백 제거 · 부분 일치 · 대소문자 구분'],['가격 필터','상한 포함 · 이름 조건과 AND · id 오름차순'],['공통','조건 없음은 전체 · 빈 결과 [] · 원본 보존']])+call('GET /products?name=노트&amp;maxPrice=3000<br>음수·숫자가 아닌 가격의 400 처리는12일 이후 · 정답 코드 없음'),note='쿼리 매개변수는 name과 maxPrice입니다. GET /products?name=노트&maxPrice=3000으로 두 조건을 함께 적용합니다. 선택브랜치 feature/name-search / feature/price-filter,제목[과제 1] 상품 이름 검색 / [과제 2] 가격 조건 검색. 단계마다Issue와PR추가,assignment라벨. 미완료선택과제를필수로강제하지않습니다.')
add('GitHub 제출','오늘 필수 Issue 1개 · 병합 PR 1개',table([['항목','지정 값'],['저장소 · 폴더','sesac-spring-boot-study / product-api/'],['브랜치','practice/product-rest'],['Issue · PR','[실습] 상품 생성·조회 REST API']])+call('README에 API·실제 결과 기록 → Closes #실제번호 → main 대상 PR'),note='본인Assignee,practice·docs라벨,milestone product-api-2026-11-09. main pull→Issue→branch→구현검증→commit/push→PR자체확인병합. 기존greeting-api와루트README링크를유지합니다. src·Gradle설정·Wrapper와gradle-wrapper.jar포함,build/.gradle/IDE/.env비밀값제외. 루트.gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar 보존. 별도문서PR강제없음.')
add('다음 책 읽기','12일에는 실패 응답과 CRUD 설계',cards(('앞 2시간','CH 10','잘못된 입력 400 · 없는 상품 404'),('뒤 2시간','CH 09 · CH 12','수정·삭제의 요구사항과 테스트 설계')))
add('읽기와 참고','교재와 보충 자료','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 목차 ↗</b><span>CH 09 · 부록 A</span></a><a href="https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestbody.html"><b>필요할 때만 보는 Spring 문서 ↗</b><span>요청 본문과 DTO</span></a></div>')

# Keep complete supplementary files reachable without restoring code lecture pages.
S[-1]['body'] += '<div class="inline-list">'+''.join('<button type="button" data-source-key="'+esc(key)+'">'+esc(key)+'</button>' for key in SOURCES)+'</div>'
S[-1]['note'] += ' 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.'
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-09-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.09</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 9장·부록 A와 함께 배우는 REST·DTO·JSON·Postman 실습"><title>11월 9일 · 상품 REST API 구현</title><style>'+css+'</style></head><body data-deck-revision="2026-11-09-v1-curriculum"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',len(out.encode()),'bytes')
