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
add('책과 함께 · 2시간 + 2시간','검증을 추가하고<br>남은 CRUD를 설계합니다','<div class="cover-bottom"><strong>CH 10 → CH 09·12 · 부록 B</strong><span>기존 product-api를 이어서 사용합니다</span></div>',kind='cover')
add('오늘의 진행','앞 2시간은 검증, 뒤 2시간은 설계',table([['교시','책과 활동'],['1','CH 10 · 입력 검증과 예외 처리 읽기'],['2','400·404 구현 · 기존 정상 요청 회귀 확인'],['3','CH 09 · 수정·삭제 요구사항 정리'],['4','CH 12 · 테스트 설계 →14일 구현 준비']])+call('교시마다45분 활동 +15분 휴식·정리 · 책에서 코드 읽기, 멘티가 직접 작성'))
section('01','교재 CH 10을 펼칩니다','')
add('함께 읽기','유효성 검사와 전역 예외 핸들러',steps('도메인 객체 및 컨트롤러 유효성 검사 찾기','전역 예외 핸들러의 입력과 응답 찾기','HTTP 응답 상태 코드와 바디 비교'),note='판본의실제쪽수를표시합니다. DTO입력검사와Product규칙의책임을구분하며기존도메인규칙을지우지않습니다. WebMVC·Validation등기존프로젝트설정사용,새프로젝트생성없음.')
add('책을 보며 질문','잘못된 요청과 없는 상품은 어떻게 다를까요?',steps('이름·가격의 잘못된 값을 어디에서 막나요?','Java 예외를 어떤 상태 코드와 오류 본문으로 바꾸나요?','실패했을 때 기존 상품 값은 그대로인가요?'))
add('직접 적용','검증과 실패 응답을 완성합니다',table([['상황','수업의 완료 기준'],['이름 null·공백 / 가격 null·음수','400 · 기존 저장 데이터 불변'],['가격 0','정상 허용'],['없는 상품 id 조회','404 · 공통 오류 JSON'],['기존 정상 생성·조회','9일의 상태·헤더·본문 유지']]),note='CreateProductRequest의Integer price와@NotNull을보존합니다. @Valid,ApiExceptionHandler를책과참고코드에서비교합니다. 도메인검증과HTTP변환을섞지않습니다. 기존선택검색이있으면findAll검색코드를지우지말고보존합니다. 숫자가아닌입력도잘못된요청400으로확인하되오늘필수검색기능추가는아닙니다.')
add('실행 확인','실패 요청 뒤 데이터를 다시 읽습니다',steps('정상 상품 생성 → 실제 id와 값을 기록','잘못된 요청 보내기 → 상태·오류 본문 확인','다시 조회 → 기존 이름·가격·목록이 유지되는지 확인'),note='메서드·상태코드·멱등성·REST성숙도는책의기술면접TIP과연결한질문으로확인합니다. Level0~3암기강의대신현재API가자원URI와HTTP메서드를어떻게쓰는지설명하게합니다. 멱등성은반복후최종상태와응답코드를구분합니다.')
section('02','CH 09 · CH 12로 돌아갑니다','')
add('읽을 곳','상품 수정·삭제와 테스트를 연결합니다',steps('CH 09 · 상품 조회/수정/삭제 구현하기','CH 12 · 리팩토링과 테스트 코드','부록 B · 요구사항과 검증 결과 문서화 참고'),note='수정삭제완성코드강사시연없이책을함께읽고설계합니다. 부록B를수업문서형식과비교하되수업에서정한HTTP계약을교재원문규칙이라고단정하지않습니다. 책의페이지는각자판본에서확인합니다.')
add('설계 과제','14일에 만들 수정·삭제를 먼저 정합니다',table([['정할 것','설계에 남길 내용'],['요구사항','무엇을 바꾸고 지울 수 있는가'],['API · 계층','URL·상태·입력값 / 각 클래스가 맡을 일'],['테스트','정상·없는 id·잘못된 값·실패 후 원본']])+call('product-api/docs/crud-design.md · 교재 근거와 수업 가정을 구분'))
add('수업에서 정한 계약','PUT과 DELETE의 결과를 설계합니다',table([['요청','성공','실패'],['PUT /products/{id}','200 · 수정 상품','없는 id404 · 입력400'],['DELETE /products/{id}','204 · 본문 없음','없는 id404']])+call('수정은 기존 id 유지 · 없는 상품을 새로 만들지 않음 · 실패하면 원본 보존'))
add('설계 완료 점검','코드를 쓰기 전에 설명할 수 있나요?',steps('입력부터 저장·응답까지 책임을 표시','정상·실패 사례의 예상 상태와 데이터 작성','가격0·동일값 수정·삭제 후 조회 테스트 설계','책과 다른 선택은 가정·이유를 기록'),note='14일공통책프로젝트CRUD구현을준비하는문서이며추가새서비스설계가아닙니다. personal-project의소장품관리에도같은학습을적용할예정입니다.')
add('별도 선택 과제','단축 URL은 따로 도전할 수 있습니다','<p><a href="../assignments/short-url/">CH 13 · 단축 URL 별도 과제 안내 ↗</a></p>'+call('개인 소장품 프로젝트와 동시에 필수로 요구하지 않습니다.'),note='기존단축URL과제규칙은변경하지않습니다. AI프론트는순수HTML/CSS/JS,외부CDN없음,기본설정만안내하고프롬프트는자율입니다. 수업기본진도는상품관리애플리케이션입니다.')
add('GitHub 제출','오늘 필수 Issue 2개 · 병합 PR 2개',table([['브랜치','Issue · PR 제목'],['practice/product-validation','[실습] 상품 API 검증과 예외 처리'],['docs/product-crud-design','[설계] 상품 수정·삭제 CRUD 설계']])+call('sesac-spring-boot-study · product-api/ · README와 설계 문서 제출'),note='main pull→Issue→branch→검증→commit/push→PR base main자체확인병합,Closes #실제번호. 본인담당,practice/docs라벨과기존수업마일스톤사용. 기존greeting-api와개인프로젝트를지우지않으며실행에필요한Wrapper포함,build/.gradle/IDE/.env제외.')
add('다음 주말','14일에는 책 CRUD와 개인 프로젝트',cards(('1~2교시','공통 상품 CRUD','수정·삭제 구현과 회귀 확인'),('3~6교시','개인 과제·발표','같은 소장품 프로젝트를 REST로 확장'),('7~8교시','DB 기초·JPA 입문','CH 11과 보충 작업지 연결')))
add('읽기와 참고','책이 기준, 참고 자료는 필요할 때','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 목차 ↗</b><span>CH 09·10·12 · 부록 B</span></a><a href="https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html"><b>Spring 예외 처리 ↗</b><span>책과 비교할 보충 문서</span></a></div>')

# Keep complete supplementary files reachable without restoring code lecture pages.
S[-1]['body'] += '<div class="inline-list">'+''.join('<button type="button" data-source-key="'+esc(key)+'">'+esc(key)+'</button>' for key in SOURCES)+'</div>'
S[-1]['note'] += ' 파일 이름 버튼은 전체 참고 코드를 여는 보충 자료입니다. 책과 직접 작성한 결과를 먼저 확인하고, 막힌 부분을 비교할 때 사용합니다.'
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-12-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.12</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 상품 관리 검증·예외 응답과 남은 CRUD 요구사항·API·테스트 설계"><title>11월 12일 · 검증과 서비스 설계</title><style>'+css+'</style></head><body data-deck-revision="2026-11-12-v1-curriculum"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',len(out.encode()),'bytes')
