from pathlib import Path
import html,json,re,textwrap
SOURCES = {}  # Keep previous product reference files separate from independent tasks.
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
TITLE='단축 URL · 주문 관리 API · JPA 입문'
add('2026.11.14','단축 URL · 주문 관리 API<br>JPA 입문','<div class="cover-bottom"><strong>개인 과제 테스트 풀이</strong><span>ORM · JPA · Spring Data JPA · 영속성 컨텍스트</span></div>',kind='cover')
add('수업 내용','개인 구현과 JPA 입문',table([['진행','내용'],['오전 · 3시간','단축 URL 서비스 요구사항 분석·구현·테스트'],['오후 · 3시간','주문 관리 API 요구사항 분석·구현·테스트'],['마지막 · 1~2시간','DB 연결 복습 · ORM·JPA·영속성 컨텍스트 입문']])+call('두 과제는 개인별로 풉니다. 구현한 코드와 실제 실행 결과로 설명합니다.'))
add('풀이 방법','요구사항을 읽고 직접 구현',steps('먼저 책의 과제 문제와 제공된 테스트 조건을 확인','책의 풀이 코드와 완성 예제는 닫고 설계·구현','막히면 오류 메시지·공식 문서·작성한 테스트부터 확인','도움받은 부분과 아직 완성하지 못한 부분을 기록'),note='문제 설명과 테스트 조건은 함께 읽되 정답 코드를 함께 따라 쓰지 않습니다. 강사는 요구사항과 오류 원인에 대한 힌트를 줍니다. 백엔드 완성 답안 생성이나 복사 대신 교육생이 자신의 코드로 해결하도록 안내합니다.')
section('01','CH 13 · 단축 URL 서비스 개발','')
add('오전 · 3시간','단축 URL · 책의 요구사항',steps('원본 URL을 받아 8글자의 단축 키를 발급','같은 원본 URL도 요청할 때마다 새로운 키 발급','이전에 발급한 키도 계속 원본 URL로 이동','이동할 때마다 횟수 증가 · 원본·단축 URL과 횟수 조회'),note='교재 CH 13과 저자 공식 예제 README의 기능 조건을 요약합니다. 짧은 주소를 만드는 API, 짧은 주소 이동, URL 정보 조회를 각각 구분합니다. API 경로와 응답 세부 형식은 문제 조건을 먼저 확인하고 자신의 계약을 기록합니다.')
add('단축 URL · 구현 범위','메모리 저장과 자동화 테스트',steps('DB 없이 컬렉션으로 단축 키와 원본 URL 저장','서로 다른 원본 URL에 같은 키가 배정되지 않게 처리','발급·이동·횟수·정보 조회의 자동화 테스트 작성','프론트 화면은 백엔드 완료 후 선택'),note='책의 과제는 DB 없는 컬렉션 저장을 전제로 합니다. 재시작하면 데이터가 초기화됨을 명시합니다. 12일 기존 프로젝트 DB 연결은 그대로 두고 별도 short-url/에서 구현합니다. 충돌 처리 방법은 직접 설계하되 키의 유일성을 보장해야 합니다.')
add('단축 URL · 설계','요청부터 이동까지',linear('원본 URL 등록 후 단축 주소로 접속하면 브라우저가 원본 URL로 이동합니다',[('등록 요청','원본 URL 전달'),('저장소','코드 ↔ 원본 URL'),('단축 주소 접속','3xx · Location')])+call('리다이렉트는 브라우저에 이동할 주소를 알려주는 응답입니다.'))
add('단축 URL · 수업 보충','입력과 실패 처리',steps('http·https로 시작하는 유효한 절대 URL만 허용','존재하지 않는 코드와 잘못된 URL을 구분해 응답','코드 충돌·중복 URL 정책은 문제 조건에 맞게 처리','원본 URL은 저장하며 서버가 해당 페이지를 가져오지 않음'),note='이 장표는 수업 보충 조건입니다. javascript:, data:, file:은 허용하지 않습니다. 메타데이터 수집과 URL 미리보기 서버는 만들지 않습니다. 성공과 실패 HTTP 계약은 책에서 정한 조건이 있으면 우선 적용하고 나머지는 README에 설명합니다.')
add('단축 URL · 직접 확인','코드와 실행 결과 설명',steps('URL 등록 → 발급된 주소 접속 → 실제 이동 확인','자신이 작성한 QA 체크리스트에 따라 실패 요청 확인','Controller·Service·Repository 역할을 코드에서 확인','남은 오류와 다음에 수정할 내용을 README에 기록'),note='정답 코드를 공개하지 않고 각자의 실제 결과로 확인합니다. 모든 교육생에게 새로운 DB 또는 JPA 전환을 동시에 요구하지 않습니다. 메모리 구현이면 재시작 시 초기화됨을 README에 표시합니다.')
section('02','CH 14 · 주문 관리 API 서버 개발','')
add('오후 · 3시간','주문 관리 · 시작 프로젝트',steps('저자 제공 14-1 시작 프로젝트의 구조와 상품 데이터 확인','빈 Order·Repository·Service를 직접 구현','여러 상품·수량으로 주문하고 주문 시점 이름·가격 보관','상품 금액 합계와 주문 상태를 함께 관리'),note='14-1은 문제 풀이용 시작 코드이며 14-2 완성 코드는 수업 중 열지 않습니다. 기존 상품 데이터와 제공 구조를 활용합니다. 각 상품 가격×수량을 합산해 주문 금액을 계산하고 첫 주문 상태는 CREATED입니다.')
add('주문 관리 · 책의 요구사항','구현할 API 5개',table([['요청','처리'],['POST /orders','여러 상품·수량 주문 · 재고 차감 · CREATED'],['PATCH /orders/{orderId}','주문 상태 강제 변경'],['GET /orders/{orderId}','주문 상세 조회'],['GET /orders?state={state}','해당 상태 주문 목록 · 없으면 []'],['PATCH /orders/{orderId}/cancel','CREATED 주문만 취소 · 주문 기록 유지']]),note='교재 과제의 상태 강제 변경 API에 임의의 상태 전이 제한을 더하지 않습니다. 상태 값과 요청·응답 필드는 제공된 시작 코드와 문제 조건을 확인합니다. 취소 후에도 주문을 조회할 수 있어야 합니다. 취소 시 재고 복원은 원문 필수 조건으로 추가하지 않습니다.')
add('주문 관리 · 요청과 응답','주문 데이터 형식',table([['구분','필드와 의미'],['POST 요청 본문','배열 · 각 항목은 id(상품 id), amount(주문 수량)'],['주문 응답','id · orderedProducts · totalPrice · state'],['orderedProducts의 각 항목','id · name · price · amount'],['주문 금액','totalPrice = 각 상품의 price × amount의 합']])+call('name·price는 주문 시점의 값을 저장합니다. 이후 상품 정보가 바뀌어도 주문 내역은 유지합니다.'),note='시작 코드와 책의 요청·응답 필드를 그대로 확인합니다. POST 요청 예시는 상품 id 1의 수량 2, 상품 id 2의 수량 1처럼 여러 항목의 배열입니다. amount는 수량이며 상품 id와 주문 id를 혼동하지 않도록 구분합니다.')
add('주문 관리 · 상태','상태 변경과 취소 구분',table([['요청·상태','규칙'],['PATCH /orders/{orderId}','요청 본문의 state 값으로 강제 변경'],['사용할 상태 값','CREATED · SHIPPING · COMPLETED · CANCELED'],['GET /orders?state={state}','지정한 상태의 주문 목록 반환'],['PATCH /orders/{orderId}/cancel','현재 CREATED일 때만 CANCELED로 변경']])+call('강제 상태 변경과 취소 API의 제약 조건은 서로 다릅니다.'),note='강제 상태 변경에 배송 순서 같은 추가 제약을 만들지 않습니다. 취소는 기록 삭제가 아닙니다. CANCELED 철자는 제공 코드의 enum과 맞춥니다.')
add('주문 관리 · 책의 요구사항','주문 실패와 데이터 보존',table([['상황','책에서 지정한 결과'],['상품 또는 주문이 없음','404'],['상품 재고가 부족함','500'],['CREATED가 아닌 주문 취소','500'],['여러 상품 중 하나라도 주문 불가','주문 생성 없음 · 모든 상품 재고 유지']])+call('500은 이 책의 과제 계약입니다. 모든 업무 오류를 500으로 처리하라는 원칙은 아닙니다.'),note='실제 API에서는 업무 충돌을 409 등으로 설계할 수 있으나 책의 과제 테스트를 푸는 동안에는 지정 계약을 유지합니다. DB나 JPA를 필수로 추가하지 않습니다. 메모리 구현에서도 검증을 먼저 하거나 변경 복구 등을 통해 부분 재고 차감을 남기지 않도록 설계합니다.')
add('주문 관리 · 설계','요청 처리와 업무 규칙 분리',table([['역할','구현할 내용'],['Controller','요청 DTO 받기 · 성공·실패 응답 만들기'],['Service·Domain','책에서 정한 주문 처리와 검증 규칙'],['Repository','주문 저장·조회 · 저장 방식 숨기기'],['테스트','정상·실패·데이터 보존 결과 확인']])+call('두 과제는 short-url/과 order-api/에서 분리합니다. 기존 프로젝트는 유지합니다.'))
add('주문 관리 · 직접 확인','요구사항과 테스트 결과 대조',steps('요구사항마다 구현 위치와 테스트 결과를 연결','실패 원인을 입력·업무 규칙·저장·응답 중에서 찾기','실제 실행한 요청과 응답을 README에 기록','완료한 기능·막힌 지점·설계 결정을 다른 교육생에게 설명'))
add('이론 적용 확인','구현 체크리스트',steps('□ 요청·응답 처리와 업무 규칙이 분리됐는가?','□ 저장·조회 코드를 Repository로 모았는가?','□ 잘못된 입력과 없는 대상을 구분하는가?','□ 실패 후 기존 값이 보존되는가?','□ 요구사항·직접 작성한 테스트·실행 결과가 일치하는가?'))
add('추가 과제 · 선택','테스트 보완과 AI 프론트',steps('필수 기능을 끝낸 뒤 경계 조건·중복 처리 테스트 보완','단축 URL 발급·결과·이동을 확인할 화면을 AI로 제작','순수 HTML·CSS·JavaScript만 사용 · 외부 라이브러리·CDN 금지','프롬프트는 자율 · QA 체크리스트를 직접 작성해 실행'),note='백엔드 완성 후 선택합니다. 실제 API를 fetch로 호출하고 샘플 화면과 실제 연동을 구분합니다. 응답 문자열은 textContent로 표시합니다. 프론트 전체 구현이나 JPA 전환은 두 과제의 필수가 아닙니다.')
add('제출','코드 · README · Issue · PR',table([['프로젝트','제출 내용'],['short-url/','단축 URL 구현 · 테스트 · 실행 방법'],['order-api/','주문 관리 API 구현 · 테스트 · 실행 방법'],['README','완료·미완료 기능 · QA 결과 · 도움받은 내용']])+call('개인 Fork의 sesac-spring-boot-study · origin에 Push · 브랜치 이름은 자율'),note='원본 main을 base, 개인 Fork 작업 브랜치를 head로 PR을 제출합니다. 공용 저장소 Issue와 PR에 변경 범위·관련 Issue #번호·실제 테스트 결과를 적습니다. 강사는 병합 없이 PR·Issue를 닫습니다. 두 과제는 한 PR의 변경 범위를 명확히 구분하거나 별도 PR로 제출할 수 있습니다. Gradle Wrapper를 포함하고 비밀값·build·.gradle·IDE 생성 파일을 제외합니다.')
section('03','Spring Data JPA와 DB 연동','')
add('DB 연결 복습','상품 객체와 DB 행',table([['Java 객체','products 테이블의 한 행'],['id = 1L','id = 1 · 기본 키'],['name = "키보드"','name = 키보드 · 문자열'],['price = 30000','price = 30000 · 정수']])+call('12일에는 JDBC로 SQL을 실행하고, 조회 결과를 Java 객체로 직접 옮겼습니다.'))
add('ORM','객체와 테이블을 연결하는 방법',linear('객체 매핑 정보를 사용해 ORM이 SQL 실행과 조회 결과 변환을 돕습니다',[('Java 객체','id · name · price'),('ORM','매핑 정보로 SQL 실행'),('DB 테이블','행 · 열 · 기본 키')])+call('ORM은 Object-Relational Mapping입니다. SQL과 DB가 없어지는 것은 아닙니다.'))
add('JPA · Hibernate · Spring Data JPA','세 가지 이름의 역할',table([['이름','의미'],['JPA','Java 객체를 DB에 저장·조회하는 표준 규칙과 API'],['Hibernate','JPA 규칙을 구현해 실제 SQL을 실행하는 구현체'],['Spring Data JPA','JPA를 이용해 Repository 구현을 줄여 주는 Spring 기능']])+call('Repository 메서드 → JPA API → Hibernate → JDBC → DB'),note='JPA 자체는 특정 DB도 구현체도 아닙니다. Spring Data JPA는 JPA의 대체물이 아니며 Hibernate는 대표 구현체입니다. 이 수업의 일반적인 실행 구성을 기준으로 설명합니다.')
add('Entity · Repository','무엇을 연결할지 정하기',table([['설정·코드','역할'],['@Entity · @Table','DB 표와 연결할 클래스와 테이블 지정'],['@Id · @GeneratedValue','기본 키와 식별자 생성 방식 지정'],['기본 생성자','JPA가 객체를 생성할 수 있게 public·protected로 제공'],['JpaRepository&lt;ProductEntity, Long&gt;','save·findById 같은 기본 저장·조회 메서드 제공']])+call('DB 접속 주소·드라이버·계정 설정은 여전히 필요합니다.'),note='Lombok @NoArgsConstructor가 필수인 것은 아닙니다. 직접 기본 생성자를 작성할 수 있습니다. 수업에서는 기존 Product 도메인과 ProductEntity를 구분합니다. JPA가 검증이나 업무 규칙을 대신하지 않습니다. save는 신규 여부에 따라 persist 또는 merge를 사용하며 호출 즉시 커밋을 보장하지 않습니다.')
add('영속성 컨텍스트','조회한 Entity를 관리하는 작업 공간',linear('EntityManager가 영속성 컨텍스트를 통해 Entity를 관리하고 DB와 동기화합니다',[('EntityManager','Entity 저장·조회 요청'),('영속성 컨텍스트','관리 중인 Entity'),('DB','SQL 실행 · 데이터 저장')])+call('새로 new한 객체는 아직 비영속 상태입니다. JPA로 조회한 Entity는 관리 대상이 될 수 있습니다.'),note='영속성 컨텍스트는 DB 자체나 서버 전체의 영구 저장소가 아닙니다. 이 수업은 Service 트랜잭션 안에서 조회·수정하고 종료하는 기본 사용 흐름을 기준으로 설명합니다. 영속성 컨텍스트를 벗어나 분리된 Entity는 변경 감지 대상이 아닙니다.')
add('영속성 컨텍스트','같은 Entity 조회 · 변경 감지',table([['트랜잭션 안에서 하는 일','관찰할 결과'],['같은 id의 Entity를 다시 find','같은 영속성 컨텍스트의 1차 캐시를 이용 가능'],['조회한 Entity의 가격을 변경','관리 중인 객체의 변경을 감지'],['flush 시점','변경 사항을 SQL로 DB에 반영']])+call('관리 중인 Entity를 트랜잭션 안에서 수정하는 상황입니다. 모든 객체의 변경이 저장되는 것은 아닙니다.'),note='1차 캐시는 같은 영속성 컨텍스트 범위의 식별자 기반 조회에 대한 설명이며 서버 공용 캐시가 아닙니다. JPQL 등 다른 조회는 SQL을 실행할 수 있습니다. 변경 감지와 flush 시점은 실제 SQL 로그로 다음 시간에 확인합니다.')
add('트랜잭션 · flush · commit','SQL 실행과 저장 확정은 다릅니다',table([['개념','상품 가격 변경 예'],['트랜잭션','조회 → 가격 수정 → 확정을 한 작업 단위로 묶기'],['flush','변경을 UPDATE SQL로 DB에 전달'],['commit','DB 트랜잭션의 변경을 최종 확정'],['rollback','아직 확정하지 않은 DB 변경을 취소']])+call('flush는 commit이 아닙니다. save 호출도 즉시 저장 확정이라는 뜻은 아닙니다.'),note='보통 쓰기 Service 메서드의 @Transactional 경계에서 작업합니다. flush는 커밋 전이나 쿼리 실행 전 등에도 일어날 수 있고 INSERT 실행 시점은 식별자 전략에 따라 달라집니다. 롤백이 Java 객체의 모든 필드까지 자동으로 원상 복구한다는 뜻은 아닙니다. 예외별 롤백 규칙과 프록시는 다음 수업에서 다룹니다.')
add('다음 수업','실행하면서 JPA 확인',cards(('16일','Entity·Repository','상품 저장·조회와 SQL 로그 확인'),('19일','저장소 JPA 전환','기존 API 결과를 유지하며 직접 구현'),('23일','관계·지연 로딩','연관관계와 N+1을 SQL로 관찰'))+call('오늘은 개념과 역할을 이해합니다. 두 과제의 JPA 전환은 필수가 아닙니다.'))
add('참고','교재 · JPA 공식 문서','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 목차 ↗</b><span>CH 13 · CH 14 과제 테스트</span></a><a href="https://github.com/lleellee0/java-for-backend/tree/main/14-1"><b>주문 관리 시작 코드 ↗</b><span>14-1 · 문제 풀이용 뼈대 코드</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html"><b>Spring Data JPA ↗</b><span>Entity 저장과 신규 상태 판단</span></a><a href="https://docs.hibernate.org/orm/current/userguide/html_single/"><b>Hibernate ORM ↗</b><span>매핑 · 영속성 컨텍스트 · flush</span></a><a href="../shared/db-basics/"><b>DB 기초 ↗</b><span>표 · SQL · 트랜잭션</span></a></div>')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 과제 테스트 직접 풀이와 JPA 입문"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v1-book"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
