from pathlib import Path
import html,json,re,textwrap
R=Path(__file__).resolve().parent
OUT=R.parent
S=[]
SOURCES={}
def esc(s):return html.escape(str(s))
def code(s,key=''):
 return '<pre'+(' data-code-key="'+esc(key)+'"' if key else '')+'><code>'+esc(textwrap.dedent(s).strip('\n'))+'</code></pre>'
def call(s):return '<div class="callout">'+s+'</div>'
def table(rows):return '<table class="lesson-table">'+''.join('<tr>'+''.join(f'<{("th" if i==0 else "td")}>{x}</{("th" if i==0 else "td")}>' for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
def steps(*xs):return '<ol class="steps">'+''.join('<li>'+x+'</li>' for x in xs)+'</ol>'
def add(ch,title,body='',note='',kind=''):S.append(dict(ch=ch,title=title,body=body,note=note,kind=kind))
_diagram_id=0
def text(x,y,value,size=23,color='#16251f',anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}">{esc(value)}</text>'
def box(x,y,w,h,title,sub='',fill='#edf5ee'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#9fbea9" stroke-width="2"/>'+text(x+w/2,y+40,title,25)+('' if not sub else text(x+w/2,y+76,sub,22,'#52665a'))
def arrow(x1,y1,x2,y2,label=''):
 return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'+('' if not label else text((x1+x2)/2,(y1+y2)/2-14,label,21,'#087f5b'))
def svg(title,inner,h=300,topic='flow'):
 global _diagram_id
 _diagram_id+=1
 return '<svg class="diagram" data-diagram-topic="'+esc(topic)+'" viewBox="0 0 1148 '+str(h)+'" role="img" aria-label="'+esc(title)+'"><title>'+esc(title)+'</title><defs><marker id="arrow-'+str(_diagram_id)+'" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9" fill="none" stroke="#087f5b" stroke-width="1.5"/></marker></defs>'+inner.replace('url(#arrow)',f'url(#arrow-{_diagram_id})')+'</svg>'
def linear(title,nodes,topic='flow'):
 n=len(nodes);gap=38;w=(1148-gap*(n-1))/n;inner=''
 for i,(name,desc) in enumerate(nodes):
  x=i*(w+gap);inner+=box(x,65,w,120,name,desc)
  if i<n-1:inner+=arrow(x+w+5,125,x+w+gap-7,125)
 return svg(title,inner,250,topic)
def relation_tables():
 inner=box(10,15,390,90,'app_users · 사용자','id(PK) · username')+box(630,15,505,90,'short_links · 단축 URL','id(PK) · code · owner_id(FK)')
 for y,a,b in [(155,'101 · learner','501 · abc · 101'),(215,'102 · other','502 · xyz · 101'),(275,'','503 · def · 102')]:
  inner+=text(35,y,a,24,anchor='start')+text(660,y,b,24,anchor='start')
 inner+=arrow(610,148,420,148)+'<path d="M610,208 H520 V155 H420" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 return svg('owner_id가 101인 두 링크는 사용자 learner에 연결됩니다. 숫자는 설명용 식별자입니다',inner,310,'relation-tables')
def object_links(bidirectional=False):
 inner=box(10,75,365,135,'AppUser 객체','id=101 · learner')+box(745,10,390,110,'ShortLink 객체','code=abc · owner')+box(745,190,390,110,'ShortLink 객체','code=xyz · owner')
 inner+='<path d="M730,65 H560 V125 H390" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M730,245 H590 V165 H390" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 if bidirectional:
  inner+='<path d="M390,95 H500 V25 H730" fill="none" stroke="#9b4d25" stroke-width="3" marker-end="url(#arrow)"/>'
  inner+=text(525,290,'links는 역방향 탐색 · DB FK는 여전히 owner_id 하나',23,'#9b4d25')
 else:inner+=text(535,290,'링크에서 사용자로 탐색 · 다대일 단방향',24,'#087f5b')
 return svg('링크의 owner 참조는 사용자 객체를 가리킵니다'+(' 사용자 links로 역방향 탐색도 추가합니다' if bidirectional else ''),inner,325,'bidirectional' if bidirectional else 'many-to-one')
def owning_side():
 inner=box(10,20,475,125,'AppUser.links','역방향 목록 · mappedBy="owner"')+box(660,20,475,125,'ShortLink.owner','FK를 쓰는 연관관계 주인')
 inner+=box(330,205,490,100,'short_links.owner_id','DB의 외래 키 한 개')+arrow(900,160,830,235,'갱신 기준')
 return svg('외래 키를 갱신하는 기준은 ShortLink.owner이며 AppUser.links는 역방향 탐색입니다',inner,325,'owning-side')
def cascade_orphan():
 inner=box(10,20,350,115,'부모 삭제 요청','cascade REMOVE')+box(790,20,345,115,'연결된 자식 삭제','부모 작업의 전파')+arrow(380,78,770,78)
 inner+=box(10,190,350,115,'부모의 관계에서 제외','orphanRemoval = true')+box(790,190,345,115,'고아 자식 삭제','관계 해제의 의미')+arrow(380,248,770,248)
 return svg('cascade REMOVE는 부모 삭제의 자식 전파이고 orphanRemoval은 관계에서 제외된 자식 삭제입니다',inner,325,'cascade-orphan')
def json_cycle():
 inner=box(10,70,370,130,'AppUser','links 목록')+box(765,70,370,130,'ShortLink','owner 참조')+arrow(400,100,745,100,'사용자 → 링크')+arrow(745,175,400,175,'링크 → 사용자')
 inner+=text(574,275,'직렬화·toString 등이 관계를 계속 따라갈 수 있음',25,'#9b4d25')
 return svg('양방향 객체를 그대로 순회하면 사용자와 링크 참조를 반복해서 따라갈 수 있습니다',inner,310,'json-cycle')
def security_flow():
 inner=linear('Spring Security 필터가 MVC Controller 실행 전에 요청 접근을 검사합니다',[('HTTP 요청','URL · 쿠키 등'),('Security 필터 체인','인증 · 인가 검사'),('DispatcherServlet','Controller 호출')],'security-filter')
 return inner

def login_session():
 inner=box(10,15,335,110,'브라우저','아이디·비밀번호 제출')+box(805,15,330,110,'서버의 인증 처리','계정 조회 · 비밀번호 검증')+arrow(365,70,785,70,'POST /login')
 inner+=box(10,200,335,110,'브라우저 쿠키','세션 ID')+box(805,200,330,110,'서버 세션','SecurityContext · 인증 상태')+arrow(785,255,365,255,'세션 ID 쿠키 전달')
 return svg('로그인 성공 후 브라우저는 세션 ID 쿠키를 받고 서버는 세션에 인증 상태를 유지합니다',inner,330,'session-login')
def context_info():
 inner=box(10,60,335,140,'SecurityContext','현재 인증 정보 보관')+box(410,60,335,140,'Authentication','principal · authorities')+box(810,60,325,140,'principal','인증된 사용자 정보')+arrow(360,130,395,130)+arrow(760,130,795,130)
 inner+=text(574,275,'principal은 AppUser 엔티티 자체라고 가정하지 않음',24,'#087f5b')
 return svg('SecurityContext 안의 Authentication은 principal과 권한 정보를 포함하며 principal이 JPA 엔티티인 것은 아닙니다',inner,310,'security-context')
def ownership_attack():
 inner=box(10,10,355,115,'learner 로그인','인증은 통과')+box(780,10,355,115,'다른 사람 링크 요청','GET /api/links/503')+arrow(385,68,760,68)
 inner+=box(10,205,355,100,'링크 503의 owner_id','102 · 다른 사용자')+box(780,205,355,100,'현재 사용자 id','101 · learner')
 inner+=text(574,184,'로그인 여부만으로 링크 503 접근을 허용하면 안 됨',24,'#9b4d25')
 return svg('로그인한 learner라도 다른 사용자의 링크 ID로 요청하면 소유권 조건으로 차단해야 합니다',inner,325,'ownership')
def csrf_attack():
 inner=box(10,20,350,120,'외부 사이트의 요청','사용자가 원하지 않은 변경')+box(790,20,345,120,'우리 서버','세션 쿠키가 따라올 수 있음')+arrow(380,80,770,80,'브라우저의 요청')
 inner+=box(220,205,710,100,'CSRF 토큰 검증','정상 화면이 받은 토큰인지 요청에서 확인')
 return svg('브라우저가 인증 쿠키를 자동 첨부할 수 있으므로 상태 변경 요청에는 CSRF 토큰 검증이 필요합니다',inner,325,'csrf')

add('2026.11.26 · 4시간','JPA 연관관계와<br>Spring Security 기초',steps('사용자와 단축 URL을 FK와 객체 참조로 연결','연관관계의 주인과 양방향 관계 관리','로그인·권한·본인 데이터 접근 제한'),kind='cover',note='23일 트랜잭션·LAZY·N+1 다음에 이어갑니다. 전체 로그인 서비스를 완성하는 실습이 아니라 기본 구조를 읽고 판단하는 수업입니다.')
add('학습 순서','관계로 연결하고 접근 권한을 검사하기',linear('한 사용자의 단축 URL 관계를 매핑하고 그 데이터를 누가 사용할 수 있는지 검사합니다',[('DB와 객체','FK · 다대일 관계'),('관계의 변경','주인 · 저장 · 삭제'),('요청의 접근','인증 · 인가 · 소유권')])+call('기존 프로젝트의 버전 관리를 따릅니다. <a href="UNDERSTANDING-WORKSHEET.md">이해 확인 작업지 ↗</a>에서 그림과 코드의 이유를 설명해 봅니다.'))
add('이전 내용 연결','관리 객체와 조회 시점을 먼저 확인',table([['질문','전 시간과 연결'],['객체를 바꾸면 바로 확정되는가?','변경 감지 → flush → commit을 구분'],['관계 필드는 모두 읽힌 상태인가?','LAZY는 실제 접근 시 추가 조회 가능'],['DTO만 만들면 N+1이 없어지는가?','아니요. 관계를 읽는 조회 계획도 필요']])+call('오늘은 관계가 어떻게 매핑되는지와 누가 그 관계의 데이터를 사용할 수 있는지로 확장합니다.'))
add('같은 서비스 사례','사용자마다 자기 링크 목록을 가진다면?',steps('learner 사용자는 abc·xyz 링크를 생성','다른 사용자는 def 링크를 생성','내 링크 목록에서는 본인 링크만 조회','공개 단축 주소 이동과 비공개 관리 기능을 구분')+call('사용자와 링크의 관계를 DB에 저장하고, 관리 요청에서 현재 사용자를 확인해야 합니다.'))
add('DB의 관계','owner_id로 어느 사용자의 링크인지 연결',relation_tables()+call('short_links.owner_id → app_users.id를 가리킵니다.<br>표의 ID는 설명용이며 실제 생성 ID를 고정 숫자로 가정하지 않습니다.'))
add('관계의 개수','한쪽에서 몇 개를 참조할까?',table([['관계','예시'],['다대일 · ManyToOne','여러 링크 → 사용자 한 명'],['일대다 · OneToMany','사용자 한 명 → 여러 링크'],['일대일 · OneToOne','사용자와 별도 프로필 정보 등'],['다대다 · ManyToMany','링크와 태그 · 필요하면 연결 Entity로 설계']])+call('오늘은 가장 자주 쓰는 다대일과 그 역방향 일대다를 중심으로 봅니다.'))
add('다대일 단방향','링크 객체가 사용자 객체를 참조',object_links()+call('DB는 owner_id 값, Java는 AppUser 객체 참조로 연결합니다.<br>단방향은 Java에서 어느 쪽으로 탐색할 수 있는지를 뜻합니다.'))
add('사용자 Entity · 발췌','사용자의 ID와 로그인 이름',code('''// jakarta.persistence import · getter 생략
@Entity
@Table(name = "app_users")
public class AppUser {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, unique = true)
    private String username;
    protected AppUser() {}
}
''','app-user')+call('보안 부분에서 비밀번호 해시와 역할 속성을 추가로 연결합니다.<br>로그인 이름은 중복되지 않도록 실제 DB 제약도 확인합니다.'),kind='code-slide')
add('링크 Entity · 관계 필드 발췌','FK를 AppUser 참조에 매핑하기',code('''// ShortLink 내부 · ID·code·originalUrl·기본 생성자·getter 생략
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;
''','link-owner')+call('@ManyToOne은 여러 링크가 사용자 한 명을 참조하는 관계입니다.<br>@JoinColumn은 이 관계에 쓰는 FK 열 이름을 지정합니다.'),kind='code-slide',note='ManyToOne 기본 fetch는 EAGER이므로 LAZY를 명시합니다. JPA 명세상 LAZY는 힌트이며 프록시 가능 여부 등 구현 조건을 확인합니다. optional=false는 관계 필수, nullable=false는 열의 null 허용 매핑이며 빈 문자열 검증과 다릅니다.')
add('단방향 저장 · Service 발췌','기존 사용자에 새 링크 연결하기',code('''@Transactional
public Long createForUser(Long ownerId, String code, String url) {
    AppUser owner = userRepository.findById(ownerId).orElseThrow();
    ShortLink link = new ShortLink(owner, code, url);
    return linkRepository.save(link).getId();
}
''','save-unidirectional')+call('기존 사용자 행을 참조하는 링크를 저장하고 실제 발급 ID를 사용합니다.<br>ownerId는 매핑 설명용 인자입니다. 실제 API에서는 인증 사용자에서 소유자를 결정합니다.'),kind='code-slide',note='생성자는 owner·code·originalUrl을 설정한다고 가정합니다. 주입·import·입력 검증은 생략했습니다. 소유자 공개 setter를 요구하지 않습니다. 소유권 이전은 이번 범위가 아닙니다.')
add('양방향이 필요한 경우','사용자에서도 링크로 탐색하려면?',object_links(True)+call('Java의 역방향 탐색을 추가해도 DB의 owner_id는 하나입니다.<br>필요한 탐색이 있을 때 양방향 관계를 추가합니다.'))
add('역방향 매핑 · AppUser 내부','mappedBy는 반대쪽 필드 이름',code('''// AppUser 내부 · import와 다른 필드 생략
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
''','inverse-links')+table([['표현','의미'],['mappedBy = "owner"','ShortLink.owner가 FK 매핑을 관리'],['owner_id','DB의 열 이름 · mappedBy 값이 아님']]),kind='code-slide')
add('연관관계의 주인','FK를 갱신하는 기준은 ShortLink.owner',owning_side()+call('여기서 “주인”은 FK를 갱신하는 매핑 용어입니다.<br>서비스에서 데이터를 소유한 사용자라는 뜻과 구분합니다.'))
add('변경할 때 주의','역방향 목록만 바꾸면 충분하지 않음',code('''// user.links는 mappedBy가 있는 역방향 목록
user.getLinks().add(link); // 이것만으로 owner FK 설정이 끝나지 않음

// DB에 저장할 관계는 ShortLink.owner에 연결되어 있어야 합니다.
// 두 객체의 참조도 같은 관계를 나타내도록 함께 관리합니다.
''','inverse-only')+call('주인 필드가 비어 있으면 FK가 설정되지 않거나 필수 관계 제약으로 실패할 수 있습니다.<br>Java 목록의 변경과 DB 외래 키의 변경을 같은 것으로 생각하지 않습니다.'),kind='code-slide')
add('신규 링크용 편의 메서드','새 링크의 양쪽 참조를 함께 맞추기',code('''// AppUser 내부 · 신규 링크 생성 전용
public ShortLink addLink(String code, String url) {
    ShortLink link = new ShortLink(this, code, url);
    links.add(link);
    return link;
}
// ShortLink의 패키지 생성자 · Objects import 생략
ShortLink(AppUser owner, String code, String url) {
    this.owner = Objects.requireNonNull(owner);
    this.code = code;
    this.originalUrl = url;
}
''','association-helper')+call('owner 참조와 사용자 목록을 동시에 맞춥니다.<br>소유권 이전 기능은 별도 규칙이 필요하며 이번 메서드의 범위가 아닙니다.'),kind='code-slide')
add('편의 메서드와 저장','관계를 맞춘 뒤 링크를 명시적으로 저장',code('''@Transactional
public Long createForUser(Long ownerId, String code, String url) {
    AppUser owner = userRepository.findById(ownerId).orElseThrow();
    ShortLink link = owner.addLink(code, url);
    return linkRepository.save(link).getId();
}
''','save-helper')+call('이 매핑에는 cascade를 지정하지 않았으므로 링크 저장을 직접 요청합니다.<br>양방향 관계를 맞추는 일과 저장 작업의 전파는 서로 다른 개념입니다.'),kind='code-slide')
add('저장·삭제 전파','cascade는 어떤 작업을 전파할까?',table([['설정','의미'],['기본값 · cascade 없음','관련 Entity의 저장·삭제를 무조건 전파하지 않음'],['PERSIST','부모 persist 작업을 지정한 자식에 전파'],['REMOVE','부모 remove 작업을 지정한 자식에 전파'],['ALL','여러 영속 작업을 포함 · 삭제까지 전파할 수 있음']])+call('링크의 @ManyToOne(owner)에 REMOVE·ALL을 무심코 붙이지 않습니다.<br>링크 하나 삭제가 사용자 삭제로 전파되면 안 됩니다.'),note='cascade 방향은 애너테이션을 지정한 연관관계 방향입니다. SQL의 ON DELETE CASCADE와 같은 설정이 아닙니다.')
add('관계 해제와 삭제','orphanRemoval과 삭제 전파 구분',cascade_orphan()+call('orphanRemoval은 관계에서 제외된 자식을 삭제하는 의미까지 가집니다.<br>사용자와 링크가 어떤 생명주기를 가지는지 먼저 정해야 합니다.'),note='관리 엔티티와 정상 트랜잭션의 자식 관계 변경을 전제로 합니다. 해당 옵션을 기본 코드에 무조건 추가하지 않습니다.')
add('데이터 삭제 정책','사용자가 탈퇴하면 링크는 어떻게 할까?',table([['정책 선택','생각할 결과'],['사용자 삭제 제한','연결된 링크가 있으면 정리 전 삭제를 제한'],['계정 비활성화','사용자 행과 링크 보관 · 접근 정책 별도'],['링크까지 명시적으로 삭제','트랜잭션·기존 단축 주소·복구 요구 확인']])+call('애너테이션이 서비스의 삭제 정책을 대신 정해 주지는 않습니다.<br>사용자 삭제와 링크 공개 여부를 먼저 결정합니다.'))
add('필요한 관계 조회','LAZY와 N+1을 연관관계에 연결',code('''// ShortLinkRepository 내부 · 특정 사용자의 링크와 owner를 함께 읽기
@Query("select l from ShortLink l join fetch l.owner "
        + "where l.owner.id = :ownerId order by l.id")
List<ShortLink> findWithOwner(@Param("ownerId") Long ownerId);
''','fetch-owner')+call('링크마다 owner 이름을 사용할 때 추가 조회가 생기는지 SQL을 확인합니다.<br>필요한 관계를 조회 범위에서 읽고 DTO로 변환합니다.'),kind='code-slide',note='owner 필수 관계를 전제로 inner fetch join을 사용합니다. LAZY가 항상 N+1을 만들거나 EAGER가 해결하는 것은 아닙니다. 앞의 컬렉션 fetch join 페이지 문제와 단일 객체 fetch join을 구분합니다.')
add('양방향 객체의 주의점','Entity를 그대로 순회하면 생기는 문제',json_cycle()+call('응답은 필요한 값을 DTO로 구성합니다.<br>양방향 필드를 포함한 Lombok @Data의 toString·equals·hashCode 자동 생성도 검토합니다.'),note='모든 getter가 나쁘다는 뜻이 아닙니다. 관계를 순회하는 자동 메서드와 JSON 직렬화가 추가 쿼리·재귀를 만들 수 있다는 설명입니다.')
add('관계 이해 확인','FK·주인·메모리 참조를 구분하기',steps('owner_id는 어느 테이블에 있고 무엇을 가리키나요?','mappedBy="owner"는 DB 열인가요, Java 필드인가요?','역방향 목록만 수정하면 왜 충분하지 않을까요?','cascade REMOVE와 orphanRemoval은 언제 삭제를 요청하나요?'))
add('보안으로 연결','관계가 있다고 접근 권한까지 검사되지는 않음',ownership_attack()+call('owner_id는 데이터의 연결 정보입니다.<br>HTTP 요청자가 이 데이터를 볼 권한이 있는지는 별도로 검사해야 합니다.'))
add('Spring Security 기초','인증과 인가는 다른 질문',table([['구분','질문','단축 URL 서비스 예'],['인증 · Authentication','누구인가?','로그인한 learner인가?'],['인가 · Authorization','이 행동을 해도 되는가?','관리자인가? 이 링크의 소유자인가?']])+call('로그인 성공만으로 모든 데이터 접근을 허용하지 않습니다.'))
add('접근 정책','공개 이동과 관리 API를 구분',table([['요청 예시','정책'],['GET /s/abc','공개 단축 주소 이동'],['/api/links/**','로그인한 사용자의 관리 기능'],['/admin/**','관리자 역할 필요'],['로그인한 사용자의 개별 링크','역할 검사에 더해 소유권 검사']])+call('예시 URL은 본인 프로젝트의 실제 경로와 맞춰야 합니다.'))
add('요청 처리 흐름','Security 필터가 Controller보다 먼저 검사',security_flow()+call('Servlet 필터 단계에서 요청을 검사한 뒤 MVC로 넘깁니다.<br>접근이 거부되면 Controller가 실행되기 전에 응답할 수 있습니다.'),note='DelegatingFilterProxy → FilterChainProxy → 선택된 SecurityFilterChain의 필터들로 연결됩니다. 사용자마다 새 SecurityFilterChain을 만든다는 의미가 아닙니다.')
add('로그인 상태 유지','세션 ID는 브라우저, 인증 상태는 서버',login_session()+call('기본 Servlet 구성에서는 보통 JSESSIONID 쿠키를 사용합니다.<br>쿠키에 비밀번호나 AppUser 엔티티 전체를 넣는다는 뜻이 아닙니다.'),note='여기서는 폼 로그인·서버 세션 방식입니다. 로그인 시 세션 ID 변경으로 세션 고정 공격을 방어합니다. JWT는 별도의 후속 주제입니다.')
add('비밀번호 검증','평문을 저장하거나 복호화하지 않기',code('''@Bean
PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
// 저장할 때: passwordEncoder.encode(rawPassword)
// 확인할 때: passwordEncoder.matches(rawPassword, storedHash)
''','password-encoder')+call('같은 원문도 salt 때문에 해시 문자열이 다를 수 있습니다.<br>다시 encode한 문자열끼리 비교하지 않고 matches로 검사합니다.'),kind='code-slide',note='org.springframework.security.crypto.password.PasswordEncoder와 bcrypt.BCryptPasswordEncoder를 사용합니다. 실제 비밀번호와 해시를 로그·응답에 노출하지 않습니다. HTTPS 전송 보호와 비밀번호 해시는 역할이 다릅니다.')
add('계정 데이터와 인증 정보','AppUser와 UserDetails의 역할',table([['대상','역할'],['AppUser Entity','DB의 사용자 id·username·passwordHash·role'],['UserDetailsService','username으로 로그인용 계정 정보를 조회'],['UserDetails','Spring Security가 검증할 사용자·해시·권한 정보'],['PasswordEncoder','제출한 비밀번호와 저장된 해시를 검증']])+call('AppUser에 passwordHash와 role 속성이 있다고 가정합니다.<br>role은 USER·ADMIN 형태이며 비밀번호 해시는 응답 DTO에 넣지 않습니다.'))
add('DB 계정 연동 · Bean 발췌','사용자 이름으로 로그인 정보를 읽기',code('''@Bean
UserDetailsService userDetailsService(AppUserRepository repository) {
    return username -> {
        AppUser user = repository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("계정 없음"));
        return User.withUsername(user.getUsername())
                .password(user.getPasswordHash())
                .roles(user.getRole())
                .build();
    };
}
''','user-details-service')+call('조회에는 Optional<AppUser> findByUsername(String username)을 사용합니다.<br>로그인 시 이 정보와 PasswordEncoder를 이용해 인증을 수행합니다.'),kind='code-slide',note='User는 org.springframework.security.core.userdetails.User입니다. AppUser의 passwordHash·role·getter, Repository와 import는 생략합니다. role은 접두사 없는 USER/ADMIN 값입니다. 계정은 별도 개발 데이터로 준비해야 하며 회원가입 전체 구현을 제공하는 예제가 아닙니다.')
add('설정 전 준비','Security 의존성과 설정 클래스를 준비',code("""// Gradle dependencies 블록 · 버전은 기존 Boot 의존성 관리 사용
implementation 'org.springframework.boot:spring-boot-starter-security'
""",'security-dependency')+table([['준비','확인할 것'],['SecurityConfig','@Configuration 클래스에 Bean 메서드 작성'],['사용자 정보','AppUserRepository · UserDetailsService · PasswordEncoder'],['요청 경로','GET /api/links와 공개 /s/{code}가 실제로 존재']])+call('Java 17+ · Spring Security 6/7의 공통 설정 형태를 사용합니다.<br>조각 코드는 같은 설정 클래스에 연결하며 필요한 import·주입은 생략했습니다.'),kind='code-slide')
add('Security 설정 · 앞부분','URL별 접근 규칙 지정하기',code('''// @Configuration 클래스 내부 · @Bean 메서드 앞부분
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth
            .requestMatchers(HttpMethod.GET, "/s/*", "/csrf").permitAll()
            .requestMatchers("/login", "/error", "/css/**", "/js/**").permitAll()
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .requestMatchers("/api/links/**").authenticated()
            .anyRequest().denyAll());
    // 다음 장표로 이어집니다.
''','security-chain-1')+call('허용할 경로를 구체적으로 정하고 나머지는 거부하는 정책 예시입니다.<br>/s/*는 코드 한 구간이며 /s/** 전체 하위 경로와 다릅니다.'),kind='code-slide',note='Spring Security 6·7 공통 lambda DSL입니다. @Configuration과 필요한 import는 생략합니다. HttpMethod는 org.springframework.http.HttpMethod입니다. 기존 프로젝트의 버전 관리를 따릅니다.')
add('Security 설정 · 뒷부분','폼 로그인·세션·기본 CSRF 보호 사용',code('''    // 앞 장표의 securityFilterChain 메서드 안에서 이어짐
    http.formLogin(form -> form.defaultSuccessUrl("/api/links", true));
    http.logout(Customizer.withDefaults());
    return http.build();
}
''','security-chain-2')+call('GET /api/links가 실제로 존재한다는 전제의 로그인 성공 위치입니다.<br>CSRF 기본 보호를 유지합니다. 세션 로그인을 JWT 방식과 섞지 않습니다.'),kind='code-slide',note='앞·뒤 코드를 같은 메서드로 연결합니다. org.springframework.security.config.Customizer를 사용합니다. 기본 생성 로그인 폼을 이용합니다. 사용자 계정과 PasswordEncoder Bean이 함께 준비되어야 합니다.')
add('규칙 해석','매처 순서와 역할 이름 확인',table([['코드·규칙','의미'],['위에서 먼저 일치한 요청 규칙','구체적인 규칙을 넓은 규칙 앞에 배치'],['hasRole("ADMIN")','기본적으로 ROLE_ADMIN authority 검사'],['hasAuthority("ADMIN")','정확히 ADMIN authority 검사'],['authenticated()','로그인 여부 확인 · 개별 데이터 소유권은 별도']])+call('DB role을 USER·ADMIN으로 저장하고 .roles(...)로 권한을 만드는 현재 예제를 기준으로 봅니다.'))
add('현재 사용자 정보','Authentication은 인증 결과를 담습니다',context_info()+call('세션의 인증 정보를 다음 요청에서 사용할 수 있습니다.<br>요청 body의 userId를 현재 로그인 사용자라고 믿지 않습니다.'),note='Authentication에는 이름·권한·principal 등의 정보가 있습니다. 익명 인증 표현도 있으므로 보호 경로 정책과 함께 설명합니다. 아래 Controller는 authenticated 경로라는 전제입니다.')
add('보호된 Controller · 발췌','인증 정보에서 사용자 이름 받기',code('''@GetMapping("/api/links/{id}")
public LinkResponse findMine(@PathVariable Long id,
        Authentication authentication) {
    return linkService.findMine(id, authentication.getName());
}
''','current-user')+call('Authentication은 Spring Security가 제공한 인증 결과입니다.<br>브라우저가 전달한 임의의 ownerId 대신 인증된 이름을 Service에 전달합니다.'),kind='code-slide',note='Authentication은 org.springframework.security.core.Authentication입니다. Controller 클래스와 주입은 생략합니다. /api/links/**는 인증 필수 경로로 설정되어 있습니다.')
add('Service와 Repository · 발췌','링크 ID와 현재 사용자 ID를 함께 조회',code('''@Transactional(readOnly = true)
public LinkResponse findMine(Long linkId, String username) {
    AppUser user = userRepository.findByUsername(username).orElseThrow();
    ShortLink link = linkRepository.findByIdAndOwnerId(linkId, user.getId())
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    return new LinkResponse(link.getId(), link.getCode(), link.getOriginalUrl());
}
// Repository: Optional<ShortLink> findByIdAndOwnerId(Long id, Long ownerId);
''','ownership-query')+call('다른 사람의 링크 ID를 넣어도 현재 사용자 조건과 일치하지 않으면 반환하지 않습니다.<br>여기서는 조회 실패를 404로 표현하는 정책 예시입니다.'),kind='code-slide',note='LinkResponse는 id·code·originalUrl을 담는 DTO로 가정합니다. HttpStatus·ResponseStatusException import와 주입은 생략합니다. 로그인 후 계정이 삭제된 경우의 별도 인증 실패 처리 정책도 실제 구현에서 정합니다. 메서드는 보호 Controller에서 전달한 인증 이름으로만 호출하는 예입니다.')
add('개별 데이터 인가','로그인 성공과 소유권 검사는 별개',ownership_attack()+call('authenticated()와 ADMIN 역할 검사만으로 모든 링크의 소유권이 보장되지 않습니다.<br>FK 매핑과 요청 접근 검사는 각각 필요합니다.'))
add('응답을 읽는 방법','302·401·403을 상황과 함께 보기',table([['상황','이 수업의 기본 동작·주의점'],['폼 로그인 · 미인증 보호 경로','보통 302로 /login 이동'],['REST API의 401 응답','API용 인증 진입점 정책으로 별도 설계'],['로그인했지만 역할 부족','일반적으로 403'],['CSRF 토큰 없는 변경 요청','미인증 상태여도 먼저 403이 날 수 있음']])+call('fetch는 기본적으로 redirect를 따라갑니다. 로그인 HTML의 200 응답을 API 성공으로 오해하지 않습니다.'))
add('CSRF가 필요한 이유','쿠키가 자동으로 따라가는 요청 주의',csrf_attack()+call('세션 쿠키만으로는 사용자가 의도한 요청인지 구분하기 어렵습니다.<br>정상 화면이 받은 CSRF 토큰을 변경 요청에 포함해 검증합니다.'),note='브라우저의 쿠키 정책과 요청 조건에 따라 전송 여부는 달라질 수 있습니다. SameSite는 방어를 보완하며 토큰 보호를 무조건 대신하는 것으로 설명하지 않습니다.')
add('기본 폼과 로그아웃','permitAll도 CSRF 검사를 면제하지 않음',table([['요청','현재 설정에서 확인할 것'],['기본 생성 로그인 폼','POST /login에 CSRF 토큰 포함'],['POST /api/links','로그인 상태 + 필요한 CSRF 토큰'],['POST /logout','CSRF 토큰과 함께 로그아웃 요청'],['로그인·로그아웃 이후','이전 토큰이 제거되므로 새 토큰을 조회']])+call('GET /logout은 기본 확인 화면이고 실제 로그아웃은 POST로 처리합니다.<br>403을 없애려고 CSRF를 무조건 끄지 않습니다.'))
add('브라우저 요청 정책','CORS와 CSRF는 다른 문제',table([['구분','다루는 문제'],['CORS','다른 출처의 브라우저 코드가 응답을 읽도록 허용할지'],['CSRF','자동 인증 쿠키를 악용한 원치 않는 상태 변경 요청 방어'],['쿠키의 HttpOnly·Secure·SameSite','쿠키 보호·전송 조건 · HTTPS와 함께 검토'],['실제 설정','필요한 출처·인증 방식에 맞게 제한']])+call('CORS 전체 허용이나 CSRF 비활성화를 공통 해결책으로 사용하지 않습니다.'))
add('보안 이해 확인','누구인지와 무엇을 허용할지 설명하기',steps('인증·역할 검사·개별 링크 소유권은 각각 무엇을 확인하나요?','세션 쿠키와 서버의 인증 상태에는 무엇이 들어 있나요?','같은 비밀번호를 다시 encode해 문자열 비교하면 왜 안 될까요?','폼 로그인에서 302와 변경 요청의 403을 어떻게 구분하나요?'))
add('보충 · 같은 출처 JavaScript','CSRF 토큰을 조회하는 작은 엔드포인트',code('''// 별도 @RestController 내부 · CsrfToken import 생략
@GetMapping("/csrf")
public CsrfToken csrf(CsrfToken csrfToken) {
    return csrfToken;
}
''','csrf-endpoint')+call('CsrfToken은 Spring Security가 준비한 토큰 정보입니다.<br>동일 출처 화면이 토큰을 읽고 다음 변경 요청에 전달합니다.'),kind='code-slide',note='org.springframework.security.web.csrf.CsrfToken을 사용합니다. 앞의 GET /csrf permitAll 규칙과 연결됩니다. 별도 교차 출처 허용을 추가하지 않은 동일 출처 전제입니다. API에 세션 쿠키를 쓰는 현재 방식의 보충입니다.')
add('보충 · 같은 출처 JavaScript','변경 요청의 헤더에 CSRF 토큰 전달',code('''const tokenResponse = await fetch("/csrf", { credentials: "same-origin" });
if (!tokenResponse.ok) throw new Error("CSRF 토큰 조회 실패");
const csrf = await tokenResponse.json();
const response = await fetch("/api/links", {
    method: "POST",
    credentials: "same-origin",
    redirect: "error",
    headers: {
        "Content-Type": "application/json",
        [csrf.headerName]: csrf.token
    },
    body: JSON.stringify({ originalUrl: "https://example.com" })
});
if (!response.ok) throw new Error(`요청 실패: ${response.status}`);
''','csrf-fetch')+call('먼저 로그인한 동일 출처 화면에서 사용하는 발췌입니다.<br>로그인 redirect를 성공으로 보지 않습니다. 로그인·로그아웃 뒤 토큰을 새로 받습니다.'),kind='code-slide',note='프론트 전체 구현을 요구하지 않습니다. fetch의 redirect 추적으로 로그인 HTML을 API JSON으로 오해하지 않도록 인증 상태와 응답 형식도 확인합니다. 실제 요청 필드는 프로젝트 API 계약에 맞춥니다.')
add('보충 · 계정 준비','DB 계정은 비밀번호 해시로 준비',table([['필드','개발용 별도 계정 데이터의 예'],['username','중복되지 않는 테스트 로그인 이름'],['passwordHash','PasswordEncoder.encode로 만든 해시'],['role','USER 또는 ADMIN · 현재 예제의 단일 역할'],['응답·로그·Git 저장소','평문 비밀번호와 비밀번호 해시 노출 금지']])+call('개발용 계정을 별도로 준비한 뒤 로그인합니다.<br>회원가입·비밀번호 재설정·토큰 인증 전체 구현은 후속 범위입니다.'),note='계정 생성 코드는 자동 실행하거나 운영 기본 관리자 계정을 추가하지 않습니다. 실제 비밀번호를 Git에 저장하지 않습니다.')
add('수업 정리','연관관계와 접근 권한을 함께 설명',steps('FK를 갱신하는 쪽과 Java 양쪽 참조를 구분','저장·삭제 전파는 서비스의 데이터 정책에 맞게 선택','인증 결과로 현재 사용자를 확인하고 역할·소유권을 검사','세션 로그인에서는 비밀번호 검증과 CSRF 보호를 함께 이해'))
add('공식 자료','연관관계·인증·요청 인가 참고','<div class="references"><a href="https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/ManyToOne.html"><b>Jakarta ManyToOne ↗</b><span>다대일 매핑과 기본 설정</span></a><a href="https://docs.hibernate.org/orm/6.6/userguide/html_single/#associations"><b>Hibernate 연관관계 ↗</b><span>양방향 관계와 생명주기</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/architecture.html"><b>Security Servlet 구조 ↗</b><span>필터 체인과 MVC 앞의 처리</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/authorization/authorize-http-requests.html"><b>요청 인가 ↗</b><span>매처·권한·정책</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/features/authentication/password-storage.html"><b>비밀번호 저장 ↗</b><span>PasswordEncoder</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/exploits/csrf.html"><b>CSRF ↗</b><span>세션·토큰·브라우저 요청</span></a></div>')
add('선택 적용','본인 서비스에서 관계와 접근 범위 정하기',steps('사용자와 단축 URL의 FK·객체 관계를 그려 보기','공개 이동과 로그인 필요한 관리 기능을 구분하기','현재 사용자만 본인 링크를 다루도록 구현 방향 정리'),note='새로운 필수 과제나 추가 제출을 요구하는 장표가 아닙니다. 기존 23일 과제의 제출 조건은 바꾸지 않습니다.')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-26-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1><div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.26</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JPA 연관관계와 Spring Security 기초"><title>11월 26일 · JPA 연관관계와 Spring Security 기초</title><style>'+css+'</style></head><body data-deck-revision="2026-11-26-v1-relations-security"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">{}</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
print(f'Created {len(S)} slides; {out.count("<svg")} native diagrams')
