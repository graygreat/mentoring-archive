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
add('2026.11.23 · 4시간','DB의 표부터<br>실행 SQL까지 관찰하기','<div class="cover-bottom"><strong>표 읽기 → SQL 예측 → Java 실행 → 결과 비교</strong><span>작은 주문 예제 · 상품 전환 피드백 · 과제 공유</span></div>',kind='cover')
add('오늘의 결과','코드보다 먼저 저장된 값을 읽습니다',steps('주문 표와 항목 표에서 PK·FK 관계를 찾기','한 주문의 항목을 읽는 SQL 시점 관찰','3개 주문을 읽는 4 SELECT를 1 SELECT로 개선','같은 결과인지 확인하고 자기 말로 설명'))
add('운영','네 블록으로 읽고 실행하고 비교',table([['블록','45분 활동 · 15분 휴식/정리'],['1','상품 전환 피드백 · 주문 표·FK·SQL JOIN'],['2','한 주문의 LAZY 관찰 · 같은 객체·flush/clear'],['3','3개 주문 N+1 재현 → fetch join → 같은 결과'],['4','동료 설명 · 단축 URL 공유 · GitHub 제출']]))
add('책과 연결','책의 상품 관리는 그대로 이어갑니다',table([['자료','역할'],['책의 상품 관리','19일 JPA 전환·재시작 결과 확인'],['order-query-lab','관계·SQL 관찰용 작은 독립 프로젝트'],['책의 주문 관리','전체 기능 구현은 선택 과제'],['단축 URL','별도 과제 · AI 프론트 연결 결과 공유']]))
add('출발 자료','실행 전에 작업지의 예측부터 작성','<p><a href="assets/order-query-lab.zip">order-query-lab ZIP ↗</a> · <a href="BEGINNER-WORKSHEET.md">쉬운 실습 작업지 ↗</a></p>'+steps('별도 order-query-lab 폴더에서 실행','<a href="../shared/db-basics/README.md">DB 기초 ↗</a>로 표·PK·FK·SQL 복습','참고 코드 포함 · 먼저 테스트의 기대 결과 예측','상품 API에는 수업용 관계를 추가하지 않기'))
section('01','표와 관계 읽기','')
add('전환 피드백','19일 상품 하나를 다시 확인',steps('실제 생성 id의 수정 값을 재시작 후 조회','요청은 같고 Memory가 Jpa 구현체로 바뀐 위치 찾기','테스트 DB와 실행 파일 DB의 URL 비교','미완료 오류는 재현 방법과 함께 기록'))
add('주문 표','주문 하나는 한 행입니다',table([['purchase_orders.id (PK)','label'],['A','주문 1'],['B','주문 2'],['C','주문 3']])+call('A·B·C는 설명용 실제 id의 별명입니다. DB가 만든 숫자를 직접 읽으세요.'))
add('항목 표','각 항목은 어느 주문에 속할까요?',table([['order_items.id (PK)','name','order_id (FK)'],['i1 / i2','노트 / 펜','A / A'],['i3 / i4','노트 / 펜','B / B'],['i5 / i6','노트 / 펜','C / C']])+call('표는 6행을 두 개씩 묶어 표시했습니다. order_id가 주문 표의 id를 가리킵니다.'))
add('PK와 FK','같은 숫자를 찾아 선으로 연결',linear('주문의 기본키가 항목의 외래키에서 참조됩니다',[('purchase_orders.id','PK · 주문 행 식별'),('order_items.order_id','FK · 어느 주문인가'),('order_items.id','PK · 항목 행 식별')])+call('주문 A ← order_id=A인 노트·펜. FK는 다른 표 행과 연결하는 값입니다.'))
add('SQL 먼저','한 주문의 항목을 읽는 방법',code('SELECT id, label\nFROM purchase_orders\nWHERE id = ?;\n\nSELECT id, name, order_id\nFROM order_items\nWHERE order_id = ?;')+call('?에는 같은 실제 주문 id를 넣는다고 읽습니다. 표·열 이름으로 조회합니다.'),kind='code-slide')
add('JOIN','두 표에서 연결된 값을 한 번에 읽기',code('SELECT o.id, o.label, i.name\nFROM purchase_orders o\nLEFT JOIN order_items i ON i.order_id = o.id\nORDER BY o.id;')+call('한 주문에 항목 2개면 결과 행도 2개. LEFT JOIN은 항목 없는 주문도 남깁니다.'),kind='code-slide')
add('Java와 연결','표의 값이 객체의 필드가 됩니다',table([['DB','Java'],['purchase_orders 한 행','PurchaseOrder 객체'],['label 열','getLabel()'],['order_id로 연결된 항목들','getItems() 컬렉션'],['order_items.name','각 OrderItem.getName()']]))
section('02','한 주문으로 SQL 관찰','')
add('LAZY','필요할 때 관계를 읽겠다는 설정',table([['코드 행동','이 실습의 관찰'],['주문 목록 조회','주문 SELECT · 항목은 아직 미초기화'],['첫 주문 getLabel()','이미 가져온 값 사용'],['첫 주문 getItems().size()','항목 SELECT가 추가될 수 있음'],['같은 항목을 다시 읽기','이미 초기화했다면 추가 조회 없음']])+call('LAZY라는 표시만 보고 항상 N+1이라고 판단하지 않습니다. 실제 접근과 SQL을 봅니다.'))
add('관찰 순서','한 주문의 항목을 읽기 전 멈추기',steps('OrderQueryTest의 기본 조회 테스트에서 시작','목록 조회 다음 줄에 중단점 설정 후 Debug 실행','첫 주문 label → items.size 순서로 접근하며 SQL 기록','테스트 마지막에는 3개 주문의 전체 항목도 확인'))
add('실행','관찰 대상 테스트를 골라 실행',code('./gradlew test --tests "*PersistenceContextTest" --info --rerun-tasks\n./gradlew test --tests "*OrderQueryTest" --info --rerun-tasks\n./gradlew test')+call('order-query-lab 폴더 · Windows는 gradlew.bat · 테스트 결과와 SQL 로그 함께 확인'),kind='code-slide')
add('실행 옵션','다시 실행하고 SQL 출력을 확인',table([['옵션','필요한 이유'],['--rerun-tasks','UP-TO-DATE 생략 없이 테스트를 다시 실행'],['--info','성공한 테스트의 표준 출력도 콘솔에서 확인'],['일반 성공 메시지만 보임','SQL을 못 봤다면 결과 보고서의 출력도 확인']]))
add('Windows','PowerShell에서 같은 테스트 실행',code('.\\gradlew.bat test --tests "*PersistenceContextTest" --info --rerun-tasks\n.\\gradlew.bat test --tests "*OrderQueryTest" --info --rerun-tasks')+call('order-query-lab 폴더에서 실행 · 관찰 후 전체 ./gradlew test로 최종 확인'),kind='code-slide')
add('SQL 보고서','콘솔이 길면 Standard output 탭 확인',steps('build/reports/tests/test/index.html을 브라우저로 열기','Classes → com.example.orderlab.OrderQueryTest 선택','Standard output에서 SQL과 lazy/fetch-select-count 확인','동일성 실험은 PersistenceContextTest 선택 · 실행마다 보고서 갱신'))
add('같은 객체','같은 id면 언제 같은 Java 객체일까요?',steps('PersistenceContextTest의 first와 두 번째 조회 비교','하나의 컨텍스트 안에서 assertSame으로 참조 확인','clear 후 다시 읽은 객체는 assertNotSame','같은 id라도 다른 컨텍스트까지 같은 객체라는 뜻은 아님'))
add('영속성 컨텍스트','지금 읽은 Entity를 관리하는 작업 공간',table([['행동','작업 공간·DB'],['findById(A)','A 객체를 관리 · 같은 id 반복 조회 재사용 가능'],['rename("변경")','관리 객체 값 변경 · 아직 확정된 DB 값과 구분'],['flush()','변경 SQL을 DB로 보내 동기화'],['clear() 후 findById(A)','관리 해제 후 재조회 · DB 값을 새 객체로 읽기']]))
add('세 단어','보내기와 확정과 비우기는 다릅니다',table([['용어','뜻'],['flush','변경 SQL 보내기 · 롤백 가능'],['commit','트랜잭션 성공으로 변경 확정'],['clear','관리하던 객체 분리 · DB 행 삭제 아님'],['테스트 rollback','flush했어도 해당 트랜잭션 변경 취소 가능']]))
add('실습','메모리 값과 DB 값을 구분하기',steps('rename 직후 같은 객체 값 확인만 하면 DB 증거 부족','flush → clear → findById 순서에서 변경 값 확인','첫 객체와 재조회 객체의 참조가 다른지 확인','각 줄 전후 관리 객체·SQL·DB 값을 작업지에 기록'))
add('관계 접근 범위','닫힌 작업 공간에서는 추가 조회가 어렵습니다',steps('미초기화 items를 둔 채 트랜잭션 종료','이후 items 접근 시 LazyInitializationException 관찰','이미 초기화된 items라면 같은 실패가 아닐 수 있음','Service 트랜잭션 안에서 필요한 관계·DTO를 준비'))
add('혼동 방지','불러온 범위와 사용 시점을 함께 확인',steps('Entity를 응답 JSON으로 그대로 반환하지 않기','OSIV=true나 EAGER 일괄 변경으로 문제를 덮지 않기','같은 컨텍스트 안의 같은 id가 1차 캐시의 핵심 조건','등록/관리 등 상태 이름 암기는 관찰한 뒤 정리'))
section('03','3개 주문을 비교하기','')
add('준비','3개 주문 × 각 2개 항목',steps('각 테스트가 주문 3개와 항목 6개를 새로 생성','seed flush: 준비 데이터 SQL을 먼저 DB로 보냄','clear: 준비 중 남은 관리 객체를 비움','statistics.clear: 준비 SQL 수를 제외하고 측정 시작'))
add('예측','왜 항목 6개인데 7회가 아닐까요?',table([['행동','이 실습의 SELECT 수'],['주문 3개 목록 조회','1회'],['주문 A의 items 읽기','추가 1회 · 항목 2개'],['주문 B·C의 items 읽기','추가 2회 · 각 2개'],['총합','4 SELECT = 목록 1 + 주문별 항목 3']]))
add('기본 조회','실제 로그에서 1 + 3 찾기',steps('findAllByOrderByIdAsc로 목록 조회','모든 주문의 items 크기·항목 이름에 접근','OrderQueryTest의 lazy-select-count=4 확인','주문 3개·항목 6개·이름 노트/펜도 같은지 확인'))
add('조건','다른 SQL이 섞이지 않았나요?',steps('prepareStatementCount는 모든 준비 SQL의 수','여기서는 측정 구간이 SELECT뿐이라 비교 가능','준비 INSERT와 테스트 종료 정리는 측정 범위 밖','배치 페치·2차/쿼리 캐시·미리 초기화 여부가 다르면 결과도 달라짐'))
add('개선','필요한 관계를 처음 조회할 때 함께 읽기',steps('OrderQueryRepository에서 findAllWithItems 확인','참고 쿼리를 보기 전에 JPQL 초안 작성','상품명이 아니라 주문과 items 관계를 지정','조회 결과가 같은지부터 확인하고 SQL 수 비교'))
add('SQL과 JPQL','이름과 가져오는 대상이 다릅니다',table([['종류','사용하는 이름·역할'],['SQL JOIN','purchase_orders·order_items · DB 표 행 결합'],['JPQL join','PurchaseOrder·o.items · 객체 관계를 이용한 조회'],['JPQL join fetch','조회한 Entity의 관계도 함께 로딩하도록 지정'],['주의','일반 join만으로 items 초기화가 보장되지는 않음']]))
add('참고 JPQL','필요한 items를 함께 로딩',code('select distinct o\nfrom PurchaseOrder o\nleft join fetch o.items\norder by o.id')+call('테이블명 대신 Entity·필드명 사용. 항목 없는 주문도 포함하도록 left join 선택.'),kind='code-slide')
add('개선 확인','같은 결과를 1 SELECT로 읽었나요?',table([['방식','주문','항목','SQL'],['기본 조회 + 모든 items 접근','3개','6개·노트/펜','4 SELECT'],['fetch join + 같은 접근','3개','6개·노트/펜','1 SELECT'],['비교 조건','같은 데이터','같은 값 단언','같은 측정 범위']]))
add('완료 기준','빠르다는 추측보다 증거를 남기기',steps('4회와 1회가 발생한 SQL 로그를 구분','데이터 개수뿐 아니라 주문명·항목 이름도 비교','준비 flush·clear·통계 초기화 이유를 한 문장씩 설명','LAZY는 항상 N+1 / EAGER면 해결이라는 말 수정'))
section('04','설명과 결과 공유','')
add('동료 설명','표 → 코드 → SQL 순서로 설명',steps('order_id가 어느 주문을 가리키는지 표에서 설명','items에 언제 접근했고 어떤 SQL이 실행됐는지 표시','4 → 1 개선 전후 결과 값이 같다는 근거 제시','flush와 commit, clear와 DELETE 차이를 설명'))
add('면접 연습','정의보다 본인 실험을 먼저 떠올리기',table([['질문','실험에서 꺼낼 근거'],['영속성 컨텍스트란?','같은 범위에서 같은 id의 객체 재사용'],['변경 감지란?','rename → flush → clear → 변경 값 재조회'],['N+1은 왜 생겼나요?','목록 1회 뒤 미초기화 items를 주문별 조회'],['왜 모두 EAGER로 안 하나요?','필요한 조회 범위와 실제 SQL로 결정']]))
add('단축 URL','AI 프론트와 백엔드 결과 공유',steps('<a href="../assignments/short-url/">별도 과제 안내 ↗</a> 확인','생성 → 복사 → 원본 이동 → 오류 표시 시연','프롬프트·본인 수정·API 연결을 설명','미완료 상태는 솔직히 기록 · 마감 별도 안내'))
add('GitHub','필수 Issue 1개 · 병합 PR 1개',table([['항목','지정 값'],['Repository','sesac-spring-boot-study'],['Branch','practice/jpa-query-lab'],['Issue · PR','[실습] 지연 로딩과 N+1 관찰·개선'],['PR 본문','예측·SQL·결과 값·Wiki 링크·Closes #실제번호']]))
add('문서','작업지 결과를 README와 Wiki에 누적',table([['문서','기록'],['order-query-lab/README.md','실행·표 관계·SQL 4→1·동일 결과'],['Home · 01-Setup · 02-Architecture','프로젝트·환경·PK/FK 관계'],['03-API · 04-Verification','API 미구현 표시 · SQL·단언·PR'],['05-Retrospective','틀린 예측·수정 이유·면접 답변']]))
add('제출','확인한 결과를 main에 반영',steps('main pull → Issue → 브랜치 → 관찰·기록','전체 테스트 → commit·push → base main PR','Wiki 별도 편집 → 링크 확인 → 자체 점검·병합','main pull → 최종 테스트 · 미완료는 구분 기록'))
add('저장 위치','별도 프로젝트로 보관합니다',code('sesac-spring-boot-study/\n├── product-api/\n├── order-query-lab/\n│   ├── src/\n│   ├── build.gradle\n│   ├── gradlew\n│   └── README.md\n└── README.md')+call('중첩 .git 없이 추가 · 실제 프로젝트 폴더에서 실행'),kind='code-slide')
add('제출 제외','소스와 관찰 증거만 Git에 포함',steps('Wrapper jar 포함 · 루트 .gitignore 예외 추가','!order-query-lab/gradle/wrapper/gradle-wrapper.jar','build/ · .gradle/ · IDE · DB · .env 제외','SQL 로그에는 필요한 부분만 · 비밀값·개인정보 제외'))
add('선택 심화','필수 관찰을 마친 뒤 읽습니다',steps('EntityGraph·배치 조회 전략 비교','컬렉션 fetch join과 페이지네이션의 제약 조사','복수 컬렉션 동시 조회는 별도 설계','책 주문 관리 전체 구현·단축 URL JPA 전환은 선택'))
add('최종 확인','예측과 실제가 달랐던 이유를 설명',steps('PK·FK와 SQL JOIN으로 표 관계를 설명했다','관리 객체·flush/clear를 실행 결과로 설명했다','동일 결과에서 N+1을 4 → 1로 개선했다','README·Wiki·PR과 별도 과제 진행 상황을 남겼다'))
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
