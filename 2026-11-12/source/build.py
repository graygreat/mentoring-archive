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
add('교재 CH 11','데이터베이스 연동','<div class="cover-bottom"><strong>상품 관리 애플리케이션</strong><span>책의 상품 API와 기존 개인 과제를 DB에 연결합니다.</span></div>',kind='cover')
add('수업 내용','수업 내용',steps('교재 CH 11을 함께 읽고 DB의 기본 용어를 확인합니다.','product-api의 저장소를 메모리에서 DB로 바꿉니다.','personal-project의 위시리스트를 DB에 저장합니다.','완료한 기능을 확인하고 구현 범위를 PR로 제출합니다.'),note='4시간 수업입니다. 책 읽기와 교육생 직접 구현을 오가며 진행하고 강사 코딩 시연은 하지 않습니다. 책의 상품 관리 애플리케이션이 기준이며 기존 Java 17·Spring Boot 4 프로젝트를 이어갑니다.')
add('교재 CH 11','책에서 함께 읽을 부분',table([['순서','교재의 내용'],['1','데이터베이스를 사용하는 웹 애플리케이션'],['2','데이터베이스 다뤄 보기'],['3·4','상품 추가 기능 구현하기 → 상품 조회/수정/삭제 구현하기']])+call('구체적인 코드 설명은 책을 보며 진행합니다. JDBC 방식으로 기존 프로젝트에 적용합니다.'),note='판본별 쪽수는 책에서 확인합니다. 교재에서 사용하는 JDBC 접근 방식과 설정을 직접 읽고 따릅니다. 책 원문을 확인하지 않은 특정 JDBC API를 교재 방식이라고 단정하지 않습니다. 오늘 JPA로 바꾸거나 새 프로젝트를 만들지 않습니다.')
add('DB 기초','Java 객체·JSON·DB 행',table([['형태','상품 하나를 표현하는 방법'],['Java 객체','Product 객체 · 실행 중인 Java 프로그램에서 사용'],['JSON','{"id": 7, "name": "키보드", "price": 50000} · HTTP로 전달'],['DB 행','products 테이블의 id=7인 행 · 파일 DB에 저장한 기록']])+call('Repository가 DB 행을 읽어 Product로 복원하고, Controller가 응답 DTO를 반환합니다.'))
add('DB 기초','테이블·행·열·기본 키',table([['용어','products 예시'],['테이블·행','상품을 모은 표 · 상품 한 개가 한 행'],['열','id, name, price처럼 각 행에 저장할 항목'],['기본 키 · PK','id로 한 행을 식별 · 서로 다른 상품의 id는 중복할 수 없음']])+call('상품 이름이 같아도 서로 다른 행일 수 있습니다. 조회·수정·삭제는 id로 대상을 찾습니다.'))
add('DB 기초','자료형과 NULL',table([['값','설계에서 구분할 내용'],['정수·문자열','id·price는 정수, name은 문자열 · Java와 DB 자료형을 맞추기'],['NULL','아직 값이 없다는 뜻 · 가격 0원이나 빈 문자열과 다름'],['제약 조건','PK·NOT NULL·UNIQUE로 DB가 지켜야 할 규칙을 지정']])+call('가격 0은 정상 값입니다. 필수 가격의 NULL을 0으로 바꾸어 저장하지 않습니다.'),note='필수 name·price는 기존 입력과 도메인 검증을 유지합니다. 외부 상품 메타데이터처럼 값이 없는 것이 허용되는 열은 별도로 결정합니다. 수동 상품의 외부 id가 NULL일 수 있으므로 외부 식별자 중복 제약과 함께 설계합니다.')
add('DB 기초','SQL 네 가지 작업',table([['SQL','상품 API에서 하는 일'],['INSERT · SELECT','상품 행 추가 · 저장된 상품 조회'],['UPDATE','조건에 맞는 기존 행의 값 수정'],['DELETE','조건에 맞는 기존 행 삭제']])+call('UPDATE·DELETE는 id 조건을 지정합니다. 입력값은 SQL에 이어 붙이지 않고 바인딩합니다.<br>목록 순서는 ORDER BY로 명시합니다.'),note='각 SQL은 교재의 상품 테이블을 보며 읽습니다. 상세 SQL 완성 답안을 배포하지 않고 테이블과 SQL은 교육생이 설계합니다. 조건 없는 UPDATE·DELETE가 여러 행에 영향을 주는 이유를 확인합니다.')
add('저장 흐름','메모리 대신 DB에 저장',linear('Service가 Repository 인터페이스를 통해 DB 저장 구현을 사용합니다',[('Service','기존 업무 규칙'),('Repository','인터페이스 유지'),('DB 구현','SQL 실행·객체 복원'),('DB','상품 행 보관')])+call('Controller·Service·DTO의 HTTP 계약은 유지하고 저장 구현을 교체합니다.'),note='기존 Map의 항목이 DB로 자동 이관되지는 않습니다. 필수 검증은 DB 전환 후 API로 저장한 데이터가 실제 DB 행과 재시작 후에도 남는지입니다. 기존 기능과 테스트의 동작 계약을 보존하며 메모리 항목 자동 이관을 요구하지 않습니다. 기존 메모리 저장 구현은 보존할 수 있지만 실행 시 실제 사용할 Repository 빈은 메모리 또는 DB 중 하나만 선택합니다. 두 구현을 모두 자동 등록해 주입이 모호해지지 않도록 책의 설정 방식에 맞춰 구성합니다.')
add('실행 설정','앱 DB와 SQL 연습 DB 구분',table([['용도','H2 연결 URL'],['책 상품 API','jdbc:h2:file:./data/products'],['개인 위시리스트','jdbc:h2:file:./data/wishlist'],['독립 SQL 연습','jdbc:h2:mem:db_basics · 종료하면 사라지는 연습용']])+call('Java 17·Spring Boot 4의 기존 설정을 유지합니다. JDBC·H2 설정은 책과 공식 문서를 확인합니다.'),note='DB 드라이버와 JDBC 접근에 필요한 의존성을 기존 build.gradle에 추가합니다. 임의의 별도 버전을 섞지 않고 프로젝트 Spring Boot의 의존성 관리를 따릅니다. 메모리 H2는 영구 저장 확인에 사용하지 않습니다. 파일 URL은 실행 작업 디렉터리를 기준으로 하므로 프로젝트와 실행 위치를 함께 기록합니다.')
add('DB 준비','재시작해도 같은 DB 사용',steps('책의 테이블 SQL을 확인하고 CREATE TABLE IF NOT EXISTS 등으로 준비합니다.','동일한 파일 URL·작업 디렉터리로 앱을 종료한 뒤 다시 실행합니다.','시작할 때마다 DROP·TRUNCATE하거나 초기 데이터로 덮어쓰지 않습니다.')+call('JPA의 ddl-auto는 JDBC 테이블을 자동 생성하는 설정이 아닙니다.'),note='schema.sql 등 초기화 기능을 선택하면 실제 실행 조건과 기존 테이블이 있을 때의 동작을 확인합니다. 실행마다 전체 삭제·고정 id 재삽입을 하지 않습니다. 파일 DB 경로를 바꾼 뒤 데이터가 사라졌다고 오해하지 않도록 URL과 작업 디렉터리를 확인합니다. 테스트는 앱 파일 DB와 분리합니다.')
add('식별자','DB가 만든 id를 사용',table([['시점','구현할 동작'],['추가','DB가 발급한 키를 읽어 생성 결과에 반영'],['조회','행을 Domain 객체로 복원할 때 저장된 id를 유지'],['수정·삭제','요청받은 기존 id로 처리 · 없는 id를 새 행으로 만들지 않음']])+call('DB 구현에서 AtomicLong이나 MAX(id)+1로 id를 만들지 않습니다.'),note='생성 결과의 실제 DB id를 응답과 Location에 사용합니다. 조회할 때 신규 생성용 생성자를 그대로 써 id를 재발급하지 않도록 복원 경로를 구분합니다. Domain 규칙을 우회하지 않되 DB 행의 식별자는 보존합니다.')
add('Repository','기존 인터페이스로 DB 구현 연결',steps('Repository 인터페이스의 저장·조회·수정·삭제 계약을 확인합니다.','DB 구현이 SQL 결과를 Domain 객체로 바꾸도록 작성합니다.','Service에 DB 구현을 생성자로 주입하고 사용할 빈 하나를 선택합니다.')+call('Service에 SQL을 옮기거나 Controller에서 DB를 직접 다루지 않습니다.'),note='수업에서는 기존 클래스 책임을 유지하면서 저장 방식만 바꿉니다. JDBC 접근 코드는 책의 구현을 참고합니다. 메모리 Repository를 삭제해야만 DB 구현을 사용할 수 있는 것은 아니며 실행 설정으로 한 구현을 선택할 수 있습니다.')
add('책 실습','상품 API를 DB에 연결',steps('CH 11의 상품 추가를 적용하고 DB가 발급한 id를 확인합니다.','조회·수정·삭제를 연결하고 기존 응답 상태·헤더·본문을 유지합니다.','DB의 실제 행을 확인하고, 같은 설정으로 재시작해 동일한 id·값을 조회합니다.')+call('기존 product-api/에서 구현합니다. 책의 코드를 읽은 뒤 직접 적용합니다.'),note='책과 기존 API의 필드·생성자·메서드가 다르면 자신의 코드에 맞춰 적용합니다. 기존 정상·실패 동작을 바꾸는 기능 추가가 아니라 저장 구현 전환입니다. 가격 0, 입력 누락/null, 없는 id의 HTTP 계약을 유지합니다.')
add('실패 처리','실패한 요청은 DB도 그대로',table([['상황','지켜야 할 동작'],['잘못된 입력','기존 400 응답 · 저장 전에 규칙 검사'],['없는 id 수정·삭제','영향받은 행 수가 0이면 404'],['저장 중 실패','부분 저장 없이 기존 값과 행을 유지']])+call('HTTP 400을 반환했다는 이유만으로 DB 변경이 자동 취소되지는 않습니다.'),note='SQL 실행 결과의 affected rows를 확인합니다. UPDATE·DELETE가 예외 없이 끝나도 대상이 없을 수 있습니다. 여러 쓰기가 한 작업을 이루면 트랜잭션이 필요할 수 있으며 HTTP 상태 변환과 DB 트랜잭션은 서로 다른 책임입니다. 구체 설정은 교재와 사용 중인 JDBC 방식에 맞춰 확인합니다.')
add('과제','과제',kind='section')
add('필수 과제','기존 위시리스트를 DB에 저장',table([['대상','유지하거나 저장할 내용'],['기본 필드','id·name·price와 실제 구현한 기존 필드'],['외부 상품 정보','source·externalId·category·image·stock 등 구현한 메타데이터'],['진행 순서','위시리스트 DB 연동 완료 → 기존 미완료 기능 이어서 구현']])+call('기존 personal-project/를 이어갑니다. 새 프로젝트나 JPA 전환은 요구하지 않습니다.'),note='실제 필드 이름은 기존 구현에 따릅니다. 기존 외부 이미지 필드가 thumbnail이면 임의로 image로 바꾸도록 강제하지 않습니다. 9일 선택 기능을 모두 끝내지 못한 교육생은 위시리스트 DB 연동을 먼저 완료한 뒤 미완료 기능을 이어갑니다. 수동 상품과 외부 상품을 모두 복원할 수 있게 설계합니다.')
add('필수 과제','기존 API와 추천 규칙 유지',steps('가격 0·입력 검증·400·404 등 기존 API 동작을 유지합니다.','추천과 정렬의 동률이면 기존 등록 순서를 유지합니다.','목록 SQL에 ORDER BY를 명시하고 기존 테스트를 유지합니다.')+call('테이블 구조·SQL·등록 순서 보존 방법을 직접 정해 README에 기록합니다.'),note='DB의 기본 반환 순서는 보장된 등록 순서가 아닙니다. id 또는 생성 순서 필드 등 실제 설계한 기준과 정렬 방향을 명시하고 동률 처리까지 기존 계약과 맞춥니다. 구현되지 않은 추가 추천 기능을 새로 필수로 만들지는 않습니다.')
add('필수 과제','외부 상품 식별자와 중복 처리',table([['항목','요구사항'],['식별자','내 로컬 id와 외부 source·externalId 구분 유지'],['중복 방지','외부 식별자 조합에 DB UNIQUE 제약 · 충돌은 409로 변환'],['외부 요청 실패','불완전한 외부 값을 저장하지 않고 기존 DB 유지']])+call('수동 상품의 이름 중복은 허용합니다. 이름에 UNIQUE를 새로 걸지 않습니다.<br>외부 상품 이름·가격·메타데이터는 저장한 값을 복원하며 자동 갱신하지 않습니다.'),note='애플리케이션의 사전 중복 검사만으로 DB 중복 제약을 대체하지 않습니다. DB 유니크 위반 중 외부 상품 식별자 충돌에 해당하는 것을 기존 409 계약으로 변환하고 모든 DB 오류를 409로 덮지 않습니다. 수동 상품의 외부 식별자 NULL 처리와 DB 유니크 제약을 함께 검토합니다. 외부 호출·쿠폰·추천·검증 기능을 제거하지 않습니다.')
add('완료자 확장','장바구니도 DB에 저장',table([['저장할 값','유지할 규칙'],['장바구니 행','행 id·원본 로컬 id·수량을 보존'],['상품 복사본','처음 담은 이름·단가·재고를 별도 보존'],['원본 변경·삭제','원본 삭제를 막거나 장바구니를 함께 삭제하지 않도록 FK 설계']])+call('쿠폰 선택과 금액 미리보기는 저장 상태로 추가하지 않습니다. 기존 계산 규칙을 유지합니다.'),note='위시리스트 DB 연동을 끝낸 교육생이 진행합니다. 원본 상품이 삭제되어도 장바구니 줄과 처음 저장한 단가·재고가 유지돼야 합니다. 원본 변경을 조회 시 자동 반영하는 조인만으로 스냅샷을 대신하지 않습니다. FK의 ON DELETE CASCADE로 장바구니를 함께 지우거나 RESTRICT로 원본 삭제를 막아 기존 계약을 바꾸지 않습니다. 스냅샷과 원본 관계를 분리하거나 삭제 시 관계만 해제하는 등 자신의 DB 구조에 맞게 설계합니다. 중복 담기·수량 변경·삭제 후 다시 담기의 기존 복사 규칙을 유지합니다.')
add('저장 단위','여러 쓰기는 함께 성공하거나 취소',steps('하나의 요청에서 두 번 이상 저장하는 부분이 있는지 찾습니다.','중간 저장이 실패해도 일부 결과만 남지 않게 처리합니다.','트랜잭션이 필요한 범위를 책과 함께 확인하고 README에 설명합니다.')+call('트랜잭션은 여러 DB 변경을 하나의 작업 단위로 묶는 방법입니다.'),note='예를 들어 한 업무가 여러 행을 함께 변경한다면 전체 성공 또는 전체 취소가 필요합니다. 트랜잭션의 구체 API를 새 강의로 확장하지 않고 교재 수준에서 적용 범위를 확인합니다. 쿠폰 미리보기처럼 읽기 계산만 하는 작업에 저장 상태를 새로 만들지 않습니다. 예외를 잡아 HTTP 400으로 바꾸는 것 자체가 롤백 설정은 아닙니다.')
add('QA·테스트','직접 확인할 항목 작성',table([['확인 방법','남길 결과'],['수동 QA','본인이 정상·실패·재시작 항목을 정하고 실제 결과 기록'],['Repository 통합 테스트','별도 테스트 DB에서 SQL·객체 복원·실패 보존 확인'],['기존 단위 테스트','기존 검증·추천·쿠폰 계산 테스트 유지']])+call('테스트에서 앱의 파일 DB를 삭제하거나 초기화하지 않습니다.'),note='상세 정답 체크리스트를 대신 배포하지 않습니다. 의미 있는 DB 통합 테스트로 실제 저장·조회·수정·삭제와 id 보존을 검증합니다. 테스트 전용 DB·URL을 사용해 앱 데이터를 오염시키지 않습니다. 단순 모의 Repository 호출 검증만으로 SQL 동작을 확인했다고 하지 않습니다. 재시작 검증은 같은 파일 URL과 작업 디렉터리로 실제 수행합니다.')
add('설계 확인','적용한 내용을 설명하기',steps('HTTP·Service·Repository의 책임과 인터페이스를 유지했는가?','DB id와 행의 자료형·NULL·중복 제약을 설명할 수 있는가?','기존 규칙과 실패 시 데이터 보존을 확인했는가?','같은 DB로 재시작한 결과와 실제 완료 범위를 기록했는가?'),note='발표 전에 자기 코드와 DB를 근거로 확인합니다. 화면에 체크 표시만 적는 것이 아니라 SQL·복원 코드·실행 결과로 설명하도록 합니다.')
add('GitHub 제출','DB 연동 결과 제출',table([['항목','제출할 내용'],['Issue·PR 제목','[11/12][이름] 기존 과제 DB 연동'],['README','테이블·SQL·실행 설정·QA·테스트·완료/미완료 범위'],['PR 본문','책 실습과 개인 과제의 실제 변경 범위 · 이전 PR 링크']])+call('개인 Fork에 Push → 공용 sesac-spring-boot-study에 Issue 1개·PR 1개.<br>이전 구현에서 자율 브랜치로 시작하고 리뷰 수정도 같은 브랜치에 Push합니다.'),note='base는 조직 원본 sesac-ddm-4-web/sesac-spring-boot-study의 main, head는 개인 Fork의 작업 브랜치입니다. 개인 origin으로 Push합니다. 원본 main을 받아 자신의 지난 구현을 대체하지 않습니다. 강사는 병합 없이 PR·Issue를 닫고 교육생의 작업 브랜치는 보존합니다. 실제 DB 데이터 파일·비밀값·build/.gradle/IDE 파일을 제출하지 않고 실행 가능한 소스와 Gradle Wrapper는 유지합니다. 필수 PR을 둘로 나누거나 자가 병합하도록 요구하지 않습니다.')
add('다음 수업','14일 · 단축 URL·주문 API·JPA',steps('오전 3시간 · 단축 URL 과제 테스트를 직접 풀이합니다.','오후 3시간 · 주문 관리 API 과제 테스트를 직접 풀이합니다.','마지막 1~2시간 · ORM·JPA·Spring Data JPA·영속성 컨텍스트를 소개합니다.'),note='먼저 책의 과제 요구사항을 확인한 뒤 풀이 코드와 완성 예제는 최대한 보지 않고 개인별로 구현합니다. 기존 상품·위시리스트 DB 연동 결과는 보존합니다. 두 과제의 필수 구현에 새 JPA 전환을 추가하지 않으며, JPA는 다음 주에 이어 학습합니다.')
add('읽기와 참고','교재와 공식 문서','<div class="references"><a href="https://www.yes24.com/product/goods/124434554"><b>교재 CH 11 ↗</b><span>상품 관리 애플리케이션에 데이터베이스 연동하기</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/jdbc.html"><b>Spring JDBC ↗</b><span>교재의 JDBC 접근 방식과 비교</span></a></div>'+call('아래 파일은 기존 HTTP 검증·예외 처리 보충 코드입니다. DB 구현 완성 답안이 아닙니다.'),note='JDBC·H2 설정은 현재 프로젝트 버전과 공식 문서를 확인합니다. 참고 파일은 기존의 입력 DTO·Controller·예외 핸들러이며 오늘 DB 구현 코드를 제공하는 파일이 아닙니다.')

# Keep complete supplementary files reachable without restoring code lecture pages.
S[-1]['body'] += '<div class="inline-list">'+''.join('<button type="button" data-source-key="'+esc(key)+'">'+esc(key)+'</button>' for key in SOURCES)+'</div>'
S[-1]['note'] += ' 파일 이름 버튼은 기존 HTTP 검증·예외 처리의 전체 보충 코드를 엽니다. DB 연동 구현은 교재를 읽고 직접 작성합니다.'
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-12-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.12</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 CH 11과 기존 상품 API·개인 위시리스트의 데이터베이스 연동"><title>11월 12일 · 데이터베이스 연동</title><style>'+css+'</style></head><body data-deck-revision="2026-11-12-v2-database"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',len(out.encode()),'bytes')
