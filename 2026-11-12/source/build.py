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
add('다섯 번째 수업','실패도 설명하는 API<br>상품 CRUD를 설계하기','<div class="cover-bottom"><span>2026.11.12 THU · 2시간 + 2시간</span><strong>상품 API 검증 → 상품 CRUD 설계</strong><span>CH 09·10·12 · 상품 관리 애플리케이션</span></div>','앞 2시간 REST 실습 · 뒤 2시간 첫 웹 서비스 설계',kind='cover')
add('오늘의 흐름','상품 API를 검증하고 남은 기능 설계',cards(('앞 2시간','검증 · 예외 응답','400 · 404 · HTTP 판단'),('뒤 2시간','상품 수정·삭제 설계','요구사항 · 도메인 · API · 테스트'),('14일 연결','설계한 기능을 직접 구현','CRUD 구현·테스트 6시간 → JPA 2시간')))
add('책과 연결','읽는 범위와 만드는 결과물을 구분',table([['교재','함께 할 일'],['CH 10','입력 검증과 예외 처리 개념을 상품 API에 적용'],['CH 09 · 상품 관리','남은 CRUD 기능과 입력·출력 계약을 확인'],['CH 12 · 테스트','수정·삭제의 정상·실패·경계 테스트를 설계'],['부록 B','책의 테스트 풀이 흐름을 설계 검증에 연결']]),note='교재의 정확한 요구사항은 수업 중 책에서 직접 확인합니다. 원문 미확인 정책을 책의 요구사항이라고 설명하지 않습니다. CH 12 추상화·테스트는 7일에 선행, CH 11 DB 연동은 이후 DB/JPA 시간에 연결하되 JDBC 방식과 JPA를 구분합니다.')
add('완료 기준','코드 검증과 설계 문서 두 결과물',steps('기존 정상 API 유지 · 잘못된 입력 400 · 없는 상품 404','실패 요청 뒤 저장 데이터가 그대로인지 확인','HTTP 메서드·상태·멱등성·REST 성숙도를 설명','교재 요구사항 근거를 표시한 product-api/docs/crud-design.md 제출'),note='총 240분 내 네 블록: 검증·예외·면접 개념45+휴식15, 자율 오류 실습·결과 확인45+휴식15, 교재 요구·도메인 설계45+휴식15, API·테스트·동료 피드백45+정리15. 앞/뒤 각120분. 강사 구현 시연 없이 개념→멘티 자율 구현→피드백. GitHub 정리는 과제 제출 흐름으로 이어갑니다.')
section('01','실패 응답을 API 계약으로','입력 형식 · 도메인 규칙 · HTTP 응답')
add('9일 복습','정상 요청은 어디까지 완성됐나요?',table([['API','기존 동작'],['POST /products','201 · Location · 상품 JSON'],['GET /products','200 · 빈 목록은 []'],['GET /products/{id}','실제로 생성된 상품 200']])+call('기존 product-api를 이어서 수정합니다. 새 프로젝트를 만들지 않습니다.'))
add('검증의 두 자리','입구와 도메인의 책임을 함께 지킵니다',table([['위치','확인하는 일'],['요청 DTO','이름 필수 · 가격 누락/null · 음수 가격'],['Product 도메인','어떤 호출 경로에서도 이름·가격 규칙 유지'],['예외 처리기','실패를 상태 코드와 오류 JSON으로 변환']])+call('DTO 검증을 추가해도 Product의 규칙을 제거하지 않습니다.'))
add('DTO 검증','제약 조건과 @Valid가 연결됩니다',table([['표시','오늘의 의미'],['@NotBlank','name이 null · 빈 문자열 · 공백이면 거부'],['@NotNull','price가 null이면 거부'],['@Min(0)','price가 0 이상'],['@Valid @RequestBody','역직렬화한 요청 DTO를 검증']])+call('Integer는 가격 누락/null을 표현할 수 있습니다. @Min만으로 null을 막지 않습니다.'))
add('변환과 검증','JSON 문법 오류와 값 오류를 구분',linear('요청 본문을 읽고 객체로 변환한 뒤 제약 조건을 검증합니다',[('JSON 읽기','문법 · 타입'),('DTO 검증','필수 · 가격 범위'),('Service 호출','업무·도메인 규칙')])+call('읽기·검증에 실패하면 정상 생성 로직에 도달하면 안 됩니다.'))
add('전역 예외 처리','실패를 공통 HTTP 응답으로 변환',table([['예외','이 수업의 계약'],['ProductNotFoundException','404 · 찾지 못한 상품 message'],['MethodArgumentNotValidException','400 · 요청값 확인 message'],['HttpMessageNotReadableException','400 · 읽을 수 없는 JSON message'],['IllegalArgumentException','400 · 도메인 규칙 message']])+call('@RestControllerAdvice + @ExceptionHandler로 응답을 모읍니다.'),note='모든 예외를 무조건 400으로 바꾸지 않습니다. 예상한 입력·도메인 예외만 지정합니다. 숫자가 아닌 경로 변수처럼 다른 바인딩 오류는 Spring 기본 처리가 적용될 수 있으며 오늘 message 통일 계약은 표에 적은 예외 범위입니다.')
add('404와 빈 목록','없는 단건과 검색 결과 없음을 구분',table([['상황','응답'],['GET /products · 저장 상품 없음','200 + []'],['검색 조건 결과 없음','200 + []'],['GET /products/{id} · 해당 상품 없음','404 + message']])+call('존재하는 컬렉션의 결과가 비어 있는 것은 실패가 아닙니다.'))
add('실패 후 상태','거부된 요청이 데이터를 바꾸지 않아야 합니다',steps('먼저 정상 상품을 하나 생성하고 목록을 기록','잘못된 요청을 한 개씩 전송','각 요청 직후 목록 개수와 기존 값을 재조회','실패 요청이 저장되지 않았음을 기대/실제로 기록'),note='실패한 도메인 생성에서 id 시퀀스가 소비될 수 있으므로 id가 빈틈없이 연속인지 요구하지 않습니다. 저장된 상품의 개수·기존 값·다른 상품 보존을 확인합니다.')
section('02','HTTP와 REST를 설명하기','기술 면접 포인트를 내 요청 결과에 연결합니다')
add('메서드 의미','안전성과 멱등성은 다릅니다',table([['메서드','안전 · 멱등성 · 판단'],['GET','안전 · 멱등 · 조회'],['POST','일반적으로 멱등 보장 없음 · 생성 반복 시 새 자원 가능'],['PUT','멱등 · 지정 자원의 표현을 생성/대체하는 의미'],['DELETE','멱등 · 반복 후 최종 자원 상태가 같음']])+call('멱등성은 응답 코드가 매번 같다는 뜻이 아닙니다.'),note='표는 HTTP 메서드의 의미입니다. 실제 서비스가 의미를 지켜 구현해야 합니다. 첫 DELETE 204 뒤 재요청 404여도 자원 부재 상태는 같으므로 멱등성과 모순되지 않습니다. PUT·DELETE 직접 구현은 14일에 설계와 연결합니다.')
add('상태 코드 선택','왜 이 상태를 골랐나요?',table([['코드','설명할 근거'],['200','처리 성공 · 조회 결과를 본문으로 전달'],['201','새 자원 생성 · Location 제공'],['204','성공했으나 응답 본문 없음 · 이후 삭제 구현 예'],['400 / 404 / 500','요청 문제 / 대상 부재 / 서버 처리 실패']])+call('오늘 구현의 상태를 실제 요청 결과로 설명하세요.'))
add('REST 성숙도','모델의 단계와 오늘 구현 범위',table([['수준','구분하는 관점'],['Level 0','HTTP를 전달 통로로만 사용하는 형태'],['Level 1','자원별 URI 분리'],['Level 2','자원 + HTTP 메서드와 상태 의미 활용'],['Level 3','하이퍼미디어로 다음 가능한 동작을 안내']])+call('오늘 필수 구현은 Level 2 범위 · Level 3는 차이를 설명합니다.'),note='Richardson 성숙도 모델은 API를 토론하는 틀이며 REST의 모든 제약을 증명하는 인증 단계가 아닙니다. JSON 반환만으로 REST라고 판단하지 않습니다. 하이퍼미디어 구현이나 HATEOAS 의존성 추가는 요구하지 않습니다.')
add('설명 연습','정의 대신 코드와 요청 결과를 근거로',steps('생성은 왜 200 대신 201을 사용했나요?','목록이 없을 때 404를 보내지 않는 이유는?','POST를 두 번 보내면 무엇이 달라질까요?','JSON만 반환하면 REST API가 완성된 걸까요?'))
section('03','자율 실습 · 검증과 예외 응답','9일의 세 API 위에 실패 계약을 추가합니다')
add('실습 · 시작','정상 API와 기존 테스트 먼저 확인',steps('최신 main → practice/product-validation 브랜치','product-api/의 기존 정상 POST · GET 확인','ProductServiceTest · ProductWiringTest 유지','7일 코어 · AOP · 9일 ProductResponse 유지'),note='정상 API가 실패하면 먼저 9일 상태를 복구합니다. 서버 재시작 시 메모리 데이터가 초기화되므로 요청 결과의 실제 id를 다시 기록합니다.')
add('실습 · 의존성','Validation 스타터를 한 줄 추가',code("implementation 'org.springframework.boot:spring-boot-starter-validation'")+call('기존 Web MVC · AspectJ · 테스트 의존성을 유지하고 Gradle 새로고침'),note='Java17·Spring Boot4.1.2·Gradle은 기존 프로젝트 값을 유지합니다. dependencies 블록 안에 한 줄만 추가하며 기존 파일을 통째로 덮어쓰지 않습니다.',kind='code-slide')
add('실습 · 파일 지도','두 파일 수정 · 한 파일 추가',table([['파일','작업'],['CreateProductRequest.java','기존 파일에 제약 조건 추가'],['ProductController.java','기존 생성 메서드에 @Valid 추가'],['ApiExceptionHandler.java','새 파일로 예외 응답 매핑']])+call('같은 클래스 이름을 새로 중복 생성하지 않습니다. 전체 코드는 수정 후 기준입니다.'))
add('실습 · 선택 검색 보존','Controller 전체 예제는 기본 API 기준입니다',steps('이름·가격 검색을 추가했다면 기존 findAll 검색 코드를 유지','jakarta.validation.Valid import 추가','기존 생성 메서드의 @RequestBody 앞에 @Valid만 추가','요청 DTO는 아래 기준으로 수정 · 처리기는 새로 추가'),note='선택 과제를 수행한 학생이 기본 Controller 전체 코드를 덮어써서 조회 기능을 잃지 않게 합니다. 전체 코드 버튼은 기본 API의 수정 후 기준입니다.')
filepages('실습 · 요청 검증','CreateProductRequest.java','기존 DTO 파일을 수정합니다')
filepages('실습 · 검증 연결','ProductController.java','기존 Controller 파일을 수정합니다')
filepages('실습 · 오류 응답','ApiExceptionHandler.java','같은 com.example.product 패키지에 추가합니다')
add('실습 · 실행','테스트 후 서버를 새로 실행',code('./gradlew test\n./gradlew bootRun')+call('product-api/에서 실행 · Windows는 .\\gradlew.bat test / bootRun'),note='서버 실행 중인 터미널을 유지합니다. 기존 서버를 종료한 뒤 수정한 서버를 재시작하고 실제 포트로 Postman URL을 맞춥니다. 기존 테스트 통과만으로 HTTP 검증이 끝난 것은 아닙니다.',kind='code-slide')
add('실습 · 정상 회귀','정상 요청을 먼저 다시 확인',table([['요청','기대'],['새 서버에서 목록 조회','200 + []'],['노트 3000 생성','201 · Location · JSON'],['생성 id 단건 · 목록','200 · 저장한 값 일치'],['가격 0 / 앞뒤 공백 이름 생성','201 / 응답 이름의 앞뒤 공백 제거']])+call('공백 제거 후 이름과 가격 0은 정상 조건입니다.'))
add('실습 · 값 검증','네 요청을 각각 따로 보냅니다',code('{"name":"   ","price":3000}\n{"name":"노트","price":-1}\n{"name":"노트"}\n{"name":"노트","price":null}')+call('모두 400 · message 확인 · 각 요청 뒤 저장 개수와 기존 값 불변'),note='각 줄은 독립된 JSON 요청입니다. name 누락과 null도 별도로 확인합니다. 입력 실패 뒤 목록 개수 증가가 없어야 합니다.',kind='code-slide')
add('실습 · 읽기 실패','잘못된 타입과 깨진 JSON',code('{"name":"노트","price":"abc"}\n{"name":"노트","price":3000')+steps('각 요청을 따로 POST · Content-Type JSON 유지','400 · "요청값을 확인하세요" message 확인','실패 전후 목록 개수와 기존 상품 값 비교'),kind='code-slide')
add('실습 · 없는 상품','빈 목록과 404를 구분해 확인',steps('GET /products 목록에서 현재 id들을 확인','존재하지 않는 양의 숫자 id 선택','GET /products/{선택id} → 404 · message 확인','기존 실제 id 조회는 계속 200인지 확인'),note='999를 무조건 없는 id라고 가정하지 않습니다. 현재 목록에 없는 숫자를 사용합니다. 문자가 섞인 경로 id는 다른 변환 실패이므로 없는 상품 검증과 구분합니다.')
add('실습 · 검증 기록','실패마다 기대와 실제를 분리',table([['기록할 것','예시 형식'],['요청','메서드 · URL · 헤더 · 본문'],['예상','400 / message / 저장 개수 불변'],['실제','상태 · 본문 · 전후 목록'],['회귀','정상 요청 · 테스트 · AOP 로그']])+call('에러 화면 캡처 하나로 모든 실패 조건을 확인했다고 쓰지 않습니다.'))
add('오류 표현 비교 · 선택','직접 던지는 오류와 공통 처리 비교',code('throw new ResponseStatusException(HttpStatus.BAD_REQUEST,\n        "요청값을 확인하세요");')+steps('직접 상태 지정은 org.springframework.web.server.ResponseStatusException 사용','HttpStatus는 org.springframework.http.HttpStatus · 두 표현의 역할 비교','현재 상품 API에서 정책을 어디에 모았는지 설명')+call('비교용 표현입니다. 현재 코드에 추가하거나 greeting-api를 수정하지 않습니다.'),note='5일에서 이연한 입력 검증 추가 과제의 연결입니다. 두 방식을 동시에 상품 API에 추가하지 않습니다. 기존 도메인 예외+Advice를 유지합니다. 선택 이름/가격 과제를 수행했다면 음수·문자 가격 400과 기존 목록 불변도 확인합니다.')
add('앞 2시간 정리','오류를 숨기지 않고 계약으로 설명',steps('검증: DTO와 도메인이 각각 무엇을 지키나요?','예외 처리: 어떤 예외가 어떤 상태와 JSON이 되나요?','HTTP: 빈 목록·없는 상품·잘못된 입력을 구분하나요?','테스트: 실패 뒤 원본 데이터가 유지됐나요?'))
section('04','상품 CRUD 설계 · 2시간','책의 상품 관리 앱을 이어 구현합니다')
add('설계 · 출발점','교재 문제를 먼저 읽고 근거를 기록',steps('교재 CH 09 상품 관리의 남은 CRUD와 관련 테스트 함께 읽기','책에 명시된 필수 요구사항과 완료 기준 표시','정책이 정해지지 않은 부분은 질문 또는 가정으로 표시','오늘은 설계 문서 · 14일에는 직접 구현·테스트'),note='교재 본문이 자료에 제공되지 않았으므로 실제 책에서 수정·삭제 요구와 예외 조건을 확인합니다. 미지정 정책은 가정으로 표시합니다. 해설 코드를 먼저 보여주거나 요구사항을 임의로 책 내용이라고 단정하지 않습니다.')
add('설계 · 범위','새 Java 프로젝트와 DB 구현은 아직 요구하지 않습니다',table([['오늘 필수','14일 이후 연결'],['product-api/docs/crud-design.md','설계 기반 구현 · 테스트 6시간'],['요구 · 도메인 · API · 테스트 · 구현 순서','완성 코드와 요구사항 대조'],['교재 근거와 미정 정책 표시','DB 확장 · JPA 개념 2시간']])+call('책의 상품 관리 기능과 이미 구현한 생성·조회를 비교해 남은 범위를 정합니다.'))
add('워크시트 1','요구사항을 필수 · 선택 · 가정으로 나누기',table([['항목','작성할 질문'],['필수','책이 반드시 요구하는 사용자 동작과 제약은?'],['선택','책 또는 내가 제안한 추가 기능은?'],['가정','책에 없는 정책을 어떻게 정했고 왜 필요한가?'],['근거','교재 장·절 또는 페이지 · 내 판단 표시']])+call('교재 요구와 내가 정한 정책을 구분해 적습니다.'))
add('워크시트 2','사용자 시나리오를 입력과 결과로 표현',steps('누가 어떤 목적에서 요청하나요?','입력으로 무엇을 제공하나요?','정상 결과를 사용자는 어떻게 확인하나요?','실패할 수 있는 경우와 사용자에게 줄 정보는?'),note='예: 기존 상품을 수정하거나 삭제하는 입력·정상 결과·없는 상품·검증 실패를 연결합니다. PUT 전체 교체 또는 PATCH 일부 변경의 선택은 책 요구와 수업 API 계약을 구분해 기록합니다.')
add('워크시트 3','도메인 규칙과 계층 책임',table([['영역','설계할 질문'],['도메인','어떤 데이터와 규칙을 함께 지킬까?'],['Controller','HTTP 입력·응답을 어디서 변환할까?'],['Service','어떤 사용자 작업 순서를 조율할까?'],['Repository','무엇을 어떤 기준으로 저장·조회할까?']])+call('클래스 이름을 먼저 늘리기보다 책임과 협력을 설명합니다.'))
add('워크시트 4','API 계약을 표로 작성',table([['기능','메서드 · 경로','요청','성공 · 실패'],['교재 요구 ①','직접 설계','헤더·경로·본문','상태·헤더·본문'],['교재 요구 ②','직접 설계','필수·선택 값','실패 조건과 응답']])+call('수정·삭제의 성공 상태와 없는 id·잘못된 입력 응답을 명시합니다.'),note='상품 생성·조회 계약은 유지합니다. 수정에는 PUT/PATCH 의미, 삭제에는 DELETE 의미를 고려해 메서드·상태·본문 유무를 결정합니다. 204는 응답 본문이 없다는 조건과 함께 확인합니다.')
add('워크시트 5','정상 · 실패 · 경계값 테스트 설계',table([['종류','작성할 질문'],['정상','요구 기능이 작동함을 어떤 입력·결과로 증명할까?'],['실패','없는 대상 · 잘못된 입력에 무엇이 달라질까?'],['경계','길이·누락·중복 등 책의 제약 경계는?'],['상태','실패 뒤 기존 데이터가 보존되는가?']])+call('테스트 이름 · 준비 · 실행 · 기대 결과까지 문장으로 적습니다.'))
add('워크시트 6','가장 작은 기능부터 구현 순서 정하기',steps('처음 끝까지 연결할 최소 사용자 시나리오 선정','도메인·Service 단위 테스트부터 구현 계획','HTTP 연결 후 성공·실패 요청 확인 계획','추가 기능·DB 확장과 미해결 질문을 분리'),note='기존 생성·조회 테스트를 보존하고 수정·삭제와 실패 후 상태 보존 테스트를 계획합니다. 14일 첫 6시간 구현은 이 설계의 최소 기능부터 검증하며 뒤 2시간 JPA 진입과 구현 범위를 혼동하지 않습니다.')
add('설계 · 첫 블록 점검','요구사항과 도메인을 동료에게 설명',steps('책에 적힌 필수 요구를 세 문장으로 설명','내 가정과 미해결 질문을 구분','책의 테스트가 어떤 요구를 확인하는지 연결','불필요한 범위를 줄이고 핵심 흐름 확정'),note='뒤 2시간 첫 블록: 책 읽기10분·요구20분·도메인10분·점검5분을 기본으로 조정합니다. 휴식15분 포함60분.')
add('설계 · 두 번째 블록 점검','API와 테스트로 설계의 빈틈 찾기',steps('동료가 API 표만 보고 요청을 만들 수 있는지 확인','각 필수 요구에 정상·실패 테스트가 연결됐는지 확인','상태·헤더·본문과 도메인 규칙의 모순 수정','14일 구현 순서와 질문을 문서 마지막에 작성'),note='두 번째 블록: API15분·테스트15분·동료 설명10분·수정5분·제출 정리15분. 총60분. 책 해설은 독자 설계 후 비교 자료로 사용하고 책과 다른 선택은 근거와 영향으로 설명합니다.')
add('별도 과제','단축 URL은 새 문제에 적용하는 과제',steps('교재 CH 13 요구를 읽고 short-url/docs/design.md 작성','메모리 기반 백엔드는 스스로 구현·테스트','AI로 HTML·CSS·JavaScript 프론트 생성·연결','AI 사용 기록·실제 연동 결과와 GitHub 제출')+call('<a href="../assignments/short-url/">단계별 과제 안내 열기 ↗</a> · 마감 별도 공지'),note='상품 관리가 수업 공통 프로젝트입니다. 단축 URL은 별도 과제이고 DB 전환은 선택입니다. CH14 주문 전체 API도 선택이며23일 최소 주문 예제 실습과 구분합니다.')
section('05','GitHub 제출','상품 오류 처리와 새 서비스 설계를 작업별로 기록합니다')
add('제출 · 두 작업','오늘 필수 Issue 2개 · 병합 PR 2개',table([['브랜치','Issue · PR 제목'],['practice/product-validation','[실습] 상품 API 검증과 예외 응답'],['docs/product-crud-design','[설계] 상품 CRUD 요구사항과 테스트 설계']])+call('저장소: sesac-spring-boot-study · 각 작업에 당일 문서 갱신 포함'))
add('제출 · 파일 위치','기존 프로젝트와 설계 문서 함께 보존',code('sesac-spring-boot-study/\n├── greeting-api/\n├── product-api/\n│   ├── README.md\n│   └── docs/crud-design.md\n└── README.md')+call('수업 공통 프로젝트는 product-api · short-url은 별도 과제 폴더입니다.'),kind='code-slide')
add('제출 · Issue와 PR','코드와 설계의 검증 근거를 구분',steps('main pull → Issue → 지정 브랜치 → 작업·검증','commit·push → base main PR → 자체 확인·병합','Closes #실제번호 · 관련 Issue/PR 링크 추가','작업마다 main pull 후 다음 브랜치 시작'),note='검증 작업은 practice·docs, 설계 작업은 assignment·docs 라벨. Assignee 본인, Milestone product-api-2026-11-12, 마감일 별도 안내 전 미지정. Issue 본문: 목표/할 일/완료 기준/검증 결과(기대·실제)/관련 PR. PR 본문: 변경 내용/검증 결과/관련 Issue. 외부 승인 필수 없이 자체 검증 후 병합합니다. 12일 필수는 두 작업이며 별도 문서 PR은 요구하지 않습니다.')
add('제출 · README와 Wiki','기존 여섯 페이지에 날짜와 프로젝트별 누적',table([['문서','갱신할 내용'],['루트 README','greeting-api · product-api · CRUD 설계 링크'],['product-api/README.md','소개·환경·실행/테스트·구현 현황·API·Wiki'],['Home / 01-Setup / 02-Architecture','목차 · 환경 · 검증/예외 흐름 및 상품 CRUD 설계'],['03-API / 04-Verification / 05-Retrospective','계약 · 기대/실제 결과와 PR · 근거/회고']]),note='Wiki는 코드 PR에 자동 포함되지 않으므로 별도 편집 후 PR에 링크·작성 확인을 남깁니다. 기존 페이지의 greeting-api/product-api 내용은 보존하고 상품 CRUD 설계를 추가합니다. 아직 실행하지 않은 수정·삭제는 설계 계획임을 표시합니다.')
add('제출 · 설계서 목차','product-api/docs/crud-design.md 여섯 항목',steps('요구사항: 필수·선택·가정·교재 근거','사용자 시나리오 · 도메인 규칙과 계층 책임','API 표: 메서드·경로·입력·정상/실패','테스트: 정상·실패·경계 · 준비/실행/기대','구현 순서 · 미정 질문','동료 피드백과 반영 내용'))
add('제출 · Wrapper 보존','기존 프로젝트의 실행 파일도 유지',table([['포함','제외'],['gradlew · gradlew.bat · gradle/wrapper/gradle-wrapper.jar','build/ · .gradle/ · IDE 파일'],['기존 greeting-api · product-api 코드','.env · 비밀값']])+call('루트 .gitignore: !product-api/gradle/wrapper/gradle-wrapper.jar 유지'))
add('제출 · 최종 점검','실행 결과와 설계 계획을 구분해 제출',steps('Public 저장소 URL · Wiki Home URL · 필수 병합 PR 2개','product-api 정상·400·404 · 실패 뒤 상태 · 테스트 기록','상품 CRUD 설계 문서와 교재 근거 · 가정 표시','기존 프로젝트·Wrapper 보존 · 비밀값 제외'),note='루트 .gitignore의 !product-api/gradle/wrapper/gradle-wrapper.jar 및 greeting-api 예외 유지. build/.gradle/IDE파일/.env와 비밀값 제외. 상품 코드는 기존 product-api에서 이어 작성합니다. 단축 URL 과제를 추가하면 해당 Wrapper도 포함하고 중첩 .git은 제외합니다. 선택 설계나 조회 과제는 수행 여부를 표시하고 필수 구현 완료와 섞지 않습니다.')
add('14일로 연결','설계한 내용을 코드와 테스트로 증명',cards(('첫 6시간','첫 웹 서비스 직접 구현','최소 기능 → 실패 처리 → 테스트·피드백'),('다음 2시간','Spring Data JPA 진입','ORM · 영속성 개념 / DB 확장 연결')))

refs=[('Spring · @RequestBody','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestbody.html','메시지 변환과 검증'),('Spring · ResponseEntity','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responseentity.html','상태 · 헤더 · 본문'),('Spring · 예외 처리','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html','ExceptionHandler와 Advice'),('교재 목차','https://www.yes24.com/product/goods/124434554','관련 장을 책에서 함께 읽기'),('GitHub · Issue와 PR','https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue','실제 Issue 번호 연결'),('HTTP 의미','https://www.rfc-editor.org/rfc/rfc9110.html','메서드 · 상태 · 멱등성')]
add('참고','교재와 공식 문서','<div class="references">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><b>{n} ↗</b><span>{d}</span></a>' for n,u,d in refs)+'</div>')
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
