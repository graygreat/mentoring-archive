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
DAY='2026-11-14'
TITLE='상품 CRUD 집중 실습과 DB 기초'
add('책과 함께 · 주말 8시간','상품 CRUD를 완성하고<br>개인 프로젝트를 발표합니다','<div class="cover-bottom"><strong>책 CRUD 2교시 → 개인 과제·발표4교시 → DB/JPA2교시</strong><span>앞6시간 CRUD 적용 · 뒤2시간 DB 기초와 JPA 맛보기</span></div>',kind='cover')
add('오늘의 진행','책 → 개인 적용·발표 → DB로 연결',table([['교시','수업 활동'],['1~2','CH 09·10·12 · 공통 product-api CRUD'],['3~6','personal-project 개인 구현·발표 · 4시간'],['7~8','CH 11 연결 · DB 기초와 JPA 보충 활동']])+call('교시마다45분 활동 +15분 휴식·정리 · 점심 별도 · 강사 코딩 시연 없음'))
section('01','책의 상품 수정·삭제를 함께 봅니다','')
add('책에서 찾을 곳','CH 09 수정·삭제 → CH 10·12 연결',steps('CH 09 · 상품 조회/수정/삭제의 입력과 순서','CH 10 · 검증·예외 처리와 실패 후 데이터','CH 12 · 리팩토링·테스트의 정상·실패 사례'),note='12일product-api/docs/crud-design.md를책과함께확인합니다. 정확한쪽수는판본에서찾아표시하며수업독립HTTP계약과책원문의차이를확인합니다. 공통product-api기존생성/조회/예외와Service테스트를유지합니다.')
add('공통 프로젝트 · 1~2교시','설계한 CRUD를 직접 구현합니다',table([['요청','성공','실패'],['PUT /products/{id}','200 · 수정 상품','없는 id404 · 입력400'],['DELETE /products/{id}','204 · 본문 없음','없는 id404']])+call('기존 POST·GET과 검증 유지 · 실패 요청 뒤 상품 값 보존'),note='추가ProductCrudTest를작성하고기존ProductServiceTest/ProductWiringTest를남깁니다. Repository·Memory·Service·Controller의수정삭제흐름을책과비교합니다. 미완료학생은강사가현재한기능을확인해최소목표로조정하고참고자료로보완합니다. 개인프로젝트로공통product-api를대체하거나덮어쓰지않습니다.')
section('02','개인 프로젝트 · 배운 CRUD를 적용합니다','')
add('개인 과제','7일의 소장품 프로젝트를 이어갑니다',steps('personal-project/ · CollectionItem(id, name, price)','책·게임·운동용품 등 내가 고른 테마 유지','메모리 Repository·Service 위에 REST CRUD 추가'),note='각자 sesac-spring-boot-study 개인저장소에서작업합니다. 7일개인코어가미완료라면책의공통예제를참고해등록·조회한기능부터완료하고막힌점을발표해도됩니다. 다른사람프로젝트를공동으로완성하는팀과제가아닙니다.')
add('개인 완료 기준','소장품 API를 실제 요청으로 확인합니다',table([['요청','기대 결과'],['POST /items','201 · 생성한 소장품'],['GET /items · /items/{id}','200 · 목록 또는 실제 생성 id 조회'],['PUT /items/{id}','200 · 수정된 같은 id'],['DELETE /items/{id}','204 · 본문 없음']])+call('빈 이름·음수 가격400 / 없는 id404 / 실패하면 기존 값 보존'))
add('과제 범위','오늘 배운 내용으로 완성합니다',steps('기존 코어 테스트를 유지하고 CRUD 사례 추가','HTTP 상태·응답·실패 후 데이터를 비교','DB·JPA·프론트 구현은 오늘 개인 필수 범위 아님'),note='공통책프로젝트와개인프로젝트를같은폴더에섞지않습니다. 서버를같이띄울경우포트를달리하거나하나를중지합니다. actual생성id를사용하고id연속성이나JSON속성순서를완료기준으로삼지않습니다. 개인프로젝트세부규칙은연결된공통과제문서에서확인합니다.')
add('개인 과제 · 3~6교시','구현·준비105분 + 발표75분',table([['교시','45분 활동'],['3','개인 구현45분'],['4','개인 구현45분'],['5','발표 준비15분 + 앞5명 발표·질문30분'],['6','뒤6명 발표·질문36분 + 공통 피드백9분']])+call('활동180분 + 휴식·정리60분 =4시간 · 11명 전원 개인 발표'))
add('발표 방법','PPT 대신 코드와 실행 결과를 보여줍니다',steps('4분: 어떤 소장품을 다루고 무엇을 완성했는지','정상 요청 하나 + 실패 요청 하나 실행','코드에서 책임 분리와 테스트 근거 설명','2분: 질문과 답변 · 미완료는 막힌 지점 설명'),note='1인4분발표+2분질문=6분,11명66분에공통피드백9분을더해75분입니다. 별도발표슬라이드는만들지않습니다. 진행중시간을표시해모든개인에게동일시간을배정합니다. 질문이길면기록해수업후피드백합니다.')
add('작업지와 제출','개인 결과를 README와 PR에 남깁니다','<p>sesac-spring-boot-study · <a href="https://github.com/graygreat/mentoring-archive/blob/main/assignments/personal-project/README.md">개인 프로젝트 요구사항·발표 기준 ↗</a></p>'+table([['폴더 · 브랜치','Issue · PR 제목'],['product-api/ · practice/product-crud','[실습] 상품 관리 CRUD와 테스트'],['personal-project/ · assignment/personal-rest','[개인 과제] 소장품 관리 REST CRUD']]),note='저장소sesac-spring-boot-study,각작업Issue와PR1개. main pull→Issue→branch→구현검증→commit/push→PR base main→Closes #실제번호→자체확인병합. 개인은assignment라벨,공통은practice라벨. 루트README에두프로젝트링크,각README에는실제테스트와API결과기록. src·Gradle설정·Wrapper와gradle-wrapper.jar포함,build/.gradle/IDE/.env제외,기존greeting-api보존.')
section('03','CH 11 · 데이터베이스 연동을 읽습니다','')
add('교재와 수업 확장','JDBC를 읽고, JPA로 이어갈 준비',steps('책에서 상품 데이터가 DB에 저장되는 흐름 찾기','7~8교시는 표·SQL·객체 매핑을 작업지로 확인','JPA는 책의 DB 접근을 바탕으로 한 수업 보충'),note='책CH11의JDBC방식과JPA구현을같은코드로설명하지않습니다. 지금은JPAEntity완성이나API저장소전환이필수가아닙니다.16일Entity·Repository연습,19일공통상품API의저장소전환으로이어집니다.')
add('DB 기초 · 7교시','상품 표를 채우고 SQL 결과를 예상합니다',steps('상품 한 개의 id·name·price를 행과 열로 표시','PK·NULL과 이름 공백·가격0의 차이를 읽기','SELECT와 WHERE의 결과를 실행 전에 예상'),note='DB=데이터모음,DBMS=관리프로그램,H2=수업에서쓰는DBMS입니다. ORDER BY없이순서를가정하지않습니다. PK는행식별자이며중복NULL불가. NOT NULL만으로공백·음수가격을모두막는것이아닙니다. 보충작업지에서UPDATE/DELETE의WHERE조건과COMMIT/ROLLBACK의뜻을쉽게확인합니다.')
add('매핑 활동 · 8교시','Java 값과 표의 열을 연결합니다',table([['Java 쪽','표에서 찾을 것'],['id · @Id','어느 행인지 구분할 기본 키'],['name · price','문자열과 정수 열'],['Entity · @Entity','표와 연결할 객체의 설계']])+call('객체와 표 매핑 초안만 · 실행 가능한 JPA 코드는16일'),note='Product도메인과JPAEntity를분리하는공통예제구조를유지합니다. JPA는DB대체물이아니며Hibernate등이매핑에따라SQL을실행합니다. 이미COMMIT한변경을나중ROLLBACK으로되돌릴수없고HTTP400만으로DB복구가보장되지않는다는점은작업지사례를읽고설명합니다.')
add('쉬운 보충 자료','모르는 DB 용어는 작업지에서 확인합니다','<p><a href="../shared/db-basics/">DB 기초 안내 ↗</a></p><p><a href="../shared/db-basics/STUDENT-WORKSHEET.md">상품 표·SQL 예상 결과 작업지 ↗</a></p>'+call('product-api/docs/jpa-mapping.md에 표·예상 결과·틀린 이유 기록'))
add('오늘 마무리','실행 결과와 다음에 고칠 점을 남깁니다',steps('공통 product-api CRUD와 기존 테스트 확인','개인 프로젝트의 완료 기능·실패 사례·PR 링크 기록','상품 표·SQL 예상·객체 매핑 초안 제출'),note='공통·개인필수의미를구분합니다. 미완료는완료했다고쓰지말고재현조건과다음행동을남깁니다. 단축URL은별도선택과제이며소장품과동시에필수로강제하지않습니다.')
add('다음 책 읽기','16일에는 SQL과 JPA를 직접 비교',cards(('16일','Entity·Repository 테스트','공통 API는 Memory 유지'),('19일','상품 저장소 JPA 전환','같은 CRUD·예외 결과 유지'),('23일','관계와 SQL 관찰','지연 로딩·N+1 보충 작업지')))
add('참고','교재와 필요할 때 보는 문서','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 목차 ↗</b><span>CH 09·10·11·12</span></a><a href="../shared/db-basics/"><b>DB 기초 보충 ↗</b><span>표·PK·NULL·SQL·트랜잭션</span></a><a href="../assignments/short-url/"><b>단축 URL 별도 과제 ↗</b><span>선택 · AI 프론트 연결</span></a></div>')

# Keep complete supplementary files reachable without restoring code lecture pages.
S[-1]['body'] += '<div class="inline-list">'+''.join('<button type="button" data-source-key="'+esc(key)+'">'+esc(key)+'</button>' for key in SOURCES)+'</div>'
S[-1]['note'] += ' 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.'
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 교재 상품 관리 자율 실습"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v1-book"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
