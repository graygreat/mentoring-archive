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
add('2026.11.19 · 4시간','상품 API의 저장소를<br>JPA로 바꾸기','<div class="cover-bottom"><strong>이준형 강사 대강 · 책과 작업지로 진행</strong><span>새 개념 설명 없이 16일 내용을 직접 적용합니다</span></div>',kind='cover')
add('책을 펼칠 곳','CH 11의 상품 저장·조회부터 다시 읽습니다',steps('책에서 상품의 데이터 접근 부분을 찾습니다','CH 12의 저장소 인터페이스와 테스트를 함께 확인합니다','책의 JDBC 코드와 오늘 JPA 연결의 차이를 말합니다')+call('공통 product-api를 이어 사용합니다. personal-project나 단축 URL 구현은 오늘의 출발 조건이 아닙니다.'))
add('시작 자료','작업지와 출발 상태를 먼저 확인합니다',table([['자료','사용 방법'],['<a href="STUDENT-WORKSHEET.md">멘티 작업지 ↗</a>','1~4교시 순서와 단계별 힌트'],['<a href="assets/product-api-start.zip">출발 ZIP ↗</a>','16일 완료 상태 · 실제 API는 Memory'],['<a href="HANDOFF.md">대강 진행표 ↗</a>','이준형 강사의 확인·복구 기준'],['<a href="../2026-11-16/BEGINNER-WORKSHEET.md">16일 쉬운 작업지 ↗</a>','DB·Entity·두 Repository가 헷갈릴 때']]))
add('네 교시 운영','작업하고 완료 기준으로 멈춥니다',table([['교시','45분 작업 · 15분 휴식·정리'],['1','책과 출발 코드 확인 · 기존 테스트 · 변경 계획'],['2','작업지 A~E · JPA Adapter와 빈·트랜잭션 연결'],['3','정상·실패 CRUD 회귀 확인'],['4','파일 DB 재시작 보존 · README · PR 제출']]),note='설명·강사 구현 시연 없이 작업지에서 막힌 한 단계만 도와줍니다. 발표를 위한 새 과제를 추가하지 않습니다.')
add('1교시 · 출발 점검','기존 API가 먼저 동작해야 합니다',steps('product-api 폴더에서 기존 테스트를 실행합니다','Memory 구현으로 CRUD·400·404를 확인합니다','바꿀 파일과 보존할 API 응답을 작업지에 적습니다')+call('동작하지 않는 경우 먼저 출발 ZIP을 임시 폴더에서 비교합니다. 기존 코드·DB를 덮어쓰지 않습니다.'))
add('2교시 · 작업지 A~E','작은 연결 다섯 개를 차례로 완성합니다',steps('A·B: ProductRepository 계약과 JPA 메서드 맞추기','C: Spring이 사용할 구현체 빈 하나 선택','D: Service 작업을 트랜잭션으로 묶기','E: main 파일 DB와 test 메모리 DB 구분'),note='실제 값은 노트 3000원을 기준으로 Entity에서 Product로 이동시켜 설명합니다. 구체 메서드 대응·빈 중복·Service 검증·파일 DB 설정은 작업지와 HANDOFF에서 확인합니다.')
add('3교시 · 회귀 확인','저장 방식이 바뀌어도 API는 같습니다',table([['요청','기대 결과'],['생성 · 조회 · 수정 · 삭제','201 · 200 · 200 · 204'],['잘못된 입력 · 없는 상품','400 · 404'],['실패 요청 전·후','기존 상품 값 유지'],['검증 방법','실제 생성 id · 전체 테스트 · DB 접근 근거']])+call('응답 상태만 보지 말고 저장한 값과 실패 뒤 원본도 비교합니다.'))
add('4교시 · 재시작 확인','같은 상품이 다시 조회되나요?',steps('별도 상품을 생성·수정하고 실제 id·값 기록','서버 정상 종료 후 같은 폴더·설정으로 재실행','같은 id의 수정 값을 조회','테스트 DB와 실행 파일 DB의 차이를 설명')+call('실행 DB는 jdbc:h2:file:./data/products · open-in-view=false. 파일을 지워 통과시키지 않습니다.'))
add('막혔을 때','작업지의 한 단계로 돌아갑니다',steps('오류 문장·기대 결과·재현 명령을 함께 읽기','DB·두 Repository가 헷갈리면 16일 작업지 확인','빈·트랜잭션·파일 잠금 문제는 HANDOFF 표 확인','해당 메서드만 참고 구현과 비교하기')+call('완료하지 못한 부분은 오류와 다음 작업을 남깁니다. 강제로 성공이나 병합으로 표시하지 않습니다.'))
add('GitHub 제출','기존 계약과 재시작 근거를 PR로 남깁니다',table([['항목','지정 값'],['저장소 · 브랜치','sesac-spring-boot-study · practice/product-jpa-migration'],['Issue · PR','[실습] 상품 API 데이터 접근 JPA 전환'],['필수 기록','README · 테스트·HTTP·재시작 결과 · Closes #실제번호']])+call('Issue 1개 · 병합 PR 1개. Wrapper의 gradle-wrapper.jar 유지 · DB 파일·비밀값은 제외합니다.'))
add('작업 뒤 참고','전체 파일은 막힌 부분을 비교할 때만',source_choices(),note='책과 작업지의 순서가 먼저입니다. 네 파일은 shared/product_sources.py의 검증된 수업 참고 구현을 원문 그대로 표시합니다.')
add('23일로 연결','전환 결과와 남은 질문을 가져옵니다',steps('같은 상품의 수정 값과 재시작 조회 결과 보관','Memory가 JPA Adapter로 바뀐 위치 표시','미완료 오류와 복구 코드 사용 범위 기록')+call('다음은 별도 주문 조회 예제로 SQL을 관찰합니다. 단축 URL은 <a href="../assignments/short-url/">별도 과제 ↗</a>입니다.'))

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-19-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.19</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="상품 API JPA 전환 실습"><title>11월 19일 · 상품 API JPA 전환 실습</title><style>'+css+'</style></head><body data-deck-revision="2026-11-19-v2-book-led"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',out.count('data-source-key='),'reference buttons;',len(out.encode()),'bytes')
