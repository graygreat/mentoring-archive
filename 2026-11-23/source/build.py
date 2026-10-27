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
add('2026.11.23 · 4시간','객체의 상태와<br>SQL을 함께 관찰하기','<div class="cover-bottom"><strong>상품 JPA 회고 → 영속성 → 지연 로딩 → N+1</strong><span>독립 주문 조회 실습 · 단축 URL 결과 공유</span></div>',kind='cover')
add('오늘의 결과','동작뿐 아니라 실행 근거까지 설명',steps('상품 API JPA 전환 결과와 남은 오류 확인','관리 상태·변경 감지·flush/clear를 테스트로 설명','주문 조회의 N+1을 재현하고 쿼리 수 비교','개선 근거와 한계를 PR·면접 답변으로 정리'))
add('책과 연결','상품 관리와 주문 예제의 역할 구분',table([['자료','오늘의 활용'],['책의 상품 관리','저장 계층·테스트·JPA 전환 결과 비교'],['독립 order-query-lab','연관관계·지연 로딩·SQL 관찰용 최소 예제'],['책의 주문 관리','선택 과제 · 요구사항은 실제 책에서 확인'],['단축 URL','별도 과제 · AI 프론트 연동 결과 공유']]))
add('운영','네 블록으로 관찰하고 비교',table([['블록','45분 활동 · 15분 휴식/정리'],['1','전환 피드백 · 영속성 컨텍스트'],['2','변경 감지·flush/clear · 지연 로딩'],['3','N+1 재현 → 개선 → SQL 수 비교'],['4','면접 설명 · 과제 공유 · GitHub 제출']]))
add('출발 자료','독립 실습 프로젝트로 관계를 관찰','<p><a href="assets/order-query-lab.zip">order-query-lab ZIP 다운로드 ↗</a></p>'+steps('product-api와 분리된 작은 프로젝트로 실행','완성 참고 코드가 포함된 비교·실험용 자료','답안을 보기 전 SQL 수를 예측하고 개선안을 직접 작성','상품 API에 수업용 관계를 억지로 추가하지 않기'))
section('01','JPA 전환 피드백','')
add('전환 회고','19일 결과를 세 가지로 설명',steps('기존 API 계약이 유지된 증거','파일 DB 재시작 보존과 테스트 격리 방법','Memory → Jpa 구현체 교체가 Service에 미친 영향','막힌 오류 하나의 원인·수정·재검증 결과'))
add('실행 확인','같은 조건으로 테스트를 비교',code('./gradlew test\n./gradlew test --tests "*PersistenceContextTest"\n./gradlew test --tests "*OrderQueryTest"')+call('order-query-lab 폴더 · Windows는 gradlew.bat'),kind='code-slide')
add('핵심 질문','같은 id 조회는 같은 객체일까요?',steps('하나의 영속성 컨텍스트 안에서 두 번 조회','객체 참조가 같은지 assertSame으로 확인','clear 후 다시 조회해 객체 상태 비교','같은 id와 같은 Java 객체라는 말을 구분'))
add('영속성 컨텍스트','Entity를 관리하는 범위',table([['상태','확인할 특징'],['새 객체','아직 persist되지 않은 객체'],['관리 상태','컨텍스트가 추적하는 Entity'],['준영속','clear 등으로 관리에서 벗어난 Entity'],['삭제 상태','삭제가 예약된 관리 객체']])+call('트랜잭션과 컨텍스트의 관계를 확인 · 전역 객체 보관함이 아닙니다.'))
add('1차 캐시','반복 조회의 조건을 함께 말하기',steps('같은 컨텍스트 안의 같은 id 조회를 관찰','테스트 사이 데이터·컨텍스트를 섞지 않기','clear 후 SQL이 다시 발생하는지 확인','2차 캐시·쿼리 캐시와 구분해서 설명'))
section('02','상태 변경과 SQL','')
add('변경 감지','관리 객체를 바꾸면 언제 반영되나요?',steps('트랜잭션 안에서 Entity를 조회','값을 변경하고 save 호출 여부를 기록','flush 후 clear하고 다시 읽어 실제 값 비교','준영속 객체 변경은 같은 결과인지 직접 확인'))
add('flush','DB에 SQL을 보내는 시점 확인',table([['행동','의미'],['flush','누적 변경을 DB와 동기화 · commit과 다름'],['clear','관리 중인 Entity를 컨텍스트에서 분리'],['commit','트랜잭션 확정'],['테스트 롤백','flush된 변경도 트랜잭션 종료 시 취소 가능']]))
add('실습 1','참조·변경·재조회를 증명',steps('PersistenceContextTest 실행 전 예상 결과 작성','동일성 테스트의 두 조회와 clear 위치 확인','변경 감지 테스트의 flush → clear → 재조회 확인','각 단언이 무엇을 증명하는지 문장으로 정리'))
add('주의','메모리 값만 확인하면 부족합니다',steps('변경 직후 같은 객체를 읽으면 DB 반영을 증명 못함','flush 없이 clear하면 반영 전 변경을 잃을 수 있음','flush가 성공해도 commit 성공과 같지 않음','로그와 테스트 결과를 함께 비교'))
add('지연 로딩','관계 데이터는 언제 읽힐까요?',table([['시점','관찰 대상'],['주문 목록만 조회','주문 SELECT'],['items에 실제 접근','미초기화 관계 SELECT 가능'],['트랜잭션 밖 미초기화 접근','LazyInitializationException 가능'],['이미 초기화된 관계','다시 접근해도 같은 추가 SQL은 없음']]))
add('실습 2','트랜잭션 밖 접근의 실패 관찰',steps('PersistenceContextTest의 관계 초기화 여부 확인','관계를 읽지 않고 컨텍스트를 종료','그 후 items 접근 결과와 예외를 확인','조회 목적에 맞는 로딩을 트랜잭션 안에서 설계'))
add('해결 방향','조회 용도를 명확히 정합니다',steps('Service 트랜잭션 안에서 필요한 관계를 조회','필요한 응답 DTO를 경계 안에서 구성','Entity를 Controller 응답으로 직접 직렬화하지 않기','OSIV=true로 예외를 숨기거나 EAGER로 일괄 변경하지 않기'))
section('03','N+1 재현과 개선','')
add('관계 모델','주문 하나가 여러 항목을 가집니다',table([['클래스','역할'],['PurchaseOrder','주문 루트 · items 컬렉션'],['OrderItem','주문 항목 · 상품명 중심의 최소 데이터'],['관계','단방향 @OneToMany · LAZY · JoinColumn'],['범위','주문 조회 실험 · 전체 주문 API 구현은 필수 아님']]))
add('데이터 준비','3개 주문 × 각 2개 항목',steps('각 테스트가 독립적으로 테스트 데이터 생성','seed를 flush하고 clear해 준비된 객체 제거','Hibernate 통계를 초기화한 뒤 측정 시작','조회와 items 접근에 발생한 SELECT만 비교'))
add('예측','목록 조회 후 항목을 읽으면?',table([['작업','예상 SQL'],['주문 3개 목록 조회','주문 SELECT 1회'],['첫 주문 items 접근','추가 SELECT 1회'],['나머지 주문 items 접근','추가 SELECT 2회'],['총합','이 실습 설정에서 4 SELECT']])+call('항목이 6개여서 7회가 아닙니다. 미초기화 컬렉션 단위로 관찰합니다.'))
add('재현','기본 조회로 4회를 확인',steps('findAllByOrderByIdAsc로 주문 목록 조회','모든 주문 items의 크기·값에 실제로 접근','statistics의 prepareStatementCount와 SQL 로그 비교','OrderQueryTest에서 기본 조회 4회를 확인'))
add('측정 조건','같은 조건이 아니면 숫자도 달라집니다',steps('seed INSERT는 flush 후 통계 초기화로 제외','1차 캐시는 clear로 비우고 측정','배치 페치·2차/쿼리 캐시 설정이 결과에 미치는 영향 확인','데이터·설정·접근 순서를 기록해 비교 가능하게 유지'))
add('개선 실습','필요한 항목을 함께 조회하세요',steps('OrderQueryRepository에 fetch join 조회를 직접 작성','메서드 이름은 findAllWithItems로 맞추기','주문이 항목 없이 존재해도 포함되도록 left join 검토','참고 구현과 비교하기 전 직접 테스트 실행'))
add('쿼리 읽기','fetch join은 연관 데이터도 로딩',code('select distinct o\nfrom PurchaseOrder o\nleft join fetch o.items\norder by o.id')+call('학습용 참고 쿼리 · Entity 이름과 필드명을 실제 코드에 맞춥니다.'),kind='code-slide')
add('개선 확인','같은 결과를 1 SELECT로 조회',steps('같은 3×2 데이터를 다시 준비하고 flush/clear','동일한 items 접근을 개선 조회로 수행','기본 4회 → 개선 1회를 비교','주문 수·항목 수·내용도 동일한지 단언'))
add('결과 표','속도 추측 대신 실행 근거를 남기기',table([['방식','주문 수','항목 수','SELECT'],['기본 조회 + items 접근','3','6','4'],['fetch join + items 접근','3','6','1'],['기록','동일 데이터','동일 단언','동일 측정 범위']]))
add('한계','관계를 모두 fetch하지 않습니다',steps('조회 화면에 필요한 관계만 선택','컬렉션 fetch join과 페이지네이션은 별도 검토 필요','복수 컬렉션을 한 번에 가져오는 문제는 선택 심화','조회 목적에 따라 DTO·EntityGraph·배치 전략 비교'))
add('완료 판정','숫자와 의미를 함께 설명',steps('기본 조회가 왜 4회인지 설명','fetch join이 무엇을 미리 읽는지 설명','flush·clear·통계 초기화가 필요한 이유 설명','테스트 통과만이 아니라 결과 내용 동일성 확인'))
section('04','설명과 결과 공유','')
add('면접 연습','한 문장 정의 뒤 실행 사례',table([['질문','답변에 포함할 근거'],['영속성 컨텍스트란?','관리 상태 · 같은 id의 동일성 · 범위'],['변경 감지란?','트랜잭션 · 수정 · flush · 재조회'],['지연 로딩과 N+1 관계는?','접근 시점 · 반복 접근 · SQL 4→1'],['왜 모두 EAGER로 안 하나요?','조회 목적 · 불필요 로딩 · 실제 SQL 확인']]))
add('동료 설명','예측 → 실행 → 비교 → 한계',steps('코드 실행 전 SQL 수를 동료에게 예측','로그·통계·단언으로 실제 결과 보여주기','예측과 다른 원인을 코드에서 찾기','개선의 범위와 적용하면 안 되는 경우 설명'))
add('단축 URL','AI 프론트와 백엔드 결과 공유',steps('<a href="../assignments/short-url/">별도 과제 안내 ↗</a>의 필수 범위 확인','생성 → 복사 → 실제 이동 → 오류 표시 시연','사용한 AI 프롬프트와 수정한 API 연결 설명','제출 마감은 별도 안내 · 미완료 항목 솔직히 표시'))
add('GitHub','필수 Issue 1개 · 병합 PR 1개',table([['항목','지정 값'],['Repository','sesac-spring-boot-study'],['Branch','practice/jpa-query-lab'],['Issue · PR','[실습] 지연 로딩과 N+1 관찰·개선'],['PR 본문','예측·SQL 비교·테스트·한계·Closes #실제번호']]))
add('저장 위치','독립 프로젝트와 문서를 연결',code('sesac-spring-boot-study/\n├── product-api/\n├── order-query-lab/\n│   ├── src/\n│   ├── build.gradle\n│   ├── gradlew\n│   └── README.md\n└── README.md')+call('압축 해제 후 중첩 .git 없이 추가 · 실제 프로젝트 폴더에서 실행'),kind='code-slide')
add('문서','실행 조건과 관찰 근거를 기록',table([['문서','기록'],['order-query-lab/README.md','실행·테스트·3×2 데이터·쿼리 4→1'],['Home · 01-Setup · 02-Architecture','프로젝트 링크·설정·관계·책과 구분'],['03-API · 04-Verification','주문 API는 미구현 표시 · SQL·단언·PR'],['05-Retrospective','오해 수정·적용 범위·면접 답변']]))
add('제출','테스트와 Wiki를 확인하고 병합',steps('main pull → Issue → 브랜치 → 실험·기록','전체 테스트 → commit·push → base main PR','Wiki는 별도 편집하고 PR에 링크','자체 점검·병합 → main pull → 최종 테스트'))
add('제출 확인','실행 가능한 코드와 증거만 포함',steps('Wrapper jar 포함 · 루트 ignore 예외 추가','!order-query-lab/gradle/wrapper/gradle-wrapper.jar','build/ · .gradle/ · IDE · DB · .env 제외','SQL 로그는 비밀값·개인 데이터 없이 필요한 부분만'))
add('선택 과제','다른 조회 전략과 비교하기',steps('동일 데이터에서 EntityGraph 방식 비교','페이지네이션이 필요할 때 별도 조회 전략 설계','주문 관리 전체 구현은 책 요구를 읽고 선택','단축 URL JPA 전환은 필수 과제와 분리해서 기록'))
add('최종 확인','무엇을 보고 판단했나요?',steps('상품 API 계약과 재시작 보존을 확인했다','영속성 상태·flush/clear를 테스트로 확인했다','지연 로딩·N+1과 개선을 SQL로 확인했다','단축 URL과 AI 활용 결과를 GitHub에 기록했다'))
section('참고','강사 참고 구현','')
add('참고 사용법','먼저 직접 작성하고 나중에 비교',steps('실습 작업과 테스트를 먼저 수행','막힌 지점의 힌트와 코드만 비교','참고 코드를 사용했다면 적용 범위 기록','전체 파일 버튼은 검증된 코드 원문을 표시'))
for name in SOURCES:
 add('강사 참고 구현',name,call('작업지 수행 후 참고용으로 확인합니다. 완성 파일은 버튼으로 펼칩니다.'),source=name)
add('참고','책과 공식 문서','<div class="references"><a href="https://docs.hibernate.org/orm/current/userguide/html_single/">Hibernate ORM ↗<span>Persistence context · Fetching · Statistics</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html">Spring Data JPA ↗<span>JPQL · Query methods · EntityGraph</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction.html">Spring 트랜잭션 ↗<span>트랜잭션 경계와 관리 상태</span></a></div>')
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-23-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.23</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="영속성과 쿼리를 관찰하는 JPA"><title>11월 23일 · 영속성과 쿼리를 관찰하는 JPA</title><style>'+css+'</style></head><body data-deck-revision="2026-11-23-v1-curriculum"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'reference buttons;',len(out.encode()),'bytes')
