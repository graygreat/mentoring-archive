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
def source_choices():
 return '<div class="references">'+''.join('<button type="button" data-source-key="'+esc(name)+'"><b>'+esc(name)+' ↗</b><span>작업 뒤 수업 참고 구현과 비교</span></button>' for name in SOURCES)+'</div>'
add('2026.11.23 · 4시간','책의 상품 관리에서<br>SQL 관찰로','<div class="cover-bottom"><strong>표 읽기 → SQL 예측 → 실행 → 결과 비교</strong><span>책은 상품 관리 · 관계와 N+1은 수업 보충 실습</span></div>',kind='cover')
add('책과 보충 자료','오늘 읽을 곳을 구분합니다',table([['자료','확인할 내용'],['CH 11 · 상품 관리 DB 연동','19일 상품 저장소 전환·재시작 결과'],['CH 12 · 테스트 복습','예상 결과와 실제 결과를 비교하는 방법'],['보충 order-query-lab','관계·영속성·LAZY·N+1 관찰'],['책 CH 14 · 주문 관리','전체 API 구현은 별도 선택 과제']])+call('교재 JDBC와 JPA 보충 실습을 구분합니다. 공통 product-api에 주문 관계를 추가하지 않습니다.'))
add('책에서 다시 찾기','19일 상품 한 개를 확인합니다',steps('책의 저장·조회 흐름과 본인 Repository 교체 위치 비교','실제 생성 id의 수정 값을 재시작 후 조회','main 파일 DB와 test DB를 구분해 설명','미완료 오류는 재현 방법과 함께 기록'))
add('실습 준비','작업지의 예측을 먼저 적습니다',table([['자료','사용 방법'],['<a href="BEGINNER-WORKSHEET.md">쉬운 실습 작업지 ↗</a>','1~4블록 순서·표·예측·결과 기록'],['<a href="assets/order-query-lab.zip">order-query-lab ZIP ↗</a>','별도 프로젝트에서 실행 · 개선 참고 코드 포함'],['<a href="../shared/db-basics/">DB 기초 ↗</a>','표·PK·FK·SQL JOIN이 어려울 때']])+call('먼저 예측하고 실행합니다. 참고 메서드는 직접 시도한 뒤 비교합니다.'))
add('네 교시 운영','책 확인 → 보충 실험 → 설명',table([['교시','활동 45분 · 휴식·정리 15분'],['1','상품 전환 피드백 · 주문 표·PK/FK·SQL 예측'],['2','한 주문의 LAZY · 같은 객체·flush/clear 관찰'],['3','3개 주문의 4 SELECT → 1 SELECT 비교'],['4','동료 설명 · 별도 과제 공유 · GitHub 제출']]))
add('작업지 1블록','주문 3행과 항목 6행을 연결합니다',steps('작업지 표에서 PK와 FK를 표시합니다','어느 주문에 노트·펜이 연결되는지 선을 긋습니다','SQL JOIN 결과를 먼저 적습니다','Java의 필드·컬렉션에서 같은 값을 찾습니다'))
add('작업지 2블록','필요한 시점에 어떤 SQL이 나오나요?',steps('주문 목록 조회 뒤 SQL을 예상합니다','label과 items에 차례로 접근해 로그를 기록합니다','같은 id의 객체를 clear 전·후로 비교합니다','flush → clear → 재조회 뒤 값을 확인합니다')+call('용어 설명이 필요하면 작업지의 해당 표로 돌아갑니다. 새 코드를 먼저 복사하지 않습니다.'))
add('실행 확인','테스트 출력과 보고서를 함께 봅니다',steps('order-query-lab 폴더에서 관찰 대상 테스트 실행','--info --rerun-tasks로 SQL 출력 확인','build/reports/tests/test/index.html의 Standard output 확인','관찰 후 전체 테스트 실행')+call('실행 명령은 작업지에 있습니다. Windows는 gradlew.bat를 사용합니다.'))
add('작업지 3블록','같은 결과를 4회와 1회로 읽습니다',table([['관찰','검증할 결과'],['기본 조회 · 각 items 접근','3개 주문 · 6개 항목 · 4 SELECT'],['fetch join · 같은 접근','같은 주문·항목·이름 · 1 SELECT'],['비교 전 준비','flush · clear · 통계 초기화'],['완료 조건','SQL 감소와 결과 값 동일성을 모두 확인']]),note='prepareStatementCount는 일반적으로 모든 SQL을 세므로 이 실습의 SELECT 전용 측정 구간을 확인합니다. 작업지의 준비 데이터와 캐시 조건을 바꾸지 않고 먼저 비교합니다.')
add('설명할 질문','정의보다 본인 실험으로 답합니다',steps('items를 읽기 전·후 실행 SQL이 어떻게 달랐나요?','flush와 commit, clear와 DELETE는 무엇이 달랐나요?','4 → 1 뒤에도 주문·항목 값이 같다는 근거는?','예측이 틀렸다면 어느 조건을 놓쳤나요?'))
add('별도 과제 공유','단축 URL은 완성한 범위만 보여줍니다',steps('<a href="../assignments/short-url/">단축 URL 별도 과제 ↗</a>의 생성·복사·이동·오류 결과 공유','AI가 만든 화면에서 본인이 고친 부분 설명','순수 HTML·CSS·JavaScript만 사용 · 외부 라이브러리 CDN 금지','미완료는 진행 상태와 다음 작업 기록')+call('상품 관리와 SQL 관찰이 공통 진도입니다. 별도 과제 완료를 오늘의 출발 조건으로 삼지 않습니다.'))
add('GitHub 제출','예측·SQL·결과를 같은 작업에 기록합니다',table([['항목','지정 값'],['저장소 · 폴더','sesac-spring-boot-study / order-query-lab'],['브랜치','practice/jpa-query-lab'],['Issue · PR','[실습] 지연 로딩과 N+1 관찰·개선']])+call('Issue 1개 · 병합 PR 1개. README와 PR에 4 → 1 로그·같은 결과·Closes #실제번호를 기록합니다.'))
add('최종 확인','공통 코드와 실행 근거를 보존합니다',steps('전체 테스트 통과 후 main 대상 PR을 자체 확인·병합','product-api·personal-project 등 기존 프로젝트 보존','gradle-wrapper.jar 포함 · build/·.gradle/·DB·.env 제외','틀린 예측과 다음 확인할 질문 기록')+call('관계 전략·EntityGraph·페이지네이션 조사는 필수 관찰을 끝낸 뒤 선택합니다.'))
add('작업 뒤 참고','책·작업지와 비교할 전체 파일',source_choices(),note='전체 파일은 shared/order_sources.py와 동일한 참고 구현입니다. SQL 예측과 직접 시도를 마친 뒤 비교합니다. 공통 상품 API와 별도 주문 조회 랩을 혼합하지 않습니다.')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-23-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.23</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="영속성과 쿼리를 관찰하는 JPA"><title>11월 23일 · 영속성과 쿼리를 관찰하는 JPA</title><style>'+css+'</style></head><body data-deck-revision="2026-11-23-v2-book-led"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',out.count('data-source-key='),'reference buttons;',len(out.encode()),'bytes')
