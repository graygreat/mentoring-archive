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
DAY='2026-11-16'
TITLE='상품 Entity와 JPA 저장소'
from code_examples import DAY16_PROPERTIES, TEST_PROPERTIES, JPA_DEPENDENCIES
def source_choices():
 return '<div class="references">'+''.join('<button type="button" data-source-key="'+esc(name)+'"><b>'+esc(name)+' ↗</b><span>작업 뒤 수업 참고 구현과 비교</span></button>' for name in SOURCES)+'</div>'
add('2026.11.16 · 4시간','책의 상품 저장에서<br>JPA 실습으로','<div class="cover-bottom"><strong>책을 읽고 · 작업지로 실행하고 · SQL로 확인합니다</strong><span>공통 product-api 유지 · DB 연결은 오늘 따로 연습</span></div>',kind='cover')
add('책을 펼칠 곳','CH 11을 읽고 저장 경로를 찾습니다',table([['읽을 자료','함께 찾을 것'],['CH 11 · 상품 관리 DB 연동','상품을 저장·조회하는 코드와 Repository 역할'],['CH 12 · 추상화와 테스트 복습','저장 구현을 바꾸어도 유지할 약속'],['수업 보충 · JPA 작업지','같은 상품을 Entity와 SQL로 저장·조회']])+call('책의 JDBC 접근과 수업의 JPA는 구현 방식이 다릅니다. 실제 판본에서 읽을 절을 표시합니다.'))
add('네 교시 운영','책 → 작업지 → 실행 결과',table([['교시','활동 45분 + 휴식·정리 15분'],['1','책 DB 접근 읽기 · 상품 표와 Entity 연결'],['2','Entity·Repository 작성 · 저장과 실제 id 조회'],['3','가격 조건·JPQL 조회 · 기대 결과 비교'],['4','변경 감지 관찰 · 두 DB 구분 · 19일 준비']]),note='강사 코딩 시연 없이 책을 함께 읽고 작업지 단계별로 멘티가 실행합니다. DB 전제가 어려우면 공통 DB 작업지로 돌아갑니다.')
add('프로젝트 경계','JPA 테스트와 실제 API를 구분합니다',table([['오늘 JPA 연습','오늘 실제 상품 API'],['ProductEntity · SpringDataProductRepository','Controller → Service → Memory 저장소'],['별도 테스트 DB · 기본 rollback','기존 CRUD·400·404 유지'],['저장·조회·SQL을 테스트로 확인','JPA Adapter 연결은 19일']])+call('공통 product-api를 이어 사용합니다. 주말 personal-project와 섞지 않습니다.'))
add('CH 11 · 읽기 질문','상품 한 개를 저장할 때 무엇이 필요할까요?',steps('책에서 상품 필드와 저장·조회 위치를 찾습니다','상품 표의 id·name·price를 Java 필드와 연결합니다','id를 직접 정할지 저장 뒤 받을지 책과 비교합니다')+call('<a href="BEGINNER-WORKSHEET.md">JPA 첫 실습 작업지 ↗</a> · <a href="../shared/db-basics/STUDENT-WORKSHEET.md">DB 기초 작업지 ↗</a>'))
add('작업지 0~2','표를 읽고 Entity·Repository를 준비합니다',steps('작업지의 상품 표를 먼저 채웁니다','기존 코드·테스트를 보존하고 JPA·H2 설정을 확인합니다','ProductEntity와 SpringDataProductRepository를 작성합니다','id·이름·가격이 어느 열과 연결되는지 설명합니다'),note='의존성·main/test 설정·기본 생성자·두 Repository의 차이는 작업지에서 한 단계씩 확인합니다. Java 비교 파일은 마지막 참고 자료 버튼에 있습니다.')
add('작업지 3','저장한 상품을 실제 id로 다시 조회합니다',steps('노트 3000원을 저장하기 전 기대 값을 적습니다','저장 반환값에서 실제 id를 읽습니다','clear 뒤 같은 id를 조회해 이름·가격을 비교합니다','테스트 결과와 SQL에서 저장·조회 근거를 찾습니다')+call('id가 1부터 연속일 것이라고 가정하지 않습니다.'))
add('작업지 4','가격 조건을 먼저 예측하고 실행합니다',steps('price <= 1000이면 어떤 상품이 남는지 적습니다','조건 메서드와 JPQL의 기대 결과를 비교합니다','결과의 경계값·빈 결과·id 정렬을 확인합니다')+call('테이블·열 이름과 Entity·필드 이름의 차이는 책과 작업지에서 확인합니다.'))
add('작업지 5','변경한 가격이 DB에 반영됐는지 확인합니다',steps('조회한 노트의 가격을 바꾼 뒤 예상 SQL을 적습니다','flush → clear → 재조회 순서로 실행합니다','작업지에 변경 전·후 가격과 SQL을 기록합니다')+call('flush와 commit은 다릅니다. 오늘 테스트는 끝나면 기본 rollback입니다.'))
add('작업지 6 · 완료 점검','테스트 DB와 실행 DB를 따로 설명합니다',table([['확인할 것','완료 근거'],['JPA 테스트','실제 id · 저장 값 · 조건 결과 · 변경 값 일치'],['실제 HTTP','기존 Memory 상품 CRUD·400·404 유지'],['DB 설정','main 파일 DB와 test 메모리 DB 구분'],['19일 준비','두 Repository를 연결할 위치 표시']]),note='테스트 성공을 실행 서버의 JPA 전환이나 재시작 보존 성공으로 발표하지 않습니다. 예제의 긴 이름 매핑은 기존 계약 보존용이며 업무 길이 정책을 새로 정하는 활동이 아닙니다.')
add('설명과 점검','자기 실행 결과를 짧게 설명합니다',steps('노트 한 개가 객체와 표에서 어떻게 보이는지 설명','실제 id와 SELECT 결과를 보여주기','flush·clear 뒤 재조회가 필요한 이유 설명','어려웠던 한 단계와 다음 확인할 점 기록'))
add('GitHub 제출','product-api의 JPA 연습을 기록합니다',table([['항목','지정 값'],['저장소 · 브랜치','sesac-spring-boot-study · practice/product-jpa-basics'],['Issue · PR','[실습] 상품 Entity와 JPA 저장소'],['완료 근거','README 실행 방법 · 테스트·SQL 결과 · Closes #실제번호']])+call('Issue 1개 · 병합 PR 1개. gradle-wrapper.jar와 기존 테스트 유지 · DB 파일과 비밀값은 제외합니다.'))
add('19일로 연결','API 저장소 교체 전까지 준비할 것',steps('Memory CRUD와 JPA 테스트를 모두 통과시킵니다','main과 test 설정·실행 폴더를 확인합니다','최신 main과 재현 가능한 오류·질문을 준비합니다')+call('<a href="../2026-11-19/STUDENT-WORKSHEET.md">19일 작업지 ↗</a> · 단축 URL은 <a href="../assignments/short-url/">별도 과제 ↗</a>입니다.'))
add('작업 뒤 참고','책·작업지와 비교할 자료','<p><a href="BEGINNER-WORKSHEET.md">JPA 첫 실습 작업지 ↗</a> · <a href="../shared/db-basics/">DB 기초 안내 ↗</a></p>'+source_choices(),note='전체 Java 파일은 수업 독립 참고 구현입니다. 책의 정답 코드라고 부르지 않습니다. 먼저 직접 작성하고 막힌 메서드만 비교합니다.')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 교재 상품 관리 자율 실습"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v2-book-led"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
