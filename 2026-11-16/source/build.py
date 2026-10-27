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
DAY='2026-11-16'
TITLE='상품 Entity와 JPA 저장소'
from code_examples import DAY16_PROPERTIES, TEST_PROPERTIES, JPA_DEPENDENCIES
add('일곱 번째 수업','상품 데이터를<br>Entity와 Repository로','<div class="cover-bottom"><span>2026.11.16 MON · 4시간</span><strong>책의 저장 흐름 → JPA 기본 동작·테스트</strong></div>',kind='cover')
add('책과 함께','CH 11의 DB 접근과 JPA를 비교',steps('책에서 상품 저장·조회와 DB 연동 흐름 읽기','JDBC 코드가 맡는 일과 Repository 책임 설명','수업 독립 Entity·Repository를 작성·테스트','CH 12의 추상화를 유지하며19일 전환 준비'),note='정확한 페이지와 본문 코드를 자료에서 단정하지 않습니다. 책을 직접 펴서 상품 DB 접근 절을 확인합니다. 교재 JDBC 구현과 수업 JPA 구현을 같은 코드라고 설명하지 않습니다.')
add('네 블록 운영','읽기 → 작성 → 실행 → 설명',table([['블록','45분 활동 · 15분 휴식·정리'],['1','DB 전제 확인15분 · 상품 매핑·설정30분'],['2','Entity·저장·조회 실습45분'],['3','조건 검색·테스트 읽기45분'],['4','트랜잭션 첫 관찰·테스트·19일 준비45분']])+call('강사 코딩 시연 없이 작업지와 비교 코드를 사용합니다.'))
add('오늘 경계','JPA 연습과 API 전환을 구분',cards(('오늘 실행','JPA Entity·Repository 테스트','실제 DB 저장·조회·쿼리 검증'),('현재 API','Memory 저장소 유지','기존 CRUD·HTTP 회귀 유지'),('19일 작업','JPA Adapter로 교체','Service 계약·API 응답 유지')))
add('완료 기준','DB 동작을 테스트와 SQL로 설명',steps('상품 Entity와 Spring Data Repository 작성','기본 CRUD·조건 쿼리·JPQL 테스트 통과','트랜잭션 안의 변경 감지를 설명','19일 전환 대상과 준비 상태 기록'))
section('01','Entity와 저장소의 역할','')
add('DB 먼저 확인','상품 세 개를 표로 읽어보기',table([['id · PK','name','price'],['실제 발급값 A','노트','3000'],['실제 발급값 B','무료','0'],['실제 발급값 C','펜','1000']])+call('질문: price ≤ 1000이면 어느 두 행인가요? PK는 행을 구분하는 값 · 행 순서와 id 연속은 가정하지 않습니다.'))
add('같은 상품의 세 모습','화면의 값과 업무 객체와 저장 객체',table([['이름','하는 일','같은 상품 예'],['요청 DTO','JSON 입력을 Java로 받기','name=노트, price=3000'],['Product','업무 규칙을 지키는 상품','new Product(id, "노트", 3000)'],['ProductEntity','DB에 저장할 모양과 표를 연결','new ProductEntity("노트", 3000)']])+call('한 사람이 상황에 맞는 옷을 입듯 역할별 모양을 구분합니다. DTO에 @Entity를 붙이는 활동이 아닙니다.'))
add('상품 하나 추적','오늘은 DB 쪽 연결을 따로 연습',linear('오늘 테스트하는 저장 흐름',[('ProductEntity','노트 · 3000'),('Repository.save','저장 요청'),('products 행','실제 id · 노트 · 3000')])+call('입력 JSON {"name":"노트","price":3000} → Product는 기존 API 흐름. 이 흐름과 DB 연결은19일에 Adapter로 이읍니다.'))
add('앞으로 연결할 전체 흐름','입력부터 행으로, 행에서 응답으로',steps('요청 JSON → 요청 DTO → Service의 Product','19일 Adapter: Product 값 → ProductEntity → Repository','JPA가 INSERT 실행 → products에 실제 id를 가진 행','SELECT → ProductEntity → toProduct() → 응답 DTO'),note='오늘은 Repository 테스트로 가운데 저장·조회를 증명합니다. 실제 HTTP 경로는 Memory입니다. 전체 흐름을 이미 연결한 것으로 설명하지 않습니다.')
add('Entity의 뜻','Java 필드와 DB 열을 연결하는 객체',table([['Java 코드','DB에서 의미'],['@Entity','JPA가 저장 대상으로 관리하는 클래스'],['@Table(name = "products")','연결할 테이블은 products'],['id / name / price','상품 행의 식별자 / 이름 / 가격'],['ProductEntity 객체 한 개','저장된 상품 한 행과 연결']])+call('질문: Entity 클래스 한 개는 행 하나인가요, 표의 모양인가요? 클래스는 모양이고 객체가 한 상품을 담습니다.'))
add('Entity의 식별자','@Id와 @GeneratedValue',steps('@Entity가 영속화 대상 클래스를 표시','@Id가 Entity의 식별자 필드를 표시','생성 전략에 따라 DB가 id를 발급','새 Entity id는 null · 저장 이후 실제 id 확인'),note='DB 생성 id를1부터 연속이라고 가정하지 않습니다. primitive long 대신 Long을 쓰는 새 Entity 상태의 의미를 설명합니다. 기존 도메인Product id와 변환은19일 Adapter에서 다룹니다.')
add('기본 생성자와 규칙','JPA가 만드는 객체의 입구를 구분',table([['구성','이유'],['protected 기본 생성자','JPA가 Entity를 구성할 수 있는 기본 진입점'],['업무 생성자·변경 메서드','정상적인 값 생성과 변경을 표현'],['DB 컬럼 제약','필수·저장 타입과 업무 검증의 차이'],['DTO·도메인 검증','사용자 입력과 업무 규칙 유지']])+call('오늘 먼저 확인할 것: id·name·price와 표의 연결. 긴 이름 저장 설정은 비교 코드의 참고 항목입니다.'),note='기존 Memory 상품 이름은 길이 상한이 없습니다. 기본 VARCHAR(255)로 전환하면 허용하던 긴 이름이 DB 오류가 되므로 수업 예제는 @Lob으로 매핑하고300자 왕복 테스트로 보존을 확인합니다. 이 선택은 수업 독립 매핑이며 교재 요구가 아닙니다. 운영에서는 실제 이름 길이 정책과 검색·정렬·인덱스 요구를 함께 설계합니다.')
add('Spring Data Repository','인터페이스로 제공받는 기본 동작',table([['메서드','확인할 것'],['save','새 Entity 저장과 반환 id'],['findById','Optional · 존재/부재'],['findAll','조회 결과 · 순서 보장 여부'],['deleteById','삭제 뒤 부재 확인']])+call('기본 findAll 결과 순서를 임의로 가정하지 않습니다.'))
add('저장하고 실제 id 받기','id를 추측하지 말고 반환값에서 읽기',code('ProductEntity saved = repository.saveAndFlush(new ProductEntity("노트", 3000));\nLong id = saved.getId();\nProductEntity found = repository.findById(id).orElseThrow();')+call('위 세 줄은 테스트 본문 안의 발췌입니다. 실제 코드는 아래 전체 파일을 참고합니다. 저장 전 id=null → 저장 후 DB가 발급한 Long 값.'),kind='code-slide')
add('SQL과 객체를 나란히','INSERT는 행 추가 · SELECT는 행 읽기',code('INSERT INTO products (name, price, id) VALUES (?, ?, default);\nSELECT id, name, price FROM products WHERE id = ?;')+table([['물음표에 들어갈 값','어디서 왔나요?'],['노트 · 3000','ProductEntity 필드'],['SELECT의 id','saved.getId()의 실제 반환값']])+call('대표 SQL 모양입니다. 실제 별칭·컬럼 순서는 Hibernate 로그에서 확인합니다.'),kind='code-slide')
add('두 Repository의 차이','이름은 비슷해도 맡은 약속이 다릅니다',table([['기존 ProductRepository','새 SpringDataProductRepository'],['Service가 요구하는 상품 저장 약속','JPA Entity를 저장하는 Spring Data 약속'],['Product를 주고받음','ProductEntity를 주고받음'],['MemoryProductRepository가 구현 중','Spring Data가 구현 객체를 제공'],['19일 Adapter가 이 약속을 구현','19일 Adapter 내부에서 사용']])+call('인터페이스를 추가했다고 기존 Memory 빈이 자동 교체되지는 않습니다.'))
add('도구 이름은 이제 연결','JPA · Hibernate · Spring Data · DB',table([['이름','쉬운 역할'],['JPA','Java 객체를 DB에 저장하는 공통 사용 규칙'],['Hibernate','JPA 규칙을 구현하고 실제 SQL을 만드는 도구'],['Spring Data JPA','Repository의 기본 저장·조회 코드를 제공하는 도구'],['H2 DB','SQL을 실행하고 상품 행을 보관하는 곳']])+call('우리 Repository → Spring Data JPA → JPA를 구현한 Hibernate → SQL → H2'))
add('조건 검색 먼저 생각','1000원 이하 상품을 id 오름차순으로',code('SELECT id, name, price FROM products\nWHERE price <= 1000\nORDER BY id;')+call('질문: 무료0원과 펜1000원은 포함, 노트3000원은 제외인가요? 먼저 결과를 예측한 뒤 실행합니다.'),kind='code-slide')
add('같은 조건을 두 방법으로','메서드 이름 또는 JPQL로 전달',code('findByPriceLessThanEqualOrderByIdAsc(1000)\n\n@Query("select p from ProductEntity p where p.price <= :maxPrice order by p.id")\nfindAffordable(@Param("maxPrice") int maxPrice)')+call('메서드 발췌: Price=price 필드 · LessThanEqual=이하 · OrderByIdAsc=id 오름차순. JPQL의 ProductEntity는 Java 클래스, p.price는 필드입니다.'),note='전체 메서드 반환 타입과 선언은 뒤의 전체 Repository 파일을 사용합니다. SQL 테이블 products와 JPQL Entity ProductEntity를 구분합니다. :maxPrice와 @Param 이름을 같게 바인딩하며 사용자 값을 문자열로 이어붙이지 않습니다.',kind='code-slide')
add('트랜잭션과 변경 감지','조회한 Entity의 변경을 언제 반영할까요?',steps('하나의 작업 묶음: 조회한 노트를 공책2000원으로 변경','flush: 변경 내용을 SQL로 DB에 전송','clear: 관리 목록을 비워 이전 객체를 재사용하지 않기','다시 SELECT해서 DB의 가격이2000원인지 확인')+call('commit은 작업 확정 · flush와 다릅니다. 오늘 테스트는 끝나면 기본 rollback으로 되돌립니다.'),note='flush는 commit과 다릅니다. 변경 감지는 관리 상태 Entity와 트랜잭션 경계가 전제입니다. 영속 상태는 현재 컨텍스트가 객체를 관리한다는 뜻이며 프로세스 재시작 후 데이터 보존과 다릅니다. 테스트는 기본 롤백이므로 테스트 성공을 실행 서버 DB에 영구 저장했다고 해석하지 않습니다.')
add('Service의 트랜잭션','한 사용자 작업의 경계를 정합니다',table([['경계','적용 의도'],['쓰기 Service 메서드','조회·규칙 확인·변경을 한 트랜잭션으로'],['조회 메서드 readOnly','조회 의도를 표현·최적화 힌트'],['Controller','HTTP 계약 · 트랜잭션 로직을 몰아넣지 않음'],['19일','Adapter 전환 코드에서 실제 경계 확인']])+call('readOnly는 모든 DB의 쓰기를 강제로 차단하는 보안 장치가 아닙니다.'))
section('02','자율 실습 · JPA 기초','')
add('실습 시작','기존 프로젝트와 테스트를 보존',steps('main pull → practice/product-jpa-basics','14일 Memory CRUD와 기존 테스트 실행','기존 ProductRepository·Memory 구현 유지','새 Entity·Spring Data Repository만 추가'))
add('환경 준비','JPA와 H2 의존성을 추가',code(JPA_DEPENDENCIES)+call('Java17 · Spring Boot4.1.2 · 기존 Web·Validation·AspectJ·테스트 의존성 유지'),note='dependencies 블록 안에 필요한 항목을 합칩니다. Boot4의 JPA 테스트 모듈 및 DataJpaTest 패키지는 제공 예제 기준을 따릅니다. Boot3의 예전 import를 그대로 붙이지 않습니다.',kind='code-slide')
add('실행 설정','main은 파일 DB · 테스트는 독립 DB',table([['위치','용도'],['src/main/resources/application.properties','H2 파일 DB · 실행 서버용'],['src/test/resources/application.properties','메모리 DB · 테스트용'],['./data/products','실행 디렉터리에 저장 · Git 제외']])+call('서로 다른 DB · 테스트 데이터와 실행 서버 데이터를 혼동하지 않습니다.'))
add('헷갈리지 않게 두 칸으로','테스트 성공과 API DB 전환은 다릅니다',table([['오늘 테스트 경로','오늘 실제 HTTP 경로'],['ProductJpaRepositoryTest → JPA → 테스트 DB','Controller → Service → MemoryProductRepository'],['테스트용 mem DB · 기본 롤백','메모리 상품 · 서버 종료 시 사라짐'],['Entity 저장·조회를 검증','기존 CRUD 응답을 유지'],['main의 파일 DB와 다른 저장 공간','19일 Adapter 연결 후 파일 DB를 사용']])+call('질문: JPA 테스트를 통과하면 POST 상품이 파일 DB에 저장될까요? 오늘은 아직 아닙니다.'))
add('main 설정','기존 application.properties에 필요한 값 합치기',code(DAY16_PROPERTIES)+call('같은 H2 파일에 여러 서버를 동시에 연결하지 않습니다.'),note='product-api 폴더에서 실행합니다. 파일 DB는 재시작 보존을 위한 수업 환경이며 운영 DB 설계가 아닙니다. ddl-auto=update는 학습 환경 값이고 운영 마이그레이션 전략을 대신하지 않습니다. DB 비밀번호나 .env는 커밋하지 않습니다.',kind='code-slide')
add('test 설정','기존 테스트 설정과 충돌 없는지 확인',code(TEST_PROPERTIES)+call('src/test/resources/application.properties · 테스트 데이터는 기본 롤백'),note='@DataJpaTest가 임베디드 DB로 대체하는 동작을 포함해 테스트 격리를 확인합니다. main 파일 DB를 지워 테스트를 통과시키지 않습니다.',kind='code-slide')
add('작업 1','책의 상품 필드를 Entity로 매핑',steps('id·이름·가격과 테이블 컬럼의 관계 정리','보호된 기본 생성자·업무 생성자 작성','조회 메서드와 명시적인 변경 메서드 작성','Product 도메인의 기존 규칙 보존'))
filepages('비교용 코드 · Entity','ProductEntity.java','교재 코드와 구분한 수업 독립 예제')
add('작업 2','Spring Data Repository를 작성',steps('Entity 타입과 id 타입을 맞춰 상속','기본 저장·id 조회 메서드 사용','가격 상한 조건 메서드 정의','@Query JPQL과 파라미터를 연결'))
filepages('비교용 코드 · Repository','SpringDataProductRepository.java','메서드 이름과 실제 조건을 연결')
add('작업 3','DB 동작을 독립 테스트로 확인',table([['사례','기대'],['저장·조회','실제 id 발급 · 값 일치'],['조건 검색','경계 포함·결과 없음 확인'],['참고 · 긴 이름 보존','기존 허용 범위300자 왕복 · 기본 매핑 다음 확인'],['JPQL','조건과 정렬 기대 일치'],['변경 감지','flush·clear 뒤 값 유지']])+call('테스트 이름과 준비·실행·검증 단계를 먼저 적습니다.'))
add('테스트를 세 부분으로 읽기','준비 → 행동 → 기대',table([['부분','첫 테스트에서 읽을 줄','뜻'],['준비','new ProductEntity("노트", 3000)','저장할 상품 만들기'],['행동','saveAndFlush → clear → findById(id)','DB에 보내고 새로 읽기'],['기대','assertEquals("노트", found.getName())','다시 읽은 이름이 노트인지 확인'],['추가 확인','assertNotSame(saved, found)','기존 Java 객체를 그대로 돌려받지 않았는지']])+call('먼저 테스트 하나만 읽고 실행합니다. 모든 단언을 외우기보다 무엇을 확인하는지 자기 말로 설명합니다.'))
filepages('비교용 코드 · JPA 테스트','ProductJpaRepositoryTest.java','기존 Service 단위 테스트와 차이 비교')
add('실행과 관찰','테스트 결과와 SQL을 함께 읽기',steps('./gradlew test --info --rerun-tasks · SQL 다시 관찰','저장·조회·수정 SQL 설명 · 삭제 테스트는 선택','DB id와 정렬을 임의로 가정한 테스트 수정','실패하면 기대·실제·원인을 기록'),note='Windows는 .\\gradlew.bat test --info --rerun-tasks. 출력이 길면 build/reports/tests/test/index.html의 해당 클래스 Standard output을 확인합니다. ProductWiringTest는 Memory 기반 Service 연결을 계속 확인합니다. JPA 저장소가 추가되어도 API가 자동으로 DB 저장으로 바뀌지 않습니다.')
add('검증 질문','세 종류 테스트가 무엇을 증명하나요?',table([['테스트','증명 범위'],['ProductServiceTest','Spring·DB 없이 업무 규칙·처리'],['ProductWiringTest','Spring 빈 연결·AOP 프록시'],['ProductJpaRepositoryTest','JPA 매핑·저장소·DB 쿼리']])+call('하나가 통과했다고 나머지 계층까지 모두 증명되지는 않습니다.'))
section('03','관계 읽기와 19일 준비','')
add('관계는 표 두 개로 시작','주문 하나에 항목 두 개가 있습니다',table([['purchase_orders · 주문 표','order_items · 주문항목 표'],['id=실제 주문키 A','id=항목키 X, order_id=A, name=노트'],['주문 A 한 건','id=항목키 Y, order_id=A, name=펜']])+call('purchase_orders.id는 PK · order_items.order_id는 FK. 질문: 주문 A의 항목은 무엇인가요? 노트와 펜 두 개입니다.'),note='상품 수업과 별개의 종이 표 읽기입니다. 공통 DB SQL 연습은 lab_orders / lab_order_items라는 독립 표를 씁니다. 실제 번호를 고정값으로 저장하라는 의미가 아닙니다.')
add('객체 참조와 FK','표의 여러 항목을 Java 목록으로 표현',table([['DB 표','Java 객체'],['order_items.order_id → purchase_orders.id','PurchaseOrder.items → 항목 목록'],['같은 order_id를 가진 여러 항목 행','주문 하나에 여러 OrderItem 객체'],['주문 A: 노트·펜 두 행','order.getItems()로 목록 읽기']])+call('오늘은 PK·FK와 목록을 연결합니다. 관계 annotation·LAZY·N+1 실행과 개선은23일에 확인합니다.'),note='양방향·cascade·튜닝을 오늘 추가 설명하지 않습니다. 현재 상품 Entity에 관계를 억지로 추가하지 않습니다.23일 최소 주문 실습의 PurchaseOrder.items와 같은 흐름입니다.')
add('19일 작업 예고','API는 유지하고 저장소 구현을 바꾸기',steps('ProductRepository 계약을 다시 읽기','Memory 구현과 JPA Adapter의 변환 지점 찾기','Service 트랜잭션·빈 선택·기존 테스트 점검','같은 화면·HTTP 요청으로 DB 전환 결과 검증'),note='19일은 이준형 강사 대강이며 새 개념 강의나 시연 없이 작업지에 따라 진행합니다. 오늘 완료 코드를 출발점으로 쓰고 미완료 학생은 복구용 출발 코드를 사용할 수 있습니다.')
add('별도 과제','단축 URL에 AI 프론트 연결','<div class="card"><h3>백엔드 API 계약을 AI에게 정확히 전달하기</h3><p>입력·결과·복사·이동·로딩·오류 표시 화면을 만들고 실제 서버와 연결합니다. 프롬프트·직접 수정한 내용·연동 결과를 기록합니다.</p><p><a href="../assignments/short-url/">단축 URL 단계별 과제 안내 ↗</a></p></div>')
section('04','GitHub 제출','')
add('오늘 제출','필수 Issue 1개 · 병합 PR 1개',table([['설정','지정 값'],['저장소','sesac-spring-boot-study'],['브랜치','practice/product-jpa-basics'],['Issue · PR','[실습] 상품 Entity와 JPA 저장소'],['산출물','Entity·Repository·테스트·설정·SQL 관찰 기록']])+call('Closes #실제번호 · 기존 Memory API는 유지했다고 기록'))
add('누적 문서','README·Wiki에 실제 증거와 계획을 구분',steps('product-api/README에 DB 설정·테스트 방법 추가','Home·01-Setup·02-Architecture에 JPA 연습 추가','03-API는 기존 계약 유지 ·04-Verification SQL·테스트','05-Retrospective에 JDBC·JPA 차이와 질문 기록'),note='최신main→Issue→branch→작업·검증→commit/push→PRbase main→자체 확인·병합. Public/main·본인Assignee·practice라벨·milestone product-api-2026-11-16. Wiki 별도 편집과 링크를 PR에 남깁니다. 필수1PR이며 별도 문서PR은 강제하지 않습니다.')
add('파일 확인','실행 파일과 학습 기록만 제출',steps('코드·설정·Wrapper·테스트 포함','루트 .gitignore의 gradle-wrapper.jar 예외 유지','data/·*.mv.db·*.trace.db·build/·.gradle/ 제외','.env·IDE 파일·비밀번호·비밀값 제외'),note='greeting-api/product-api 기존 파일은 보존합니다. H2 파일을 Git에 올리지 않습니다. README에 product-api 폴더에서 실행해야 상대경로가 일정함을 기록합니다.')
add('실습 작업지','막히면 단계별 확인으로 돌아가기','<div class="card"><h3>설정 → 저장 한 건 → 조회 → 조건 검색 → 변경</h3><p><a href="BEGINNER-WORKSHEET.md">멘티용 JPA 첫 실습 작업지 ↗</a></p><p><a href="../shared/db-basics/README.md">DB 기초 설명 ↗</a> · <a href="../shared/db-basics/STUDENT-WORKSHEET.md">DB 기초 작업지 ↗</a></p></div>')
add('19일 출발 체크','네 가지가 준비됐나요?',steps('14일 CRUD 정상·실패 계약 유지','Entity·Repository·JPA 테스트 전체 통과','main과 test DB 설정 위치를 설명','최신 main·실행 명령·포트·검증 기록 확보'))
add('공식 참고','JPA와 Spring Data 공식 문서','<div class="references"><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html"><b>Spring Data JPA · 쿼리 ↗</b><span>쿼리 메서드 · @Query</span></a><a href="https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html"><b>Spring Boot · 테스트 ↗</b><span>DataJpaTest와 테스트 슬라이스</span></a><a href="https://docs.hibernate.org/orm/current/userguide/html_single/"><b>Hibernate ORM ↗</b><span>Entity · 변경 감지 · 연관관계</span></a></div>')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 교재 상품 관리 자율 실습"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v1-book"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
