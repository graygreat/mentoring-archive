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
def add(ch,title,body='',note='',kind='',source=None):S.append(dict(ch=ch,title=title,body=body,note=note,kind=kind,source=source))
def section(n,title):add(title,title,'<div class="section-number">'+n+'</div>',kind='section')
def filepages(ch,key,goal):
 lines=SOURCES[key].splitlines();chunks=[lines[i:i+14] for i in range(0,len(lines),14)]
 for i,chunk in enumerate(chunks):
  add(ch,key+f' · {i+1}/{len(chunks)}',code('\n'.join(chunk),preserve_whitespace=True),note='전체 코드 버튼으로 package와 import를 포함한 파일 전체를 확인할 수 있습니다. 새 클래스 틀과 중복되지 않게 작성합니다. 파일 경로는 코드 보기 창 상단에 표시됩니다.',kind='code-slide file-slide',source=key)
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
# Stage-specific publication: future REST answer files stay out of today's viewer.
TODAY_KEYS = ('ProductApplication.java','Product.java','ProductRepository.java','MemoryProductRepository.java','ProductNotFoundException.java','ProductService.java','ProductServiceTest.java','TimingAspect.java','ProductWiringTest.java')
TODAY_SOURCES = {key: SOURCES[key] for key in TODAY_KEYS}
add('세 번째 수업','객체를 연결하고<br>MVC 구조 읽기','<div class="cover-bottom"><span>2026.11.07 SAT · 세 번째 수업</span><strong>상품 객체로 배우는 Spring</strong><span>IoC / DI · 빈 컨테이너 · 자동 설정 · AOP · MVC</span></div>',kind='cover')
add('오늘의 흐름','책 읽기 → 짧은 설명 → 직접 구현',cards(('설명·읽기·활동 약2시간','책에서 구조 찾기','짧게 읽고 질문 · DI와 MVC 활동'),('자율 실습 약5시간','직접 작성하고 테스트','상품 객체 · 저장소 · Service · AOP'),('피드백 약1시간','동작과 이유 설명','매시간 활동45분+휴식15분 · 점심 별도')),note='총 8시간은 설명·책 읽기·활동 약2시간, 자율 실습5시간, 결과 피드백1시간의 운영 블록입니다. 각 시간은 활동45분+휴식15분, 점심 별도입니다. 설명을 연속으로 4시간 진행하지 않습니다. 책 함께 읽기→핵심 질문→멘티 구현→테스트→책과 비교를 반복하며 코딩 시연은 하지 않습니다. 핵심6시간/MVC2시간은 내용 배정이고 실제 활동은 섞어서 운영합니다.')
add('책과 연결','이번 주 교재를 나누어 봅니다',table([['시점','교재와 수업'],['5일 · 복습 완료','1~8장 · Java · 서버/클라이언트 · JSON/HTTP'],['오늘 · 9장 일부','상품 객체 · 컬렉션 · 저장과 조회'],['오늘 · 12장 일부 선행','인터페이스 · 생성자 DI · 단위 테스트'],['9일 → 12일','9장 REST·DTO → 10장 검증·예외 응답'],['이후','11장 DB · 상품 CRUD 완성 · 14일 JPA 시작']]),note='책의 장 순서를 모두 오늘 끝낸다는 뜻이 아닙니다. 같은 상품 프로젝트를 단계별로 확장합니다. 책 9장 List와 수업 Map을 구분하고, 12장의 객체지향·테스트 일부를 먼저 연결합니다. 책 11장 DB는 이후 DB/JPA 진도와 연결합니다.')
add('책 9장 연결','List로 관리한 상품을 Map으로',code('List<Product> products = new ArrayList<>();\n// 책의 컬렉션 학습을 오늘의 저장소 역할로 연결합니다.')+cards(('교재 연결','상품 묶음과 조건 찾기','List · 반복 · 조건'),('오늘의 변형','id를 키로 저장·조회','Map<Long, Product>')),note='교재 예제를 그대로 옮긴 코드가 아닙니다. 같은 요구를 다른 자료구조로 표현한 독립 예제입니다. List가 틀린 구현이라는 뜻은 아닙니다.',kind='code-slide')
add('필수 결과물','오늘은 객체와 테스트를 완성합니다',steps('Product에 이름·가격 규칙 표현','Repository 인터페이스와 메모리 구현 작성','Service의 생성자로 Repository 전달','단위 테스트 3개와 주입·AOP 확인 테스트 통과'),note='HTTP 서버나 Controller 없이 완료할 수 있습니다. Java 예외와 HTTP 상태 코드는 구분합니다. 오늘의 없는 상품 처리는 ProductNotFoundException 발생까지입니다.')
add('진행 방식','실습 예제와 별도 과제는 다릅니다',cards(('실습','직접 작성하고 확인','요구사항·완료 기준 먼저 읽기 → 해설 코드 참고'),('별도 과제','새 테스트와 조건 검색','정답 코드 없이 자율 구현'),('확인','실행 결과와 이유 설명','발표 PPT 대신 코드·테스트·로그 공유')),note='강사의 코딩 시연은 하지 않습니다. 완성 예제는 비교·해설 자료이며 직접 작성할 파일 범위를 표시합니다. 막히면 힌트를 주고 여러 명의 공통 오류만 짧게 설명합니다.')
section('01','객체를 연결하는 Spring')
add('지난 수업 복습','직접 만들기와 전달받기',cards(('직접 생성','new GreetingService()','사용하는 코드가 구현과 생성을 결정'),('생성자로 받기','GreetingController(service)','외부에서 준비한 객체를 전달')),note='생성자 주입은 일반 Java에서도 가능합니다. Spring은 이를 컨테이너의 빈 생성·연결에 적용합니다.')
add('DI의 출발점','구현 클래스를 직접 고르면',code('public class ProductService {\n    private final MemoryProductRepository repository\n            = new MemoryProductRepository();\n}')+call('저장 방식을 바꾸려면 Service의 생성 코드도 바뀝니다.'),kind='code-slide')
add('DI의 출발점','필요한 역할을 생성자로 받습니다',code('public class ProductService {\n    private final ProductRepository repository;\n\n    public ProductService(ProductRepository repository) {\n        this.repository = repository;\n    }\n}')+call('ProductRepository는 “저장·조회 역할”을 나타내는 인터페이스입니다.'),kind='code-slide')
add('객체 연결 그림','일반 Java에서도 DI가 가능합니다',linear('외부 조립 코드가 Repository와 Service를 생성하고 의존성을 전달합니다',[('조립하는 코드','객체를 준비'),('Repository 객체','저장·조회 역할'),('Service 객체','생성자로 전달받음')])+code('ProductRepository repository = new MemoryProductRepository();\nProductService service = new ProductService(repository);'),kind='code-slide')
add('IoC와 DI','객체를 연결하는 주체가 달라집니다',table([['용어','이 예제에서 읽는 뜻'],['IoC · 제어의 역전','객체 생성과 연결을 외부에 맡김'],['DI · 의존성 주입','필요한 객체를 외부에서 전달받음'],['Bean · 빈','Spring 컨테이너가 관리하는 객체']])+call('IoC는 더 넓은 개념이고, DI는 이를 구현하는 방식 중 하나입니다.'))
add('빈 컨테이너','Spring이 만들고 연결하는 객체들',container()+call('new로 만든 모든 Java 객체가 자동으로 빈이 되는 것은 아닙니다.'))
add('빈 등록','역할 표시를 읽어 객체를 찾습니다',table([['표시','오늘의 클래스'],['@Controller','웹 입력을 받는 계층 · 개념 소개'],['@Service','ProductService'],['@Repository','MemoryProductRepository'],['@Component','공통 역할의 Spring 관리 객체']])+call('시작 클래스의 패키지와 하위 패키지에서 기본 스캔이 이뤄집니다.'))
add('생성자 주입','생성자가 하나면 이렇게 연결됩니다',linear('타입에 맞는 Repository 빈을 찾아 Service 생성자에 전달합니다',[('필요한 타입','ProductRepository'),('등록된 구현','MemoryProductRepository'),('생성자 주입','ProductService(repository)')])+call('이 예제는 생성자가 하나이므로 @Autowired를 생략합니다.'))
add('빈 등록의 다른 방법','@Bean은 메서드의 반환 객체를 등록',code('@Configuration\npublic class ProductConfig {\n    @Bean\n    public ProductRepository productRepository() {\n        return new MemoryProductRepository();\n    }\n}')+call('비교 예시입니다. 실습은 @Repository 방식 하나만 사용합니다.'),note='이 코드를 추가하려면 MemoryProductRepository의 @Repository를 제거해야 같은 역할을 이중 등록하지 않습니다. Configuration과 Bean의 import는 org.springframework.context.annotation입니다. 이 예시는 필수 프로젝트에 작성하지 않습니다.',kind='code-slide')
add('빈을 찾지 못할 때','등록 · 범위 · 타입을 확인합니다',table([['상황','확인할 곳'],['주입할 빈이 없음','@Repository · 패키지 위치'],['후보가 두 개 이상','불필요한 중복 등록 여부'],['구현 클래스와 타입이 맞지 않음','implements ProductRepository'],['생성자에서 연결되지 않음','this.repository = repository']]),note='Qualifier나 Primary는 후보를 의도적으로 여러 개 사용할 때 확장합니다. 초반에는 후보를 하나로 유지합니다. 빈 이름 암기보다 오류 메시지의 required type과 후보 수를 읽게 합니다.')
add('기본 싱글턴','여러 요청이 Service 하나를 공유합니다',singleton()+call('기본 싱글턴은 컨테이너 안에서 빈 정의마다 하나입니다.'),note='JVM 전체에 모든 클래스 객체가 하나라는 뜻이 아닙니다. 컨테이너가 다르거나 같은 클래스의 빈 정의가 여러 개면 객체도 달라질 수 있습니다. 요청 스코프 등은 이름만 소개하고 구현하지 않습니다.')
add('공유 객체의 주의점','요청별 값은 지역 변수로 다룹니다',code('// 피하기: 여러 요청이 같은 필드를 바꿉니다\nprivate String currentName;\n\n// 이번 예제: 요청값은 매개변수와 지역 변수로 사용합니다\npublic Product create(String name, int price) {\n    return repository.save(name, price);\n}')+call('싱글턴이라고 스레드 안전이 자동으로 보장되지는 않습니다.'),note='Repository의 저장소는 의도적으로 공유하는 상태입니다. 공유 상태와 요청별 임시 값을 구분합니다. 이번 메모리 구현은 ConcurrentHashMap과 AtomicLong을 사용하되 트랜잭션이나 영속성을 제공하지 않습니다.',kind='code-slide')
add('면접 연결','IoC와 DI를 자신의 코드로 설명',steps('어떤 객체가 다른 객체를 필요로 하나요?','생성·연결을 누가 맡았나요?','생성자로 받으면 무엇을 바꾸기 쉬워지나요?'),note='예시 답변: ProductService가 ProductRepository에 의존하며 Spring이 구현 빈을 전달합니다. 인터페이스를 기준으로 받으므로 Service를 유지하면서 저장 구현이나 테스트용 객체를 바꿀 수 있습니다.')
section('02','실행 준비와 공통 처리')
add('스타터','함께 사용하는 라이브러리 묶음',cards(('기본 스타터','Spring 실행 기반','Initializr 기본 구성 유지'),('AspectJ 스타터','AOP 지원','오늘 추가할 공통 처리 의존성')),note='스타터는 의존성 묶음입니다. 클래스가 생기는 것과 빈이 등록되는 것은 다릅니다. Web 스타터와 Validation은 9일·12일에 필요해질 때 추가합니다.')
add('자동 설정','조건을 보고 기본 구성을 준비합니다',linear('라이브러리와 설정 조건을 확인한 자동 설정이 필요한 기본 빈 구성을 제공합니다',[('조건 확인','라이브러리 · 설정 · 기존 빈'),('자동 설정','적합한 구성을 선택'),('실행 환경','웹 요청 처리 준비')])+call('모든 클래스가 자동 등록되거나, 모든 사용자 설정이 무조건 대체되는 것은 아닙니다.'))
add('자동 설정과 스캔','둘은 어떤 차이가 있을까요?',table([['구분','주로 하는 일'],['컴포넌트 스캔','내 코드의 @Service · @Repository 등을 찾아 등록'],['자동 설정','조건에 맞는 프레임워크 기본 구성 제공'],['스타터','관련 라이브러리 의존성을 함께 가져옴']])+call('@SpringBootApplication은 스캔과 자동 설정을 함께 시작하도록 구성됩니다.'))
add('AOP의 출발점','모든 Service에 시간을 기록한다면',code('long started = System.nanoTime();\ntry {\n    // 원래 상품 기능 실행\n} finally {\n    // 걸린 시간 기록\n}')+call('같은 시간 기록 코드를 여러 메서드에 반복해서 넣게 됩니다.'),kind='code-slide')
add('AOP 그림','공통 처리를 프록시에서 실행합니다',proxy()+call('Service를 호출하기 전과 끝난 뒤에 공통 처리를 둘 수 있습니다.'))
add('AOP 용어','이 예제에서 세 단어만 연결',table([['용어','오늘의 코드'],['Aspect','시간 기록을 모은 TimingAspect'],['Advice','실행 전후 동작인 measure 메서드'],['Pointcut','ProductService의 어떤 메서드에 적용할지 지정']])+call('프록시는 호출을 받아 실제 객체로 전달하는 중간 객체입니다.'))
add('AOP 확인','프록시를 통과하는 호출을 비교',table([['호출 방식','이 예제의 AOP'],['제공 테스트 → 주입받은 Service','적용 대상 메서드의 시간 기록'],['테스트의 new ProductService(...)','Spring이 만든 프록시를 사용하지 않음'],['같은 객체 내부의 this.메서드()','보통 프록시를 다시 지나지 않음']]),note='개념 설명 뒤 집중 실습에서 프로젝트와 Aspect를 작성하고, 제공된 Spring 연결 테스트로 적용을 확인합니다. 이 표는 Spring의 기본 프록시 기반 AOP에 대한 설명이며 AspectJ weaving까지 일반화하지 않습니다. final/private 제약은 질문이 나오면 설명합니다.')
add('면접 연결','자동 설정과 AOP를 설명해 봅시다',steps('스타터를 추가한 것과 자동 설정은 어떻게 다른가요?','왜 Service에 직접 시간 기록 코드를 넣지 않았나요?','new로 만든 Service에도 AOP가 적용될까요?'),note='답변은 정의 암기보다 오늘의 dependencies·TimingAspect·주입 코드를 근거로 하게 합니다. DI와 AOP는 서로 다른 개념이며 DI 자체가 모든 메서드 호출을 가로채는 것은 아닙니다.')
section('03','서버·클라이언트와 MVC')
add('1~8장 연결','요청하는 쪽과 응답하는 쪽',linear('클라이언트가 네트워크 요청을 보내면 서버가 처리 결과를 응답합니다',[('클라이언트','브라우저 · 요청 도구'),('서버','요청 수신 · 처리'),('응답','화면 또는 데이터')])+call('5일의 요청·응답 경험을 MVC 처리 구조에 연결합니다.'))
add('서버의 역할','연결·업무·저장 책임을 구분합니다',table([['책임','맡을 구성'],['네트워크 요청 수신','웹 서버와 서블릿 실행 환경'],['요청 처리 흐름 조율','DispatcherServlet'],['입력과 업무 호출 연결','Controller'],['업무 진행 / 저장·조회','Service / Repository']]),note='DispatcherServlet이 모든 업무와 저장을 직접 수행하지 않습니다. Service와 Repository는 애플리케이션이 설계하는 역할입니다.')
add('MVC 복습','화면의 역할과 업무의 역할을 나눕니다',table([['역할','의미'],['Model','업무 데이터와 처리 결과'],['View','사용자에게 보여줄 화면'],['Controller','입력을 받고 처리 결과를 연결']])+call('Model은 DB나 특정 클래스 하나와 같은 뜻이 아닙니다.'))
add('MVC 요청 그림','DispatcherServlet이 흐름을 조율합니다',mvc(),note='DispatcherServlet은 프런트 컨트롤러입니다. HandlerMapping에서 담당 핸들러 정보를 찾고 HandlerAdapter에 실행을 위임합니다. 상세 확장점 구현은 하지 않습니다.')
add('MVC 요청 읽기','담당 코드를 찾는 일과 실행하는 일',table([['구성','역할'],['DispatcherServlet','공통 진입점에서 전체 처리 조율'],['HandlerMapping','요청에 맞는 핸들러 탐색'],['HandlerAdapter','찾은 핸들러를 호출하는 방법 지원'],['Controller','업무 계층 호출과 결과 연결']]))
add('계층별 책임','역할 표시와 실제 책임을 연결',table([['표시·객체','역할'],['@Controller','웹 입력과 처리 결과 연결'],['@Service','상품 생성·조회 업무 흐름'],['@Repository','상품 저장과 조회 구현'],['Product','상품 정보와 유효한 상태']])+call('어노테이션만 붙인다고 책임이 자동으로 분리되지는 않습니다.'))
add('두 가지 응답','HTML 화면과 응답 본문',cards(('화면 응답','View를 통해 화면 렌더링','서버가 화면을 구성해 전달'),('본문 응답','데이터를 본문으로 전달','다른 클라이언트가 데이터를 활용'))+call('오늘은 차이를 구분합니다. JSON 변환과 REST 코드는 9일에 구현합니다.'),note='일반적인 Controller의 뷰 반환과 본문 반환을 개념적으로 구분합니다. 템플릿 설정이나 반환값 처리 코드까지 구현시키지 않습니다.')
add('흐름 읽기','두 종류의 연결을 구분합니다',table([['질문','관련 개념'],['Service는 누가 만들고 전달하나요?','컨테이너 · 빈 · DI'],['요청에 맞는 Controller는 누가 찾나요?','DispatcherServlet · HandlerMapping'],['상품을 어디에 저장하나요?','Repository 구현'],['화면과 데이터 중 무엇을 보내나요?','응답 처리 방식']]))
add('구조 확인 활동','상품 요청 흐름을 말로 그려봅니다',steps('클라이언트부터 Controller까지 요청 화살표 그리기','Controller → Service → Repository 책임 표시','빈을 연결하는 컨테이너를 별도로 표시','화면 응답과 데이터 본문 응답의 차이 설명'),note='코딩 시연이나 새 Controller 작성 없이 진행하는 구조 활동입니다. MVC 2교시 안에서 개념 설명·책 코드 읽기·질문·이 활동을 함께 진행합니다.')
add('교재 12장 연결','테스트 범위를 나눕니다',table([['확인 방법','오늘 확인할 것'],['ProductServiceTest · new로 조립','객체 기능 · Java 예외 · 저장소 분리'],['ProductWiringTest · Spring 주입','빈 연결 · 프록시 · AOP 로그'],['9일 이후 API 확인','URL · JSON · HTTP 응답']])+call('단위 테스트와 Spring 연결 테스트가 증명하는 범위는 다릅니다.'))
add('교재 12장 연결','테스트용 구현으로 바꿀 수 있습니다',code('ProductRepository repository = new MemoryProductRepository();\nProductService service = new ProductService(repository);')+call('실제 메모리 구현체를 사용합니다. Mock 도구 사용은 이후 확장합니다.'),note='Memory 구현 자체는 mock이 아닙니다. 인터페이스와 생성자 DI 덕분에 이후 fake 또는 mock으로 바꿀 수 있다는 연결까지만 합니다.',kind='code-slide')
section('04','집중 실습 · 상품 객체와 저장소')
add('실습 A · 시작','Initializr에서 본인 프로젝트 생성',table([['항목','선택'],['Project / Language','Gradle - Groovy / Java'],['Spring Boot / Java','4.1.2 공통 안정버전 / 17'],['Group / Artifact','com.example / product'],['Package / Dependencies','com.example.product / 선택 없음']]),note='리허설 기준 공통 4.1.2를 사용하고 미리보기는 제외합니다. Spring Boot 4.x Java 17 조건과 starter 이름은 공식 문서 기준입니다. 시작 클래스명은 ProductApplication으로 생성됩니다. AOP 의존성은 뒤에서 한 줄 추가합니다.')
add('실습 A · 구조','파일은 모두 같은 패키지에서 시작',code('src/main/java/com/example/product/\n  ProductApplication.java\n  Product.java\n  ProductRepository.java\n  MemoryProductRepository.java\n  ProductNotFoundException.java\n  ProductService.java')+call('새 Java Class / Interface를 만들고 파일명과 public 타입명을 맞춥니다.'),note='첫 실습은 프로젝트 생성과 객체 연결에 집중합니다. 요청 DTO·Controller는9일, 검증과 예외 응답은12일에 추가합니다. 새 파일 생성 시 package와 class 틀이 이미 있으면 참고 코드로 전체를 교체하거나 중복 부분을 제거합니다.',kind='code-slide')
add('실습 A · Gradle','기본 실행·테스트 의존성을 유지',code("dependencies {\n    implementation 'org.springframework.boot:spring-boot-starter'\n    testImplementation 'org.springframework.boot:spring-boot-starter-test'\n}\n\ntasks.named('test') {\n    useJUnitPlatform()\n}")+call('생성된 build.gradle을 유지 · 위 항목이 있으면 중복 추가하지 않습니다.'),note='이 부분만으로 build.gradle 전체를 덮어쓰지 않습니다. 생성된 테스트 런처 의존성 등도 유지합니다. 오늘은 Web·Validation 선택이 필요하지 않습니다. 테스트 의존성과 JUnit Platform 설정을 삭제하지 않습니다.',kind='code-slide')
filepages('실습 A · 시작 클래스','ProductApplication.java','Initializr가 생성한 시작점 확인')
add('실습 A · Product','상품 객체가 지킬 규칙',table([['정보','규칙'],['id','저장소가 번호 부여'],['name','null · 공백 불가, 앞뒤 공백 제거'],['price','0 이상'],['변경 방식','생성자로 값 설정 · getter로 조회']])+call('이번 필수 실습에서는 상품 정보를 만든 뒤 수정하지 않습니다.'))
filepages('실습 A · Domain','Product.java','상품 정보와 규칙 작성')
add('실습 A · 인터페이스','저장 방법 대신 할 일을 약속합니다',linear('Service는 ProductRepository 인터페이스에 의존하며 Memory 구현체를 사용합니다',[('ProductService','역할을 사용'),('ProductRepository','저장·조회 약속'),('Memory 구현체','메모리에 보관')])+call('메서드 이름·입력·반환 타입을 인터페이스에 선언합니다.'))
filepages('실습 A · 저장소 계약','ProductRepository.java','Interface로 생성')
add('실습 A · 메모리 저장소','id를 키로 상품을 찾습니다',table([['도구','사용 목적'],['Map<Long, Product>','id와 상품 연결'],['ConcurrentHashMap','여러 요청의 기본 저장·조회에 사용'],['AtomicLong','상품 번호 증가'],['Optional<Product>','상품이 없을 수도 있음을 표현']]),note='고급 동시성 알고리즘을 가르치는 시간이 아닙니다. 빈에서 공유하는 저장 상태를 다루기 위한 도구의 역할만 설명합니다. 단일 JVM 학습용 메모리 저장소이며 재시작하면 데이터와 번호가 초기화됩니다. 여러 연산을 묶은 트랜잭션은 제공하지 않습니다.')
filepages('실습 A · 저장소 구현','MemoryProductRepository.java','Class로 생성 · implements 확인')
add('실습 A · 조회 코드 읽기','정렬해서 목록을 반환합니다',code('return store.values().stream()\n        .sorted(Comparator.comparingLong(Product::getId))\n        .toList();')+cards(('입력','저장된 상품들','Map의 values()'),('처리와 결과','id 오름차순 목록','정렬 → List로 변환')),note='교재 3장의 모던 Java 복습과 연결합니다. 메서드 참조 Product::getId는 각 상품의 id를 정렬 기준으로 읽는 표현입니다. Stream 전체 API를 설명하지 않습니다. 반환 목록은 수정용 저장소가 아니라 조회 결과입니다.',kind='code-slide')
filepages('실습 A · 없는 상품','ProductNotFoundException.java','없는 id를 나타내는 예외')
filepages('실습 A · Service','ProductService.java','생성자 주입으로 저장소 사용')
add('실습 A · 완료 기준','웹 없이 객체 연결부터 확인',steps('상품 생성·목록·단건 조회를 Service에서 호출','빈 이름·음수 가격은 IllegalArgumentException','없는 id는 ProductNotFoundException','각 테스트는 새 저장소로 시작'),note='서버 포트나 URL 호출은 오늘의 완료 기준이 아닙니다. 기본 스타터만 사용한 main은 웹 서버를 열지 않고 정상 종료할 수 있습니다. 다음 단위 테스트로 객체 기능을 직접 확인합니다.')
add('실습 A · 작은 테스트','Spring 없이도 Service를 사용할 수 있습니다',code('ProductService service =\n        new ProductService(new MemoryProductRepository());\nProduct product = service.create("노트", 3000);\nProduct found = service.findById(product.getId());')+call('생성자 DI 덕분에 테스트에서도 필요한 객체를 직접 연결할 수 있습니다.'),note='이 코드는 관계를 읽는 짧은 예시이며 시작 클래스 main에 무조건 붙이라는 의미가 아닙니다. 다음 테스트 파일에서 실제로 실행합니다. plain new 객체에는 Spring AOP가 적용되지 않습니다. 이후 AOP 비교에서 다시 확인합니다.',kind='code-slide')
filepages('실습 A · 테스트','ProductServiceTest.java','src/test/java의 같은 패키지에 생성')
add('실습 A · 테스트 실행','정상 · 잘못된 값 · 없는 상품',code('# macOS / Linux · 프로젝트 루트\n./gradlew test\n\n# Windows PowerShell\n.\\gradlew.bat test')+call('테스트 3개가 통과하면 상품 로직과 예외를 확인한 것입니다.'),note='서버와 DB를 실행하는 테스트가 아닙니다. 테스트마다 새 테스트 인스턴스와 저장소를 사용합니다. 테스트 통과는 HTTP 매핑이나 AOP 적용까지 증명하지 않습니다. Wrapper 실행 권한이 없으면 bash ./gradlew test로도 실행할 수 있습니다.',kind='code-slide')
add('AOP 실습 · 의존성','Spring Boot 4.x의 스타터 추가',code("implementation 'org.springframework.boot:spring-boot-starter-aspectj'")+steps('build.gradle의 dependencies 안에 한 줄 추가','Gradle 프로젝트 새로고침','다음 TimingAspect 클래스를 같은 패키지에 작성'),note='Spring Boot 4에서 예전 spring-boot-starter-aop 이름은 spring-boot-starter-aspectj로 변경되었습니다. 이 수업에서는 Boot 자동 설정을 사용하므로 @EnableAspectJAutoProxy를 별도로 추가하지 않습니다. 공식 AOP 문서와 마이그레이션 가이드를 확인했습니다.',kind='code-slide')
filepages('AOP 실습 · 시간 기록','TimingAspect.java','서비스 호출 전후에 시간 측정')
add('AOP 실습 · 핵심 한 줄','proceed()가 원래 메서드를 실행합니다',code('try {\n    return joinPoint.proceed();\n} finally {\n    // 성공하거나 예외가 나도 시간 기록\n}')+call('proceed()를 호출하지 않으면 이 예제의 실제 상품 기능도 실행되지 않습니다.'),note='실행 시간은 짧으면 0ms가 나올 수 있습니다. 0ms 자체가 AOP 실패가 아닙니다. return 값을 전달하고 예외를 삼키지 않는 구조를 설명합니다.',kind='code-slide')
add('AOP 실습 · 제공 틀','Spring이 주입한 Service를 테스트에서 호출',steps('src/test/java/com/example/product/에 다음 파일 작성','제공된 연결 확인 틀을 그대로 사용','단위 테스트와 함께 전체 test 실행','프록시 여부·값 검증과 시간 로그 비교'),note='새 Controller나 실행용 seed를 추가하지 않습니다. 제공 테스트는 웹 환경 없이 Spring 컨텍스트에서 빈을 주입합니다. 뒤 수업에 Web 의존성이 추가되어도 그대로 재사용할 수 있습니다. SpringBootTest는 SpringBootTest.WebEnvironment.NONE을 사용합니다.')
filepages('AOP 실습 · 연결 확인','ProductWiringTest.java','제공 틀 · src/test/java의 같은 패키지에 생성')
add('AOP 실습 · 실행 결과','단위 테스트와 주입 테스트를 비교',code('create : 0ms\nfindAll : 1ms\nfindById : 0ms')+call('단위 테스트 3개 + 연결 테스트 1개 통과 · 시간 숫자는 실행마다 다릅니다.'),note='Initializr 기본 contextLoads 테스트를 유지했다면 전체5개입니다. 예제4개는 ProductServiceTest3개와 ProductWiringTest1개입니다. 로그가 안 보이면 IDE 테스트 콘솔 또는 Gradle --info로 확인합니다. 단위 테스트 new 호출에는 AOP 로그가 없고, 주입된 Service에는 나타납니다. 숫자0ms도 정상입니다.',kind='code-slide')
add('문제 해결','실패한 범위를 먼저 구분합니다',table([['증상','확인'],['컴파일 실패','package · import · 클래스/파일명'],['단위 테스트 실패','상품 규칙 · 저장·조회 결과'],['연결 테스트 실패','빈 등록 · 패키지 · AOP 의존성'],['프록시 또는 로그 없음','TimingAspect · Pointcut · 주입된 Service'],['실행 종료 / 데이터 초기화','웹 없는 실행 · 메모리 저장 방식']]))
section('05','검증하고 설명하기')
add('발표 준비','화면으로 결과와 구조를 설명',steps('단위 테스트 성공·실패 사례 보여주기','주입 테스트의 프록시 확인과 시간 로그 보여주기','Product → Repository → Service 책임 설명','오늘 해결한 오류 또는 헷갈린 점 공유'),note='마지막 교시 안에서 자율 실습 마무리 20분과 피드백 25분을 운영합니다. 시연 없이 멘티 실행 결과로 확인하며, 모든 팀의 발표를 길게 반복하지 않습니다.')
add('발표 질문','정의보다 내 코드의 이유를 설명',steps('누가 ProductService를 생성하고 연결하나요?','Service가 인터페이스를 받는 이유는 무엇인가요?','new 호출과 주입된 Service의 AOP 차이는 무엇인가요?','MVC의 요청 연결과 DI의 객체 연결은 어떻게 다른가요?'))
add('다음 수업 연결','같은 상품 프로젝트에 순서대로 추가',table([['날짜','추가할 학습'],['11월 9일 · 4시간','REST 설계 · DTO · JSON · Controller · 정상 요청'],['11월 12일 · 앞 2시간','검증 · 예외 응답 · 실패 요청 · 면접 포인트'],['11월 12일 · 뒤 2시간','상품 남은 CRUD 요구사항·계층·API·테스트 설계'],['11월 14일 · 6 + 2시간','설계한 CRUD 구현·테스트 6시간 → JPA 시작 2시간']])+call('책 11장 DB는 이후 DB/JPA와 연결 · 오늘 저장소는 재실행하면 초기화'))
section('06','별도 과제 · 객체와 테스트 확장')
add('과제 1 · 기초','상품 규칙의 경계값 테스트 추가',table([['입력','기대 결과'],['가격 0','정상 생성 · 가격 0 유지'],['이름 앞뒤 공백','저장된 이름의 앞뒤 공백 제거'],['null / 공백 이름','각각 IllegalArgumentException'],['잘못된 생성 뒤 목록','이전 상품 값과 개수 유지']])+call('ProductServiceTest에 독립적인 테스트 추가 · 정답 코드 없음'),note='기존 테스트를 삭제하지 않습니다. 각 테스트는 새 저장소에서 시작하고 기대값과 실제값을 assert로 비교합니다. 실패 후 번호 연속성은 요구하지 않습니다. HTTP나 검증 어노테이션은 사용하지 않습니다.')
add('과제 2 · 응용','Service에 가격 상한 조회 추가',table([['메서드','findByMaxPrice(int maxPrice) → List<Product>'],['가격 상한','상한 이하 상품 · 같은 가격 포함'],['결과 순서','id 오름차순'],['조건 불일치','빈 목록'],['음수 상한','IllegalArgumentException']])+call('노트 3000 · 펜 1000 · 무료샘플 0 / 상한 1000 → 펜과 무료샘플'),note='메서드 이름은 상품 id 조회와 구분합니다. 기존 findAll 결과를 조건으로 조회하되 저장소를 덮어쓰지 않습니다. Repository 계약 변경은 필수가 아닙니다. 상한 0 · 동일 가격 · 결과 없음 · 음수 · 조회 전후 원본 보존을 테스트합니다. HTTP 검색은 9일 이후 별도 과제입니다.')
add('과제 제출','새 기능을 테스트와 함께 설명',steps('실습 필수 · 추가 과제 수행 범위 표시','요구사항과 테스트 기대·실제 결과 기록','기존 3개 단위 테스트와 연결 테스트 유지','GitHub Issue·브랜치·PR로 제출'),note='추가 과제는 실습 코드에 없는 구현입니다. 수업시간 안에 두 과제의 완료를 강제하지 않으며 마감은 별도 안내합니다. API 이름 검색·수정·삭제는 후속 범위입니다.')
section('07','GitHub 제출')
add('GitHub 제출 · 저장소','Spring 학습용 저장소 하나를 계속 사용',table([['설정','지정 값'],['Repository name','sesac-spring-boot-study'],['Description','Spring Boot 학습 실습 및 과제 기록'],['Visibility / Default branch','Public / main'],['Settings → Features','Issues · Wiki 활성화 확인']])+call('기존 학습 저장소 재사용 · 없을 때만 README·Java .gitignore로 생성'),note='저장소 생성/clone 상세 절차는 수업 슬라이드에 추가하지 않습니다. 기존 greeting-api,Issue,PR,Wiki는 유지합니다. GitHub Free의 Public 저장소 Wiki기능을 확인합니다.')
add('GitHub 제출 · 파일','product-api/에 오늘의 파일을 보관',table([['포함','제외'],['src/ · build.gradle · settings.gradle','build/ · .gradle/'],['gradlew · gradlew.bat · gradle/wrapper/','.idea/ · *.iml'],['gradle-wrapper.jar','.env · 비밀값이 담긴 파일']])+call('루트 .gitignore: !product-api/gradle/wrapper/gradle-wrapper.jar 예외 확인'),note='Wrapper jar는 실행에 필요합니다. 루트Java.gitignore의 *.jar에 대한 예외를 유지하고 greeting-api의 예외도 보존합니다. 프로젝트 내부의 별도.git은 복사하지 않습니다. 비밀값 포함 여부를 확인합니다.')
add('GitHub 제출 · 필수 이름','오늘의 실습과 문서를 각각 제출',table([['브랜치','Issue · PR 제목'],['practice/product-core','[실습] 상품 객체·저장소·Service와 테스트'],['docs/product-core','[문서] 상품 객체 구조와 테스트 기록']])+call('필수: Issue 2개 · 병합 PR 2개 · HTTP API 구현은 오늘 제출 범위 아님'))
add('GitHub 제출 · 과제 이름','수행한 추가 과제마다 작업 하나',table([['브랜치','Issue · PR 제목'],['test/product-boundaries','[과제 1] 상품 규칙 경계값 테스트'],['feature/core-price-filter','[과제 2] Service 가격 상한 조회']])+call('수행 과제당 Issue·병합 PR 각각 1개 추가 · 정답 코드 없이 구현'))
add('GitHub 제출 · 작업 순서','매 단계 최신 main에서 시작합니다',steps('기존 저장소는 main pull → Issue 생성 → 지정 브랜치','구현·테스트 → 목적별 commit → push','base main으로 PR → 자체 확인 → 병합','main pull 뒤 다음 작업 시작'),note='완료한 실습을 사후정리하는 경우 Issue에 완료결과정리임을 명시합니다. 본인이 자체확인 후 병합할 수 있습니다. Wiki는 코드PR에 자동포함되지 않으므로 문서PR에서 Wiki링크와작성확인을 남깁니다.')
add('GitHub 제출 · Issue 설정','이름과 작업 정보를 통일합니다',table([['항목','규칙'],['Assignee','본인'],['Labels','practice · assignment · docs · bug'],['작업별 라벨','실습practice · 과제assignment · 문서docs'],['Milestone','product-core-2026-11-07 · 마감일 미지정']]))
add('GitHub 제출 · Issue 본문','목표와 검증 근거를 남깁니다',steps('목표','구현할 일 체크리스트','완료 기준','검증 결과(기대·실제)','관련 PR')+call('Issue 번호는 실제 자동 발급 번호 · PR 생성 뒤 링크 추가'))
add('GitHub 제출 · PR','Issue 연결 후 자체 확인하고 병합',steps('본문: 변경 내용 / 검증 결과 / 관련 Issue','Closes #12의 12를 실제 Issue 번호로 교체','코드·테스트·실행기록·비밀값 포함 여부 확인','base main 병합 → 연결 Issue 종료 확인')+call('실습·문서 필수 2개 · 두 추가 과제까지 수행하면 각각 총 4개'),note='Issue와PR제목은같게사용합니다. 커밋은 feat:·test:·docs:·fix:로 목적을 표시하며 최소개수나 타인승인은강제하지않습니다. main직접push대신교육용PR흐름으로제출합니다.')
add('GitHub 제출 · README','프로젝트 README 여섯 항목',steps('프로젝트 소개','개발 환경: 실제 Java·Spring Boot 버전','실행·테스트 방법','구현 현황: 실습과 추가 과제 수행 범위','객체 기능 목록 · API는 9일 구현 예정','Wiki 링크')+call('product-api/README.md 작성 · 루트 README에 프로젝트 목록과 링크 누적'),note='greeting-api등기존루트README링크를보존합니다. docs/product-core PR에두README변경과Wiki작성확인을기록합니다. 웹없는main정상종료와실제테스트명령을구분해적습니다.')
add('GitHub 제출 · Wiki ①','여섯 페이지를 프로젝트별로 누적',table([['페이지','product-api 섹션 내용'],['Home','공통 목차와 프로젝트별 링크'],['01-Setup','JDK·Boot·의존성·테스트 실행 방법'],['02-Architecture','Product·Service·Repository · DI · AOP']])+call('기존 greeting-api / product-api 내용을 유지하고 오늘 기록 추가'))
add('GitHub 제출 · Wiki ②','구현한 범위와 근거를 정확히 기록',table([['페이지','product-api 섹션 내용'],['03-API','오늘 미구현 · 9일 구현 예정 명시'],['04-Verification','단위 테스트·주입 테스트·프록시·AOP 로그<br>과제 기대·실제와 Issue/PR 링크'],['05-Retrospective','오류 또는 헷갈린 점 · 원인·해결·배운 점']])+call('아직 구현하지 않은 API와 HTTP 상태 결과를 제출하지 않습니다.'),note='Wiki는GitHubWiki화면에작성하며일반코드PR과별도입니다.6페이지기존섹션보존,문서PR에Wiki링크와작성확인을포함합니다.')
add('GitHub 제출 · 최종 확인','필수 실습·문서를 링크로 제출',steps('Public 저장소 URL + Wiki Home URL','필수 병합 PR 2개: 실습·문서','추가 과제 수행 여부와 수행한 PR 링크','main의 product-api/ 테스트 실행 · 기존 프로젝트 보존')+call('9일 practice/product-rest → 12일 practice/product-validation로 같은 프로젝트 확장'),note='12일설계는docs/product-crud-design로이어집니다. 단축 URL은 별도 과제입니다.오늘REST나오류응답을미리구현하도록요구하지않습니다.마감은별도공지전미지정입니다.')
refs=[('교재 · CH 09 / 12 일부','https://www.yes24.com/product/goods/124434554','상품 객체 · 객체지향 · 테스트'),('DI · 빈 등록','https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html','생성자 주입'),('빈 스코프','https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html','기본 싱글턴'),('자동 설정','https://docs.spring.io/spring-boot/reference/using/auto-configuration.html','조건과 기본 구성'),('Spring AOP','https://docs.spring.io/spring-framework/reference/core/aop/proxying.html','프록시와 호출'),('Spring MVC','https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html','DispatcherServlet 처리 흐름')]
add('참고','교재와 Spring 공식 문서','<div class="references">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><b>{n} ↗</b><span>{d}</span></a>' for n,u,d in refs)+'</div>')
refs=[('GitHub Wiki','https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis','Public 저장소 Wiki'),('PR과 Issue 연결','https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue','Closes와 기본브랜치 병합')]
add('GitHub 참고','제출 규칙의 공식 문서','<div class="references">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><b>{n} ↗</b><span>{d}</span></a>' for n,u,d in refs)+'</div>')
# Short reading/implementation cycles keep the Saturday lesson hands-on.
def at(title): return next(i for i,d in enumerate(S) if d['title']==title)
a=at('객체를 연결하는 Spring'); b=at('실행 준비와 공통 처리'); c=at('서버·클라이언트와 MVC'); d=at('집중 실습 · 상품 객체와 저장소'); e=at('Spring Boot 4.x의 스타터 추가'); f=at('검증하고 설명하기')
t=at('테스트 범위를 나눕니다')
S = S[:a] + S[a:b] + S[d:e] + S[b:c] + S[e:f] + S[c:d] + S[f:]
# Section numerals follow the visible alternating order.
section_number=0
for record in S:
 if record['kind']=='section':
  section_number+=1
  record['body']='<div class="section-number">'+f'{section_number:02}'+'</div>'
# Emit a self-contained, read-only deck. No private notes or local editing drafts are shipped.
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson3-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.07</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 9·12장과 함께 배우는 IoC·DI·AOP·MVC 구조와 상품 객체 실습"><title>11월 7일 · 객체 연결과 MVC 구조</title><style>'+css+'</style></head><body data-deck-revision="2026-11-07-v6-staged-core"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(TODAY_SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(t in out for t in ['강사 시연','contenteditable=','localStorage'])
assert not re.search('gray',''.join(slides),re.I)
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
# Full source examples are canonical for verification, but are not a downloadable starter project.
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',out.count('class="diagram"'),'SVG diagrams;',len(out.encode()),'bytes')
