from pathlib import Path
import html,json,re
SOURCES = {}  # Runnable examples stay in the archive, outside today's lecture.
R=Path(__file__).resolve().parent
OUT=R.parent
S=[]
def esc(s):return html.escape(str(s))
def call(s):return '<div class="callout">'+s+'</div>'
def table(rows):return '<table class="lesson-table">'+''.join('<tr>'+''.join(f'<{("th" if i==0 else "td")}>{x}</{("th" if i==0 else "td")}>' for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
def steps(*xs):return '<ol class="steps">'+''.join('<li>'+x+'</li>' for x in xs)+'</ol>'
def add(ch,title,body='',sub='',note='',kind='',source=None):S.append(dict(ch=ch,title=title,body=body,sub=sub,note=note,kind=kind,source=source))
def section(n,title,sub=''):add(title,title,'<div class="section-number">'+n+'</div>',sub,kind='section')
# Diagrams are native SVG with text, explicit states and directional arrows.
_diagram_id=0
def svg(title,inner,h=300,topic='flow'):
 global _diagram_id
 _diagram_id+=1
 return '<svg class="diagram" data-diagram-topic="'+esc(topic)+'" viewBox="0 0 1148 '+str(h)+'" role="img" aria-label="'+esc(title)+'"><title>'+esc(title)+'</title><defs><marker id="arrow-'+str(_diagram_id)+'" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9" fill="none" stroke="#087f5b" stroke-width="1.5"/></marker></defs>'+inner.replace('url(#arrow)',f'url(#arrow-{_diagram_id})')+'</svg>'
def text(x,y,value,size=23,color='#16251f',anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}">{esc(value)}</text>'
def box(x,y,w,h,title,sub='',fill='#edf5ee'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#9fbea9" stroke-width="2"/>'+text(x+w/2,y+40,title,25)+('' if not sub else text(x+w/2,y+75,sub,22,'#52665a'))
def arrow(x1,y1,x2,y2,label=''):
 return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'+('' if not label else text((x1+x2)/2,(y1+y2)/2-14,label,21,'#087f5b'))
def linear(title,nodes,topic='flow'):
 n=len(nodes);gap=38;w=(1148-gap*(n-1))/n;inner=''
 for i,(name,desc) in enumerate(nodes):
  x=i*(w+gap);inner+=box(x,70,w,115,name,desc)
  if i<n-1:inner+=arrow(x+w+5,127,x+w+gap-7,127)
 return svg(title,inner,255,topic)
def object_db():
 return svg('Java 객체의 가격을 변경해도 SQL 반영 전 DB 값은 30000입니다',box(12,55,430,130,'Java 상품 객체','키보드 · 현재 25000원')+box(704,55,430,130,'DB 상품 행','키보드 · 아직 30000원')+arrow(465,120,680,120,'UPDATE 필요'),245,'object-db')
def partial_success():
 inner=box(12,20,500,110,'가격 변경은 확정','products · 25000원')+box(636,20,500,110,'이력 저장은 실패','price_history · 기록 없음', '#fff1e7')
 inner+=text(574,190,'가격은 바뀌었는데 변경 이력이 없다',28,'#9b4d25')
 inner+=text(574,240,'원하는 규칙: 둘 다 저장하거나, 둘 다 취소',25,'#087f5b')
 return svg('DB 작업이 따로 확정되면 가격 변경만 성공하고 이력은 실패할 수 있습니다',inner,275,'atomicity')
def service_boundary():
 inner='<rect x="15" y="14" width="1118" height="245" rx="16" fill="#f3f7ee" stroke="#087f5b" stroke-width="2"/>'
 inner+=text(574,52,'Service 기능 하나의 트랜잭션 범위',26,'#087f5b')
 inner+=box(45,90,280,110,'상품 조회','현재 가격 확인')+box(435,90,280,110,'가격 변경','30000 → 25000')+box(825,90,280,110,'이력 저장','변경 내용 기록')+arrow(340,145,420,145)+arrow(730,145,810,145)
 return svg('조회와 변경과 이력 저장을 같은 Service 트랜잭션 안에 포함합니다',inner,280,'service-boundary')
def proxy_return():
 inner=box(10,24,310,110,'호출하는 빈','Controller 등')+box(420,24,310,110,'Spring 프록시','호출 전 시작·참여')+box(830,24,308,110,'실제 Service','업무 메서드 실행')
 inner+=arrow(333,78,407,78)+arrow(743,78,817,78)
 inner+='<path d="M985,145 V215 H575 V145" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+=text(790,250,'처리 결과를 받아 commit·rollback 판단',24,'#087f5b')
 return svg('외부 호출을 프록시가 받아 트랜잭션을 시작하거나 참여하고 실제 Service 결과를 받아 종료를 처리합니다',inner,280,'proxy-return')
def dirty_check():
 inner='<rect x="10" y="10" width="760" height="265" rx="15" fill="#f3f7ee" stroke="#087f5b" stroke-width="2"/>'
 inner+=text(390,48,'영속성 컨텍스트 · 관리 중인 상품',25,'#087f5b')
 inner+=box(30,78,325,115,'조회 당시 상태','price = 30000')+box(425,78,325,115,'현재 Entity','price = 25000')+arrow(367,135,413,135)
 inner+=text(390,239,'두 상태의 차이 → 변경 감지',24,'#087f5b')
 inner+=box(840,78,295,115,'DB 상품 행','아직 price = 30000')
 return svg('관리 중인 상품의 조회 당시 가격 30000과 현재 가격 25000을 비교해 변경을 감지합니다',inner,300,'dirty-check')
def flush_commit():
 return svg('flush는 UPDATE를 DB에 전달하고 commit은 그 트랜잭션의 변경을 확정합니다',box(10,60,310,125,'객체 변경','Java price = 25000')+box(420,60,310,125,'flush · SQL 동기화','DB 25000 · 미확정')+box(830,60,308,125,'commit · 변경 확정','DB 25000 · 확정')+arrow(333,122,407,122,'UPDATE')+arrow(743,122,817,122),260,'flush-commit')
def commit_rollback():
 inner=box(10,85,330,120,'flush 뒤 DB','25000원 · 미확정')
 inner+='<path d="M355,145 H420 V65 H570" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M420,145 V230 H570" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+=text(485,49,'정상 완료',22,'#087f5b')+text(485,214,'취소할 실패',22,'#9b4d25')
 inner+=box(585,10,550,110,'commit → 25000원 확정','같은 트랜잭션의 DB 변경 유지')
 inner+=box(585,175,550,110,'rollback → 30000원 유지','같은 트랜잭션의 DB 변경 취소','#fff1e7')
 return svg('flush 후에는 commit과 rollback 두 갈래가 있습니다. commit은 DB 25000 확정, rollback은 기존 30000 유지입니다',inner,310,'commit-rollback')
def exception_paths():
 inner=box(10,75,315,125,'Service에서 실패','예외 발생')
 inner+=box(560,10,575,110,'밖으로 예외 전달','프록시가 rollback 규칙 적용')+box(560,175,575,110,'안에서 잡고 정상 반환','취소 표시가 없다면 commit 가능','#fff1e7')
 inner+='<path d="M340,137 H440 V65 H545" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M440,137 V230 H545" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 return svg('예외가 밖으로 전달되는 경우와 내부에서 잡고 정상 반환하는 경우는 트랜잭션 처리에서 다릅니다',inner,310,'exception-paths')
def pk_fk():
 inner=box(10,15,395,90,'주문 표 · purchase_orders','id (PK) · label')+box(610,15,525,90,'주문 항목 표 · order_items','name · order_id (FK)')
 for y,label,fk in [(150,'A · 주문 1','노트 · order_id = A'),(205,'B · 주문 2','펜 · order_id = A'),(260,'C · 주문 3','다른 항목은 B·C 주문에 연결')]:
  inner+=text(35,y,label,24,anchor='start')+text(635,y,fk,24,anchor='start')
 inner+=arrow(598,142,420,142)+ '<path d="M598,198 H535 V150 H420" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 return svg('주문 표의 PK는 주문을 식별합니다. 항목 표의 FK order_id가 A인 노트와 펜은 주문 A를 가리킵니다',inner,300,'pk-fk')
def object_relation():
 inner=box(10,90,365,130,'주문 객체 A','이름: 주문 1 · items 목록')+box(710,10,425,110,'항목 객체','이름: 노트')+box(710,185,425,110,'항목 객체','이름: 펜')
 inner+='<path d="M390,155 H540 V65 H695" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M540,155 V240 H695" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 return svg('Java에서는 주문 객체가 items 목록으로 노트와 펜 항목 객체를 참조합니다',inner,320,'object-relation')
def lazy_timing():
 inner=box(10,25,510,115,'주문을 먼저 조회','주문 A · 이름은 이미 읽음')+box(625,25,510,115,'이름만 사용','추가 항목 SELECT 없음')+arrow(535,82,610,82)
 inner+=box(10,185,510,115,'아직 안 읽은 items 사용','항목 개수·이름 등이 필요')+box(625,185,510,115,'항목을 추가 조회','노트 · 펜 로딩')+arrow(535,242,610,242,'SELECT')
 return svg('지연 로딩은 주문 조회와 아직 읽지 않은 항목 목록 접근 시점을 나누며 필요할 때 항목 SELECT가 추가될 수 있습니다',inner,325,'lazy-timing')
def dto_boundary():
 inner='<rect x="10" y="15" width="745" height="240" rx="15" fill="#f3f7ee" stroke="#087f5b" stroke-width="2"/>'
 inner+=text(382,55,'Service · 조회 트랜잭션 안',26,'#087f5b')
 inner+=box(30,95,310,115,'필요한 관계까지 조회','주문 · 항목 이름 읽기')+box(410,95,325,115,'DTO에 값 복사','응답용 이름·개수')+arrow(353,152,397,152)
 inner+=box(845,95,290,115,'Controller','완성된 DTO 사용')+arrow(770,152,830,152)
 return svg('Service 트랜잭션 안에서 필요한 주문과 항목 값을 읽어 DTO로 만들고 Controller는 DTO를 사용합니다',inner,285,'dto-boundary')
def query_trips(fetch=False):
 inner=box(10,75,310,150,'애플리케이션','주문 3개 · 항목 6개 필요')+box(830,75,308,150,'DB','주문 표 · 항목 표')
 if fetch:
  inner+=arrow(340,130,810,130,'함께 조회 1회 · fetch join')
  inner+=text(575,215,'같은 3개 주문 · 같은 6개 항목',24,'#087f5b')
 else:
  for y,label in [(35,'① 주문 목록'),(105,'② 주문 A의 항목'),(175,'③ 주문 B의 항목'),(245,'④ 주문 C의 항목')]:
   inner+=arrow(340,y+20,810,y+20,label)
 return svg('fetch join은 주문과 항목을 1 SELECT로 함께 읽습니다' if fetch else '주문 목록 1 SELECT 뒤 A와 B와 C의 항목을 각각 읽으면 총 4 SELECT입니다',inner,310,'fetch-one' if fetch else 'n-plus-one')
def self_call():
 inner=box(10,20,315,110,'다른 빈','Service 기능 호출')+box(420,20,315,110,'프록시','외부 진입 때 설정 적용')+box(830,20,305,110,'실제 Service','바깥 메서드 실행')+arrow(338,75,407,75)+arrow(748,75,817,75)
 inner+='<path d="M985,140 V215 H830" fill="none" stroke="#9b4d25" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+=text(590,230,'자기 메서드 직접 호출 → 프록시를 다시 지나지 않음',24,'#9b4d25')
 return svg('같은 Service 안의 자기 호출은 프록시를 다시 통과하지 않아 안쪽 메서드의 새 트랜잭션 설정이 적용되지 않습니다',inner,280,'self-call')

add('2026.11.23 · 4시간','트랜잭션과 JPA',steps('16일 28쪽부터: DB 변경을 함께 확정·취소하는 방법','객체 변경과 SQL · 관계와 조회 시점 이해','개인 과제: 나만의 단축 URL 서비스를 JPA로 전환'),kind='cover',note='19일 완료를 가정하지 않습니다. 독립 실행 예제 대신 개념·그림으로 설명하고 개인 프로젝트에 적용합니다.')
add('학습 순서','오늘 다룰 내용',linear('DB 작업을 함께 묶는 이유에서 시작해 객체 관리와 관계 조회를 거쳐 개인 서비스에 적용합니다',[('왜 묶을까?','트랜잭션 · Service'),('언제 바뀔까?','객체 · SQL · DB'),('언제 읽을까?','관계 · 지연 로딩')])+call('책 CH 11의 JDBC 상품 관리를 참고합니다. JPA는 수업 자료로 보충합니다.'))
add('이전 내용 연결','객체의 가격과 DB 가격은 별개',object_db()+call('Entity는 DB와 매핑되는 객체입니다. Java 메모리와 DB는 서로 다른 곳입니다.<br>객체만 바꿔서는 끝나지 않고, DB 변경에는 SQL 실행이 필요합니다.'))
add('트랜잭션이 필요한 이유','가격 변경만 저장되고 이력이 실패한다면?',partial_success(),note='이력은 부분 성공을 설명하는 상황입니다. 모든 기본 과제에 이력 기능을 새로 요구하지 않습니다.')
add('트랜잭션 기본','DB 작업을 하나의 성공·실패 단위로 묶기',table([['용어','뜻'],['트랜잭션','함께 성공해야 할 DB 작업을 하나의 처리 단위로 묶음'],['commit · 확정','해당 트랜잭션의 DB 변경을 확정'],['rollback · 취소','해당 트랜잭션의 DB 변경을 취소']])+call('가격 변경과 이력 저장을 같은 트랜잭션에 묶습니다.<br>정상 완료하면 함께 확정하고, 취소할 실패가 나면 함께 되돌립니다.'),note='하나의 관계형 DB와 트랜잭션 관리자를 사용하는 기본 상황입니다. 모든 예외의 rollback 여부는 뒤에서 구분합니다.')
add('Service의 역할','함께 성공해야 할 범위를 Service에서 정하기',service_boundary()+call('Service는 하나의 기능을 진행합니다. @Transactional로 그 DB 작업 범위를 정합니다.<br>같은 기능의 Repository 호출을 각각 따로 확정하지 않도록 묶습니다.'))
add('Spring이 적용하는 방법','프록시가 Service 호출 앞뒤를 처리합니다',call('빈은 Spring이 만들고 관리하는 객체입니다.<br>프록시는 실제 Service 대신 호출을 받아 공통 처리를 하는 대리 객체입니다.')+proxy_return(),note='기본 프록시 방식에서 다른 빈이 public Service 메서드를 호출하는 상황입니다. 트랜잭션을 시작하거나 기존 트랜잭션에 참여합니다. 최종 commit 과정에서도 실패할 수 있습니다.')
add('JPA가 관리하는 객체','관리 중인 상품의 변경을 감지하기',call('영속성 컨텍스트는 JPA가 Entity를 관리하는 공간입니다.<br>일반 쓰기 트랜잭션에서 조회한 관리 Entity의 변경을 추적합니다.')+dirty_check(),note='일반적인 스냅샷 기반 설명입니다. new만 한 객체나 분리 객체에는 같은 변경 감지를 적용하지 않습니다. 두 번 find한 동일성 등 전 시간 설명은 필요할 때 복습합니다.')
add('변경이 반영되는 순서','flush는 SQL 전달, commit은 변경 확정',flush_commit()+call('flush는 객체 변경을 SQL로 DB에 동기화합니다.<br>관리 Entity는 별도 save 없이 변경을 반영할 수 있지만, flush만으로 확정되지는 않습니다.'))
add('정상 완료와 실패','같은 UPDATE 뒤에도 두 결과가 가능합니다',commit_rollback()+call('rollback해도 이미 바뀐 Java 가격 25000은 자동 복원되지 않습니다.<br>실패한 객체를 그대로 믿지 말고 새 트랜잭션에서 DB를 다시 조회합니다.'),note='commit과 rollback은 서로 다른 두 경우입니다. 이미 commit한 변경을 나중에 같은 트랜잭션의 rollback으로 취소할 수 없습니다. DB 값은 현재 트랜잭션 기준이며 다른 트랜잭션의 관찰은 격리 수준에 달립니다.')
add('SQL과 확정 구분','save 직후 INSERT가 보여도 commit은 별개',table([['상황','이해할 내용'],['새 상품 저장','INSERT를 실행해도 트랜잭션 확정 여부는 별도'],['IDENTITY · DB가 ID 생성','생성된 ID를 얻기 위해 INSERT가 일찍 실행될 수 있음'],['그 뒤 rollback','아직 확정 전이라면 해당 DB 변경을 취소 가능']])+call('SQL 로그가 보였다는 사실과 저장 확정은 다릅니다.<br>모든 SQL이 반드시 commit 직전에만 실행되는 것도 아닙니다.'))
add('실패를 처리하는 기준','어떤 예외에서 rollback할까?',table([['예외 종류·정책','뜻과 기본 처리'],['RuntimeException','처리·선언을 강제하지 않는 예외 · IllegalArgumentException 등'],['Error','실행을 계속하기 어려운 심각한 오류'],['위 두 종류가 밖으로 전파','Spring 기본 rollback 대상'],['checked exception','컴파일러가 처리·선언을 요구 · IOException 등'],['checked exception 기본 정책','자동 rollback 대상 아님 · 필요 시 rollbackFor 지정']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('예외가 났다는 사실만으로 모두 같은 결과가 되지는 않습니다.<br>프로젝트의 실제 rollback 정책을 확인합니다.'),note='org.springframework.transaction.annotation.Transactional을 사용합니다. 전역 정책으로 기본 규칙을 변경할 수 있으며 checked exception이면 언제나 commit된다고 단정하지 않습니다.')
add('예외 전달','실패를 밖으로 전달하는지 확인하기',exception_paths()+call('실패를 숨기고 정상 반환하면 예상과 다르게 저장될 수 있습니다.<br>예외 처리와 rollback 정책을 함께 정합니다.'),note='그림의 내부 catch 경로는 다른 rollback-only 표시가 없는 상황입니다. 이미 취소 표시된 트랜잭션은 정상 반환해도 취소됩니다. 상세 조건은 뒤 보충으로 구분합니다.')
add('읽기와 쓰기','조회인지 변경인지 실제 동작으로 판단하기',table([['기능','트랜잭션 판단'],['목록·상세를 읽기만 함','readOnly = true로 조회 의도 전달 가능'],['링크 생성·수정·삭제','쓰기 트랜잭션'],['이동하면서 클릭 수 증가','DB 변경이 있으므로 쓰기 작업']])+call('readOnly는 최적화 힌트이며 쓰기 차단 보안 장치가 아닙니다.<br>HTTP GET이라는 이름보다 Service에서 실제로 하는 일을 봅니다.'))
add('이해 확인','객체 변경·SQL 실행·확정을 구분해 볼까?',table([['상황','확인할 질문'],['객체의 가격만 25000으로 변경','관리 Entity인가? new만 한 객체인가?'],['UPDATE 로그가 출력됨','flush만 된 것인가? commit도 끝났는가?'],['DB 값은 30000으로 남음','rollback 여부와 새 트랜잭션의 조회 결과를 확인했는가?']])+call('관리 Entity · 트랜잭션 경계 · commit 여부로 이유를 설명합니다.<br>JPA를 사용해도 실제 SQL·인덱스·DB 동작을 이해해야 합니다.'))
add('관계 조회로 연결','주문을 볼 때 어떤 데이터까지 필요할까?',linear('한 상품의 변경에서 관계를 가진 주문과 항목의 조회로 범위를 넓힙니다',[('지금까지','상품 한 개 변경'),('이제부터','주문과 여러 항목'),('같은 질문','무엇을 언제 DB에서 읽나?')])+call('주문 하나에 항목이 여러 개 연결됩니다.<br>필요한 데이터를 트랜잭션 안에서 어디까지 읽을지 확인합니다.'))
add('DB 관계','PK와 FK로 어느 주문의 항목인지 연결',pk_fk()+call('PK는 한 행을 식별합니다. FK는 연결된 다른 표의 행을 가리킵니다.<br>A·B·C는 설명용 별명입니다. 실제 생성 ID를 1부터라고 가정하지 않습니다.'))
add('객체 관계','Java에서는 주문이 항목 목록을 가집니다',object_relation()+call('DB는 FK 값으로 연결하고, Java는 객체 참조와 목록으로 연결합니다.<br>JPA 매핑은 이 두 관계를 어떻게 대응할지 정하는 정보입니다.'))
add('지연 로딩 · LAZY','항목이 필요해질 때 추가 조회할 수 있음',lazy_timing()+call('LAZY는 관련 데이터를 실제로 필요로 할 때 읽는 방식입니다.<br>이미 읽은 값과 아직 읽지 않은 관계를 구분합니다.'),note='DB 접근이 가능한 영속성 컨텍스트를 전제로 합니다. 캐시·배치 페치·초기화 상태에 따라 실제 SQL은 달라집니다. 연관관계 애너테이션·cascade 코드 나열은 하지 않습니다.')
add('트랜잭션과 응답','필요한 값을 Service에서 읽고 DTO로 전달',dto_boundary()+call('DTO는 응답에 필요한 값을 담는 객체입니다.<br>관계가 아직 로딩되지 않았다면 열려 있는 컨텍스트가 없을 때 접근이 실패할 수 있습니다.'),note='open-in-view=false 기준입니다. 미초기화 관계에 접근하면 LazyInitializationException이 날 수 있습니다. 이미 초기화된 관계는 다릅니다. DTO 생성만으로 N+1이 저절로 해결되지는 않습니다.')
add('N+1이 생기는 과정','주문 목록 1회 뒤 항목 조회가 반복됨',query_trips()+call('3개 주문을 읽고 각 항목에 접근하면 1 + 3 = 4 SELECT가 될 수 있습니다.<br>N+1은 목록 조회 뒤 관련 데이터 조회가 반복되는 문제입니다.'))
add('필요한 관계 함께 조회','fetch join으로 주문과 항목을 함께 읽기',query_trips(True)+call('fetch join은 필요한 관련 객체·컬렉션도 함께 로딩하도록 요청합니다.<br>이 조건에서는 같은 주문과 항목을 1 SELECT로 읽을 수 있습니다.'))
add('개선 결과 확인','SQL을 줄여도 같은 데이터여야 합니다',table([['비교할 내용','기본 조회','fetch join'],['주문 수','3개 주문','같은 3개 주문'],['항목 이름·개수','노트·펜 · 전체 6개','같은 이름·같은 6개'],['관계 접근까지 SELECT','4 SELECT','1 SELECT']])+call('캐시·배치 페치 없이 관계가 아직 로딩되지 않은 같은 조건의 비교입니다.<br>EAGER로 바꾸기만 하면 해결된다고 생각하지 않습니다.'),note='일반 SQL JOIN은 표의 결과를 결합하고, JPQL fetch join은 연관 객체 초기화까지 요청합니다. 누락·중복과 결과 내용을 함께 확인합니다.')
add('핵심 정리','객체·트랜잭션·관계 조회를 연결하기',steps('관리 Entity의 변경은 flush에서 SQL로 반영','commit은 확정 · rollback은 해당 DB 변경 취소','LAZY 관계는 실제 접근할 때 조회가 추가될 수 있음','필요한 관계를 읽고 DTO로 응답 · SQL 수와 결과 함께 확인')+call('이제 같은 원리를 본인이 만든 단축 URL 서비스에 적용합니다.'))
section('과제','나만의 단축 URL 서비스를 JPA로 전환','')
add('과제 목표','서비스 기능을 유지하고 저장 방식을 교체',steps('본인이 만들었던 단축 URL 프로젝트에서 이어서 개발','메모리·직접 JDBC 등의 저장 코드를 JPA 저장소로 교체','기존 URL 생성·리다이렉트와 프론트/API 계약 유지','이미 구현한 통계·관리 등 부가 기능도 동작 유지')+call('새 서비스를 처음부터 다시 만드는 과제가 아닙니다.<br>없던 수정·삭제·통계 기능을 모두 추가할 필요는 없습니다.'))
add('필수 요구사항 · Entity와 저장소','단축 코드의 고유성을 DB에서도 보장',table([['대상','구현할 내용'],['Entity','@Entity · @Id · 생성 전략 · 기본 생성자'],['저장할 값','원본 URL · 단축 코드 · 본인이 이미 쓰던 필요한 값'],['단축 코드','애플리케이션 중복 확인 + DB UNIQUE 제약'],['Repository','Spring Data JPA 사용 · 기존 인터페이스는 어댑터로 유지 가능'],['DTO','요청·응답 계약과 Entity 저장 모델의 역할 구분']])+call('기존 DB에도 실제 UNIQUE 제약이 적용됐는지 확인합니다.<br>애너테이션만 추가했다고 기존 스키마가 반드시 바뀌는 것은 아닙니다.'))
add('필수 요구사항 · Service','어디까지 함께 성공해야 하는지 정하기',table([['기능','트랜잭션 판단'],['생성·기존 수정·삭제 기능','쓰기 트랜잭션 경계에서 처리'],['목록·상세 등 순수 조회','readOnly = true 적용 여부와 이유 설명'],['리다이렉트 + 클릭 수 증가','DB 수정이 있으므로 쓰기 작업으로 판단'],['이력이 이미 있는 복합 기능','관련 DB 변경을 같은 트랜잭션으로 묶기']])+call('URL 이동에 필요한 응답과 DB 변경은 역할을 구분합니다.<br>쓰기 여부는 HTTP 메서드 이름보다 실제 DB 변경 유무로 판단합니다.'))
add('필수 요구사항 · 데이터 보존','재시작 후에도 기존 단축 주소 사용',table([['설정·작업','기준'],['DB','파일 기반 H2 또는 서버 DB 사용'],['테이블','명시적 DDL·마이그레이션 등으로 준비 · 설정 선택 이유 기록'],['금지할 설정','보존용 DB에 mem DB·create·create-drop 사용'],['기존 데이터','복사·내보내기 등 보존 방법을 정하고 무단 삭제하지 않기'],['Git 제외','DB 파일·비밀번호·.env · build/ · .gradle/']])+call('생성한 실제 단축 코드로 재시작 뒤 다시 조회·이동해 봅니다.<br>기존 데이터가 없다면 새로 만든 데이터의 재시작 보존을 확인합니다.'))
add('필수 요구사항 · DB 설정','데이터 보존에 맞는 설정을 고르기',table([['확인할 설정','선택과 이유'],['접속 주소','파일·서버 DB 사용 · 기존 주소를 임의로 바꾸지 않기'],['테이블 변경','기존 데이터 백업 · 실제 열과 UNIQUE 제약 확인'],['학습용 자동 변경','ddl-auto=update를 선택해도 안전한 이관을 보장하지 않음'],['조회 범위','open-in-view=false 기준으로 Service에서 필요한 데이터 읽기']])+call('메모리 DB와 create·create-drop은 보존 확인에 사용하지 않습니다.<br>DB가 달라지면 기존 데이터가 자동으로 옮겨지는 것은 아닙니다.'))
add('필수 요구사항 · 실패 관찰','정상 commit과 실패 rollback 비교',steps('정상 생성·변경 후 별도 요청으로 저장 결과 확인','로컬 임시 실패 경로에서 DB 변경 → flush → RuntimeException 전파','요청 종료 뒤 새 트랜잭션으로 조회해 해당 DB 변경 취소 확인','기존 원본값·행 수와 비교하고 임시 실패 코드는 제거')+call('같은 관리 객체 값만 보거나, 항상 rollback되는 테스트만으로 commit을 단정하지 않습니다.<br>실패 실험 방법·기대 결과·실제 DB 결과를 README에 남깁니다.'),note='flush는 SQL 실행을 관찰하기 위한 것이며 commit이 아닙니다. 실패 전에 새 요청으로 초기 상태를 확정합니다. 새 테스트 작성 대신 임시 로컬 실험으로 확인해도 됩니다. 위험한 실패용 공개 엔드포인트는 제출 결과에 남기지 않습니다.')
add('필수 요구사항 · QA','본인 서비스의 QA 체크리스트 작성',steps('본인 기능별 정상·실패·경계 조건을 직접 정하기','각 항목에 입력·예상 응답·예상 DB 상태를 적기','실행 후 실제 응답·DB 값·통과 여부 기록','기존 기능·고유 코드·유효성 검사·없는 코드·재시작·rollback 포함')+call('유효하지 않은 입력과 없는 코드의 응답 정책은 기존 계약을 유지합니다.<br>체크리스트 내용은 본인이 작성합니다. 테스트 코드 작성은 필수가 아닙니다.'))
add('추가 과제 · 선택','완료한 사람은 1 → 2 → 3단계로 확장',table([['단계','추가 개발'],['1 · 조회','내 링크를 키워드로 검색하고 생성일·조회 수 정렬과 페이지 조회 추가'],['2 · 변경과 이력','원본 URL 변경 + 변경 이력 저장을 한 트랜잭션으로 처리'],['3 · 동시 요청','같은 단축 코드 생성 경쟁에서 UNIQUE 충돌 처리·재시도 정책 구현']])+call('각 단계는 기본 전환과 QA를 끝낸 뒤 선택합니다.<br>클릭 수 동시 증가를 확장하면 단순 읽기 후 +1의 갱신 손실도 함께 확인합니다.'),note='경쟁 시 재시도를 같은 rollback-only 트랜잭션에서 무조건 반복하지 않도록 경계를 설계합니다. 낙관적 잠금·원자적 UPDATE 등은 선택 조사입니다. 모든 기능을 필수로 강제하지 않습니다.')
add('AI 사용','기존 프론트를 연결하고 변경 코드를 설명',steps('백엔드는 직접 설계·구현하되 AI 도움을 받아도 됨','AI가 제안한 Entity·쿼리·트랜잭션 경계는 본인이 설명','프론트는 기존 화면 유지 또는 AI로 보완 · 프롬프트는 자율','프론트는 순수 HTML·CSS·JavaScript · 외부 라이브러리 CDN 사용 금지')+call('새 프론트 구현보다 기존 API와 화면이 계속 동작하는지 먼저 확인합니다.'))
add('GitHub 제출','기존 fork에서 개발하고 공용 저장소로 PR',table([['항목','지정 값·방법'],['저장소','sesac-ddm-4-web/sesac-spring-boot-study의 본인 fork'],['폴더·브랜치','본인 기존 프로젝트 폴더 유지 · 브랜치 이름 자율'],['공용 저장소 Issue','[과제] 이름 / 단축 URL JPA 전환'],['공용 저장소 PR','[이름] 단축 URL 서비스 JPA 전환 · base: 공용 원본 main'],['PR에 포함','연결한 Issue URL · 전환 내용 · QA·rollback·재시작 확인 근거']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('본인 fork에 push → 공용 원본으로 PR을 올립니다. 직접 병합하지 않습니다.<br>기존 fork·열린 PR이 있으면 이어가되 이번 전환 변경을 구분해 적습니다.'),note='공용 Issue를 연결할 때 URL을 명시합니다. 다른 저장소의 같은 번호 Issue가 자동 종료된다고 가정하지 않습니다. 다른 교육생 폴더를 수정하지 않습니다.')
add('완료 기준','전환 전후의 차이를 설명하고 제출',steps('기존 생성·이동과 본인이 구현한 부가 기능 유지','파일·서버 DB에서 재시작 후 데이터 보존','Service 경계·정상 commit·실패 rollback을 근거로 설명','README·직접 작성한 QA 체크리스트·PR 제출')+call('<a href="SHORT-URL-JPA-ASSIGNMENT.md">과제 정리 ↗</a><br>gradle-wrapper.jar는 포함하고 DB 파일·계정 정보는 올리지 않습니다.'))
add('보충 · 자기 호출','같은 객체 안의 호출은 프록시를 다시 지나지 않음',self_call()+call('안쪽 메서드의 @Transactional 설정이 새로 적용되지 않습니다.<br>이미 바깥 트랜잭션이 있다면 그 범위는 계속 유효할 수 있습니다.'),note='기본 프록시 방식의 설명입니다. 외부에서 호출하는 Service 기능에 경계를 두거나 별도 Service 빈으로 분리합니다. private 메서드에 애너테이션을 옮기는 것으로 해결하지 않습니다.')
add('보충 · 기본 전파 REQUIRED','기존 트랜잭션이 있으면 함께 참여',linear('기본 REQUIRED는 기존 트랜잭션에 참여하고 최종 확정은 바깥 경계에서 처리합니다',[('바깥 Service','트랜잭션 시작'),('안쪽 Service','같은 트랜잭션 참여'),('바깥 경계 종료','최종 commit·rollback')])+call('안쪽 메서드 종료가 독립적인 commit은 아닙니다.<br>바깥 readOnly 범위가 안쪽 애너테이션만으로 쓰기 범위가 되지는 않습니다.'))
add('보충 · 예외를 잡았는데 취소되는 경우','이미 취소 표시된 트랜잭션은 정상 확정 불가',table([['상태','설명'],['rollback-only','이 트랜잭션은 취소해야 한다는 표시'],['안쪽 작업이 표시한 뒤 예외를 catch','예외를 잡아도 취소 표시가 사라지는 것은 아님'],['바깥에서 commit 시도','rollback되거나 UnexpectedRollbackException 등이 발생 가능']])+call('catch하면 무조건 commit, 예외가 나면 무조건 rollback으로 외우지 않습니다.'))
add('보충 · 트랜잭션이 해결하지 않는 것','동시 요청과 외부 처리는 별도 대책이 필요',table([['상황','추가로 생각할 것'],['같은 단축 코드가 동시에 생성','DB UNIQUE 제약 · 충돌 처리'],['두 요청이 조회 수를 읽고 각각 +1','갱신 손실 가능 · 원자적 UPDATE·잠금 등 검토'],['외부 API·이메일 처리 완료','DB rollback이 상대 서비스 처리를 자동 취소하지 않음']])+call('@Transactional이 모든 요청을 순서대로 실행하거나 모든 부수 효과를 되돌리지는 않습니다.'))
add('보충 · 관리 해제','clear는 DB 데이터를 삭제하지 않습니다',table([['동작','무엇을 하나?'],['flush','객체 변경을 SQL로 DB에 동기화'],['clear','영속성 컨텍스트의 관리 Entity들을 분리'],['DELETE','DB의 행 삭제 요청'],['clear 전 미반영 변경','반영되지 않을 수 있으므로 순서에 주의']])+call('객체 관리 해제 · DB 행 삭제 · 트랜잭션 취소는 서로 다른 동작입니다.'))
add('보충 · 면접에서 묻는 ACID','트랜잭션의 네 가지 특성',table([['특성','지금 배운 내용과 연결'],['원자성 · Atomicity','한 트랜잭션의 DB 작업을 함께 확정하거나 취소'],['일관성 · Consistency','정의된 제약과 규칙을 지키는 상태로 처리'],['격리성 · Isolation','동시 트랜잭션의 간섭·보이는 범위를 제어'],['지속성 · Durability','commit한 데이터를 DB의 보장에 따라 유지']])+call('임의의 업무 규칙 자동 검증·모든 요청 직렬 실행이라는 뜻은 아닙니다.<br>메모리 DB나 테이블 삭제 설정을 사용하면 재시작 보존을 기대할 수 없습니다.'))
add('보충 · Repository 구조','기존 저장소 인터페이스를 유지할 수 있음',linear('기존 Repository의 JPA 구현체가 Spring Data Repository에 저장·조회를 위임합니다',[('Service','기존 Repository 사용'),('직접 만든 JPA 어댑터','Domain ↔ Entity 변환'),('Spring Data Repository','실제 저장·조회 위임')])+call('임의로 만든 모든 Repository가 자동 구현되는 것은 아닙니다.<br>기존 설계에 맞춰 직접 사용 또는 어댑터 방식을 선택합니다.'))
add('보충 · save · persist · merge','save 반환값과 원본 객체를 구분하기',table([['작업','의미'],['Spring Data save','신규 판단에 따라 persist 또는 merge 사용'],['persist','새 Entity 자체를 관리'],['merge','상태를 관리 Entity에 복사하고 관리 Entity 반환'],['분리된 원본','전달한 원본 자체가 관리 상태가 되는 것은 아님']])+call('신규 판단은 버전·ID 등을 참고합니다. save 반환값을 사용합니다.'))
add('참고','공식 문서','<div class="references"><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html"><b>Spring @Transactional ↗</b><span>프록시와 적용 범위</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html"><b>Spring rollback ↗</b><span>예외와 취소 정책</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html"><b>트랜잭션 전파 ↗</b><span>기존 트랜잭션 참여</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html"><b>Spring Data JPA ↗</b><span>Entity 저장과 관리</span></a><a href="https://docs.hibernate.org/orm/current/userguide/html_single/"><b>Hibernate ORM ↗</b><span>매핑·관계·SQL</span></a><a href="../shared/db-basics/"><b>DB 기초 ↗</b><span>표·PK·FK·SQL</span></a></div>')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-23-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.23</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="트랜잭션과 JPA · 단축 URL 서비스 전환"><title>11월 23일 · 트랜잭션과 JPA · 단축 URL 서비스 전환</title><style>'+css+'</style></head><body data-deck-revision="2026-11-23-v4-visual-flow"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',out.count('data-source-key='),'reference buttons;',len(out.encode()),'bytes')
