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
TITLE='상품 CRUD 집중 실습과 JPA 입문'
add('여섯 번째 수업','책과 함께 완성하는<br>상품 관리 애플리케이션','<div class="cover-bottom"><span>2026.11.14 SAT · 8시간</span><strong>CRUD 직접 구현·테스트 → JPA 입문</strong></div>',kind='cover')
add('책과 함께','책을 읽고 직접 구현하는 하루',steps('책 CH 09에서 상품 수정·삭제와 계층 흐름 함께 읽기','CH 10의 검증·예외, CH 12의 추상화·테스트와 연결','멘티가 작성·실행하고 실제 결과를 동료와 비교','CH 11 DB 접근은 JDBC와 JPA의 차이를 보며 연결'),note='책의 쪽수와 본문 코드를 확인하지 않은 자료입니다. 장 제목을 기준으로 실제 책에서 해당 절을 찾습니다. 제공 코드는 수업 독립 예제이며 교재 코드의 복제 또는 정답이라고 설명하지 않습니다.')
add('주말 운영','설명보다 구현하고 확인하는 시간',table([['시간 블록','수업 활동'],['1–2교시','책 읽기·계약 정리 → 수정 구현'],['3–4교시','삭제 구현 → 정상·실패 회귀 테스트'],['5–6교시','독립 보완·동료 검증·GitHub 제출'],['7–8교시','ORM·JPA 핵심 → 테이블·Entity 매핑 활동']])+call('매 블록 45분 활동 + 15분 휴식·정리 · 점심 별도'),note='8개 블록 총480분. 설명·읽기·설계 활동 약90분, 자율 구현·실습330분, 결과 확인·피드백60분을 휴식 포함 운영 블록으로 배분합니다. 실제 집중 활동은 각45분, 나머지는 휴식과 정리입니다. 연속 강의나 강사 코딩 시연 없이 막힌 공통 지점만 짧게 보충합니다.')
add('오늘 완료 기준','상품 CRUD를 테스트 결과로 설명',steps('기존 생성·목록·단건 조회와 400·404 동작 유지','PUT 수정과 DELETE 삭제를 직접 구현','실패 요청 뒤 기존 상품이 보존됨을 확인','메모리 저장의 한계와 JPA 전환 대상을 설명'))
section('01','책에서 계약 찾기','')
add('읽기 질문','수정·삭제는 어느 계층의 책임인가요?',table([['책을 보며 찾을 것','설명할 질문'],['Controller 입력과 응답','경로 id와 본문의 값은 어디서 받나요?'],['Service의 처리 순서','존재 확인과 변경은 어떤 순서인가요?'],['Repository의 역할','저장·교체·삭제를 어떻게 추상화하나요?'],['검증·예외','실패하면 기존 값은 어떻게 되나요?']]))
add('수업 독립 계약','PUT과 DELETE의 완료 상태',table([['요청','성공','실패'],['PUT /products/{id}','200 · 수정 상품 JSON','없는 id 404 · 잘못된 본문 400'],['DELETE /products/{id}','204 · 본문 없음','없는 id 404'],['기존 POST · GET','기존 상태·본문 유지','기존 예외 계약 유지']])+call('이 표는 수업 예제의 계약 · 교재와 다른 선택은 근거를 비교합니다.'))
add('PUT 수정 범위','이름과 가격을 한 번에 교체',steps('경로 id로 기존 상품 존재 확인','요청 name·price를 모두 검증','같은 id와 새 값으로 상품을 교체','변경된 상품을 응답하고 다시 조회'),note='부분 수정 PATCH는 필수가 아닙니다. id는 새로 발급하지 않습니다. 불변 Product를 유지하여 새 값으로 교체하고 실패 도중 기존 객체가 부분 변경되는 일을 방지합니다.')
add('DELETE와 멱등성','응답 코드와 최종 상태를 구분',table([['상황','수업의 응답과 상태'],['첫 삭제','204 · 본문 없음 · 상품 부재'],['같은 id 재삭제','404 · 상품 부재 유지'],['다른 상품 조회','기존 값 유지']])+call('응답이 달라도 반복 후 최종 자원 상태가 같으면 멱등 의미와 모순되지 않습니다.'))
add('실패 후 상태','성공뿐 아니라 보존도 확인',steps('기존 상품 이름·가격과 목록 개수를 기록','잘못된 PUT을 전송하고 400 확인','기존 상품이 바뀌지 않았는지 재조회','없는 상품 수정·삭제 뒤 다른 상품이 남는지 확인'))
section('02','자율 실습 · 상품 CRUD','')
add('실습 시작','새 프로젝트 없이 product-api를 이어 사용',steps('최신 main → practice/product-crud 브랜치','12일 정상·오류 API와 기존 테스트 먼저 실행','책의 수정·삭제 절을 읽고 변경 파일 목록 작성','선택 검색 과제 코드는 보존하고 수정점만 반영'),note='기준 예제는 필수 생성·조회만 포함합니다. 선택 이름·가격 검색을 구현했다면 Controller/Service 전체 파일을 덮어쓰지 않습니다. 같은 클래스 중복 생성도 금지합니다.')
add('작업 1','수정·삭제 테스트를 먼저 문장으로',table([['테스트','기대 결과'],['정상 수정','id 유지 · 이름·가격 교체'],['잘못된 수정','예외 · 기존 값 보존'],['없는 상품 수정·삭제','ProductNotFoundException'],['정상 삭제','목록과 단건 조회에서 제거']])+call('준비 → 실행 → 기대 결과를 적고 코드로 옮깁니다.'))
add('작업 2','도메인·저장소·Service를 구현',steps('기존 Product.java는 변경 없이 입력 규칙·불변 필드 유지','Repository에 수정·삭제 계약을 추가','Memory 저장소에서 실제 교체·삭제 구현','Service에서 대상 확인 후 저장소 호출'),note='이 작업에서는 HTTP가 없어도 단위 테스트로 실행 가능해야 합니다. 코어가 통과한 뒤 Controller를 연결합니다.')
for key in ['ProductRepository.java','MemoryProductRepository.java','ProductService.java']:
 filepages('비교용 코드 · 코어',key,'먼저 자율 구현한 뒤 비교')
add('첫 중간 점검','HTTP 없이 수정·삭제를 증명',steps('수정 뒤 id는 같은가요?','이름 공백 정리와 가격 0이 유지되나요?','음수·빈 이름 수정 뒤 기존 값이 남나요?','없는 상품을 수정·삭제하면 무엇이 발생하나요?'))
add('작업 3','Controller에 HTTP 계약 연결',steps('PUT에 기존 요청 DTO·@Valid 연결','수정 결과를 ProductResponse로 변환','DELETE 성공은 ResponseEntity.noContent()','기존 전역 예외 처리기로 400·404 확인'),note='ApiExceptionHandler와 CreateProductRequest는12일 파일을 유지합니다. 새 Update DTO나 예외를 무조건 늘리지 않습니다. 경로 id는 본문 id와 중복 관리하지 않습니다.')
filepages('비교용 코드 · HTTP','ProductController.java','기존 선택 검색이 있으면 변경점만 반영')
add('작업 4','Service 단위 테스트로 회귀 확인',steps('기존 생성·목록·없는 id 테스트 보존','수정·실패 후 값 보존·삭제 테스트 추가','./gradlew test로 전체 테스트 실행','실패는 기대·실제·원인을 기록하고 수정'))
filepages('비교용 코드 · 테스트','ProductCrudTest.java','기존 ProductServiceTest를 유지하고 새 테스트 추가')
add('HTTP 검증 순서','실제 생성 id로 끝까지 확인',table([['순서','요청·확인'],['1','POST로 상품 두 개 생성 → 실제 id 기록'],['2','PUT 첫 상품 → 200 · 같은 id · 새 값'],['3','잘못된 PUT → 400 · 재조회 값 보존'],['4','없는 id PUT/DELETE → 404'],['5','DELETE 첫 상품 → 204 · 빈 본문'],['6','삭제 상품 GET 404 · 다른 상품 GET 200']]))
add('추가 회귀','예전 기능도 같은 결과인가요?',steps('새 서버 빈 목록은 200 + []','정상 POST 201 · Location과 응답 id 일치','이름·가격 오류와 잘못된 JSON은 400','상품 조회·순서·AOP 로그·Wiring 테스트 유지'),note='메모리 저장이므로 재시작 후 데이터가 사라지는 것은 오늘의 예상 동작입니다. 번호의 연속성이나 특정 고정 id를 가정하지 않습니다.')
add('동료 피드백','책과 내 구현의 차이를 설명',steps('동료에게 클래스 이름 대신 요청 흐름 설명','교재와 수업 예제의 계약 차이 한 가지 찾기','정상·실패 요청을 동료가 직접 재현','실패 후 데이터 보존의 근거를 제시'))
add('별도 과제','책에 없는 조건을 직접 확장',table([['필수 응용','선택 도전'],['가격 범위 검색과 경계 테스트 보완','동시 요청에서 저장소가 지킬 조건 조사'],['필터 결과 없음은 빈 목록','수정 이력 설계 문서 작성'],['기존 API 회귀 결과 기록','PATCH와 PUT의 차이 설명']])+call('단축 URL·AI 프론트 과제는 별도 과제 안내에서 단계별 진행합니다.'))
add('단축 URL 과제','수업 밖에서 배운 내용을 적용','<div class="card"><h3>설계 → 백엔드 → AI 프론트 → 통합 검증</h3><p>상품 관리는 공통 수업 프로젝트입니다. 단축 URL은 별도 과제로 수행하며 필수 수업 진도를 대신하지 않습니다.</p><p><a href="../assignments/short-url/">단축 URL 과제 안내 ↗</a></p></div>')
section('03','JPA 입문 · 직접 매핑하기','')
add('책 CH 11과 연결','같은 저장 요구를 다른 방식으로 구현',table([['JDBC','JPA'],['SQL 작성과 실행·결과 매핑을 직접 제어','객체와 테이블의 매핑·변경 추적 활용'],['DB 접근과 자원 관리를 이해','EntityManager·Repository를 통해 접근'],['책의 구현 흐름을 읽기','수업에서 같은 요구를 JPA로 전환']])+call('JPA도 SQL과 데이터베이스 위에서 동작합니다.'))
add('메모리에서 DB로','재시작 뒤 무엇이 남아야 할까요?',cards(('현재','Memory 저장소','프로세스 종료 시 상품 소실'),('전환 목표','DB 저장소','재시작 뒤 저장한 상품 조회'),('유지할 것','Service와 HTTP 계약','사용자 기능과 응답을 함께 검증')))
add('ORM·JPA·Spring Data','서로 맡는 역할을 구분',table([['이름','역할'],['ORM','객체와 관계형 테이블의 차이를 매핑'],['JPA','자바 영속성 표준 API'],['Hibernate','JPA 구현체'],['Spring Data JPA','JPA 기반 Repository 구현 지원']]))
add('영속성 컨텍스트','한 작업 안에서 Entity 상태를 관리',steps('조회한 Entity를 관리하는 작업 단위 이해','같은 id 조회와 객체 동일성 관찰 준비','트랜잭션 안의 변경과 DB 반영을 구분','오늘은 개념·매핑 초안,16일부터 실행'),note='영속성 컨텍스트가 애플리케이션 전체 데이터를 영구 보관하는 전역 캐시라고 설명하지 않습니다. SQL 시점과 flush/commit의 세부 관찰은16일·23일에 연결합니다.')
add('매핑 활동 1','상품 테이블을 종이에 설계',table([['항목','멘티가 결정·기록할 것'],['식별자','상품 id · 생성 주체'],['컬럼','이름 · 가격 · 필수 여부'],['제약','이름 길이 · 가격 범위의 근거'],['기존 도메인','Product 규칙과 DB 제약의 역할 차이']])+call('교재에 없는 길이나 정책은 수업 가정으로 표시합니다.'))
add('매핑 활동 2','Entity 초안을 서로 검토',steps('@Entity와 테이블의 연결을 표시','@Id와 자동 생성 id의 의미 설명','JPA 기본 생성자와 도메인 생성자 구분','도메인 Product와 Entity를 분리할 이유 토론'),note='오늘 Entity 완성·JPA 전환은 필수가 아닙니다. 종이 또는 docs/jpa-mapping.md 초안이면 됩니다.16일 공통 Entity로 실행하고19일 API 저장소를 전환합니다.')
section('04','GitHub 제출과 다음 시간','')
add('오늘 제출','필수 Issue 1개 · 병합 PR 1개',table([['설정','지정 값'],['저장소','sesac-spring-boot-study'],['브랜치','practice/product-crud'],['Issue · PR','[실습] 상품 관리 CRUD와 테스트'],['산출물','코드·테스트·HTTP 검증·JPA 매핑 초안']])+call('최신 main → Issue → branch → 구현·검증 → PR → 자체 확인·병합'))
add('문서 누적','README와 Wiki에 실제 결과를 남기기',steps('product-api/README.md에 PUT·DELETE 계약 추가','Wiki Home·01-Setup·02-Architecture 누적','03-API·04-Verification·05-Retrospective 갱신','PR에 Closes #실제번호와 기대·실제 결과 첨부'),note='Public/main, 본인 Assignee, practice 라벨, milestone product-api-2026-11-14. Wiki는 별도 저장소이므로 편집 뒤 PR에 링크를 남깁니다. 원하지 않는 추가 문서 PR을 필수로 만들지 않습니다.')
add('제출 확인','다른 사람이 실행할 수 있게',steps('src·build.gradle·settings.gradle·Wrapper 전부 포함','gradle-wrapper.jar 예외를 루트 .gitignore에 유지','build/·.gradle/·IDE·.env·비밀값 제외','코드·테스트·문서·실제 병합 PR URL 확인'))
add('16일로 연결','상품 Entity와 JPA 저장소를 따로 연습',cards(('16일','JPA 기본 동작·테스트','실제 API는 Memory 유지'),('19일','실습 작업지로 저장소 전환','같은 상품 API를 DB와 연결'),('23일','SQL 관찰과 성능 문제','영속성·지연 로딩·N+1')))
add('공식 참고','책과 공식 문서로 비교','<div class="references"><a href="https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2"><b>Jakarta Persistence ↗</b><span>Entity · 영속성 컨텍스트</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/"><b>Spring Data JPA ↗</b><span>Repository와 쿼리</span></a><a href="https://www.rfc-editor.org/rfc/rfc9110.html"><b>HTTP 의미 ↗</b><span>PUT · DELETE · 멱등성</span></a></div>')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 교재 상품 관리 자율 실습"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v1-book"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
