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
add('2026.11.19 · 4시간','상품 API를<br>JPA 저장소로 전환하기','<div class="cover-bottom"><strong>작업지 → 구현 → 회귀 확인 → 제출</strong><span>진행: 이준형 강사 · 자율 실습</span></div>',kind='cover')
add('오늘의 결과','화면과 API는 유지하고 저장 방식을 바꿉니다',steps('상품 생성·전체/단건 조회·수정·삭제 정상 동작','검증 400 · 없는 상품 404 · 실패 시 데이터 유지','프로세스를 재시작해도 생성한 상품을 조회','기존 테스트와 전환 검증 결과를 PR에 기록'))
add('책과 연결','상품 관리의 데이터 접근 부분을 다시 읽기',steps('책에서 Repository 역할과 상품 저장·조회 흐름 확인','책의 JDBC 접근과 오늘 JPA 구현의 차이 설명','Controller → Service → Repository 호출 흐름 표시','페이지 번호는 소지한 판본에서 직접 기록'))
add('운영','네 번의 작업과 확인',table([['블록','45분 작업 · 15분 휴식/정리'],['1','출발 코드 실행 · 기존 테스트 · 변경 계획'],['2','JPA adapter 구현 · 빈 연결 · 트랜잭션'],['3','CRUD · 검증 · 예외 회귀 확인'],['4','재시작 보존 · 문서 · GitHub 제출']]))
add('진행 방식','직접 구현하고 결과로 확인합니다',steps('새 개념 설명·강사 코딩 시연 없이 16일 내용을 적용','STUDENT-WORKSHEET.md 순서대로 단계별 체크','막히면 오류와 재현 방법을 정리한 뒤 힌트 사용','완료 지점마다 강사에게 테스트·응답을 보여주기'))
add('실습 자료','출발 코드와 작업지를 준비',table([['자료','사용 방법'],['<a href="assets/product-api-start.zip">출발 코드 ZIP ↗</a>','16일 완료 상태 · API는 메모리 저장소'],['<a href="STUDENT-WORKSHEET.md">멘티 작업지 ↗</a>','필수 작업·완료 기준·단계별 힌트'],['<a href="HANDOFF.md">대강 진행표 ↗</a>','블록별 점검·공통 오류·중단/복구 기준'],['기존 sesac-spring-boot-study','product-api를 이어 사용 · 새 저장소 생성 없음']]))
add('기초 복습','모르는 단어부터 짧게 확인',table([['말','오늘 쓰는 뜻'],['Entity','products 표의 한 행과 연결할 Java 객체'],['빈 등록','Spring이 만들고 주입할 객체로 지정'],['영속 상태','Entity가 영속성 컨텍스트에서 관리되는 상태'],['트랜잭션','한 업무의 DB 변경을 함께 확정하거나 취소']])+call('<a href="../shared/db-basics/README.md">DB 기초 ↗</a> · <a href="../2026-11-16/BEGINNER-WORKSHEET.md">16일 쉬운 작업지 ↗</a>'))
add('역할 구분','Repository라는 이름이 두 번 나옵니다',table([['이름','누가 사용','주고받는 값'],['ProductRepository','ProductService','Product · 기존 업무 계약'],['SpringDataProductRepository','JpaProductRepository','ProductEntity · JPA DB 도구'],['JpaProductRepository','두 계약을 연결','Entity를 Product로 바꾸는 중간 연결자']]))
add('호출 경로','Service에서 DB까지 따라가기',linear('Service가 기존 계약을 호출하고 Jpa 구현체가 Spring Data 도구를 사용해 DB에 접근',[('ProductService','ProductRepository 호출'),('JpaProductRepository','값 변환·위임'),('Spring Data JPA','Entity 저장·조회')])+call('오른쪽 도구가 DB에 SQL을 보냅니다. Controller는 ProductEntity를 반환하지 않습니다.'))
section('01','출발 상태 확인','')
add('1교시','16일 상태에서 출발하기',steps('작업 내용을 commit하고 현재 main을 확인','ProductEntity · SpringDataProductRepository 존재 확인','ProductRepository의 현재 빈이 Memory인지 확인','JPA 저장소 실습 테스트와 기존 테스트 실행'))
add('실행','기존 테스트 결과를 먼저 저장',code('./gradlew test\n./gradlew bootRun')+call('Windows는 gradlew.bat 사용 · product-api 폴더에서 실행'),kind='code-slide')
add('출발 점검','아직 API가 JPA로 연결되지는 않았습니다',table([['존재하는 코드','오늘 연결할 부분'],['ProductEntity','DB 매핑 · 도메인 Product와 분리'],['SpringDataProductRepository','JPA 기본 저장·조회 기능'],['MemoryProductRepository','현재 API가 사용하는 구현체'],['ProductRepository','Service가 의존하는 기존 인터페이스']]))
add('작업 계획','바꾸는 책임을 한 문장으로 적기',steps('Controller와 요청/응답 DTO의 계약 유지','Service는 ProductRepository 인터페이스에 의존','JpaProductRepository가 JPA와 도메인 사이를 변환','메모리 구현체 대신 JPA 구현체 하나를 빈으로 연결'))
add('중간 확인','다음 단계로 넘어갈 조건',steps('출발 테스트가 통과했는지 기록','기존 API로 상품을 만들고 실제 id를 저장','책의 데이터 접근 코드와 변경 위치를 표시','원인을 모르는 기존 실패는 먼저 강사에게 공유'))
section('02','저장소 연결 실습','')
add('2교시','JpaProductRepository를 구현하세요',steps('기존 ProductRepository의 모든 메서드 목록 작성','SpringDataProductRepository를 생성자로 주입','Product ↔ ProductEntity 변환 책임 구현','저장·조회·수정·삭제 계약을 기존 동작과 비교'))
add('파일 찾기','한 메서드씩 짝을 맞춥니다',table([['기존 계약','Spring Data 도구·변환'],['save(name, price)','새 ProductEntity → data.save → toProduct'],['findAll()','findAllByOrderByIdAsc → 각 Entity.toProduct'],['findById(id)','findById → Optional 안의 값 변환'],['update / delete','먼저 findById → 있으면 변경/삭제']]))
add('값 따라가기','노트 3000이 표의 한 행이 됩니다',table([['단계','값'],['POST 본문','name=노트, price=3000 · id 없음'],['new ProductEntity','name=노트, price=3000 · id는 DB에 맡김'],['data.save 반환','id=실제 생성값, name=노트, price=3000'],['toProduct → 응답','같은 id·이름·가격 · POST 201']])+call('화면 응답만으로 JPA 연결 성공을 단정하지 말고 INSERT 로그와 재시작도 확인합니다.'))
add('저장','DB에서 부여한 id로 결과를 반환',steps('생성 시 새 Entity의 id는 DB 생성 전략에 맡기기','save가 반환한 Entity에서 실제 id 읽기','조회 결과 없음은 기존 Optional 계약으로 표현','목록 정렬은 기존 API의 id 오름차순 유지'))
add('수정과 삭제','없는 상품의 동작도 보존',steps('실제 생성한 id의 수정 전후 값을 비교','없는 상품 수정·삭제가 기존 404로 연결되는지 확인','수정 성공 시 같은 id가 유지되는지 확인','삭제 후 해당 id 조회가 404인지 확인'))
add('빈 연결','ProductRepository 구현체는 하나만 등록',table([['구현체','오늘의 설정'],['MemoryProductRepository','클래스는 보존 · @Repository 등록 제거'],['JpaProductRepository','@Repository 등록'],['ProductService','인터페이스 주입 유지'],['두 구현체가 동시에 빈','중복 빈 오류를 등록 정책으로 해결']]))
add('트랜잭션','Service에서 한 업무 단위를 묶기',steps('쓰기 작업은 @Transactional 범위에서 처리','조회 작업은 readOnly=true 적용 여부 확인','변경 감지에 의존하는 코드는 트랜잭션 안에서 실행','Controller에 DB 작업을 옮기지 않기'))
add('수정 예측','PUT 뒤 어떤 값이 남을까요?',table([['행동','예측'],['같은 id에 PUT: 노트, 3500','해당 Entity를 찾고 change로 가격 변경'],['Service 업무 정상 종료','트랜잭션 확정 · 변경 감지가 UPDATE 반영'],['같은 id GET','price=3500 · 새 상품 행이 생기면 오류'],['이후 재시작 GET','같은 id·노트·3500이어야 보존 성공']]))
add('트랜잭션 읽기','설정의 뜻을 말하며 확인',table([['설정·용어','쉽게 읽기'],['@Transactional','이 메서드의 DB 업무를 한 묶음으로 처리'],['readOnly=true','조회 업무임을 알리는 설정 · 쓰기 차단 장치 아님'],['변경 감지','관리하는 Entity의 바뀐 값을 DB에 반영'],['flush','변경 SQL을 DB로 보내기 · 확정(commit)은 별도']]))
add('DB 설정','파일 DB 경로와 실행 위치를 확인',code('spring.datasource.url=jdbc:h2:file:./data/products\nspring.datasource.username=sa\nspring.datasource.password=\nspring.jpa.hibernate.ddl-auto=update\nspring.jpa.open-in-view=false')+call('로컬 학습용 설정 · 같은 프로젝트 폴더에서 한 프로세스만 실행'),kind='code-slide')
add('DB 두 개','앱과 테스트가 같은 DB인가요?',table([['설정 파일','DB·목적'],['src/main/resources/application.properties','h2:file:./data/products · 앱 종료 후 보관'],['src/test/resources/application.properties','h2:mem:… · 테스트별 격리·create-drop'],['상대 경로 ./data','product-api 실행 폴더 기준 · 실행 위치 기록'],['실제 API JPA 판정','INSERT/SELECT 로그 + 파일 DB 재시작 후 같은 값']]))
add('주의','운영 방식과 테스트 환경을 구분',steps('update는 로컬 학습용 · 운영 스키마 변경 정책과 구분','파일 DB는 data/ 아래 생성 · Git 추적 제외','테스트는 별도 인메모리 DB·롤백으로 격리','실패 복구를 위해 기존 DB 파일을 무작정 지우지 않기'))
add('막힐 때','세 단계 힌트로 범위를 줄이기',table([['1단계','인터페이스 계약·주입 대상·오류 첫 원인 확인'],['2단계','Entity 변환·빈 중복·트랜잭션 범위 확인'],['3단계','강사와 참고 구현을 비교하고 본인 코드에 반영']])+call('학습자 작업지에는 완성 답안을 넣지 않습니다.'))
section('03','API 계약 회귀 확인','')
add('3교시','생성한 id를 이후 요청에 사용',table([['요청','필수 확인'],['POST /products','201 · Location · 응답의 실제 id 저장'],['GET /products','200 · id 오름차순 목록'],['GET /products/{실제 id}','200 · 생성한 이름과 가격'],['PUT /products/{실제 id}','200 · 수정 값 · id 유지'],['DELETE /products/{실제 id}','204 · 이후 조회 404']]))
add('실패 확인','실패 전후 저장 상태를 비교',table([['입력','기대 결과'],['공백 이름·음수·가격 누락/null','400 · 새 상품 없음'],['JSON 문법/타입 오류','400 · 기존 데이터 유지'],['존재하지 않는 id 조회·수정·삭제','404 · 기존 데이터 유지'],['이름 앞뒤 공백·가격 0','정상 처리 · trim과 0 허용']]))
add('확인 표','요청과 SQL과 행을 함께 기록',table([['행동','예상 SQL 종류·행 변화'],['POST 노트 3000','INSERT · 상품 행 1개 추가'],['GET 실제 id','SELECT · 행 변경 없음'],['PUT 같은 id 가격 3500','SELECT/UPDATE · 같은 행 가격 변경'],['400 입력 실패','상품 행·값 변화 없음']])+call('실행 SQL의 정확한 수·순서는 구현과 flush 시점에 따라 달라집니다. 실제 로그와 비교하세요.'))
add('증거','기대와 실제를 나란히 남기기',steps('요청 메서드·URL·본문과 응답 상태 기록','생성 응답의 id·Location을 다음 요청과 연결','실패 전후 목록의 개수·값 비교','자동 테스트 결과와 수동 API 확인을 구분'))
add('테스트 격리','데이터 순서에 의존하지 않는 테스트',steps('각 테스트가 필요한 상품을 직접 생성','반환받은 id를 사용하고 id=1을 가정하지 않기','JPA 테스트의 롤백 범위를 확인','수동 실행 DB와 테스트 DB가 같은지 확인'))
add('문제 분석','어느 경계에서 실패했나요?',table([['증상','먼저 확인'],['주입 후보 2개','Memory와 Jpa 빈 등록 상태'],['테이블 없음','현재 프로필·datasource·DDL 설정'],['수정이 반영 안 됨','트랜잭션·관리 상태·변환 로직'],['기존 응답 변경','DTO 변환·예외 연결·Controller diff']]))
section('04','보존과 제출','')
add('4교시','재시작해도 상품을 찾을 수 있나요?',steps('상품 생성 후 실제 id와 값을 기록','애플리케이션을 정상 종료','같은 폴더·설정으로 다시 실행','저장한 id 조회 200 · 수정 값·목록 확인'))
add('보존 확인','테스트 DB가 아닌 API 실행 DB 확인',steps('파일 datasource와 data/ 생성 위치 확인','create/create-drop 설정으로 재시작하지 않기','DB 파일 잠금이면 중복 실행부터 종료','DB 파일 삭제 대신 로그·URL·작업 폴더 비교'))
add('완료 판정','강사에게 보여줄 네 가지 증거',steps('전체 테스트 통과 결과','실제 id 기반 CRUD와 400·404 결과','재시작 전후 같은 id·값 조회 결과','설정·빈 선택·트랜잭션을 설명한 문서'))
add('선택 확장','필수 완료 후 비교 테스트',steps('메모리/JPA 구현체의 계약 테스트 차이 정리','읽기 전용 트랜잭션의 의미를 문서로 설명','단축 URL 과제의 저장 계층 전환 계획 작성','N+1은 23일 별도 관계 예제로 진행'))
add('GitHub','필수 Issue 1개 · 병합 PR 1개',table([['항목','지정 값'],['Repository','sesac-spring-boot-study'],['Branch','practice/product-jpa-migration'],['Issue · PR','[실습] 상품 API 데이터 접근 JPA 전환'],['PR 본문','변경·기대/실제 결과·Wiki 링크·Closes #실제번호']]))
add('제출 순서','검증한 코드를 main에 반영',steps('main pull → Issue → 지정 브랜치 → 구현·검증','commit·push → base main PR → 자체 점검·병합','main pull 후 최종 테스트·상태 확인','실습 복구본 사용 시 사용 지점과 수정 내용 기록'))
add('문서','기존 README와 Wiki에 누적',table([['위치','갱신 내용'],['product-api/README.md','실행·DB 경로·CRUD·테스트·현황'],['Home · 01-Setup · 02-Architecture','JPA 연결·환경·책의 JDBC와 비교'],['03-API · 04-Verification','응답 계약·재시작·기대/실제·PR'],['05-Retrospective','실패 원인·힌트 사용·다음 질문']]))
add('제출 제외','실행 파일과 개인 데이터를 구분',code('# 루트 .gitignore에 기존 규칙과 함께 유지\n**/build/\n**/.gradle/\n**/data/\n**/*.mv.db\n**/*.trace.db\n.env\n!product-api/gradle/wrapper/gradle-wrapper.jar')+call('src · Gradle 설정 · Wrapper 포함 / DB·IDE·비밀값 제외'),kind='code-slide')
add('별도 과제','단축 URL 웹 서비스도 이어갑니다',steps('상품 실습과 별도인 <a href="../assignments/short-url/">단축 URL 과제 안내 ↗</a> 확인','본인 설계 → 백엔드 → AI 프론트 → 연동 확인','프롬프트·수정·테스트·GitHub 기록 누적','제출 마감은 별도 안내 · 23일 결과 공유 권장'))
add('23일 연결','저장된 객체와 실행되는 SQL 관찰',steps('영속성 컨텍스트·변경 감지·flush/clear 확인','독립 주문 예제로 지연 로딩과 N+1 재현','쿼리 수를 비교하고 fetch join으로 개선','상품 API에 불필요한 관계를 추가하지 않기'))
section('참고','강사 참고 구현','')
add('참고 사용법','먼저 직접 작성하고 나중에 비교',steps('실습 작업과 테스트를 먼저 수행','막힌 지점의 힌트와 코드만 비교','참고 코드를 사용했다면 적용 범위 기록','전체 파일 버튼은 검증된 코드 원문을 표시'))
for name in SOURCES:
 add('강사 참고 구현',name,call('작업지 수행 후 참고용으로 확인합니다. 완성 파일은 버튼으로 펼칩니다.'),source=name)
add('참고','책과 공식 문서','<div class="references"><a href="https://docs.spring.io/spring-data/jpa/reference/">Spring Data JPA ↗<span>Repository · Query methods</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html">Spring 트랜잭션 ↗<span>Service 경계와 프록시</span></a><a href="https://docs.spring.io/spring-boot/reference/data/sql.html">Spring Boot SQL 데이터 ↗<span>datasource · JPA 설정</span></a></div>')
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-19-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.19</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="상품 API JPA 전환 실습"><title>11월 19일 · 상품 API JPA 전환 실습</title><style>'+css+'</style></head><body data-deck-revision="2026-11-19-v1-curriculum"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'reference buttons;',len(out.encode()),'bytes')
