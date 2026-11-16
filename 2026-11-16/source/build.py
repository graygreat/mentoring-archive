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
def repository_bridge():
 inner=box(5,20,300,110,'기존 Service','ProductRepository에 의존')
 inner+=box(420,20,300,110,'직접 만든 인터페이스','ProductRepository')
 inner+=box(835,20,308,110,'직접 만든 JPA 구현','JpaProductRepository')
 inner+=arrow(315,75,410,75,'호출')+arrow(730,75,825,75,'구현 선택')
 inner+=box(835,190,308,110,'Spring Data 인터페이스','ProductJpaRepository')
 inner+=box(420,190,300,110,'Hibernate · DB','매핑 · SQL 실행')
 inner+=arrow(989,140,989,180,'위임')+arrow(825,245,730,245)
 return svg('Service가 기존 ProductRepository를 호출하고 직접 만든 JPA 구현이 Spring Data Repository에 저장과 조회를 위임합니다',inner,320)
def context_inside():
 inner='<rect x="245" y="15" width="615" height="290" rx="16" fill="#f3f7ee" stroke="#087f5b" stroke-width="2"/><text x="270" y="49" font-size="23" fill="#087f5b" font-weight="700">영속성 컨텍스트 · flush 전</text>'
 inner+=box(5,65,190,100,'first','객체 참조')+box(5,195,190,100,'second','객체 참조')
 inner+=box(280,85,260,120,'관리 Entity · id=1','현재 price = 25000')
 inner+=box(565,85,265,120,'스냅샷','조회 당시 price = 30000')
 inner+=arrow(205,115,270,125)+arrow(205,245,270,155)
 inner+='<text x="552" y="253" text-anchor="middle" font-size="23" fill="#087f5b">flush 때 현재 값과 기억한 값을 비교</text>'
 inner+=box(905,85,235,120,'DB 행 · id=1','price = 30000')
 inner+=arrow(870,260,1020,260,'변경 시 UPDATE')
 return svg('first와 second는 같은 관리 Entity를 참조합니다. 현재 가격은 25000, 조회 당시 가격은 30000이며 flush 전 DB 값은 30000입니다',inner,330)
def jpa_providers():
 inner=box(369,10,410,105,'JPA · 공통 표준','Entity · EntityManager · 동작 규칙')
 for x,title,sub in [(14,'Hibernate','이 수업에서 사용하는 구현체'),(409,'EclipseLink','JPA 구현체'),(804,'Apache OpenJPA','JPA 구현체')]:
  inner+=box(x,185,330,110,title,sub)
  center=x+165
  inner+=f'<path d="M574,115 V148 H{center} V175" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#jpa-provider-arrow)"/>'
 title='JPA 표준을 구현한 Hibernate, EclipseLink, Apache OpenJPA 중 이 수업에서는 Hibernate를 사용합니다'
 return '<svg class="diagram" style="max-height:260px" viewBox="0 0 1148 310" role="img" aria-label="'+esc(title)+'"><title>'+esc(title)+'</title><defs><marker id="jpa-provider-arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9" fill="none" stroke="#087f5b" stroke-width="1.5"/></marker></defs>'+inner+'</svg>'
def entity_mapping():
 inner=box(5,15,480,235,'ProductEntity 클래스','@Table(name = "products")')
 inner+=box(650,15,493,235,'products 테이블','상품 데이터를 담는 표')
 for y,left,right in [(135,'@Id Long id','id · BIGINT · 기본 키'),(177,'String name','name · VARCHAR'),(219,'int price','price · INTEGER')]:
  inner+=f'<text x="35" y="{y}" font-size="23" fill="#16251f">{esc(left)}</text>'
  inner+=f'<text x="680" y="{y}" font-size="23" fill="#16251f">{esc(right)}</text>'
  inner+=arrow(500,y-8,635,y-8)
 inner+='<text x="574" y="292" text-anchor="middle" font-size="23" fill="#087f5b">이 예제의 상품 객체 한 개 ↔ 상품 행 한 개 · 키보드 / 30000원</text>'
 return svg('ProductEntity 클래스는 products 테이블, id·name·price 필드는 같은 이름의 열에 매핑됩니다. 이 예제의 한 상품 객체는 한 상품 행에 대응합니다',inner,320)
def context_and_database():
 inner=box(5,20,480,180,'영속성 컨텍스트','관리 Entity · 스냅샷 · 1차 캐시')
 inner+=box(650,20,493,180,'데이터베이스','상품 행 · 변경 확정은 commit')
 inner+=arrow(500,110,635,110,'flush: SQL')
 inner+='<text x="245" y="245" text-anchor="middle" font-size="23" fill="#087f5b">clear → 객체 관리 해제</text>'
 inner+='<text x="245" y="282" text-anchor="middle" font-size="21" fill="#52665a">DB의 행을 삭제하는 동작이 아님</text>'
 inner+='<text x="896" y="245" text-anchor="middle" font-size="23" fill="#087f5b">파일·서버 DB의 확정된 데이터</text>'
 inner+='<text x="896" y="282" text-anchor="middle" font-size="21" fill="#52665a">앱을 다시 켜도 조회 가능</text>'
 return svg('영속성 컨텍스트의 관리 객체를 clear로 해제해도 데이터베이스 행은 삭제되지 않습니다. 테이블·파일을 삭제하지 않는 설정에서 파일이나 서버 DB에 commit한 데이터는 앱 재시작 뒤에도 남습니다',inner,310)
DAY='2026-11-16'
TITLE='단축 URL 서비스 발표 · JPA'
add('발표','나만의 단축 URL 서비스 만들기',steps('누구를 위한 서비스인지와 해결하려던 불편 소개','직접 구현한 주요 기능과 실제 동작 보여주기','백엔드 구조·설계 결정과 AI 도움을 받은 부분 설명','개발 중 해결한 문제와 남은 작업 공유'),note='발표용 PPT를 별도로 요구하지 않습니다. 서비스 화면·코드·실행 결과로 설명하며, 미완료 기능은 실제 완료한 범위와 구분합니다. 발표 후 14일에 진행하지 못한 JPA 자료를 그대로 이어서 설명합니다.')
section('03','Spring Data JPA와 DB 연동','')
add('오늘 이해할 흐름','상품 하나로 네 가지 질문 확인',linear('왜 JPA를 쓰는지, 객체와 표를 어떻게 연결하는지, 어떻게 저장하고 조회하는지, 변경을 언제 반영하는지 순서대로 확인합니다',[('왜 JPA를 쓰나?','JDBC · SQL Mapper · ORM'),('무엇을 연결하나?','Entity 필드 ↔ 테이블 열'),('어떻게 저장하나?','save → 실제 id로 조회'),('언제 반영되나?','변경 감지 → flush → commit')])+call('같은 상품을 사용합니다. 키보드 30000원을 저장하고, 조회한 뒤 가격을 25000원으로 바꿉니다.'),note='오늘의 핵심은 용어를 모두 외우는 것이 아니라 같은 상품의 객체·SQL·DB 행이 연결되는 과정을 설명하는 것입니다. 보충으로 표시한 저장소 어댑터·merge 세부 동작·고급 트랜잭션 규칙은 이해도와 남은 시간에 따라 참고합니다.')
add('DB 연결 복습','상품 하나를 Java와 DB에서 표현',table([['Java의 ProductEntity','products 테이블'],['id = 1L','id = 1 · BIGINT · 기본 키'],['name = "키보드"','name = 키보드 · VARCHAR'],['price = 30000','price = 30000 · INTEGER']])+call('객체를 저장하려면 INSERT가, 행을 객체로 읽으려면 SELECT 결과 변환이 필요합니다.'))
add('JDBC · SQL Mapper · ORM','누가 SQL을 쓰고 결과를 옮길까?',table([['방식','개발자가 주로 작성하는 것'],['JDBC 직접 사용','SQL · 파라미터 설정 · ResultSet → 객체 변환'],['SQL Mapper · MyBatis','SQL · SQL과 메서드 연결 · 결과 매핑 설정'],['ORM · JPA 구현체','Entity와 테이블 매핑 · 객체의 저장·조회·변경']])+call('ORM은 Object-Relational Mapping, 객체·관계 매핑입니다.<br>세 방식 모두 SQL로 DB를 사용하며 MyBatis와 Hibernate도 내부에서 JDBC를 사용합니다.'))
add('SQL Mapper · MyBatis','상품 조회 SQL을 직접 작성',code("""// MyBatis Mapper 인터페이스 발췌
@Select("SELECT id, name, price FROM products WHERE id = #{id}")
ProductRow findById(@Param("id") Long id);
""")+call('개발자가 SELECT와 조회할 열을 정합니다.<br>MyBatis가 id 값을 바인딩하고 결과 열을 ProductRow 객체에 매핑합니다.'),kind='code-slide',note='ProductRow는 id·name·price를 가진 결과용 객체라고 가정한 발췌입니다. Mapper 등록과 import는 생략했습니다. MyBatis도 설정에 따라 캐시와 지연 로딩을 제공하므로 캐시가 전혀 없다고 비교하지 않습니다.')
add('ORM · JPA','객체 매핑을 바탕으로 조회',code("""// EntityManager 사용 예 · 매핑과 트랜잭션 설정은 뒤에서 설명
ProductEntity product = entityManager.find(ProductEntity.class, 1L);

// DB 조회가 필요한 경우 Hibernate가 실행할 SQL의 예
// SELECT id, name, price FROM products WHERE id = ?
""")+call('어떤 테이블·열을 사용할지는 Entity 매핑을 보고 결정합니다.<br>객체를 조회하고 관리하는 기능까지 제공합니다.'),kind='code-slide')
add('면접 질문 · ORM과 SQL Mapper','차이를 어떻게 설명할까?',table([['비교','설명'],['SQL 작성 중심','MyBatis는 SQL을 직접 쓰고 실행 결과를 객체에 매핑'],['객체 관리 중심','ORM은 객체·테이블 매핑과 객체 상태를 바탕으로 SQL 처리'],['MyBatis를 선택할 때','복잡한 조회 SQL을 직접 제어해야 하는 요구에 적합'],['객체 필드만 바꾸면?','MyBatis는 UPDATE Mapper 호출 필요 · JPA는 관리 Entity 변경 감지']])+call('복잡한 SQL의 직접 제어와 반복 CRUD·객체 관리 중 필요한 장점을 비교합니다.<br>JPA도 JPQL·네이티브 SQL을 사용하며, ORM이 항상 빠른 것은 아닙니다.'),note='선택은 팀 경험·도메인·조회 복잡도·운영 요구를 함께 고려합니다. ORM을 쓰면 SQL을 몰라도 된다는 답변을 피합니다.')
add('가격 수정 비교 · 코드 발췌','같은 가격 변경을 두 방식으로 구현', '<div class="cols"><div><div class="eyebrow">MyBatis · UPDATE를 직접 작성하고 호출</div>'+code("""// Mapper에 등록할 SQL
@Update("UPDATE products SET price = #{price} "
        + "WHERE id = #{id}")
void updatePrice(@Param("id") Long id,
        @Param("price") int price);

// Service에서 실행
mapper.updatePrice(1L, 25000);
""")+'</div><div><div class="eyebrow">JPA · 관리 Entity를 트랜잭션 안에서 수정</div>'+code("""// Service 메서드 발췌
@Transactional
public void changePrice() {
    ProductEntity product = entityManager
            .find(ProductEntity.class, 1L);
    product.changePrice(25000);
}
""")+'</div></div>'+call('두 방식 모두 UPDATE SQL로 DB 값을 바꿉니다.<br>지금은 작성 방식만 비교합니다. 관리 상태·트랜잭션·변경 감지는 뒤에서 설명합니다.'),kind='code-slide',note='메서드 발췌이며 Mapper 등록·주입·import는 생략했습니다. id=1 상품이 존재한다고 가정합니다. MyBatis에서는 반환된 일반 객체 필드를 바꾸는 것만으로 UPDATE가 실행되지 않습니다. JPA는 Spring 프록시로 진입한 쓰기 트랜잭션 안의 관리 Entity를 수정하는 조건입니다. 실제 Hibernate UPDATE 열 구성은 매핑·설정에 따라 달라집니다.')
add('JPA · Hibernate · Spring Data JPA','세 가지 이름의 역할',table([['이름','상품을 조회할 때 맡는 역할'],['JPA · 공통 표준','EntityManager.find()처럼 객체를 조회·관리하는 API와 동작 규칙을 정함'],['Hibernate · JPA 구현체','그 API의 실제 동작을 구현 · 필요한 SQL 생성과 결과 객체 구성'],['Spring Data JPA · Repository 지원','findById() 등 반복되는 Repository 구현을 제공 · 내부에서 JPA 사용']])+call('우리는 Spring Data JPA와 Hibernate를 함께 사용합니다.<br>JPA는 공통 표준, Hibernate는 실제 구현, Spring Data JPA는 Repository 작성을 줄이는 기능입니다.'))
add('JPA · 표준과 API','객체를 조회하는 공통 사용 방법',table([['JPA가 정한 것','코드에서 사용하는 의미'],['@Entity','저장·조회할 대상 클래스를 표시'],['@Id','Entity를 구분하는 식별자 필드를 표시'],['EntityManager','Entity 저장·조회·삭제·관리를 요청하는 표준 인터페이스']])+code("""// JPA API 사용 예 · import와 주입 설정은 생략
ProductEntity product = entityManager.find(ProductEntity.class, 1L);
""")+call('의미: ProductEntity 중 id가 1인 객체를 찾아주세요.<br>JPA는 명세와 공통 API를 제공하며, 실제 처리는 Hibernate 같은 구현체가 담당합니다.'),kind='code-slide',note='JPA를 인터페이스 하나나 문서만으로 설명하지 않습니다. EntityManager는 표준 인터페이스이고 @Entity와 @Id도 JPA API에 포함됩니다. 이 예제의 EntityManager 실제 동작은 Hibernate가 제공합니다.')
add('Hibernate · JPA 구현체','조회 요청을 SQL과 객체로 연결',steps('EntityManager.find() 요청을 Hibernate의 구현이 처리','ProductEntity와 products 테이블의 매핑 정보를 확인','DB 조회가 필요하면 SQL을 만들고 JDBC를 통해 요청','DB 조회 결과를 ProductEntity 객체로 구성하고 관리')+code("""-- DB 조회가 필요한 경우 실행할 SELECT의 예
SELECT id, name, price FROM products WHERE id = ?;
""")+call('EntityManager는 JPA의 인터페이스이며, 그 실제 동작을 Hibernate가 제공합니다.<br>이미 관리 중인 객체를 찾으면 DB 조회를 생략할 수도 있습니다.'),kind='code-slide',note='DB가 SQL을 실행합니다. Hibernate는 SQL 생성·JDBC 호출·행과 객체의 변환·Entity 관리를 담당합니다. EntityManager와 Hibernate를 서로 독립된 서버처럼 그리지 않습니다. 1차 캐시와 SQL 생략 조건은 뒤에서 설명합니다.')
add('Spring Data JPA · Repository 지원','기본 조회 코드를 직접 반복하지 않기',code("""// Spring Data JPA 인터페이스 · import와 주입은 생략
public interface ProductJpaRepository
        extends JpaRepository<ProductEntity, Long> {
}

// 사용하는 쪽: 기본 findById 구현을 직접 작성하지 않음
Optional<ProductEntity> product = repository.findById(1L);
""")+call('내 Service → Spring Data Repository 구현 → EntityManager.find() → Hibernate<br>Spring Data JPA가 JPA를 호출하고, Hibernate가 실제 조회를 처리합니다.'),kind='code-slide',note='기본 findById 경로를 단순화한 설명입니다. Spring Data가 Repository 프록시와 기본 구현을 연결합니다. ProductEntity는 관리할 타입, Long은 식별자 타입입니다. Spring Data JPA 자체가 JPA 구현체인 것은 아니며 Service의 업무 규칙은 직접 작성합니다.')
add('다른 JPA 구현체','Hibernate 외에도 구현체가 있습니다',jpa_providers()+call('JPA 구현체가 여러 가지라는 정도만 확인합니다. 이름을 모두 외울 필요는 없습니다.<br>교체할 때는 설정·지원 버전·생성 SQL·전용 기능을 확인하고 테스트합니다.')+'<p><a href="https://eclipse.dev/eclipselink/">EclipseLink 공식 자료 ↗</a> · <a href="https://openjpa.apache.org/">Apache OpenJPA 공식 자료 ↗</a></p>',note='그림은 공통 표준과 구현체의 관계이며 실행 순서가 아닙니다. 세 구현체가 동시에 한 요청을 처리한다는 뜻도 아닙니다. 표준 API 중심으로 작성하면 교체 영향을 줄일 수 있지만 설정이나 구현체 전용 기능까지 무수정 교체가 보장되는 것은 아닙니다.')
add('DB 연동 준비','의존성과 접속 설정은 계속 필요',table([['준비할 것','예시와 목적'],['Spring Data JPA 의존성','spring-boot-starter-data-jpa · Repository와 JPA 사용'],['DB 드라이버','H2는 com.h2database:h2 · DB와 통신'],['접속 정보','spring.datasource.url · username · password'],['테이블 준비','기존 스키마 또는 학습용 DDL 생성 설정']])+call('기존 JDBC DB 연동을 지우지 않습니다. JPA 확인은 별도 학습 프로젝트와 별도 DB에서 진행합니다.'),note='프로젝트의 기존 Spring Boot 버전과 의존성 관리를 따릅니다. 실제 계정 비밀번호나 로컬 DB 파일을 저장소에 올리지 않습니다. 개인 단축 URL 프로젝트를 JPA로 전환하라는 요구가 아닙니다.')
add('학습용 설정 · application.properties','별도 메모리 DB에서 SQL 관찰',code("""spring.datasource.url=jdbc:h2:mem:jpa-preview
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
""")+call('학습용 H2 메모리 DB 예시입니다. create-drop은 테이블을 만들고 종료 시 삭제합니다.<br>기존 데이터가 있는 DB와 운영 DB에는 그대로 적용하지 않습니다.'),kind='code-slide',note='H2 드라이버와 Spring Data JPA 의존성이 준비된 프로젝트의 설정 발췌입니다. 메모리 DB는 프로세스 종료 후 사라집니다. show-sql은 학습 관찰용이며 운영 SQL 로깅 정책과 구분합니다.')
add('Entity 매핑 · 클래스 발췌','Java 필드와 테이블 열 연결',code("""@Entity
@Table(name = "products")
public class ProductEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false)
    private String name;
    private int price;
    // 생성자와 메서드는 다음 장표
}
""")+call('Entity는 DB 매핑·관리 대상이고, DTO는 요청·응답 데이터를 전달하는 객체입니다.<br>@Id는 기본 키, IDENTITY는 DB의 id 생성입니다. NOT NULL은 공백·음수 검증을 대신하지 않습니다.'),kind='code-slide',note='jakarta.persistence의 Entity·Table·Id·GeneratedValue·GenerationType·Column import는 생략한 클래스 발췌입니다. 테이블명과 필드 대응을 먼저 설명합니다. 별도 Product 도메인을 유지하는 기존 구조와 Entity를 혼동하지 않습니다.')
add('Entity 매핑 · 클래스 내부 발췌','생성자와 변경 메서드',code("""protected ProductEntity() {}

public ProductEntity(String name, int price) {
    this.name = name;
    this.price = price;
}

public void changePrice(int price) {
    if (price < 0) throw new IllegalArgumentException("음수 가격");
    this.price = price;
}
""")+call('public 또는 protected 기본 생성자가 필요합니다.<br>업무 규칙은 직접 구현합니다. Lombok이나 모든 필드의 setter는 필수가 아닙니다.'),kind='code-slide',note='앞 장표 ProductEntity 클래스 안에 들어갈 일부 메서드입니다. 생성자 입력 검증·조회용 메서드 등 전체 구현은 생략했습니다. JPA가 업무 검증을 대신한다는 의미가 아닙니다.')
add('Entity와 테이블 연결','클래스·필드와 표·열을 함께 보기',entity_mapping()+call('@Table은 연결할 테이블을, @Id는 기본 키로 사용할 필드를 지정합니다.<br>클래스는 객체의 설계이고, 실제 저장·조회하는 상품은 그 클래스로 만든 객체입니다.'),note='상품 Entity 한 종류를 한 테이블에 매핑한 현재 예제를 설명합니다. 모든 JPA 매핑이 항상 클래스 하나와 테이블 하나로 끝난다고 일반화하지 않습니다. 관계 매핑과 상속 매핑은 오늘의 기본 그림 범위에 넣지 않습니다.')
add('Spring Data JPA Repository','인터페이스로 기본 CRUD 사용',code("""public interface ProductJpaRepository
        extends JpaRepository<ProductEntity, Long> {
}

// 사용하는 쪽의 코드 발췌
ProductEntity product = repository.findById(1L)
        .orElseThrow(() -> new IllegalArgumentException("상품 없음"));
""")+call('ProductEntity는 관리 대상 타입, Long은 기본 키 타입입니다.<br>Spring Data가 Repository 구현체를 제공합니다. Service의 업무 코드는 직접 작성합니다.'),kind='code-slide',note='JpaRepository import와 Repository 주입은 생략했습니다. 예외는 간단한 예시이며 HTTP 상태 매핑은 별도 ControllerAdvice 등의 책임입니다.')
add('상품 등록과 조회 · 코드 발췌','저장한 상품의 실제 id로 다시 조회',code("""// @Transactional Service 메서드 안의 코드 발췌
ProductEntity saved = repository.save(
        new ProductEntity("키보드", 30000));
Long actualId = saved.getId();
ProductEntity found = repository.findById(actualId)
        .orElseThrow();
// SQL 예: INSERT INTO products(name, price) VALUES (?, ?)
// DB 조회가 필요하면 SELECT ... WHERE id = ?
""")+call('DB가 발급해 반환한 actualId를 사용합니다. id가 1이라고 가정하지 않습니다.<br>같은 컨텍스트의 재조회는 SELECT를 생략할 수 있습니다. save는 commit과 다릅니다.<br>그 이유를 이해하려면 JPA가 객체를 어떻게 관리하는지 알아야 합니다.'),kind='code-slide',note='주입된 ProductJpaRepository를 사용하는 쓰기 트랜잭션의 메서드 내부 발췌입니다. ProductEntity.getId()는 조회용 메서드로 가정하며 앞 클래스 발췌에서는 생략했습니다. 새 객체의 id는 처음에는 null이고 IDENTITY 방식에서는 DB가 식별자를 발급합니다. 반환된 실제 식별자를 다음 조회에 사용합니다. SQL의 열과 실행 시점은 구현과 설정에 따라 다르며 같은 컨텍스트의 findById가 항상 SELECT를 실행한다는 뜻은 아닙니다.')
add('영속성 컨텍스트','조회한 객체를 관리하는 작업 공간',linear('EntityManager가 영속성 컨텍스트를 통해 Entity의 상태와 변경을 관리합니다',[('EntityManager','find · persist · remove'),('영속성 컨텍스트','관리 Entity · 변경 추적'),('DB','SELECT · INSERT · UPDATE')])+call('DB 자체나 서버 전체의 공용 캐시가 아닙니다.<br>이 예제에서는 Service 트랜잭션 범위 안에서 객체를 조회하고 변경합니다.'),note='Spring에서 사용하는 EntityManager 참조는 프록시일 수 있습니다. 실제 컨텍스트의 수명은 트랜잭션 경계와 OSIV 등 설정에 영향을 받습니다. 기본 예제의 범위를 명시하고 모든 요청이 반드시 한 컨텍스트라는 식으로 단정하지 않습니다.')
add('영속성 컨텍스트와 DB','객체 관리와 데이터 보관은 다릅니다',context_and_database()+call('파일·서버 DB도 create-drop처럼 테이블을 삭제하는 설정이면 데이터가 사라집니다.<br>수업의 H2 메모리 DB는 종료 시 사라집니다. clear는 DB의 행을 삭제하지 않습니다.'),note='DB에 반영됐더라도 commit 전이면 확정된 데이터가 아니므로 rollback할 수 있습니다. 파일·서버 DB의 commit된 데이터는 정상적인 앱 재시작 이후에도 보존된다는 뜻이며 모든 메모리 DB에 같은 보존을 가정하지 않습니다. 실제 컨텍스트 수명은 트랜잭션·OSIV 설정 등의 영향을 받습니다. clear는 영속성 컨텍스트의 Entity를 준영속 상태로 만들며 DB 행 자체를 삭제하지 않습니다.')
add('Entity 상태','new한 객체는 아직 관리 대상이 아님',table([['상태','예시와 의미'],['비영속 · new','new ProductEntity(...) · 아직 영속성 컨텍스트와 관계없음'],['영속 · managed','persist하거나 find로 조회 · 컨텍스트가 관리'],['준영속 · detached','detach·clear 등으로 분리 · 변경 감지 대상에서 제외'],['삭제 · removed','remove로 삭제 대상 지정 · flush 때 DELETE 가능']])+call('persist는 관리 상태로 만드는 작업입니다. 호출 직후 항상 INSERT·commit이 완료되는 것은 아닙니다.'))
add('1차 캐시 · EntityManager 발췌','같은 id를 두 번 find하면?',code("""// 같은 영속성 컨텍스트 안에서 실행
ProductEntity first = entityManager.find(ProductEntity.class, 1L);
ProductEntity second = entityManager.find(ProductEntity.class, 1L);

System.out.println(first == second); // true
""")+call('관리 중인 같은 Entity를 다시 find하면 1차 캐시에서 찾을 수 있습니다.<br>다른 컨텍스트까지 공유하는 캐시가 아니며, JPQL 조회가 항상 SQL을 생략하는 것도 아닙니다.'),kind='code-slide',note='해당 id가 존재하며 두 find 사이에 detach·clear가 없는 경우입니다. 서버 전체에서 DB 조회가 한 번뿐이라는 설명을 피합니다. JPQL은 쿼리 실행과 결과 Entity 동일성 보장을 구분합니다.')
add('영속성 컨텍스트 내부','같은 객체와 조회 당시 값을 함께 관리',context_inside()+call('first와 second는 같은 Entity를 가리킵니다.<br>현재 값과 조회 당시 값을 비교할 수 있습니다.<br>다음으로 이 차이를 이용한 변경 감지가 어떻게 UPDATE로 이어지는지 봅니다.'),note='같은 컨텍스트에서 id=1을 두 번 find하고 가격만 변경한 flush 전 시점입니다. 일반적인 Hibernate 스냅샷 기반 변경 감지를 단순화한 그림이며 스냅샷과 Entity는 같은 객체라는 뜻이 아닙니다. 조회된 Entity의 같은 식별자 객체 재사용과 변경 추적을 함께 설명합니다. UPDATE 실행 전이므로 DB 행은 아직 30000입니다.')
add('변경 감지 · Dirty Checking','어떻게 UPDATE가 나갈까?',table([['순서','상품 가격 30000 → 25000 예시'],['1. 조회','Entity를 관리하고 조회 시점 상태를 기억'],['2. 객체 변경','product.changePrice(25000)으로 필드 값 변경'],['3. flush','기억한 상태와 비교해 변경을 감지하고 UPDATE 실행'],['4. commit','DB 트랜잭션의 변경을 확정']])+call('new한 객체나 컨텍스트에서 분리된 객체는 같은 방식으로 자동 저장되지 않습니다.'),note='일반적인 스냅샷 기반 설명입니다. Hibernate의 바이트코드 개선 등 내부 최적화와 구분합니다. 기본 설정에서는 커밋 전 flush가 일어납니다. SQL 형식과 변경 열 구성은 구현·설정에 따라 다릅니다.')
add('트랜잭션 기본','왜 Service에 @Transactional을 붙일까?',table([['작업','같은 트랜잭션으로 묶는 이유'],['상품 조회 → 가격 변경','관리 Entity를 조회하고 수정하는 작업을 한 범위에서 처리'],['commit · 변경 확정','정상적으로 완료한 DB 변경을 확정'],['rollback · 변경 취소','실패한 트랜잭션의 DB 변경을 취소']])+call('Service의 한 기능을 성공·실패 단위로 묶습니다.<br>Spring 기본 설정에서는 RuntimeException·Error가 밖으로 전파되면 rollback합니다.'),note='이 Service 메서드가 트랜잭션을 시작하고 외부 호출로 적용되는 일반적인 예입니다. 기존 트랜잭션에 참여하면 최종 commit은 바깥 경계에서 결정됩니다. 체크 예외·readOnly·자기 호출은 뒤의 보충 장표에서만 설명합니다.')
add('가격 변경 · Service 메서드 발췌','조회한 상품을 트랜잭션 안에서 수정',code("""@Transactional
public void changePrice(Long id, int price) {
    ProductEntity product = repository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("상품 없음"));
    product.changePrice(price);
}
""")+call('트랜잭션 안에서 조회한 관리 상태 Entity입니다.<br>별도 save 없이 변경 감지로 가격 변경을 반영할 수 있습니다.<br>이제 실제 UPDATE가 실행되는 시점과 변경이 확정되는 시점을 구분합니다.'),kind='code-slide',note='주입된 ProductJpaRepository를 사용하는 Spring Service의 메서드 발췌입니다. 외부에서 Spring 프록시를 통해 호출되는 기본 상황이며 org.springframework.transaction.annotation.Transactional을 사용합니다. ProductEntity가 관리 상태인 조건을 생략해서 설명하지 않습니다.')
add('flush · commit · rollback','SQL 전달과 변경 확정은 다르다',code("""// 진행 중인 트랜잭션 안의 EntityManager 코드 발췌
ProductEntity product = entityManager.find(ProductEntity.class, 1L);
product.changePrice(25000);
entityManager.flush();
// UPDATE products SET ... price = 25000 ... WHERE id = 1
// 아직 commit 전: DB 트랜잭션을 rollback할 수 있음
""")+call('flush는 SQL을 DB에 전달합니다. commit이 최종 확정입니다.<br>rollback해도 Java 객체의 price 필드까지 자동으로 30000으로 돌아가지는 않습니다.'),kind='code-slide',note='SQL은 설명용 예시입니다. flush가 영속성 컨텍스트를 비우는 것도 아닙니다. 롤백 뒤 객체를 계속 사용하지 말고 트랜잭션·컨텍스트 경계에 맞게 다시 조회합니다.')
add('가격 변경 타임라인','객체 값과 DB 값은 언제 바뀔까?',table([['단계','Java 객체 price','DB 값 · 해당 트랜잭션 기준'],['조회','30000','30000'],['객체 수정','25000','30000 · 아직 UPDATE 전'],['flush','25000','25000 · UPDATE 실행, 아직 미확정'],['이후 commit 선택','25000','25000 · 변경 확정'],['또는 rollback 선택','25000 · 자동 복구 안 됨','30000 · DB 변경 취소']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('commit과 rollback은 flush 이후의 서로 다른 선택입니다.<br>다른 트랜잭션에서 보이는 값은 격리 수준에 따라 다릅니다.'),note='하나의 쓰기 트랜잭션에서 기존 상품 가격을 변경하는 단순 예입니다. commit 후 다시 rollback하면 취소된다는 뜻이 아닙니다. flush 뒤 같은 DB 트랜잭션에서 읽은 값과 다른 트랜잭션의 관찰값을 구분합니다. rollback 뒤 남은 Java 객체를 그대로 재사용하지 않고 새 트랜잭션과 컨텍스트에서 다시 조회합니다.')
add('INSERT 실행 시점','save 직후 SQL이 보일 수도 있음',table([['상황','주의할 점'],['새 Entity 저장','JPA가 관리하고 INSERT를 준비'],['IDENTITY 방식','DB에서 id를 받아야 해서 INSERT가 일찍 실행될 수 있음'],['flush 발생','커밋 전 또는 필요한 쿼리 실행 전에 SQL이 반영될 수 있음'],['commit','SQL이 먼저 실행됐어도 DB 변경 확정은 별개']])+call('“JPA는 모든 SQL을 commit 순간에만 실행한다”라고 외우면 안 됩니다.'),note='식별자 전략·flush 모드·API·구현체에 따라 실행 시점이 달라집니다. 이 예제는 IDENTITY를 사용하므로 지연 INSERT를 무조건 전제하지 않습니다.')
add('면접 질문 · 영속성 컨텍스트','1차 캐시와 변경 감지를 설명해 볼까?',table([['질문','답변에 포함할 내용'],['영속성 컨텍스트는 무엇인가?','Entity를 관리하고 DB와 동기화하는 작업 공간'],['같은 id를 다시 find하면?','같은 컨텍스트의 관리 객체를 재사용할 수 있음'],['save 없이 수정 가능한 이유는?','트랜잭션 안의 관리 Entity 변경을 감지해 SQL 반영'],['어떤 객체든 필드만 바꾸면 되는가?','아니요. 비영속·준영속 객체와 관리 Entity를 구분']])+call('price를 바꾸는 코드가 어느 트랜잭션과 영속성 컨텍스트 안에 있는지 함께 설명합니다.'))
add('면접 질문 · SQL과 트랜잭션','flush와 commit을 구분해 볼까?',table([['질문','답변에 포함할 내용'],['flush하면 저장이 확정되는가?','SQL은 실행하지만 commit 전이면 롤백 가능'],['save 직후 INSERT가 보이면?','IDENTITY 등으로 일찍 실행 가능 · commit과는 별개'],['rollback하면 객체 값도 되돌아가는가?','DB 변경 취소와 Java 메모리의 필드 값은 별개'],['JPA를 쓰면 SQL을 몰라도 되는가?','실제 SQL·인덱스·트랜잭션을 이해해야 오류와 성능 분석 가능']]))
add('이해 확인 · 코드 결과 예측','실행 전에 결과와 이유를 말해 보기',table([['코드·조건','예측할 결과와 이유'],['같은 컨텍스트에서 find(1L) 두 번<br>first == second ?', 'true · 같은 관리 객체 재사용<br>상품 존재, 중간 clear·detach 없음'],['쓰기 트랜잭션에서 find 후<br>changePrice(25000) · save 없음','정상 commit하면 UPDATE 가능<br>관리 Entity의 변경 감지'],['new ProductEntity(...) 후<br>changePrice(25000)만 호출','DB 저장 없음<br>persist·save 없이 비영속 객체만 수정'],['find → 변경 → flush → rollback','DB는 기존 값 30000<br>Java 필드 25000은 자동 복구 안 됨']]).replace('<table ', '<table style="font-size:20px" ').replace('<td>', '<td style="padding:9px 12px">')+call('먼저 답을 가리고 예상한 뒤, 객체의 관리 상태와 트랜잭션 경계로 이유를 설명합니다.'),note='각 행은 독립된 코드 상황을 줄여 쓴 것으로 완성 프로그램이 아닙니다. 첫 사례의 find는 EntityManager.find의 축약입니다. 두 번째는 일반 쓰기 트랜잭션의 정상 커밋을 전제로 합니다. 네 번째는 초기 가격 30000을 25000으로 바꾼 예입니다. 강사는 답변 열을 가리거나 질문을 먼저 읽고 교육생이 이유를 말한 뒤 답을 함께 확인합니다.')
add('다음 주 · 관계와 조회 성능','지연 로딩과 N+1은 다음에 연결',table([['상황','다음 수업에서 확인할 것'],['주문과 주문상품 연결','연관관계와 외래 키를 어떻게 매핑할까?'],['목록 조회 후 연결된 데이터 접근','필요한 시점에 추가 SELECT가 실행되는 지연 로딩'],['주문 N건마다 추가 조회','1번 목록 조회 뒤 N번 추가 조회가 생기는 N+1'],['조회 요구에 맞춘 개선','fetch join 등으로 필요한 데이터와 SQL 수를 함께 확인']])+call('오늘은 용어와 기본 저장·변경 과정을 이해합니다. 연관관계 구현과 N+1 해결 실습은 다음 주에 이어갑니다.'))
add('정리','상품 가격 변경 과정을 연결하기',steps('Repository로 상품 조회 → EntityManager와 영속성 컨텍스트가 관리','관리 Entity의 가격 수정 → 변경 감지','flush로 UPDATE 실행 → commit으로 DB 변경 확정','SQL 로그와 DB 값을 함께 보며 예상한 동작인지 확인'),note='외울 단어보다 객체·SQL·트랜잭션을 연결해 설명하는 데 집중합니다. 16일 실행과 SQL 관찰, 19일 저장소 JPA 전환, 23일 관계·지연 로딩·N+1로 이어갑니다.')
add('보충 · 기존 코드와 연결','직접 만든 Repository는 어디에 남을까?',repository_bridge()+call('ProductRepository는 저장소의 약속으로 유지할 수 있습니다.<br>JPA 구현 클래스는 직접 작성하고, Domain ↔ Entity 변환과 Spring Data 호출을 맡깁니다.'),note='기존 Repository 인터페이스를 유지하는 설계의 예입니다. Spring Data가 임의의 ProductRepository까지 자동으로 구현해 주는 것은 아닙니다. JpaProductRepository는 ProductRepository를 구현하는 직접 작성한 어댑터이고, ProductJpaRepository는 JpaRepository를 상속한 Spring Data 인터페이스입니다. 앞 장표의 Entity 직접 사용 코드는 학습용 축약이며 기존 Domain 분리 구조에 적용할 때 어댑터와 변환이 필요합니다.')
add('보충 · save · persist · merge','save는 무엇을 할까?',table([['작업','기본 동작과 주의점'],['Spring Data save(entity)','Entity가 새 것인지 판단해 persist 또는 merge 사용'],['persist(entity)','새 Entity 자체를 영속성 컨텍스트에서 관리'],['merge(entity)','전달된 상태를 관리 Entity로 복사하고 관리 Entity를 반환'],['준영속 Entity의 merge','전달한 원본이 자동으로 관리 상태가 되는 것은 아님']])+call('save 반환값을 무시하지 않습니다. 새 Entity 판단은 기본적으로 버전·id 등을 참고하며 단순히 INSERT/UPDATE 이름만 바꾼 기능은 아닙니다.'),note='Spring Data JPA 기본 상태 판단은 nullable 버전 필드를 먼저 보고 그 밖에 id를 검사합니다. Persistable 구현으로 바꿀 수도 있습니다. 이 장표는 예외 전략까지 외우기보다 persist와 merge의 객체 관리 차이를 이해하는 용도입니다.')
add('보충 · 트랜잭션 주의사항','트랜잭션 설정에서 주의할 점',table([['항목','기본 동작과 주의점'],['체크 예외','기본 설정에서는 rollback하지 않음 · 필요하면 rollbackFor 등 지정'],['readOnly = true','읽기 전용 의도를 전달하는 힌트 · 쓰기 차단 보장은 아님'],['같은 객체 안의 자기 호출','기본 프록시 방식에서는 새 @Transactional 설정이 적용되지 않음']])+call('RuntimeException·Error의 기본 rollback 규칙과 구분합니다.<br>예외를 잡고 정상 반환하거나 HTTP 오류 응답만 반환하면 기대한 rollback이 일어나지 않을 수 있습니다.'),note='트랜잭션 기본 설명을 마친 뒤 필요한 경우 확인합니다. 자기 호출의 핵심은 프록시를 지나지 않는다는 점입니다. 기존 트랜잭션 참여와 독립적인 새 트랜잭션 시작도 구분합니다.')
add('참고','JPA · MyBatis 공식 문서','<div class="references"><a href="https://jakarta.ee/specifications/persistence/"><b>Jakarta Persistence ↗</b><span>JPA 표준과 Entity 관리</span></a><a href="https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html"><b>Spring Data JPA ↗</b><span>save · persist · merge</span></a><a href="https://docs.hibernate.org/orm/current/userguide/html_single/"><b>Hibernate ORM ↗</b><span>매핑 · 변경 감지 · flush</span></a><a href="https://mybatis.org/mybatis-3/"><b>MyBatis ↗</b><span>SQL Mapper와 결과 매핑</span></a><a href="https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html"><b>Spring 트랜잭션 ↗</b><span>프록시 · 롤백 규칙</span></a><a href="../shared/db-basics/"><b>DB 기초 ↗</b><span>표 · SQL · 트랜잭션</span></a></div>')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-'+DAY+'-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>'+DAY.replace('-','.')+'</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+DAY+' · '+TITLE+'</title><meta name="description" content="'+TITLE+' · 단축 URL 서비스 발표와 지난 수업 JPA 이어가기"><style>'+css+'</style></head><body data-deck-revision="'+DAY+'-v1-book"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(DAY,len(S),'slides;',len(SOURCES),'source files')
