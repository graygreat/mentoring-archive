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
add('네 번째 수업','상품 기능을<br>REST API로 연결하기','<div class="cover-bottom"><span>2026.11.09 MON · 4시간</span><strong>7일의 product-api를 그대로 확장합니다</strong><span>REST · DTO · JSON / Jackson · Postman</span></div>','교재 CH 09 · 부록 A / CH 07~08 재연결',kind='cover')
add('오늘의 연결','객체에서 HTTP로 한 단계 확장',cards(('7일에 완성','Domain · Repository · Service','DI · AOP · 단위 테스트'),('오늘 추가','DTO · Controller','상품 생성·조회 정상 요청'),('12일에 확장','검증 · 예외 응답','400 · 404 · 실패 후 데이터 확인')))
add('완료 기준','오늘은 정상 요청 세 가지를 완성',table([['요청','검증 기준'],['POST /products','201 · Location · 생성한 상품 JSON'],['GET /products','200 · id 오름차순 목록 · 없으면 []'],['GET /products/{id}','실제로 생성된 id 조회 · 200']])+call('새 프로젝트를 만들지 않습니다. 7일 코어와 테스트를 유지합니다.'))
add('책과 연결','같은 개념을 책과 프로젝트에서 찾기',table([['읽을 곳','연결할 질문'],['CH 09 · 상품 관리','상품 추가와 조회를 어떤 계층이 맡나요?'],['CH 07~08 복습','JSON 본문과 HTTP 헤더는 어떻게 구분하나요?'],['부록 A','API 요청 도구로 무엇을 확인하나요?'],['CH 10 · 다음 시간','검증 실패와 없는 상품을 어떻게 응답할까요?']]),note='교재 본문을 복제하지 않습니다. 지정한 장에서 관련 예제를 함께 읽고 자체 상품 예제와 비교합니다. CH 12 추상화·테스트는 7일에 선행했고 CH 11 DB 연결은 이후 다룹니다. JDBC 교재 예제와 이후 JPA를 같은 구현이라고 설명하지 않습니다.')
add('진행 방식','개념 먼저 · 구현은 멘티가 직접',steps('정상 요청의 API 계약과 변환 흐름 이해','기존 product-api에 DTO 두 개와 Controller 추가','Postman으로 상태·헤더·본문 확인','동작 근거를 README · Wiki · PR로 제출'),note='4시간 배정: 1블록 REST/MVC·HTTP 복습, 2블록 DTO/JSON/응답 설명, 3블록 자율 구현, 4블록 요청 검증·질문·기록. 각 블록 45분+휴식15분을 기본으로 총 240분 안에 운영합니다. 강사 구현 시연 없이 요구사항 안내→자율 구현→결과 피드백. 참고 완성 코드는 실습용이며 별도 과제의 정답은 제공하지 않습니다.')
section('01','HTTP 계약을 먼저 정합니다','MVC 복습 → 자원 · 메서드 · 상태 코드')
add('7일 복습','DispatcherServlet이 요청을 조율',mvc()+call('Controller는 입력을 받고, Service의 업무 기능을 호출합니다.'))
add('계층의 연결','HTTP 처리를 Service에 넣지 않습니다',linear('Controller가 Service를 호출하고 Repository에서 데이터를 읽습니다',[('Controller','HTTP ↔ Java'),('Service','상품 업무 진행'),('Repository','메모리 저장·조회')])+call('기존 Service의 매개변수·반환값을 재사용합니다.'))
add('REST의 출발점','동작보다 자원을 URI로 표현',table([['표현','이 수업에서 선택한 경로'],['상품 컬렉션','/products'],['상품 하나','/products/{id}'],['조회 · 생성의 구분','같은 자원 경로 + GET / POST']])+call('REST는 URI 이름만의 규칙이 아닙니다. HTTP 의미와 일관된 계약을 함께 봅니다.'))
add('HTTP 메서드','요청의 의도를 메서드로 구분',table([['메서드','의미 · 오늘 범위'],['GET','조회 · 서버 상태를 바꾸는 작업에 쓰지 않음'],['POST','상품 생성 · 같은 요청을 반복하면 새 상품 생성 가능'],['PUT / DELETE','수정·삭제 · 14일 CRUD 구현에 연결']])+call('수정·삭제의 정답 구현은 오늘 추가하지 않습니다.'))
add('상태 코드','정상과 실패를 구분하는 약속',table([['상태','뜻 · 오늘의 적용'],['200 OK','조회 성공 · 빈 목록도 성공'],['201 Created','생성 성공 · Location으로 생성 자원 위치 제공'],['400 / 404','잘못된 요청 / 없는 자원 · 12일에 응답 완성'],['500','서버 처리 실패 · 중간 구현의 예외가 여기에 도달할 수 있음']]),note='9일에는 예외 처리기를 아직 작성하지 않으므로 없는 상품 조회를 404로 보장하지 않습니다. ProductNotFoundException은 상태 매핑 전에는 500이 될 수 있습니다. 실패 응답의 통일은 12일 실습 완료 기준입니다.')
add('요청값의 위치','경로 · 쿼리 · 본문을 구분',table([['입력','예시','받는 방법'],['경로 변수','/products/1','@PathVariable'],['쿼리 매개변수','/products?name=노트','@RequestParam · 추가 과제'],['JSON 본문','{"name":"노트","price":3000}','@RequestBody']])+call('어노테이션 이름보다 실제 HTTP 요청의 어느 부분인지 먼저 찾습니다.'))
section('02','Java 객체와 JSON의 경계','Controller · DTO · 메시지 변환 · 응답 구성')
add('Controller 두 방식','화면 이름과 응답 본문을 구분',table([['어노테이션','일반적인 반환 처리'],['@Controller','뷰 이름과 모델을 연결하는 MVC 처리'],['@ResponseBody','반환값을 HTTP 응답 본문으로 처리'],['@RestController','@Controller + @ResponseBody 의미 결합']])+call('@RestController도 Spring MVC의 Controller입니다.'))
add('요청 DTO','입력 형식을 별도의 객체로 정의',code('POST /products\nContent-Type: application/json\n\n{"name":"노트","price":3000}')+call('CreateProductRequest에는 name · price가 들어갑니다.'),kind='code-slide',note='오늘의 DTO는 아직 검증 어노테이션이 없습니다. price는 Integer로 유지하여 12일에 누락/null을 명시적으로 검증합니다. 9일 필수 검증은 정상 요청만 다룹니다.')
add('DTO와 도메인','입력 · 업무 · 출력의 책임을 구분',table([['객체','책임'],['CreateProductRequest','클라이언트가 보낸 name · price'],['Product','id · 상품명 · 가격과 도메인 규칙'],['ProductResponse','클라이언트에게 공개할 id · name · price']])+call('클라이언트가 상품 id를 직접 지정하게 만들지 않습니다.'))
add('JSON / Jackson','문자열과 객체 사이를 메시지 변환기가 연결',linear('Spring MVC 메시지 변환기가 Jackson을 사용해 JSON과 DTO를 변환합니다',[('JSON 요청','HTTP 본문'),('요청 DTO','역직렬화'),('응답 DTO','JSON으로 직렬화')])+call('직접 ObjectMapper를 생성하거나 JSON 문자열을 조립하지 않습니다.'))
add('접근 메서드','요청 setter · 응답 getter를 읽기',code('public String getName() { return name; }\npublic void setName(String name) { this.name = name; }')+steps('요청 DTO: 기본 생성 후 setter로 값을 채울 수 있는 구조','응답 DTO: getter로 공개할 속성을 제공','응답 JSON 속성 순서보다 이름과 실제 값을 확인'),kind='code-slide',note='이 설명은 오늘 제공하는 JavaBean 형태의 DTO에 대한 것입니다. Jackson이 모든 경우에 setter를 강제한다거나 record를 사용할 수 없다고 일반화하지 않습니다.')
add('응답 구성','ResponseEntity는 상태 · 헤더 · 본문',code('URI location = URI.create("/products/" + product.getId());\nreturn ResponseEntity.created(location)\n        .body(new ProductResponse(product));')+table([['부분','생성 응답'],['상태','201'],['헤더','Location: /products/실제id'],['본문','id · name · price JSON']]),kind='code-slide')
add('빈 목록','조회 결과가 없어도 요청은 성공',code('GET /products\n\nHTTP 200\n[]')+call('목록이 비어 있음과 단건 자원이 없음은 서로 다른 상황입니다.'),kind='code-slide')
add('요청 도구','Postman에서 요청과 응답을 나누어 읽기',steps('메서드와 URL 설정 · 서버 포트 확인','POST는 Body → raw → JSON 선택','Content-Type: application/json 확인','응답 Status · Headers · Body 각각 확인'),note='Postman UI는 버전에 따라 위치가 다를 수 있습니다. 동일한 메서드/URL/헤더/본문을 보내는 것이 핵심입니다. 웹 버전에서 로컬 서버 연결이 막히면 Desktop 앱/Agent 또는 curl 대안을 사용합니다.')
section('03','자율 실습 · 상품 REST API','7일 product-api를 이어서 사용합니다')
add('실습 준비','기존 프로젝트가 먼저 통과해야 합니다',steps('sesac-spring-boot-study의 최신 main에서 브랜치 생성','product-api/에서 기존 ProductServiceTest와 ProductWiringTest 실행','7일의 Product · Repository · Service · TimingAspect 유지','추가 파일 3개는 시작 클래스와 같은 com.example.product 패키지'),note='기존 테스트 명령은 ./gradlew test이며 Windows PowerShell은 .\u005cgradlew.bat test입니다. 실패가 남아 있으면 HTTP 코드를 붙이기 전에 원인을 먼저 해결합니다. 이전 파일 참고: ../2026-11-07/. 새 Initializr 프로젝트를 받거나 중첩 git init을 하지 않습니다.')
add('실습 · 의존성','Web MVC 스타터만 추가',code("implementation 'org.springframework.boot:spring-boot-starter-webmvc'")+steps('build.gradle의 기존 dependencies 안에 한 줄 추가','기존 Spring Boot 스타터 · AspectJ · 테스트 의존성 유지','Gradle 새로고침 후 테스트 실행'),note='7일의 Java 17 · Spring Boot 4.1.2 · Gradle 구성을 유지합니다. 오늘 validation 스타터는 추가하지 않습니다. 기존 dependencies 블록을 통째로 바꾸지 않습니다.',kind='code-slide')
add('실습 · 파일 지도','새로 작성할 파일은 세 개',table([['파일','맡을 일'],['CreateProductRequest.java','생성 JSON을 입력받음 · 오늘은 검증 없음'],['ProductResponse.java','응답 속성 제공'],['ProductController.java','POST · GET 목록 · GET 단건']])+call('기존 7일 파일은 그대로 둡니다. 전체 코드 버튼은 이 세 파일만 제공합니다.'))
filepages('실습 · 입력 DTO','CreateProductRequest.java','정상 JSON의 name · price를 받습니다')
filepages('실습 · 응답 DTO','ProductResponse.java','Product를 응답 데이터로 바꿉니다')
filepages('실습 · Controller','ProductController.java','기존 Service를 생성자로 주입받습니다')
add('실습 · 실행','테스트를 확인한 뒤 서버 실행',code('./gradlew test\n./gradlew bootRun')+call('두 명령은 product-api/에서 실행 · 서버 실행 중인 터미널은 유지'),note='Windows PowerShell: .\u005cgradlew.bat test / .\u005cgradlew.bat bootRun. IDE에서 main을 실행해도 됩니다. 포트 충돌이면 기존 서버를 종료하거나 application.properties의 server.port를 변경하고 모든 요청 URL에 같은 포트를 사용합니다. 재시작하면 메모리 상품이 초기화됩니다.',kind='code-slide')
add('실습 · 순서 1','빈 목록을 먼저 조회',code('GET http://localhost:8080/products\n\n기대 상태: 200\n기대 본문: []')+call('새로 시작한 서버에서 확인합니다. 기존 상품이 있으면 재시작 여부를 확인하세요.'),kind='code-slide')
add('실습 · 순서 2','상품을 생성하고 실제 id 기록',code('POST http://localhost:8080/products\nContent-Type: application/json\n\n{"name":"노트","price":3000}')+steps('201 확인','본문의 실제 id · name · price 확인','Location이 같은 id를 가리키는지 확인'),kind='code-slide')
add('실습 · 순서 3','생성한 id로 단건 조회',code('GET http://localhost:8080/products/{실제id}')+steps('POST 본문의 실제 id를 URL에 넣습니다.','200 · 생성한 이름과 가격이 같은지 확인합니다.','응답 Content-Type에 application/json이 있는지 확인합니다.'),kind='code-slide')
add('실습 · 순서 4','상품 두 개와 목록 순서 확인',steps('펜 1000원을 한 개 더 생성','GET /products에서 두 상품 확인','id 오름차순인지 확인 · JSON 속성 순서는 비교하지 않음','Service 호출의 AOP 시간 로그와 기존 테스트 통과 확인'),note='Spring MVC Controller에 주입된 Service도 7일에 확인한 프록시를 사용합니다. 0ms 로그도 정상일 수 있으며 메서드 실행 시간을 정밀 성능 지표로 사용하지 않습니다.')
add('실습 · 대체 도구','Postman과 같은 요청을 curl로 확인',code('curl -i http://localhost:8080/products\ncurl -i -X POST http://localhost:8080/products \\\n  -H "Content-Type: application/json" \\\n  -d \'{"name":"노트","price":3000}\'')+call('위 줄바꿈 문법은 macOS · Linux 셸 기준입니다.'),kind='code-slide',note='Windows PowerShell은 curl 별칭 차이가 있으므로 Postman을 우선 사용하거나 curl.exe와 JSON 파일을 사용합니다. JSON을 UTF-8 product.json으로 저장한 뒤 curl.exe -i -X POST http://localhost:8080/products -H "Content-Type: application/json" --data-binary "@product.json"으로 보낼 수 있습니다. 파일 경로와 포트를 실제 환경에 맞춥니다.')
add('실습 · 범위 확인','실패 응답 완성은 12일에 이어갑니다',table([['현재 확인','오늘의 판단'],['정상 생성·조회','필수 완료 기준'],['없는 상품 / 공백 / 누락 입력','관찰 가능 · 응답 형식과 상태는 아직 미완성'],['404 · 검증 400 · 공통 오류 JSON','12일에 DTO와 Controller를 수정하고 처리기 추가']])+call('중간 구현의 500을 완성된 API 계약으로 제출하지 않습니다.'))
add('결과 공유','요청 한 개의 왕복을 설명하기',steps('JSON은 어디에서 어떤 DTO로 바뀌었나요?','Controller는 어떤 Service 메서드를 호출했나요?','201과 Location은 어느 코드에서 정했나요?','Postman 결과와 테스트 결과를 구분해 보여주세요.'))
section('04','별도 과제 · 조회 조건 확장','기본 API 이후 선택 수행 · 정답 코드 없음')
add('과제 1 · 이름 검색','기존 목록 API에 조건 하나 추가',code('GET /products?name=노트')+table([['조건','완료 기준'],['name 있음','앞뒤 공백 제거 후 부분 일치 · 대소문자 구분'],['미지정 · 공백만','전체 목록'],['결과 없음','200 + []'],['공통','id 오름차순 · 원본 상품 불변']]),kind='code-slide')
add('과제 2 · 가격 필터','이름과 가격 조건을 누적 적용',code('GET /products?maxPrice=5000\nGET /products?name=노트&maxPrice=5000')+table([['조건','완료 기준'],['가격 상한','상한과 같은 가격 포함 · 미지정이면 제한 없음'],['조건 결합','두 조건을 모두 만족 · id 오름차순'],['검증','0 · 상한 경계 · 빈 결과 · 원본 불변']])+call('음수·숫자가 아닌 가격의 400 응답은 12일 이후 추가합니다.'),kind='code-slide')
add('JSON 표현 비교 · 선택','Map 응답과 DTO 응답을 비교',code('Map.of("id", product.getId(),\n        "name", product.getName(), "price", product.getPrice())')+steps('위 표현과 ProductResponse의 속성 이름·타입·변경 위치 비교','어떤 방식이 요구사항을 드러내기 쉬운지 회고에 작성')+call('비교용 표현입니다. 추가 구현이나 greeting-api 수정은 필수가 아닙니다.'),note='5일에서 옮긴 JSON 추가 과제의 연결 읽기입니다. 기존 greeting-api는 보존합니다. PUT·DELETE는 14일 CRUD 구현과 통합하며 오늘 별도 필수 과제로 부과하지 않습니다.')
section('05','GitHub 제출','기존 학습 저장소에 오늘 작업을 누적합니다')
add('제출 · 한 작업으로 묶기','오늘 필수 Issue 1개 · 병합 PR 1개',table([['항목','지정 값'],['저장소 · 폴더','sesac-spring-boot-study / product-api/'],['브랜치','practice/product-rest'],['Issue · PR 제목','[실습] 상품 생성·조회 REST API'],['Milestone / Labels','product-api-2026-11-09 / practice · docs']])+call('기본 API 코드와 당일 README · Wiki 기록을 같은 작업에서 정리합니다.'))
add('제출 · 작업 흐름','이전 수업 결과 위에서 시작',steps('clone 또는 main pull → Issue 생성 · 본인 Assignee','지정 브랜치 → 구현 · 테스트 · 요청 검증','commit · push → base main PR → 자체 확인 · 병합','Closes #실제번호 연결 · 다음 과제는 main pull 후 시작'),note='코드 PR에 Wiki 변경이 자동 포함되지는 않습니다. Wiki는 별도 편집하고 PR에 URL과 완료 체크를 남깁니다. 문서만의 추가 PR은 강제하지 않습니다. 타인 승인 대신 자체 검증 후 병합할 수 있습니다. 선택 과제는 feature/name-search / [과제 1] 상품 이름 검색, feature/price-filter / [과제 2] 가격 조건 검색으로 각각 Issue·PR을 추가하며 assignment 라벨을 사용합니다. 마감일은 별도 안내 전 지정하지 않습니다.')
add('제출 · 파일 확인','실행에 필요한 파일과 기존 기록 보존',table([['포함','제외'],['src · Gradle 설정 · gradlew · gradlew.bat','build/ · .gradle/ · IDE 파일'],['gradle/wrapper/gradle-wrapper.jar','.env · 비밀값']])+call('루트 .gitignore: !product-api/gradle/wrapper/gradle-wrapper.jar 유지'),note='기존 greeting-api와 그 Wrapper 예외도 보존합니다. 저장소는 Public / main · Issues와 Wiki 활성화. 이미 만들어 둔 저장소를 재사용합니다. Initializr로 새로 받지 않고 product-api에 누적합니다.')
add('제출 · README','프로젝트 문서에 여섯 항목 갱신',steps('프로젝트 소개 · 개발 환경(실제 버전)','실행·테스트 방법 · 구현 현황(9일 정상 API)','API 목록 · Wiki 링크')+call('루트 README의 greeting-api · product-api 목차와 기존 링크를 유지합니다.'))
add('제출 · Wiki','기존 여섯 페이지에 product-api 기록 누적',table([['페이지','오늘 추가할 내용'],['Home / 01-Setup','프로젝트 목차 / 실제 실행·테스트·포트'],['02-Architecture / 03-API','요청 변환·계층 / 정상 API 계약'],['04-Verification','201 · Location · 200 · [] · 실제 id · AOP · 테스트'],['05-Retrospective','오류 또는 헷갈린 점 · 원인 · 해결 · 배운 점']]),note='각 페이지 기존 greeting-api 및 7일 product-api 내용을 보존합니다. 결과는 기대와 실제를 나눠 기록하고 Issue·PR 링크를 포함합니다. 미구현 400/404를 완료했다고 쓰지 않습니다.')
add('제출 · 최종 확인','저장소 · Wiki · 병합 PR 링크 제출',steps('main에서 product-api 테스트와 서버 실행 가능','정상 API의 상태·헤더·본문 기대/실제 기록','Public 저장소 URL · Wiki Home URL · 필수 PR 1개 링크','선택 과제 수행 여부와 해당 PR 링크 표시'))
add('다음 수업','정상 동작에서 실패 계약으로 확장',cards(('12일 앞 2시간','검증 · 예외 · REST 판단','CH 10 / HTTP 메서드·상태·성숙도'),('12일 뒤 2시간','교재 과제 기반 설계','CH 13 단축 URL / 14일 직접 구현')))

refs=[('Spring · @RequestBody','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestbody.html','메시지 변환과 검증'),('Spring · ResponseEntity','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responseentity.html','상태 · 헤더 · 본문'),('Spring · 예외 처리','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html','ExceptionHandler와 Advice'),('교재 목차','https://www.yes24.com/product/goods/124434554','관련 장을 책에서 함께 읽기'),('GitHub · Issue와 PR','https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue','실제 Issue 번호 연결'),('HTTP 의미','https://www.rfc-editor.org/rfc/rfc9110.html','메서드 · 상태 · 멱등성')]
add('참고','교재와 공식 문서','<div class="references">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><b>{n} ↗</b><span>{d}</span></a>' for n,u,d in refs)+'</div>')
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-09-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+('<div class="subtitle">'+d['sub']+'</div>' if d['sub'] else '')+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.09</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 9장·부록 A와 함께 배우는 REST·DTO·JSON·Postman 실습"><title>11월 9일 · 상품 REST API 구현</title><style>'+css+'</style></head><body data-deck-revision="2026-11-09-v1-curriculum"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',len(out.encode()),'bytes')
