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
def many_to_many():
 inner=box(10,75,285,120,'ShortLink','id · code')+box(390,40,370,190,'ShortLinkTag','id · link · tag')+box(850,75,285,120,'Tag','id · name')
 inner+=text(575,185,'createdAt · 연결한 시각',22,'#52665a')
 inner+=arrow(375,135,310,135,'N:1')+arrow(775,135,835,135,'N:1')
 inner+=text(574,295,'링크 하나에 여러 태그 · 태그 하나도 여러 링크에 연결',24,'#087f5b')
 return svg('ShortLink와 Tag의 다대다 관계를 ShortLinkTag의 두 다대일 관계로 나눕니다',inner,325,'many-to-many')
def study_relations():
 inner=box(10,10,285,100,'Member','닉네임')+box(10,205,285,100,'MemberProfile','자기소개 · 관심 분야')
 inner+=box(845,10,290,100,'Study','제목 · 설명 · 정원')+box(845,205,290,100,'StudyMeeting','제목 · 일시 · 장소')
 inner+=box(400,150,340,140,'StudyMember','member · study')+text(570,265,'role · status · joinedAt',22,'#52665a')
 inner+=arrow(825,60,315,60,'creator · N:1')+arrow(152,190,152,125)+text(200,165,'1:1',21,'#087f5b')+arrow(990,190,990,125)+text(1040,165,'N:1',21,'#087f5b')
 inner+=arrow(385,190,310,110,'N:1')+arrow(755,190,830,110,'N:1')
 return svg('프로필은 회원과 일대일, 스터디는 개설자와 다대일, 일정은 스터디와 다대일, 가입 정보는 회원과 스터디 각각을 다대일로 참조합니다',inner,325,'study-project')
def security_flow():
 inner=linear('Spring Security 필터가 MVC Controller 실행 전에 요청 접근을 검사합니다',[('HTTP 요청','URL · 쿠키 등'),('Security 필터 체인','인증 · 인가 검사'),('DispatcherServlet','Controller 호출')],'security-filter')
 return inner

def login_session():
 inner=box(10,15,335,110,'브라우저','아이디·비밀번호 제출')+box(805,15,330,110,'서버의 인증 처리','계정 조회 · 비밀번호 검증')+arrow(365,70,785,70,'POST /login')
 inner+=box(10,200,335,110,'브라우저 쿠키','세션 ID')+box(805,200,330,110,'서버 세션','로그인한 사용자 · 권한')+arrow(785,255,365,255,'세션 ID 쿠키 전달')
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

add('2026.11.26 · 4시간','JPA 연관관계와<br>Spring Security 기초',steps('표의 FK와 Java 객체 참조를 같은 예시로 확인','단방향·양방향 관계를 저장하고 읽는 방법','시큐리티 기초와 자율 학습 · 스터디 서비스 과제'),kind='cover')
add('학습 순서','연관관계 예시와 스터디 서비스 개발',linear('수업은 단축 URL 예시로 관계를 익히고, 과제는 새로운 스터디 서비스에 적용합니다',[('JPA 연관관계','표 → 객체 → 저장'),('Security 기초','로그인 · 접근 권한'),('새 프로젝트 과제','스터디 모집 · 모임 관리')])+call('<a href="UNDERSTANDING-WORKSHEET.md">이해 확인 작업지 ↗</a> · 코드와 그림을 보고 결과를 먼저 예상해 봅니다.'))
add('엔티티 매핑 복습','클래스·필드와 테이블·컬럼 연결',table([['Java 쪽 설정','DB에서 연결할 대상'],['@Entity · @Table(name = "app_users")','AppUser 클래스 ↔ app_users 테이블'],['@Id · @GeneratedValue','id 필드 ↔ 기본 키와 값 생성 전략'],['@Column(name = "username")','username 필드 ↔ username 컬럼'],['public 또는 protected 기본 생성자','JPA가 객체를 만들 때 사용']])+call('예제는 jakarta.persistence를 사용한 발췌입니다.<br>nullable·unique 같은 DB 매핑은 요청값 유효성 검사를 대신하지 않습니다.'))
add('표의 번호 읽기','PK는 내 행의 번호, FK는 연결할 행의 번호',table([['종류','이 예시의 값','무엇을 구분하는가?'],['사용자 PK','app_users.id = 101','learner 사용자 행'],['링크 PK','short_links.id = 501','abc 링크 행'],['링크의 FK','short_links.owner_id = 101','abc가 참조하는 사용자 행']])+call('PK는 각 행을 구분하는 고유한 값입니다. 여기서는 숫자 ID를 사용합니다.<br>FK는 다른 행의 키를 참조합니다. 링크 ID 501과 사용자 ID 101은 역할이 다릅니다.'))
add('FK 예시','owner_id가 101인 링크를 찾아보기',relation_tables()+call('learner의 링크는 abc와 xyz입니다. 두 행 모두 owner_id가 101입니다.<br>def는 owner_id가 102이므로 other의 링크입니다. ID는 모두 설명용입니다.'))
add('개수와 탐색 방향','링크 여러 개가 사용자 한 명을 참조',table([['어느 쪽에서 보는가?','관계의 개수'],['abc·xyz 링크 → learner 사용자','여러 개(N) → 한 개(1) · 다대일'],['learner 사용자 → abc·xyz 링크','한 개(1) → 여러 개(N) · 일대다'],['ShortLink에만 owner 필드가 있음','링크에서 사용자로만 탐색 · 단방향'],['AppUser에도 links 필드가 있음','양쪽에서 탐색 · 양방향']])+call('N은 “여러 개”, 1은 “한 개”입니다.<br>방향은 Java 참조로 어디에 접근할 수 있는지를 말합니다.'))
add('Java 객체 예시','두 링크가 같은 사용자 객체를 참조',code("""// 이 예시는 new로 Java 객체만 만듭니다.
AppUser user = new AppUser("learner");
ShortLink first = new ShortLink(user, "abc", "https://example.com/a");
ShortLink second = new ShortLink(user, "xyz", "https://example.com/b");

boolean sameOwner = first.getOwner() == second.getOwner(); // true
first.getOwner().getUsername();        // "learner"
""",'plain-objects')+call('AppUser 생성자는 username을, ShortLink 생성자는 owner·code·originalUrl을 설정한다고 가정합니다.<br>두 owner는 같은 객체를 가리킵니다. new만 했으므로 DB에 저장된 것은 아닙니다.'),kind='code-slide')
add('다대일 단방향 그림','링크에서 사용자로 이동하기',object_links()+call('first.getOwner().getUsername() → learner<br>숫자 ownerId를 직접 넘겨 다시 조회하는 대신 owner 객체를 따라갑니다.'))
add('관계 매핑','owner 객체 참조와 owner_id 컬럼 연결',code("""// ShortLink 내부 · 다른 필드와 기본 생성자 생략
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;
""",'link-owner')+table([['설정','이 예시에서의 뜻'],['@ManyToOne','여러 링크가 같은 사용자 한 명을 참조 가능'],['@JoinColumn(name = "owner_id")','연결 값을 저장할 FK 컬럼 이름'],['FetchType.LAZY','관계 데이터의 조회를 필요할 때까지 미루도록 설정']])+call('Java에는 AppUser owner, DB에는 owner_id 값이 있습니다.<br>optional=false는 필수 관계, nullable=false는 FK 컬럼의 null 불허 매핑입니다.'),kind='code-slide')
add('저장 예시','저장된 사용자에 새 링크 연결하기',code("""// ShortLink 생성자 · java.util.Objects 사용
public ShortLink(AppUser owner, String code, String url) {
    this.owner = Objects.requireNonNull(owner);
    this.code = code;
    this.originalUrl = url;
}
// Service 메서드 내부 · @Transactional 범위
AppUser user = userRepository.findById(ownerId).orElseThrow();
ShortLink link = new ShortLink(user, "abc", "https://example.com/a");
linkRepository.save(link);
""",'save-unidirectional')+call('조회한 사용자의 ID가 101이면 새 링크 행의 owner_id는 101로 저장됩니다.<br>새 링크는 명시적으로 저장합니다. 실제 보호 API에서는 인증 정보로 사용자를 결정합니다.'),kind='code-slide')
add('조회 예시','객체 탐색 결과와 DB 조회 구분하기',table([['코드·질문','예상 결과'],['조회한 abc의 link.getOwner().getUsername()','learner'],['조회한 def의 link.getOwner().getUsername()','other'],['owner 필드를 읽으면 SQL이 항상 한 번뿐인가?','아니요. 초기화 상태와 조회 방식에 따라 추가 조회 가능'],['DTO로 변환하면 관계 조회도 없어지는가?','아니요. DTO를 만들며 관계에 접근할 수도 있음']])+call('객체 참조는 탐색 방법입니다. SQL 횟수를 자동으로 줄이는 기능은 아닙니다.<br>LAZY 접근과 N+1은 지난 시간의 조회 시점 설명과 연결합니다.'))
add('양방향 관계','사용자에서도 링크 목록을 읽으려면?',object_links(True)+call('AppUser에 links를 추가하면 user.getLinks()로 역방향 탐색도 가능합니다.<br>DB FK는 여전히 owner_id 하나입니다. 단방향만으로도 매핑할 수 있습니다.'))
add('역방향 필드','mappedBy에는 owner_id가 아닌 owner',code("""// AppUser 내부 · import와 다른 필드 생략
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
""",'inverse-links')+table([['이름','어디에 있는가?'],['owner','ShortLink의 Java 관계 필드'],['owner_id','short_links의 DB 컬럼'],['mappedBy = "owner"','ShortLink.owner를 기준으로 읽는 역방향 목록']])+call('mappedBy에는 상대 엔티티의 필드 이름을 적습니다.<br>이 목록에만 추가하는 것으로 FK 등록·수정이 결정되지는 않습니다.'),kind='code-slide')
add('연관관계의 주인','FK를 갱신하는 기준은 ShortLink.owner',owning_side()+call('Java 참조는 owner와 links 두 군데, DB FK는 owner_id 한 개입니다.<br>이 다대일 양방향 매핑에서는 ShortLink.owner가 FK 등록·수정의 기준입니다.<br>이때 “주인”은 FK 갱신 기준이며, 실제 서비스를 소유한 사용자를 뜻하지 않습니다.'))
add('주인 필드 변경 예시','목록에 넣기와 FK 변경은 다른 동작',table([['별개의 실험 · 저장된 xyz의 owner_id = 101','flush·commit 후 DB 값'],['other.getLinks().add(xyz)만 실행','owner_id = 101 그대로'],['xyz.owner를 other로 변경','owner_id = 102로 변경'],['양방향 객체 상태까지 맞추려면?','learner 목록에서 제거 + other 목록에 추가도 필요']])+call('관리 상태의 객체와 활성 트랜잭션을 가정한 매핑 원리 예시입니다.<br>실제 사용자 간 링크 이전 기능을 만들라는 뜻은 아닙니다. 다른 실험은 새로 조회해 시작합니다.'))
add('양쪽 참조 관리','새 링크를 만들 때 두 참조를 함께 설정',code("""// AppUser 내부 · 새 링크 생성 전용 편의 메서드
public ShortLink addLink(String code, String url) {
    ShortLink link = new ShortLink(this, code, url); // link.owner 설정
    links.add(link);                              // 내 목록에도 추가
    return link;
}
// Service · 이미 저장된 user를 조회한 트랜잭션 안
ShortLink created = user.addLink("abc", "https://example.com/a");
linkRepository.save(created);
""",'association-helper')+call('편의 메서드는 Java 양쪽 참조를 맞춥니다. save는 새 링크를 저장합니다.<br>새 링크 생성 전용 코드이므로 기존 링크를 다른 사용자로 옮기는 처리는 포함하지 않습니다.'),kind='code-slide')
add('일대일 예시','사용자 한 명에 프로필 하나',table([['관계','예시'],['AppUser ↔ UserProfile','사용자 한 명의 별도 프로필 한 개'],['프로필 테이블의 user_id','어느 사용자의 프로필인지 가리키는 FK'],['user_id에 UNIQUE 제약','같은 사용자에게 프로필 행이 여러 개 생기지 않도록 제한'],['@OneToOne','일대일 매핑 · 역방향이 필요하면 mappedBy 사용']])+call('일대다 단방향으로 다른 테이블의 FK를 관리하는 방식도 있지만,<br>이번에는 FK가 있는 쪽의 @ManyToOne부터 익히고 필요한 탐색만 추가합니다.'))
add('다대다 예시','링크와 태그 사이에 연결 Entity 추가',many_to_many()+call('abc에 Java·공부 태그, xyz에도 Java 태그를 붙일 수 있습니다.<br>ShortLinkTag는 link·tag를 @ManyToOne으로 참조합니다. DB에는 link_id·tag_id와 연결 시각을 저장합니다.'))
add('연관관계 정리','예상한 결과를 설명하기',table([['질문','이유와 답'],['양방향으로 바꾸면 FK도 두 개 필요한가?','아니요. Java 참조만 두 방향이고 DB FK는 하나'],['mappedBy 목록만 바꾸면 FK도 바뀌는가?','아니요. 이 매핑의 기준은 ShortLink.owner'],['처음부터 양방향을 만들어야 하는가?','아니요. 단방향부터 시작하고 필요할 때 역방향 추가']])+call('관계를 맺었다고 저장·삭제가 자동 전파되지는 않습니다.<br>응답은 DTO로 구성하고, 양방향 순환 참조와 관계 조회 시점도 확인합니다.'))
add('Security로 연결','관계 정보와 접근 권한은 별개',ownership_attack()+call('learner로 로그인했어도 other의 링크 503을 관리하도록 허용하면 안 됩니다.<br>owner_id는 데이터 연결 정보이고, 현재 요청자의 권한 검사는 별도입니다.'))
add('Security 기초','인증과 인가',table([['구분','확인할 질문','단축 URL 예시'],['인증','누구인가?','아이디·비밀번호로 learner인지 확인'],['인가','이 행동을 해도 되는가?','관리자 메뉴 접근이나 내 링크 수정 허용'],['로그인 성공 이후','각 데이터까지 확인했는가?','다른 사람 링크 ID로 바꾼 요청도 차단 필요']])+call('이번 수업에서는 기본 개념과 흐름을 봅니다.<br>로그인 구현 세부 설정은 뒤의 자율 학습 순서로 이어갑니다.'))
add('요청 흐름','Security 필터가 Controller보다 먼저 검사',security_flow()+call('먼저 인증·접근 정책을 검사하고, 통과하면 MVC의 Controller로 진행합니다.<br>거부된 요청은 Controller가 실행되기 전에 응답할 수 있습니다.'))
add('세션 로그인','브라우저는 세션 ID, 서버는 인증 상태 보관',login_session()+call('다음 요청에 세션 ID 쿠키가 오면 서버가 기존 로그인 상태를 찾습니다.<br>기본 Servlet 환경에서는 보통 JSESSIONID 쿠키를 사용합니다. 비밀번호를 쿠키에 넣지 않습니다.'))
add('비밀번호 기초','해시를 저장하고 matches로 검사',code("""PasswordEncoder encoder = new BCryptPasswordEncoder();
String hash = encoder.encode("practice-password");

encoder.matches("practice-password", hash); // true
encoder.matches("wrong-password", hash);    // false
""",'password-encoder')+call('Spring Security의 PasswordEncoder·BCryptPasswordEncoder를 사용한 예시입니다.<br>평문을 저장하거나 해시를 복호화하지 않습니다. 새 encode 결과끼리 문자열 비교도 하지 않습니다.'),kind='code-slide')
add('접근 정책 예시','공개 이동과 내 링크 관리를 구분',table([['요청','기본 정책 예시'],['GET /s/abc','공개 · 로그인 없이 원본 URL로 이동'],['/api/links/**','로그인 필요 · 개별 링크는 소유권도 확인'],['/admin/**','관리자 역할 필요'],['현재 사용자 판단','요청 body의 userId 대신 서버의 인증 정보 사용']])+call('URL의 로그인 여부 검사와 개별 데이터의 소유권 검사는 별개입니다.<br>예를 들어 현재 사용자 ID와 링크 ID를 함께 조건으로 조회할 수 있습니다.'))
add('CSRF 기초','로그인 쿠키만으로 요청 의도를 알 수 없음',csrf_attack()+call('세션 쿠키로 인증하는 브라우저의 변경 요청에는 CSRF 토큰도 검증합니다.<br>기본 로그인 폼과 POST 로그아웃에도 적용됩니다. 403을 없애려고 보호를 무조건 끄지 않습니다.'))
add('보안 응답 기초','로그인 이동과 접근 거부 구분',table([['관찰한 응답','확인할 상황'],['302 → /login','폼 로그인에서 미인증 사용자를 로그인 화면으로 이동'],['401','API가 미인증에 401을 응답하도록 별도 설정한 경우'],['403','권한 부족 또는 CSRF 검증 실패 등'],['fetch의 최종 200 HTML','로그인 redirect를 따라온 것은 아닌지 확인']])+call('401·403만 보고 원인을 단정하지 않습니다.<br>요청 메서드, 로그인 상태, 접근 정책, CSRF 토큰을 함께 확인합니다.'))
add('Security 자율 학습','기본 로그인부터 단계적으로 학습',table([['순서','자료와 학습 범위'],['1. 기본 로그인','<a href="https://docs.spring.io/spring-security/reference/servlet/getting-started.html">시작하기 ↗</a> · <a href="https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/form.html">폼 로그인 ↗</a>'],['2. 내 DB 계정 연결','UserDetailsService로 계정 조회 · <a href="https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html">PasswordEncoder ↗</a>'],['3. 접근 정책','<a href="https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html">요청 인가 ↗</a> · 공개/로그인/관리자 경로와 소유권'],['4. 변경 요청 보호','<a href="https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html">CSRF ↗</a> · 정상 토큰을 포함해 요청']])+call('프로젝트의 Spring Boot·Security 버전에 맞는 문서를 선택합니다.<br>JWT는 이 흐름을 이해한 뒤 별도로 학습합니다. JPA 과제의 필수 기능은 아닙니다.'))
add('Security 자율 학습','작게 실행하고 차이를 설명해 보기',steps('기본 로그인 폼에서 로그인 전·후의 보호 경로 응답 비교','공개 단축 주소와 다른 사용자의 링크 관리 권한을 각각 설명','CSRF가 없는 변경 요청의 실패 이유와 정상 토큰 전달 방법 확인')+call('자율 학습용 연습입니다. 보안 구현을 JPA 과제의 필수 조건으로 추가하지 않습니다.'))
add('JPA 과제','스터디 모집·모임 관리 서비스',steps('회원이 스터디를 개설하고 다른 회원이 가입하는 새 프로젝트','스터디별 멤버와 모임 일정을 조회하는 REST API 개발','1단계·2단계는 기본 제출 · 3단계는 선택 심화')+call('별도의 Spring Boot 프로젝트에 Spring Web·Data JPA·사용 DB 드라이버를 추가합니다.<br>기존 환경의 버전을 따르고, 데이터는 DB에 저장합니다.<br>로그인 없이 학습용 memberId로 회원을 선택합니다. 이 값은 인증 정보가 아닙니다.'))
add('JPA 과제 · 관계 설계','다섯 Entity의 관계',study_relations()+call('MemberProfile.member: @OneToOne · member_id에 UNIQUE<br>Study.creator·StudyMeeting.study·StudyMember.member/study: @ManyToOne<br>단방향부터 매핑하고, 필요한 역방향 탐색만 추가합니다.'))
add('1단계 · 기본','회원과 프로필 등록',table([['기능','요구사항'],['회원 등록','닉네임을 가진 Member 생성'],['프로필 등록','자기소개·관심 분야를 가진 MemberProfile을 회원과 함께 등록'],['일대일 관계','회원당 프로필 하나 · 프로필의 member_id에 UNIQUE'],['회원 조회','회원 ID로 닉네임과 프로필 내용을 함께 응답']])+call('회원과 프로필은 하나의 트랜잭션으로 등록합니다.<br>예: 서연 / “Java를 공부합니다” / “백엔드” → 회원과 프로필이 연결되어 조회됩니다.'))
add('1단계 · 기본','스터디 개설과 모임 일정 등록',table([['기능','요구사항'],['스터디 개설','제목·설명·정원(2명 이상)·기존 개설자 지정'],['스터디 목록·상세','스터디 정보와 개설자의 닉네임 응답'],['모임 일정 등록','제목·일시·장소·기존 스터디 지정'],['스터디별 일정 조회','선택한 스터디의 일정만 목록으로 응답']])+call('예: 서연의 Java 스터디에 “연관관계 복습 / 19시 / 강의실” 일정 등록.<br>없는 회원·스터디는 404로 처리합니다. 개설자의 자동 가입은 2단계에서 구현합니다.'))
add('2단계 · 응용','가입 정보로 회원과 스터디 연결',table([['대상','요구사항'],['StudyMember 필드','member·study·role·status·joinedAt'],['스터디 생성 시','개설자를 LEADER·ACTIVE로 자동 가입'],['다른 회원 가입','MEMBER·ACTIVE로 가입 · joinedAt에 최초 가입 시각 저장'],['중복 방지','(study_id, member_id)에 DB UNIQUE 제약']])+call('role은 LEADER/MEMBER, status는 ACTIVE/WITHDRAWN으로 구분합니다.<br>회원↔스터디의 다대다를 가입 정보의 다대일 두 개로 구현합니다.<br>1단계 생성 기능에 자동 가입을 추가하고 같은 트랜잭션으로 처리합니다.'))
add('2단계 · 응용','멤버 조회와 탈퇴 처리',table([['기능','요구사항'],['스터디별 멤버 목록','ACTIVE인 회원의 닉네임·역할 조회'],['회원별 내 스터디 목록','해당 회원이 ACTIVE로 가입한 스터디만 조회'],['일반 멤버 탈퇴','가입 행을 삭제하지 않고 WITHDRAWN으로 변경'],['불가 요청','중복 가입·탈퇴 후 재가입·리더 탈퇴는 409로 거절']])+call('Java 스터디: 서연(LEADER)·민수(MEMBER) → 민수 탈퇴 후 목록에는 서연만 표시.<br>민수의 가입 행은 WITHDRAWN으로 남고, 민수의 내 스터디 목록에서도 제외됩니다.'))
add('3단계 · 선택 심화','정원과 재가입 규칙',table([['선택 기능','요구사항'],['정원 제한','LEADER 포함 ACTIVE 인원이 정원이면 가입 거절 · 재가입에도 적용'],['정원 변경도 구현한다면','현재 ACTIVE 인원보다 작게 변경하는 요청 거절'],['재가입 허용','WITHDRAWN인 기존 행을 ACTIVE로 변경 · 중복 행 생성 금지'],['가입 시각','재가입해도 joinedAt은 최초 가입 시각 유지']])+call('3단계는 선택입니다. 도전한다면 두 장의 기능 중 하나 이상을 구현합니다.<br>예: 정원 3명에 서연·민수·지우가 ACTIVE이면 네 번째 가입은 409로 거절합니다.'))
add('3단계 · 선택 심화','스터디장 위임과 탈퇴',steps('현재 LEADER가 같은 스터디의 다른 ACTIVE 회원에게 역할 위임','기존 리더는 MEMBER, 새 리더는 LEADER로 한 트랜잭션에서 변경','위임을 마친 이전 리더는 일반 멤버와 같이 탈퇴 가능')+call('Study.creator는 최초 개설자로 유지하고 현재 리더는 StudyMember.role로 판단합니다.<br>스터디의 ACTIVE 리더는 한 명을 유지합니다.<br>추가 도전: 동시 가입 요청으로 정원을 초과하는 상황도 해결해 봅니다.'))
add('JPA 과제 · 제출','구현 단계와 연관관계를 PR에 설명',steps('새 Spring 프로젝트를 기존 fork 저장소의 자율 이름 폴더에 추가하고 PR 제출','1·2단계 완료 범위와 3단계 도전 여부·선택 기능을 구분해 작성','PR description에 관계·FK·UNIQUE·트랜잭션·응답 DTO에서 고민한 점 설명')+call('기존 프로젝트는 보존합니다. API 경로·브랜치 이름은 자율입니다.<br>프론트·로그인·테스트 코드 구현은 필수가 아닙니다.<br><a href="https://github.com/sesac-ddm-4-web/sesac-spring-boot-study">공용 저장소 ↗</a>로 PR을 제출합니다.'))

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-26-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1><div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.26</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JPA 연관관계와 Spring Security 기초"><title>11월 26일 · JPA 연관관계와 Spring Security 기초</title><style>'+css+'</style></head><body data-deck-revision="2026-11-26-v4-study-project"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">{}</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
print(f'Created {len(S)} slides; {out.count("<svg")} native diagrams')
