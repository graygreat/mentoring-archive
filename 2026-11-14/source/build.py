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
TITLE='상품 CRUD · 개인 REST 프로젝트 · DB 기초'
add('2026.11.14','상품 CRUD · 개인 REST 프로젝트<br>DB 기초','<div class="cover-bottom"><strong>CH 09·10·12 · 상품 관리와 테스트</strong><span>개인 위시리스트 REST CRUD · CH 11 DB 연동</span></div>',kind='cover')
add('수업 내용','상품 CRUD · 개인 프로젝트 · DB 기초',steps('책의 상품 수정·삭제와 검증·테스트 확인','개인 위시리스트에 REST CRUD 적용','구현 결과 발표와 다른 교육생 코드 확인','책의 DB 접근과 JPA 보충 자료 읽기'))
section('01','CH 09·10·12 · 상품 CRUD와 테스트','')
add('교재 학습','상품 수정·삭제 · 검증 · 테스트',call('상품 수정·삭제, 유효성 검사와 테스트는 교재를 보며 설명합니다.'),note='12일 product-api/docs/crud-design.md를 책과 함께 확인합니다. CH 09 상품 수정·삭제, CH 10 검증·예외, CH 12 테스트를 연결합니다. 쪽수는 소지한 판본에서 찾습니다. 수업 독립 HTTP 계약과 책 원문은 구분합니다.')
add('공통 프로젝트','product-api 수정·삭제',table([['요청','성공','실패'],['PUT /products/{id}','200 · 수정 상품','없는 id 404 · 입력 400'],['DELETE /products/{id}','204 · 본문 없음','없는 id 404']])+call('기존 POST·GET과 테스트를 유지하고 실패 후 저장 값이 같은지 확인합니다.'),note='ProductCrudTest를 추가하고 기존 ProductServiceTest와 ProductWiringTest를 남깁니다. 공통 product-api는 19일 JPA 전환에 계속 사용합니다. 개인 프로젝트로 덮어쓰지 않습니다. 미완료 교육생은 한 기능부터 확인하고 책과 참고 코드로 보완합니다.')
section('02','개인 프로젝트 · 위시리스트 REST API','')
add('개인 과제','위시리스트와 예산 추천',steps('personal-project/ · CollectionItem(id, name, price)','책·게임·장비 중 선택한 위시리스트 주제 유지','등록·목록·단건 조회에 REST API 연결','각 항목 가격이 예산 이하인 후보를 최대 3개 추천')+call('개별 가격 기준 · 가격 오름차순·같은 가격은 등록 순 · 없으면 [] · 원본 보존'),note='7일 코어를 이어 사용합니다. 각 후보의 개별 가격이 예산 이하인 항목을 가격 오름차순, 같은 가격은 등록 순으로 최대 3개 반환합니다. 결과가 없으면 빈 목록이고 예산 0은 무료 항목을 포함합니다. 음수 예산은 거부합니다. 코어 미완료자는 등록·조회부터 복구하고 실제 완성 범위를 설명합니다.')
add('개인 API','/items CRUD',table([['요청','기대 결과'],['POST /items','201 · id, name, price · Location'],['GET /items · /items/{id}','200 · 목록 또는 실제 생성 id의 항목'],['PUT /items/{id}','200 · 이름·가격을 변경하고 기존 id 유지'],['DELETE /items/{id}','204 · 본문 없음']])+call('요청 본문은 name·price입니다. 목록이 비어 있으면 []를 반환합니다.'))
add('개인 API · 실패 처리','입력 오류 · 없는 id · 데이터 보존',table([['확인할 상황','기대 결과'],['이름 누락·공백 / 가격 누락·null·음수','400'],['없는 id 조회·수정·삭제','404'],['실패한 등록·수정 뒤 재조회','기존 데이터 유지'],['가격 0 / 이름 앞뒤 공백','정상 처리 / 이름 공백 제거']])+call('없는 id와 잘못된 입력은 따로 요청해 확인합니다. 기존 코어 테스트 최소 4개도 유지합니다.'))
add('개인 작업','구현 및 준비 · 150분',steps('Controller·DTO를 추가하고 기존 Service·Repository 연결','정상·실패 요청과 수정·삭제 테스트 실행','실제 결과와 미완료 범위를 정리하고 발표 준비'),note='구현 및 준비 시간은 150분입니다. 현재 동작하는 기능과 테스트를 정리해 발표합니다. 서버를 동시에 실행한다면 하나를 중지하거나 포트를 구분합니다.')
add('이론 적용 확인','코드·테스트 체크리스트',steps('□ Domain에서 이름·가격 규칙을 지키는가?','□ Controller 입력·응답과 Service 업무 처리가 분리됐는가?','□ Service가 Repository 인터페이스를 생성자로 받는가?','□ 저장·조회는 Repository, 추천 규칙은 Service에 있는가?','□ 정상·실패·원본 보존을 테스트와 실제 요청으로 확인했는가?'),note='다른 교육생의 코드와 실행 결과를 보며 확인합니다. 미완료는 체크하지 않고 동작한 범위와 다음 작업을 말합니다. 추가 AOP 구현은 공통 로그가 업무 코드와 분리되고 주입된 객체 호출에 적용되는지 봅니다.')
add('추가 과제 · 선택','검색 · 추천 API · AI 프론트',steps('이름 검색·즐겨찾기·구매 완료 상태 중 원하는 기능 추가','선택: GET /items/recommendations?budget=5000으로 개별 가격 추천 노출','AI로 목록·등록·예산 입력·추천 결과 화면 제작','순수 HTML·CSS·JavaScript 사용 · 외부 라이브러리·CDN 제외'),note='추가 추천 API를 만들면 정상 200과 음수 예산 400을 확인합니다. 필수 CRUD를 끝낸 뒤 선택합니다. 프롬프트는 자율이며 백엔드 핵심 로직은 직접 작성합니다. 실제 API를 fetch로 호출해 정상·실패를 확인합니다. 샘플 데이터만 쓰는 화면은 실제 연동과 구분해 표시합니다. JPA·DB·프론트 구현은 기본 개인 과제의 필수가 아닙니다.')
add('결과 발표','구현 기능 · 실행 결과 · 설계 결정',steps('프로젝트 주제와 완성한 기능 소개','정상 요청과 실패 요청의 결과 제시','책에서 배운 역할 분리와 테스트가 적용된 코드 설명','해결한 문제 또는 미완료 지점 설명'),note='발표용 PPT는 요구하지 않습니다. 코드·테스트·실행 화면을 보여줍니다. 다른 교육생은 이론 적용 체크리스트를 보며 질문하고 피드백합니다.')
add('제출','README · 테스트 결과 · PR',table([['폴더','제출 내용'],['product-api/','상품 CRUD 코드·회귀 테스트·매핑 초안'],['personal-project/','위시리스트 REST 코드·테스트·README']])+call('각자 sesac-spring-boot-study 사용 · 브랜치 이름은 자율'),note='본인의 의미 있는 브랜치 이름을 정합니다. 각 작업의 Issue와 PR에 변경 내용·실제 테스트 결과를 적고 Closes #실제번호로 연결합니다. 공통 실습과 개인 적용을 구분합니다. README에 완성한 기능과 실행 방법, 실제 결과를 적습니다. src·Gradle 설정·Wrapper를 포함하고 build/.gradle/IDE/.env/비밀값을 제외합니다.')
section('03','CH 11 · 데이터베이스 연동','')
add('교재와 보충 자료','JDBC · DB 기초 · JPA',steps('상품 데이터가 DB에 저장되는 흐름은 교재로 설명','표·SQL·객체 매핑은 DB 기초 작업지로 확인','JPA는 교재의 DB 접근을 바탕으로 한 수업 보충'),note='책 CH 11의 JDBC 코드와 JPA 코드를 동일한 것으로 설명하지 않습니다. 기존 CRUD 학습과 DB/JPA 입문의 내용 배정은 유지합니다. 실행 가능한 Entity·Repository는 16일, 공통 API 저장소 전환은 19일에 이어갑니다.')
add('DB 기초','상품 표와 SQL 결과',steps('id·name·price를 행과 열로 표시','PK·NULL과 이름 공백·가격 0을 구분','SELECT·WHERE·ORDER BY의 결과 예상','UPDATE·DELETE의 조건과 COMMIT·ROLLBACK 확인'),note='DB는 데이터 모음, DBMS는 관리 프로그램, H2는 수업에서 사용하는 DBMS입니다. ORDER BY 없이 순서를 가정하지 않습니다. PK는 중복·NULL이 불가합니다. NOT NULL만으로 공백·음수 가격을 모두 막는 것은 아닙니다. HTTP 400만으로 DB 롤백이 보장되지 않으며 이미 COMMIT한 내용을 나중 ROLLBACK으로 취소할 수 없음을 작업지로 확인합니다.')
add('객체 매핑','Java 필드와 DB 열',table([['Java 쪽','표에서 찾을 것'],['id · @Id','어느 행인지 구분할 기본 키'],['name · price','문자열과 정수 열'],['Entity · @Entity','표와 연결할 객체의 설계']])+call('product-api/docs/jpa-mapping.md에 표·SQL 예상·객체 대응 초안을 기록합니다.'),note='Product 도메인과 JPA Entity를 분리하는 공통 예제 구조를 유지합니다. JPA는 DB 대체물이 아니며 매핑에 따라 SQL 실행을 돕습니다. 지금은 객체와 표의 대응을 이해하고 초안을 작성합니다. 개인 과제에 JPA를 붙일 필요는 없습니다.')
add('다음 수업','Entity · Repository · 저장소 전환',cards(('16일','Entity·Repository 테스트','공통 API는 Memory 유지'),('19일','상품 저장소 JPA 전환','기존 CRUD·예외 결과 유지'),('23일','관계와 SQL 관찰','지연 로딩·N+1 보충 작업지')))
add('참고','교재 · DB 기초 자료','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 목차 ↗</b><span>CH 09·10·11·12</span></a><a href="../shared/db-basics/"><b>DB 기초 ↗</b><span>표·PK·NULL·SQL·트랜잭션</span></a><a href="../shared/db-basics/STUDENT-WORKSHEET.md"><b>DB 작업지 ↗</b><span>상품 표·SQL 예상 결과</span></a></div>')

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
