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
def source_choices():
 return '<div class="references">'+''.join('<button type="button" data-source-key="'+esc(name)+'"><b>'+esc(name)+' ↗</b><span>작업 뒤 수업 참고 구현과 비교</span></button>' for name in SOURCES)+'</div>'
add('2026.11.23 · 4시간','트랜잭션과 JPA',steps('16일 28쪽부터: @Transactional과 DB 변경 확정','남은 JPA: 객체 변경 · 관계 · 지연 로딩 · N+1','개인 과제: 나만의 단축 URL 서비스를 JPA로 전환'),kind='cover',note='16일 28쪽 이후를 이미 배웠다고 가정하지 않습니다. 설명 뒤 개인 서비스 전환을 시작하고, 미완료는 과제로 이어갑니다.')
add('진행','오늘 다룰 내용',linear('트랜잭션을 이해하고 JPA 조회 동작을 본 뒤 개인 단축 URL에 적용합니다',[('트랜잭션','시작 · commit · rollback'),('JPA 조회','관계 · LAZY · N+1'),('개인 서비스','JPA 저장소로 교체')])+call('책 CH 11의 JDBC 상품 관리를 참고합니다. JPA·트랜잭션·관계는 수업 보충 내용입니다.'),note='교재에 없는 JPA 장이나 쪽수를 지정하지 않습니다. 19일 실습 완료 여부를 오늘의 출발 조건으로 삼지 않습니다.')
add('앞 내용 연결','객체의 가격과 DB 가격은 별개',table([['현재 상황','Java 객체','DB의 상품 행'],['조회 직후','키보드 · 30000원','키보드 · 30000원'],['changePrice(25000) 직후','25000원','아직 SQL 반영 전이면 30000원'],['관리 중인 Entity','변경 감지 대상','UPDATE가 실행되어야 값 변경']])+call('new만 한 객체·관리에서 분리된 객체와 구분합니다.<br>이제 조회·변경을 묶는 트랜잭션부터 이어갑니다.'))
add('트랜잭션 기본','왜 Service에 @Transactional을 붙일까?',table([['작업','같은 범위로 묶는 이유'],['상품 조회 → 가격 변경','관리 Entity를 조회하고 수정하는 작업을 한 범위에서 처리'],['commit · 변경 확정','정상적으로 완료한 DB 변경을 확정'],['rollback · 변경 취소','실패한 트랜잭션의 DB 변경을 취소']])+call('Service의 한 기능을 성공·실패 단위로 묶습니다.<br>아래 예제는 하나의 관계형 DB와 트랜잭션 관리자를 사용하는 경우입니다.'),note='16일 28쪽의 기본 설명을 여기서 다시 시작합니다. Spring 기본 rollback 규칙은 뒤에서 코드와 함께 다룹니다.')
add('여러 DB 작업','가격 변경만 저장되고 이력이 실패한다면?',table([['기능: 가격 변경과 이력 저장','트랜잭션을 함께 묶지 못한 경우'],['UPDATE products …','가격은 25000원으로 먼저 확정'],['INSERT price_history …','오류가 발생해 이력은 저장되지 않음'],['원하는 결과','두 작업이 함께 성공하거나, 해당 DB 변경을 함께 취소']])+call('각 SQL이 따로 확정되면 기능 전체의 일부만 성공할 수 있습니다.<br>같은 트랜잭션에 묶고 실패를 전달해야 함께 rollback할 수 있습니다.'),note='price_history는 원자성을 설명하기 위한 가상 이력 테이블입니다. 모든 단축 URL 과제에 새 이력 기능을 필수로 추가한다는 뜻은 아닙니다.')
add('트랜잭션 범위','Repository 호출을 Service 기능으로 묶기',linear('하나의 Service 트랜잭션에 조회, 가격 변경, 이력 저장을 포함합니다',[('Service 진입','트랜잭션 시작·참여'),('업무 처리','조회 → 변경 → 이력 저장'),('Service 처리 뒤','commit 또는 rollback')])+call('Repository 메서드마다 별개로 끝내지 않고, 함께 성공해야 할 작업의 경계를 정합니다.'),note='기본 REQUIRED 전파와 동일 트랜잭션 관리자 사용을 전제로 합니다. 기존 트랜잭션에 참여한 경우 최종 종료는 바깥 경계에서 일어납니다.')
add('Spring 동작','애너테이션을 읽고 트랜잭션을 적용하는 곳',linear('외부 호출이 Spring 프록시를 통해 실제 Service로 전달됩니다',[('다른 빈의 호출','Controller 등'),('Spring 프록시','트랜잭션 시작·참여'),('실제 Service','조회 · 변경')])+table([['처리 결과','프록시·트랜잭션 관리자의 처리'],['정상 반환','자신이 시작한 트랜잭션이면 flush·commit 시도'],['예외 전파','rollback 규칙에 따라 rollback 또는 commit 결정']]),note='기본 프록시 방식의 public Service 메서드 예입니다. 프록시는 실제 빈의 앞에서 공통 처리를 수행하는 대리 객체입니다. commit 과정 자체에서도 실패할 수 있습니다.')
add('정상 처리 · Service 메서드 발췌','관리 중인 상품은 save 없이 수정 가능',code("""// Service 발췌 · repository 주입과 클래스 선언 생략
import org.springframework.transaction.annotation.Transactional;

@Transactional
public void changePrice(Long id, int price) {
    ProductEntity product = repository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("상품 없음"));
    product.changePrice(price);
}
""")+call('외부 호출로 쓰기 트랜잭션이 적용되고, 조회한 Entity가 관리 상태인 예입니다.<br>변경 감지 → flush 때 UPDATE → 트랜잭션 commit으로 확정합니다.'),kind='code-slide',note='org.springframework.transaction.annotation.Transactional을 사용합니다. 조회 결과가 없는 경우의 HTTP 404 변환은 ControllerAdvice 등의 별도 처리입니다.')
add('실패 처리 · Service 메서드 발췌','UPDATE 뒤 예외가 나도 rollback 가능',code("""// 주입된 repository·entityManager 사용 · 학습용 실패 코드
@Transactional
public void changeThenFail(Long id) {
    ProductEntity product = repository.findById(id).orElseThrow();
    product.changePrice(25000);
    entityManager.flush(); // UPDATE 실행, 아직 commit 아님
    throw new IllegalStateException("실패 실험");
}
""")+call('외부 호출로 시작한 트랜잭션 밖으로 RuntimeException이 전파됩니다.<br>UPDATE 로그가 보여도 DB 가격 변경은 rollback됩니다.'),kind='code-slide',note='초기 가격 30000인 기존 상품을 사용합니다. 임시 실패 코드는 로컬 학습용이며 최종 서비스에서 제거합니다. 실제 commit 이전, 정상 트랜잭션 관리가 적용된 상황입니다.')
add('객체와 DB 비교','rollback은 Java 필드값을 복구하지 않음',table([['단계','Java price','DB · 현재 트랜잭션 기준'],['조회','30000','30000'],['객체 수정','25000','30000 · UPDATE 전'],['flush','25000','25000 · 미확정'],['commit하는 경우','25000','25000 · 확정'],['대신 rollback하는 경우','25000 · 자동 복원 안 됨','30000 · 변경 취소']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('commit과 rollback은 서로 다른 경우입니다.<br>실패한 작업의 객체를 계속 신뢰하지 말고 새 트랜잭션에서 다시 조회합니다.'),note='다른 트랜잭션에서 관찰하는 값은 격리 수준에 따라 다릅니다. 이미 commit한 DB 변경을 같은 트랜잭션의 rollback으로 취소할 수는 없습니다.')
add('세 동작 구분','flush · clear · commit을 나누어 보기',table([['동작','무엇이 바뀌나?','같지 않은 것'],['flush','객체 변경을 SQL로 DB에 동기화','commit · 최종 확정'],['clear','관리 중인 Entity들을 분리','DELETE · DB 행 삭제'],['commit','DB 트랜잭션 변경 확정','객체의 필드만 수정']])+call('clear 전에 flush하지 않은 변경은 반영되지 않을 수 있습니다.<br>관리 해제와 DB 변경 취소를 같은 동작으로 생각하지 않습니다.'))
add('INSERT 실행 시점','save 직후 INSERT가 보여도 commit은 별개',table([['상황','설명'],['새 Entity 저장','JPA가 Entity를 관리하고 INSERT 수행을 준비'],['IDENTITY 식별자','DB에서 생성한 id를 얻으려고 INSERT를 일찍 실행할 수 있음'],['그 뒤 예외와 rollback','아직 commit 전인 트랜잭션의 DB 변경은 취소 가능'],['조회 전에 flush','필요한 경우 쿼리 전에 변경 SQL이 실행될 수도 있음']])+call('save = INSERT = commit으로 외우지 않습니다.<br>모든 SQL이 반드시 commit 직전에만 실행되는 것도 아닙니다.'))
add('기본 rollback 규칙','어떤 예외에서 rollback할까?',table([['Spring 기본 설정','처리'],['RuntimeException · Error 전파','rollback 대상'],['checked exception 전파','기본적으로 rollback하지 않음'],['checked exception도 취소해야 한다면','rollbackFor로 필요한 예외 타입 지정']])+code("""// 예: IOException도 rollback 대상으로 정하는 메서드 선언
@Transactional(rollbackFor = IOException.class)
public void importLinks() throws IOException {
    // DB 작업과 파일 읽기 등 실제 구현은 생략
}
"""),kind='code-slide',note='프로젝트의 전역 rollback 정책이나 버전에 따른 설정으로 기본값을 바꿀 수 있습니다. checked exception이 발생하면 언제나 무조건 commit된다는 뜻은 아닙니다.')
add('예외 처리','예외를 잡고 정상 반환하면?',code("""// 조회한 관리 Entity가 있고, 쓰기 트랜잭션이 적용된 메서드 내부
try {
    product.changePrice(25000);
    throw new IllegalStateException("업무 검증 실패");
} catch (IllegalStateException ex) {
    return; // 프록시에는 정상 반환으로 보일 수 있음
}
""")+call('이처럼 내부에서 만든 예외를 삼키면 변경이 commit될 수 있습니다.<br>단, 이미 rollback-only라면 정상 반환해도 종료 시 rollback·예외가 날 수 있습니다.'),kind='code-slide',note='저장소가 이미 트랜잭션을 rollback-only로 표시한 상황과 구분합니다. 오류 HTTP 응답을 반환하는 것만으로 rollback되는 것은 아닙니다. 실패 정책을 정하고 예외를 적절히 전파합니다.')
add('프록시와 자기 호출','같은 객체 안에서 호출하면 새 설정이 적용 안 됨',code("""// 같은 Service 안의 메서드 발췌
public void create() {
    this.saveLink(); // Spring 프록시를 거치지 않음
}

@Transactional
public void saveLink() {
    // DB 저장
}
""")+call('기본 프록시 방식에서 saveLink의 @Transactional이 이 호출로 새로 적용되지 않습니다.<br>바깥에 이미 트랜잭션이 있다면 그 범위 안에서 실행될 수는 있습니다.'),kind='code-slide',note='자기 호출은 트랜잭션이 반드시 하나도 없다는 뜻이 아니라 호출 대상 애너테이션의 새 설정이 적용되지 않는다는 뜻입니다.')
add('경계 정하기','외부에서 호출하는 Service에 트랜잭션 적용',code("""// Controller 등 다른 빈이 LinkService.create()를 호출
@Transactional
public void create(CreateLinkRequest request) {
    // 조회 · 고유 코드 결정 · DB 저장을 한 기능으로 처리
    saveLink(request); // 같은 트랜잭션의 내부 작업
}

private void saveLink(CreateLinkRequest request) {
    // 실제 DB 저장 구현은 생략
}
""")+call('예시는 경계를 보여주는 발췌입니다. 실제 저장 코드는 직접 구현합니다.<br>별도 경계가 필요하면 다른 Service 빈으로 분리해 프록시를 거쳐 호출합니다.'),kind='code-slide',note='위 스니펫의 private 메서드의 실제 저장 본문은 구조 설명을 위해 생략했습니다. private 메서드에 애너테이션을 옮겨 해결한다고 가르치지 않습니다.')
add('읽기와 쓰기','readOnly는 쓰기 금지 보안 장치가 아님',table([['기능','설정 예와 판단'],['링크 목록·상세 조회','@Transactional(readOnly = true) · 조회 의도 전달'],['링크 생성·수정·삭제','@Transactional · DB 변경을 포함한 작업'],['이동하면서 클릭 수 증가','조회처럼 보여도 DB를 수정하므로 쓰기 작업'],['readOnly의 한계','최적화 힌트 · 모든 환경에서 쓰기 차단 보장은 아님']])+call('HTTP GET이라는 이유만으로 Service를 무조건 readOnly로 정하지 않습니다.<br>메서드 안에서 실제로 무엇을 하는지 확인합니다.'))
add('기본 전파 · REQUIRED','안쪽 메서드 종료가 최종 commit은 아님',linear('기본 REQUIRED에서는 안쪽 Service가 같은 트랜잭션에 참여할 수 있습니다',[('바깥 Service','트랜잭션 시작'),('안쪽 Service','같은 트랜잭션 참여'),('바깥 경계 종료','최종 commit·rollback')])+call('안쪽 메서드가 끝났다고 별도 저장 확정이 되는 것은 아닙니다.<br>안쪽에서 rollback-only로 표시되면 바깥 commit도 실패할 수 있습니다.'),note='동일 트랜잭션 관리자와 기본 REQUIRED 전파를 전제로 합니다. 기존 읽기 전용 트랜잭션에 참여하면 안쪽 애너테이션만으로 쓰기 범위로 바뀐다고 가정하지 않습니다. REQUIRES_NEW·격리 수준 심화는 필수가 아닙니다.')
add('동시 요청','트랜잭션만으로 동시 수정이 해결되지는 않음',table([['동시에 실행한 작업','별도로 필요한 대책'],['같은 단축 코드가 없는지 확인 후 저장','두 요청이 모두 통과할 수 있음 → DB UNIQUE 제약·충돌 처리'],['조회 수를 읽고 각각 +1','같은 값을 읽어 증가분이 사라질 수 있음 → 원자적 UPDATE·잠금 등 검토'],['@Transactional의 역할','기능의 DB 변경 범위 설정 · 모든 요청을 자동으로 순서대로 실행하지 않음']])+call('중복 확인과 저장 사이에도 다른 요청이 들어올 수 있습니다.<br>동시성 구현은 추가 과제이며, 기본 과제에서도 DB 고유 제약은 필요합니다.'))
add('트랜잭션의 범위','외부 HTTP 호출까지 되돌려 주지는 않음',table([['작업','DB rollback 시'],['같은 트랜잭션의 링크·이력 저장','해당 DB 변경을 취소 가능'],['이미 전송한 이메일','메일 전송을 자동 취소하지 않음'],['외부 API에 완료된 요청','상대 서비스의 처리를 자동 복구하지 않음'],['응답을 보내기 전 commit 실패','메서드 본문이 끝나도 성공을 단정할 수 없음']])+call('@Transactional은 모든 부수 효과를 되돌리는 기능이 아닙니다.<br>외부 호출을 새로 추가하는 것은 이번 필수 과제가 아닙니다.'))
add('이해 확인','다음 코드의 DB 결과를 예상해 보기',table([['독립된 상황','결과와 이유'],['쓰기 트랜잭션에서 조회·변경 후 정상 종료','관리 Entity 변경 감지 · 정상 commit하면 UPDATE 반영'],['new한 객체의 가격만 변경','저장·관리 등록 없으므로 DB 저장 안 됨'],['조회 → 변경 → flush → RuntimeException 전파','DB 변경 rollback · Java 값 자동 복원 안 됨'],['같은 컨텍스트에서 같은 id를 find 두 번','중간 clear·detach 없고 상품 존재 시 같은 객체 참조']]).replace('<table ', '<table style="font-size:20px" ')+call('답을 먼저 가리고, 관리 상태·트랜잭션 경계·commit 여부로 이유를 설명합니다.'))
add('상품에서 관계로','트랜잭션 안에서 무엇을 조회할까?',linear('상품 하나의 변경에서 여러 연관 객체 조회로 학습 범위를 확장합니다',[('지금까지','상품 한 개 · 가격 변경'),('다음 예제','주문 3개 · 항목 6개'),('확인할 문제','언제 조회? · SQL 몇 번?')])+call('주문 예제는 관계를 관찰하는 최소 예제입니다.<br>책의 전체 주문 관리 API를 새로 완성하라는 과제가 아닙니다.'))
add('DB 관계','주문 PK와 항목 FK 연결',table([['purchase_orders · 주문 3행','order_items · 항목 6행'],['A · 주문 1','노트 → order_id A / 펜 → order_id A'],['B · 주문 2','노트 → order_id B / 펜 → order_id B'],['C · 주문 3','노트 → order_id C / 펜 → order_id C']])+call('PK는 각 행을 식별하고, FK인 order_id는 어느 주문의 항목인지 연결합니다.<br>A·B·C는 설명용 별명입니다. 실제 생성 id를 1부터라고 가정하지 않습니다.'))
add('Entity 관계 · 참고 코드 발췌','주문 객체는 항목 목록을 가집니다',code("""// PurchaseOrder 클래스 내부 · import와 다른 필드 생략
@OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
@JoinColumn(name = "order_id")
private List<OrderItem> items = new ArrayList<>();

public List<OrderItem> getItems() {
    return items;
}
""")+call('이 최소 예제는 PurchaseOrder → OrderItem 단방향 관계입니다.<br>order_items.order_id가 주문을 연결하고, LAZY는 관련 항목을 필요할 때 읽는 방식입니다.'),kind='code-slide',note='shared/order_sources.py와 동일한 매핑입니다. cascade ALL은 여기서 함께 저장할 항목의 생명주기를 위한 설정이며 모든 실무 관계에 그대로 복사하는 규칙이 아닙니다.')
add('LAZY 동작','주문 조회와 항목 접근을 나누어 보기',linear('미초기화된 지연 컬렉션은 필요한 접근 시 추가 조회할 수 있습니다',[('주문 조회','주문 행 SELECT'),('label 읽기','이미 읽은 주문 값'),('items 사용','항목 SELECT 가능')])+call('DB 접근이 가능한 영속성 컨텍스트 안에서 관찰합니다.<br>디버거가 컬렉션을 자동으로 펼쳐도 조회가 발생할 수 있습니다.'))
add('접근 코드 · 관찰용 발췌','items를 실제로 읽는 줄을 찾기',code("""// 진행 중인 조회 트랜잭션 안의 코드 발췌
List<PurchaseOrder> orders = repository.findAllByOrderByIdAsc();
for (PurchaseOrder order : orders) {
    System.out.println(order.getLabel());
    System.out.println(order.getItems().size());
}
""")+call('주문 목록 조회 한 번 뒤, 각 주문의 미초기화 items에 접근합니다.<br>기본 학습 설정에서는 주문마다 항목 조회가 추가됩니다.'),kind='code-slide',note='배치 페치·캐시·이미 초기화된 관계에 따라 쿼리 수가 달라질 수 있습니다. 로그는 실제 접근 순서와 함께 읽습니다.')
add('트랜잭션과 지연 로딩','필요한 값을 읽고 DTO로 반환하기',table([['Service 안','Service 밖'],['트랜잭션 안에서 주문 조회','Controller는 응답 DTO를 사용'],['응답에 필요한 items 조회·초기화','미초기화 Entity 관계를 뒤늦게 탐색하지 않음'],['이름·개수 등을 DTO에 담기','조회 범위가 끝난 뒤에도 DTO 값 사용']])+call('열려 있는 컨텍스트가 없는 분리 상태에서 미초기화 관계에 접근하면<br>LazyInitializationException이 날 수 있습니다.'),note='이미 초기화된 관계는 같은 예외가 나지 않을 수 있습니다. Entity 직접 직렬화나 OSIV=true 전환으로 우회시키지 않습니다. DTO를 만들더라도 fetch 전략이 잘못되면 N+1이 날 수 있습니다.')
add('N+1 · 이 예제의 SQL','주문 3개에서 왜 4 SELECT일까?',table([['접근','SELECT 수'],['주문 목록 3개 조회','1회'],['주문 A의 items 사용','1회 추가'],['주문 B의 items 사용','1회 추가'],['주문 C의 items 사용','1회 추가'],['합계','1 + 3 = 4 SELECT']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('목록 1회 + 각 결과의 관련 데이터 조회 N회가 생기는 문제입니다.<br>LAZY 표시만 보고 단정하지 말고 실제 SQL을 확인합니다.'))
add('조회 개선 · Repository 발췌','필요한 항목을 fetch join으로 함께 읽기',code("""// OrderQueryRepository의 실제 참고 메서드
@Query("select distinct o from PurchaseOrder o "
        + "left join fetch o.items order by o.id")
List<PurchaseOrder> findAllWithItems();
""")+table([['표현','의미'],['SQL JOIN','연결된 표를 결합해 결과 행 조회'],['JPQL join fetch','관련 Entity·컬렉션을 함께 로딩하도록 요청'],['left join fetch','항목이 없는 주문도 포함할 수 있음']]),kind='code-slide',note='JPQL은 테이블명이 아닌 Entity와 속성명을 사용합니다. 일반 join만으로 연관관계 초기화가 보장되는 것은 아닙니다. 참고 구현과 동일 쿼리입니다.')
add('같은 결과 비교','SQL을 줄여도 결과 값은 같아야 함',table([['같은 준비 데이터','기본 조회','fetch join'],['주문 수','3개 주문','같은 3개 주문'],['주문별 항목','노트·펜 / 전체 6개','같은 이름·같은 6개'],['관련 데이터 접근까지 SELECT','4 SELECT','1 SELECT'],['확인할 것','실행 SQL과 결과 내용','누락·중복 없는지 함께 확인']]).replace('<table ', '<table style="font-size:20px" ')+call('준비 데이터 flush → EntityManager.clear → 통계 초기화 후 측정합니다.<br>이 조건의 비교입니다. EAGER로 바꾸는 것만으로 N+1이 해결되지는 않습니다.'),note='준비 SQL과 측정 SQL을 섞지 않습니다. prepareStatementCount는 모든 준비된 SQL문 수지만 이 측정 구간에는 SELECT만 있습니다. EAGER로 바꾸는 것만으로 N+1 해결이 보장되지 않습니다.')
add('선택 관찰','준비된 주문 예제에서 SQL 확인',table([['자료','사용 방법'],['<a href="assets/order-query-lab.zip">order-query-lab ZIP ↗</a>','별도 폴더에서 기존 테스트 실행 · 개선 참고 코드 포함'],['<a href="BEGINNER-WORKSHEET.md">관찰 작업지 ↗</a>','실행 조건·예상 SQL·실제 결과를 비교'],['<a href="../shared/db-basics/">DB 기초 ↗</a>','PK·FK·SQL JOIN 복습']])+code("""# order-query-lab 폴더 · Windows는 .\\gradlew.bat 사용
./gradlew test --tests '*OrderQueryTest' --info --rerun-tasks
""")+call('새 테스트 코드를 직접 작성하는 것은 필수가 아닙니다.<br>시간이 부족하면 참고로 남기고 개인 서비스 JPA 전환을 시작합니다.'),kind='code-slide',note='build/reports/tests/test/index.html의 해당 클래스 Standard output에서도 SQL을 확인합니다. 주문 랩의 별도 Issue·PR 제출은 필수가 아닙니다.')
add('수업 정리','객체 · SQL · 트랜잭션을 함께 설명',steps('쓰기 트랜잭션의 관리 Entity 변경 → flush 때 UPDATE','commit은 확정 · rollback은 DB 변경 취소 · clear는 관리 해제','관계 접근 시점을 확인하고 실제 SELECT 수 관찰','응답에 필요한 데이터를 조회한 뒤 DTO로 반환')+call('이제 같은 원리를 본인이 만든 단축 URL 서비스에 적용합니다.'))
section('과제','나만의 단축 URL 서비스를 JPA로 전환','')
add('과제 목표','서비스 기능을 유지하고 저장 방식을 교체',steps('본인이 만들었던 단축 URL 프로젝트에서 이어서 개발','메모리·직접 JDBC 등의 저장 코드를 JPA 저장소로 교체','기존 URL 생성·리다이렉트와 프론트/API 계약 유지','이미 구현한 통계·관리 등 부가 기능도 동작 유지')+call('새 서비스를 처음부터 다시 만드는 과제가 아닙니다.<br>없던 수정·삭제·통계 기능을 모두 추가할 필요는 없습니다.'))
add('필수 요구사항 · Entity와 저장소','단축 코드의 고유성을 DB에서도 보장',table([['대상','구현할 내용'],['Entity','@Entity · @Id · 생성 전략 · 기본 생성자'],['저장할 값','원본 URL · 단축 코드 · 본인이 이미 쓰던 필요한 값'],['단축 코드','애플리케이션 중복 확인 + DB UNIQUE 제약'],['Repository','Spring Data JPA 사용 · 기존 인터페이스는 어댑터로 유지 가능'],['DTO','요청·응답 계약과 Entity 저장 모델의 역할 구분']])+call('기존 DB에도 실제 UNIQUE 제약이 적용됐는지 확인합니다.<br>애너테이션만 추가했다고 기존 스키마가 반드시 바뀌는 것은 아닙니다.'))
add('필수 요구사항 · Service','어디까지 함께 성공해야 하는지 정하기',table([['기능','트랜잭션 판단'],['생성·기존 수정·삭제 기능','쓰기 트랜잭션 경계에서 처리'],['목록·상세 등 순수 조회','readOnly = true 적용 여부와 이유 설명'],['리다이렉트 + 클릭 수 증가','DB 수정이 있으므로 쓰기 작업으로 판단'],['이력이 이미 있는 복합 기능','관련 DB 변경을 같은 트랜잭션으로 묶기']])+call('URL 이동에 필요한 응답과 DB 변경은 역할을 구분합니다.<br>외부 사이트 요청·브라우저 이동까지 DB rollback이 취소해 주지는 않습니다.'))
add('필수 요구사항 · 데이터 보존','재시작 후에도 기존 단축 주소 사용',table([['설정·작업','기준'],['DB','파일 기반 H2 또는 서버 DB 사용'],['테이블','명시적 DDL·마이그레이션 등으로 준비 · 설정 선택 이유 기록'],['금지할 설정','보존용 DB에 mem DB·create·create-drop 사용'],['기존 데이터','복사·내보내기 등 보존 방법을 정하고 무단 삭제하지 않기'],['Git 제외','DB 파일·비밀번호·.env · build/ · .gradle/']])+call('생성한 실제 단축 코드로 재시작 뒤 다시 조회·이동해 봅니다.<br>기존 데이터가 없다면 새로 만든 데이터의 재시작 보존을 확인합니다.'))
add('파일 DB 설정 예 · 새 학습 DB','처음 파일 DB를 만들 때의 설정',code("""# 새 학습 DB 예시 · 기존 DB 접속 주소를 임의로 바꾸지 않기
spring.datasource.url=jdbc:h2:file:./data/short-url
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
spring.jpa.show-sql=true
""")+call('update는 학습용 자동 반영 예입니다. 운영 마이그레이션이나 기존 스키마 변경을 보장하지 않습니다.<br>기존 DB는 먼저 백업하고 실제 제약을 확인합니다. 같은 실행 폴더에서 재시작합니다.'),kind='code-slide',note='H2 드라이버와 Spring Data JPA 의존성이 필요합니다. 이미 서버 DB를 사용하는 프로젝트는 그대로 유지해도 됩니다. DB 파일을 Git에 올리지 않습니다. ddl-auto=update가 기존 데이터를 새 DB로 복사해 주지는 않습니다.')
add('필수 요구사항 · 실패 관찰','정상 commit과 실패 rollback 비교',steps('정상 생성·변경 후 별도 요청으로 저장 결과 확인','로컬 임시 실패 경로에서 DB 변경 → flush → RuntimeException 전파','요청 종료 뒤 새 트랜잭션으로 조회해 해당 DB 변경 취소 확인','기존 원본값·행 수와 비교하고 임시 실패 코드는 제거')+call('같은 관리 객체 값만 보거나, 항상 rollback되는 테스트만으로 commit을 단정하지 않습니다.<br>실패 실험 방법·기대 결과·실제 DB 결과를 README에 남깁니다.'),note='flush는 SQL 실행을 관찰하기 위한 것이며 commit이 아닙니다. 실패 전에 새 요청으로 초기 상태를 확정합니다. 새 테스트 작성 대신 임시 로컬 실험으로 확인해도 됩니다. 위험한 실패용 공개 엔드포인트는 제출 결과에 남기지 않습니다.')
add('필수 요구사항 · QA','본인 서비스의 QA 체크리스트 작성',steps('본인 기능별 정상·실패·경계 조건을 직접 정하기','각 항목에 입력·예상 응답·예상 DB 상태를 적기','실행 후 실제 응답·DB 값·통과 여부 기록','기존 기능·고유 코드·유효성 검사·없는 코드·재시작·rollback 포함')+call('유효하지 않은 입력과 없는 코드의 응답 정책은 기존 계약을 유지합니다.<br>체크리스트 내용은 본인이 작성합니다. 테스트 코드 작성은 필수가 아닙니다.'))
add('추가 과제 · 선택','완료한 사람은 1 → 2 → 3단계로 확장',table([['단계','추가 개발'],['1 · 조회','내 링크를 키워드로 검색하고 생성일·조회 수 정렬과 페이지 조회 추가'],['2 · 변경과 이력','원본 URL 변경 + 변경 이력 저장을 한 트랜잭션으로 처리'],['3 · 동시 요청','같은 단축 코드 생성 경쟁에서 UNIQUE 충돌 처리·재시도 정책 구현']])+call('각 단계는 기본 전환과 QA를 끝낸 뒤 선택합니다.<br>클릭 수 동시 증가를 확장하면 단순 읽기 후 +1의 갱신 손실도 함께 확인합니다.'),note='경쟁 시 재시도를 같은 rollback-only 트랜잭션에서 무조건 반복하지 않도록 경계를 설계합니다. 낙관적 잠금·원자적 UPDATE 등은 선택 조사입니다. 모든 기능을 필수로 강제하지 않습니다.')
add('AI 사용','기존 프론트를 연결하고 변경 코드를 설명',steps('백엔드는 직접 설계·구현하되 AI 도움을 받아도 됨','AI가 제안한 Entity·쿼리·트랜잭션 경계는 본인이 설명','프론트는 기존 화면 유지 또는 AI로 보완 · 프롬프트는 자율','프론트는 순수 HTML·CSS·JavaScript · 외부 라이브러리 CDN 사용 금지')+call('새 프론트 구현보다 기존 API와 화면이 계속 동작하는지 먼저 확인합니다.'))
add('GitHub 제출','기존 fork에서 개발하고 공용 저장소로 PR',table([['항목','지정 값·방법'],['저장소','sesac-ddm-4-web/sesac-spring-boot-study의 본인 fork'],['폴더·브랜치','본인 기존 프로젝트 폴더 유지 · 브랜치 이름 자율'],['공용 저장소 Issue','[과제] 이름 / 단축 URL JPA 전환'],['공용 저장소 PR','[이름] 단축 URL 서비스 JPA 전환 · base: 공용 원본 main'],['PR에 포함','연결한 Issue URL · 전환 내용 · QA·rollback·재시작 확인 근거']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('본인 fork에 push → 공용 원본으로 PR을 올립니다. 직접 병합하지 않습니다.<br>기존 fork·열린 PR이 있으면 이어가되 이번 전환 변경을 구분해 적습니다.'),note='공용 Issue를 연결할 때 URL을 명시합니다. 다른 저장소의 같은 번호 Issue가 자동 종료된다고 가정하지 않습니다. 다른 교육생 폴더를 수정하지 않습니다.')
add('완료 기준','전환 전후의 차이를 설명하고 제출',steps('기존 생성·이동과 본인이 구현한 부가 기능 유지','파일·서버 DB에서 재시작 후 데이터 보존','Service 경계·정상 commit·실패 rollback을 근거로 설명','README·직접 작성한 QA 체크리스트·PR 제출')+call('<a href="SHORT-URL-JPA-ASSIGNMENT.md">과제 정리 ↗</a> · 별도 주문 랩 제출은 필수가 아닙니다.<br>gradle-wrapper.jar는 포함하고 DB 파일·계정 정보는 올리지 않습니다.'))
add('보충 · Repository 구조','기존 저장소 인터페이스를 유지할 수 있음',linear('기존 인터페이스를 유지하면 JPA 어댑터가 Spring Data 저장소에 위임합니다',[('Service','기존 Repository 사용'),('직접 만든 JPA 어댑터','Domain ↔ Entity 변환'),('Spring Data Repository','저장·조회 위임')])+call('임의로 만든 모든 Repository가 자동 구현되는 것은 아닙니다.<br>프로젝트 규모와 기존 설계에 맞춰 직접 사용 또는 어댑터 방식을 선택합니다.'))
add('보충 · save · persist · merge','save가 전달 객체를 항상 관리 상태로 바꿀까?',table([['동작','의미'],['Spring Data save','신규 판단에 따라 persist 또는 merge 사용'],['persist','새 Entity 자체를 관리'],['merge','상태를 관리 Entity에 복사하고 관리 Entity 반환'],['분리된 원본','merge에 전달했다고 원본 자체가 관리되는 것은 아님']])+call('save 반환값을 사용합니다. 신규 판단은 버전·id 등 상태 정보를 참고합니다.<br>EntityGraph·배치 페치·컬렉션 fetch join의 페이징 한계는 선택 심화입니다.'))
add('참고 자료','공식 문서와 주문 예제', '<div class="references"><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html"><b>Spring @Transactional ↗</b><span>적용 위치 · 프록시 · 기본 설정</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html"><b>Spring rollback ↗</b><span>예외와 rollback 정책</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html"><b>트랜잭션 전파 ↗</b><span>REQUIRED · 바깥 트랜잭션 참여</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html"><b>Spring Data JPA ↗</b><span>save · persist · merge</span></a><a href="https://docs.hibernate.org/orm/current/userguide/html_single/"><b>Hibernate ORM ↗</b><span>매핑 · 지연 로딩 · 쿼리</span></a></div>')
add('선택 관찰 · 전체 참고 코드','주문 예제의 전체 파일',source_choices(),note='참고 코드는 shared/order_sources.py와 동일한 6개 파일입니다. 기존 ZIP·Java를 바꾸지 않습니다. 단축 URL 과제의 정답 코드가 아니며 별도 실습 프로젝트입니다.')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-23-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.23</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="트랜잭션과 JPA · 단축 URL 서비스 전환"><title>11월 23일 · 트랜잭션과 JPA · 단축 URL 서비스 전환</title><style>'+css+'</style></head><body data-deck-revision="2026-11-23-v3-transactions"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(x in out for x in ['contenteditable=','localStorage'])
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',out.count('data-source-key='),'reference buttons;',len(out.encode()),'bytes')
