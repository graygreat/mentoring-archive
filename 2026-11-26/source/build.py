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
def profile_relation():
 inner=box(10,20,420,105,'app_users','id(PK) · username')+box(735,20,400,105,'user_profiles','id(PK) · user_id(FK · UNIQUE)')
 inner+=text(35,190,'101 · learner',25,anchor='start')+text(760,190,'301 · 101',25,anchor='start')+arrow(715,175,450,175,'user_id → id')
 inner+=text(574,270,'다른 프로필 행에 user_id=101을 다시 저장하면 UNIQUE 위반',23,'#9b4d25')
 return svg('프로필 테이블에 사용자 FK를 두고 UNIQUE로 사용자당 프로필 최대 한 행을 보장합니다',inner,300,'one-to-one')
add('2026.11.26 · 4시간','JPA 연관관계와<br>Spring Security 기초',steps('ManyToOne · OneToMany · OneToOne · ManyToMany 비교','관계별 FK·주인·코드를 같은 예시로 확인','보안 개념과 요청 흐름 · 스터디 서비스 과제'),kind='cover')
add('학습 순서','연관관계 네 가지와 보안 개념',linear('관계의 개수와 FK를 읽고, 보안 개념을 이해한 뒤 스터디 서비스에 적용합니다',[('JPA 네 가지 관계','예시 · FK · 주인 · 코드'),('Security 기초','인증 · 인가 · 요청 흐름'),('새 프로젝트 과제','스터디 모집 · 모임 관리')])+call('<a href="UNDERSTANDING-WORKSHEET.md">이해 확인 작업지 ↗</a> · 수업 예시는 단축 URL, 과제는 직접 설계하는 스터디 서비스입니다.'))
add('관계 읽기','내 객체 하나가 상대 몇 개와 연결될까?',table([['매핑','내 객체 하나 → 상대 객체','같은 서비스의 예'],['@ManyToOne','여러 개 중 하나 → 한 개','링크 → 사용자'],['@OneToMany','한 개 → 여러 개','사용자 → 링크 목록'],['@OneToOne','한 개 → 최대 한 개','사용자 ↔ 별도 프로필'],['@ManyToMany','여러 개 ↔ 여러 개','링크 ↔ 태그']])+call('PK는 각 행의 고유한 키, FK는 연결할 행의 키를 참조하는 값입니다.<br>Java는 객체 참조, DB는 FK로 연결합니다. 코드는 jakarta.persistence를 사용한 발췌입니다.'))
add('① ManyToOne · 다대일','여러 링크가 사용자 한 명을 참조',relation_tables()+call('abc와 xyz는 owner_id=101이므로 같은 learner 사용자에 연결됩니다.<br>링크 한 행에는 사용자 한 명의 ID를 저장하면 됩니다. 숫자는 설명용 ID입니다.'))
add('① ManyToOne · 다대일','ShortLink.owner가 owner_id를 매핑',code("""// ShortLink 내부 · 다른 필드·기본 생성자·getter 생략
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;
""",'link-owner')+table([['확인','이 예시의 답'],['FK는 어느 테이블에 있는가?','short_links.owner_id'],['어느 관계 필드가 FK를 매핑하는가?','ShortLink.owner · 이 관계의 주인'],['이후 양방향으로 만든다면?','@ManyToOne인 owner가 FK 등록·수정의 기준']])+call('주인은 사람이나 Entity 전체가 아니라 FK 값을 결정하는 관계 필드입니다.<br>사용자가 링크를 소유한다는 업무 의미와 구분합니다.'),kind='code-slide')
add('① ManyToOne · 다대일','사용자 객체를 연결한 뒤 링크 저장',code("""// Service의 @Transactional 메서드 내부 · 이미 저장된 사용자
AppUser user = userRepository.findById(ownerId).orElseThrow();
ShortLink link = new ShortLink(user, "abc", "https://example.com/a");
linkRepository.save(link);
String username = link.getOwner().getUsername(); // "learner"
""",'save-unidirectional')+call('생성자는 this.owner = Objects.requireNonNull(owner)와 code·originalUrl을 설정한다고 가정합니다.<br>사용자 ID가 101이면 링크의 owner_id에 101이 저장됩니다. new만으로 저장되지는 않습니다.<br>LAZY는 필요할 때 조회하도록 설정하는 것이며 SQL 횟수나 N+1 해결을 보장하지 않습니다.'),kind='code-slide')
add('② OneToMany · 일대다','사용자에서도 링크 목록으로 탐색',object_links(True)+call('user.getLinks()로 사용자 → 링크 탐색을 추가합니다.<br>앞의 ShortLink.owner는 유지합니다. Java 참조는 두 방향, DB FK는 owner_id 하나입니다.'))
add('② OneToMany · 일대다','양방향 목록은 mappedBy로 연결',code("""// AppUser 내부 · java.util.List, ArrayList 사용
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
""",'inverse-links')+table([['이름','무엇을 가리키는가?'],['owner','상대 ShortLink의 Java 관계 필드 이름'],['owner_id','DB 컬럼 이름 · mappedBy 값이 아님'],['mappedBy = "owner"','FK 변경 기준은 반대편 ShortLink.owner라는 뜻']])+call('이 N:1 양방향 매핑에서 AppUser.links는 역방향입니다.<br>목록 변경만으로 FK가 바뀌지는 않습니다. AppUser의 일반 속성 수정까지 금지하는 뜻은 아닙니다.'),kind='code-slide')
add('② OneToMany · 일대다','양쪽 객체 참조를 맞추고 저장',code("""// AppUser 내부 · 새 링크 생성 전용 편의 메서드
public ShortLink addLink(String code, String url) {
    ShortLink link = new ShortLink(this, code, url); // link.owner 설정
    links.add(link);                              // 내 목록에도 추가
    return link;
}
// Service의 @Transactional 메서드 내부 · 저장된 user
ShortLink created = user.addLink("abc", "https://example.com/a");
linkRepository.save(created);
""",'association-helper')+call('목록에만 추가하면 owner_id 설정이 끝나지 않습니다. 주인 필드도 설정해야 합니다.<br>반대로 주인을 바꿔도 이미 읽은 목록이 자동 수정되지는 않으므로 양쪽을 맞춥니다.<br>이 예시에는 cascade가 없어서 새 링크도 명시적으로 저장합니다.'),kind='code-slide')
add('② OneToMany · 일대다','일대다 단방향은 별도의 매핑 방식',code("""// 대안 모델의 AppUser 내부 · ShortLink.owner는 없는 경우
@OneToMany
@JoinColumn(name = "owner_id")
private List<ShortLink> links = new ArrayList<>();
""",'one-to-many-unidirectional')+table([['앞의 양방향 매핑','이 단방향 대안'],['ShortLink.owner가 FK 쓰기 관리','AppUser.links가 링크 테이블의 FK 쓰기 관리'],['목록에 mappedBy="owner"','목록에 @JoinColumn · mappedBy 없음']])+call('두 설정을 같은 필드에 동시에 적용하는 예제가 아닙니다. FK 위치는 모두 링크 테이블입니다.<br>추가 UPDATE 등이 생길 수 있어 이 수업은 다대일을 먼저 매핑하고 필요한 역방향만 추가합니다.'),kind='code-slide')
add('③ OneToOne · 일대일','사용자 한 명에 별도 프로필 하나',profile_relation()+call('이 예시는 프로필 테이블에 user_id를 둡니다. FK는 사용자를 연결하고 UNIQUE는 중복을 막습니다.<br>UNIQUE는 사용자당 프로필이 최대 하나임을 보장하며, 모든 사용자에게 프로필을 자동 생성하지는 않습니다.'))
add('③ OneToOne · 일대일','프로필의 user 필드가 FK를 매핑',code("""// UserProfile 내부 · 다른 필드·기본 생성자 생략
@OneToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "user_id", unique = true, nullable = false)
private AppUser user;

// AppUser 내부 · 역방향 탐색이 필요할 때만 추가
@OneToOne(mappedBy = "user", fetch = FetchType.LAZY)
private UserProfile profile;
""",'one-to-one-mapping')+call('이 예시의 주인은 UserProfile.user입니다. 반대쪽은 mappedBy="user"를 사용합니다.<br>일대일 FK를 어느 테이블에 둘지 먼저 정한 뒤 판단합니다.<br>역방향 일대일의 실제 LAZY 동작은 구현체·설정에 따라 달라질 수 있습니다.'),kind='code-slide')
add('③ OneToOne · 일대일','프로필 저장과 중복 연결 결과',code("""// Service의 @Transactional 메서드 내부
AppUser user = userRepository.findById(userId).orElseThrow();
UserProfile profile = new UserProfile(user, "백엔드를 공부합니다");
profileRepository.save(profile);
String username = profile.getUser().getUsername(); // "learner"
""",'one-to-one-save')+call('생성자는 user·자기소개를 설정한다고 가정합니다. 새 프로필은 명시적으로 저장합니다.<br>이미 user_id=101인 프로필이 있는데 다른 프로필도 101에 연결하면 DB UNIQUE 제약에 걸립니다.<br>역방향 profile까지 사용한다면 Java 양쪽 참조도 직접 맞춰야 합니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','링크와 태그는 서로 여러 개 연결',table([['연결 테이블의 link_id','tag_id','읽는 방법'],['501 · abc','201 · Java','abc에 Java 태그'],['501 · abc','202 · 공부','abc에 공부 태그'],['502 · xyz','201 · Java','xyz에도 Java 태그']])+call('링크 하나에 태그 여러 개, 태그 하나에도 링크 여러 개가 연결됩니다.<br>DB에서는 두 테이블 사이에 연결 테이블이 필요합니다. ID는 설명용입니다.'))
add('④ ManyToMany · 다대다','단순 연결은 @ManyToMany로 매핑 가능',code("""// ShortLink 내부 · Tag는 이미 저장된 Entity라고 가정
@ManyToMany
@JoinTable(name = "link_tag_pairs",
    joinColumns = @JoinColumn(name = "link_id"),
    inverseJoinColumns = @JoinColumn(name = "tag_id"))
private Set<Tag> tags = new HashSet<>();
""",'many-to-many-direct')+call('이 설정에서는 ShortLink.tags가 연결 테이블의 쓰기 관리 기준입니다.<br>양방향이 필요하면 Tag 쪽에 @ManyToMany(mappedBy = "tags")를 추가할 수 있습니다.<br>연결한 시각·상태 같은 추가 속성을 직접 다뤄야 한다면 연결 Entity가 더 적합합니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','연결을 Entity로 만들면 다대일 두 개',many_to_many()+call('ShortLinkTag.link → ShortLink, ShortLinkTag.tag → Tag로 각각 @ManyToOne을 매핑합니다.<br>연결 한 건을 객체로 다루므로 createdAt 같은 속성도 저장할 수 있습니다.<br>이후 코드는 직접 @ManyToMany를 쓰는 앞 방식 대신 선택하는 설계입니다.'))
add('④ ManyToMany · 다대다','연결 Entity의 식별자와 중복 제약',code("""// ShortLinkTag 선언 · 뒤 장표에서 필드가 이어집니다.
@Entity
@Table(name = "short_link_tags", uniqueConstraints =
    @UniqueConstraint(columnNames = {"link_id", "tag_id"}))
public class ShortLinkTag {
    @Id @GeneratedValue
    private Long id;
    // 관계 필드·createdAt·기본 생성자·getter는 다음 장표 또는 생략
}
""",'link-tag-identity')+call('별도 id로 연결 한 건을 구분합니다. (link_id, tag_id)의 UNIQUE로 같은 태그의 중복 연결을 막습니다.<br>@Table 제약은 실제 DB 스키마에도 반영되어 있어야 합니다. 요청값 검사와는 별개입니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','연결 Entity가 FK 두 개를 각각 매핑',code("""// 앞 장표의 ShortLinkTag 클래스 내부
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "link_id", nullable = false)
private ShortLink link;

@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "tag_id", nullable = false)
private Tag tag;

private LocalDateTime createdAt;
""",'link-tag-fields')+call('ShortLinkTag.link와 ShortLinkTag.tag가 각각 자기 관계의 주인입니다.<br>하나의 Entity에도 주인 관계 필드가 여러 개 있을 수 있습니다. 기본 생성자·import는 생략했습니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','저장할 대상은 태그 자체가 아닌 연결 한 건',code("""// Service의 @Transactional 메서드 내부
ShortLink link = linkRepository.findById(linkId).orElseThrow();
Tag tag = tagRepository.findById(tagId).orElseThrow();
ShortLinkTag assigned = new ShortLinkTag(link, tag, LocalDateTime.now());
linkTagRepository.save(assigned);

List<ShortLinkTag> rows = linkTagRepository.findByLinkId(linkId);
// 각 row.getTag().getName()으로 링크의 태그 이름을 읽습니다.
""",'link-tag-save')+call('생성자는 link·tag·createdAt을 설정하며 Repository는 JpaRepository를 확장한다고 가정합니다.<br>조회 메서드는 List&lt;ShortLinkTag&gt; findByLinkId(Long linkId)입니다.<br>양방향 목록은 필요할 때 추가합니다. 새 태그까지 자동 저장·삭제된다고 가정하지 않습니다.'),kind='code-slide')
add('관계별 정리','개수·FK·주인을 나눠 확인',table([['매핑 사례','FK·연결 정보','이 예시의 쓰기 관리 기준'],['N:1 양방향','short_links.owner_id','ShortLink.owner'],['1:N 단방향 대안','short_links.owner_id','AppUser.links'],['1:1 · 프로필에 FK','user_profiles.user_id + UNIQUE','UserProfile.user'],['N:M → 연결 Entity','short_link_tags의 link_id·tag_id','ShortLinkTag.link · ShortLinkTag.tag']])+call('주인은 관계의 쓰기 기준입니다. 중요한 사람·Entity를 고르는 말이 아닙니다.<br>양쪽 Java 참조는 개발자가 맞추고, 응답 DTO와 LAZY·N+1 조회도 따로 확인합니다.'))
# Concept diagrams: simplified Servlet form-login/session and redirect-based web SSO.
def sec_session_flow():
    inner=box(10,0,330,85,'브라우저 · 로그인','아이디·비밀번호 제출')+box(805,0,330,85,'서버 · 로그인 검증','계정·비밀번호 확인')
    inner+=arrow(360,45,785,45,'1. 로그인 요청')
    inner+=box(10,110,330,85,'브라우저 · 쿠키','세션 ID 보관')+box(805,110,330,85,'서버 · 세션','인증 결과 보관')
    inner+=arrow(785,155,360,155,'2. 세션 ID 쿠키 응답')
    inner+=box(10,220,330,85,'브라우저 · 다음 요청','전송 조건에 맞는 쿠키 첨부')+box(805,220,330,85,'서버 · 인증 정보 복원','세션 ID로 상태 확인')
    inner+=arrow(360,265,785,265,'3. 보호 경로 요청')
    return svg('로그인 검증 후 서버가 인증 결과를 보관하고 세션 ID를 쿠키로 응답하며 다음 요청에서 그 ID로 인증 결과를 복원합니다',inner,325,'session-login')

def sec_filter_roundtrip():
    inner=box(10,55,220,105,'브라우저','HTTP 요청')+box(305,55,220,105,'필터 A','예: 요청 기록')+box(600,55,220,105,'필터 B','예: 보안 검사')+box(895,55,240,105,'Servlet','MVC 요청 처리')
    for a,b in [(250,285),(545,580),(840,875)]:inner+=arrow(a,100,b,100)
    inner+=text(574,25,'요청 → A의 앞 처리 → B의 앞 처리 → Servlet',23,'#087f5b')
    inner+=arrow(1000,205,145,205)+text(574,250,'응답은 호출이 끝나는 순서대로 B → A → 브라우저',23,'#087f5b')
    return svg('필터는 chain.doFilter로 다음 필터와 Servlet을 호출하며 반환 시 앞선 필터로 되돌아옵니다',inner,285,'filter-roundtrip')

def sec_proxy_architecture():
    inner=box(10,10,335,110,'DelegatingFilterProxy','컨테이너 → Spring 빈 위임')+box(405,10,335,110,'FilterChainProxy','요청에 맞는 보안 체인 선택')+box(800,10,335,110,'SecurityFilterChain','여러 보안 필터의 묶음')
    inner+=arrow(360,65,390,65)+arrow(755,65,785,65)
    inner+=box(405,205,335,100,'DispatcherServlet','Controller로 요청 전달')
    inner+='<path d="M970,135 V170 H575 V190" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
    inner+=text(725,160,'계속 진행하는 요청',21,'#087f5b')
    return svg('Servlet 필터인 DelegatingFilterProxy가 FilterChainProxy에 위임하고 선택한 보안 필터들을 거친 요청이 MVC로 진행합니다',inner,325,'security-proxies')

def sec_chain_selection():
    inner=box(10,95,300,115,'GET /api/links','FilterChainProxy가 선택')+box(505,5,630,120,'1번 체인 · /api/**','필터 A → 필터 B → 필터 C')
    inner+=box(505,195,630,120,'2번 체인 · /**','필터 D → 필터 E · 이 요청에는 미실행')+arrow(330,140,485,70,'첫 일치')
    return svg('api 경로 요청은 먼저 일치한 1번 체인 하나를 사용하며 그 체인 내부의 여러 필터를 순서대로 실행합니다',inner,325,'security-chain-selection')

def sec_request_paths():
    inner=box(10,5,290,100,'POST /login','아이디·비밀번호 제출')+box(430,5,290,100,'인증 필터','계정·비밀번호 확인')+box(850,5,285,100,'인증 성공 처리','세션 저장 · 화면 이동')
    inner+=arrow(320,55,410,55)+arrow(740,55,830,55)
    names=[('GET /api/links','다음 일반 요청'),('인증 정보 복원','세션의 인증 결과'),('인가 검사','이 요청을 허용할지 판단'),('MVC','업무 처리')]
    for i,(name,desc) in enumerate(names):
        x=10+i*290;inner+=box(x,185,255,100,name,desc)
        if i<3:inner+=arrow(x+265,235,x+280,235)
    return svg('로그인 요청은 인증 필터의 성공 처리로 끝날 수 있고 일반 보호 요청은 인증 정보 복원과 인가를 거쳐 MVC로 진행합니다',inner,310,'security-request-paths')

def sec_sso_flow():
    inner=box(10,10,320,105,'앱 A에 접근','A의 로그인 시작')+box(410,10,320,105,'중앙 인증 서버 · IdP','처음에는 로그인 필요')+box(810,10,325,105,'앱 A','인증 응답 검증 · A 세션')
    inner+=arrow(350,60,390,60)+arrow(750,60,790,60)
    inner+=box(10,200,320,105,'앱 B에 접근','B의 로그인 시작')+box(410,200,320,105,'같은 IdP','기존 로그인 상태 재사용')+box(810,200,325,105,'앱 B','인증 응답 검증 · B 세션')
    inner+=arrow(350,250,390,250)+arrow(750,250,790,250)
    inner+=text(574,160,'브라우저가 로그인 경로로 이동하고 각 앱으로 돌아오는 흐름',22,'#087f5b')
    return svg('앱 A 로그인 후 앱 B도 같은 IdP로 이동하여 기존 인증 상태를 활용하고 각 앱은 자기 세션과 권한을 관리합니다',inner,325,'sso-flow')

add('Security 기초','인증과 인가',table([['구분','확인하는 질문','예시'],['인증 · Authentication','누구인가?','아이디·비밀번호로 learner인지 확인'],['인가 · Authorization','이 요청을 허용할까?','관리자 메뉴 접근 · 내 링크 수정 권한 확인']])+call('로그인에 성공해도 다른 사용자의 링크를 수정할 권한이 생기지는 않습니다.<br>Spring Security는 인증·인가와 여러 웹 보안 기능을 지원합니다.'))
add('로그인 상태','쿠키·세션·인증 정보',table([['용어','어디에 무엇이 있는가?'],['쿠키','브라우저가 보관하고 전송 조건에 맞는 요청에 보내는 값'],['세션','서버가 요청 사이에 유지하는 상태 · 세션 ID로 구분'],['SecurityContext','현재 요청에서 사용할 인증 결과(Authentication)를 담음'],['세션 로그인 예시','브라우저는 세션 ID, 서버 세션은 인증 결과를 보관']])+call('여기서는 웹 브라우저의 폼 로그인·서버 세션 방식을 봅니다.<br>기본 Servlet 환경에서는 보통 JSESSIONID 쿠키를 사용합니다.'))
add('세션 로그인 흐름','로그인 이후에는 세션 ID로 상태 연결',sec_session_flow()+call('다음 요청에서 세션의 인증 결과를 복원해 현재 사용자를 확인합니다.<br>브라우저 쿠키에 비밀번호나 사용자 Entity 전체를 넣는다는 뜻은 아닙니다.'))
add('필터와 체인','Filter는 요청·응답을 처리하는 중간 단계',sec_filter_roundtrip()+call('chain.doFilter(request, response)는 다음 필터 또는 Servlet을 호출합니다.<br>필터는 요청 기록·CORS·보안 등에 쓰이며, 다음 단계로 보내지 않고 응답할 수도 있습니다.'))
add('Spring Security 구조','보안 필터와 MVC가 연결되는 구조',sec_proxy_architecture()+call('DelegatingFilterProxy는 Spring의 보안 처리 빈으로 연결하는 다리입니다.<br>SecurityFilterChain은 Controller가 아니라 보안 필터들의 묶음입니다.'))
add('필터와 체인','체인은 하나 선택하고 내부 필터는 여러 개 실행',sec_chain_selection()+call('설정한 우선순위대로 검사해 처음 일치한 SecurityFilterChain 하나를 선택합니다.<br>선택된 체인 안의 필터들은 정해진 순서로 실행합니다. 체인별 경로와 정책은 직접 설정합니다.'))
add('요청 처리 흐름','로그인 요청과 일반 요청의 처리',sec_request_paths()+call('주요 역할만 묶은 개념도입니다. CSRF 등 다른 필터는 생략했습니다.<br>인가에서 거부되거나 인증 필터가 응답하면 Controller까지 진행하지 않을 수 있습니다.'))
add('기본 보안 기능','비밀번호 검증과 CSRF 보호',table([['기능','무엇을 확인하는가?'],['PasswordEncoder','BCryptPasswordEncoder 등으로 해시 저장 · matches로 원문과 해시 검증'],['비밀번호 비교','해시 복호화나 새 encode 결과의 문자열 비교로 처리하지 않음'],['CSRF 보호','인증 쿠키를 악용한 원치 않는 변경 요청을 토큰 등으로 방어'],['응답 구분','미인증 보호 경로는 폼 로그인에서 보통 302 이동 · API는 정책에 따라 401 · 권한/CSRF 실패는 403 가능']])+call('세션 쿠키 인증에서는 변경 요청의 CSRF 보호도 함께 학습합니다.<br>403의 원인을 단정하거나 보호를 무조건 끄지 않습니다.'))
add('SSO','한 번의 로그인으로 여러 앱 이용',table([['구성 요소','역할'],['SSO · Single Sign-On','중앙의 로그인 상태를 활용해 여러 앱에서 반복 로그인을 줄임'],['IdP · Identity Provider','사용자를 인증하고 앱이 확인할 수 있는 인증 결과 제공'],['각 앱','인증 결과를 검증하고 자기 로그인 상태와 접근 권한을 관리']])+call('예: 회사 포털에 로그인한 뒤 같은 인증 서버를 쓰는 업무 앱을 이용합니다.<br>SSO여도 앱마다 이용 권한이 다를 수 있고, 추가 인증이나 동의가 필요할 수 있습니다.'))
add('SSO 흐름','앱 A 다음 앱 B에서 로그인할 때',sec_sso_flow()+call('일반적인 리다이렉트 기반 웹 SSO의 개념도입니다.<br>앱끼리 비밀번호를 전달하거나 모든 도메인이 같은 쿠키를 공유하는 구조가 아닙니다.'))
add('보안 용어 구분','SSO·OAuth 2.0·OIDC·JWT',table([['용어','서로 다른 역할'],['SSO','여러 앱에서 로그인 상태를 활용하는 사용자 경험·구성'],['OAuth 2.0','다른 서비스 자원에 대한 제한된 접근을 위임하는 인가 프레임워크'],['OpenID Connect · OIDC','OAuth 2.0 위에서 사용자 인증과 신원 정보를 전달하는 표준'],['JWT','정보를 담는 토큰 형식 · 그 자체가 로그인이나 SSO를 완성하지는 않음']])+call('소셜 로그인은 외부 계정으로 로그인하는 기능이며 SSO와 같은 뜻은 아닙니다.<br>SSO는 OIDC나 SAML 등으로 구성할 수 있습니다.'))
add('Security 자율 학습','개념을 확인한 뒤 작은 기능부터 구현','<div class="references"><a href="https://docs.spring.io/spring-security/reference/servlet/getting-started.html"><b>1. 기본 로그인 ↗</b><span>폼 로그인과 로그인 전·후 요청</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html"><b>2. 세션과 인증 상태 ↗</b><span>저장과 다음 요청의 복원</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/architecture.html"><b>3. 필터 체인 구조 ↗</b><span>위임 · 체인 선택 · 필터 실행</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html"><b>4. 요청 인가 ↗</b><span>공개·로그인·관리자 경로와 데이터 권한</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/oauth2/login/core.html"><b>5. 외부 계정 로그인 ↗</b><span>OAuth 2.0 Login · OIDC</span></a><a href="https://openid.net/developers/how-connect-works/"><b>6. OpenID Connect ↗</b><span>앱과 중앙 인증 서버의 역할</span></a></div>'+call('프로젝트 버전에 맞는 문서를 사용합니다. Security 구현은 스터디 과제의 필수 조건이 아닙니다.'))

add('JPA 과제','스터디 모집·모임 관리 서비스',table([['핵심 기능','만들 서비스'],['회원·프로필','회원 정보와 자기소개 관리'],['스터디','스터디 개설과 목록·상세 조회'],['참여','스터디 참여·탈퇴와 참여 목록 조회'],['모임 일정','스터디별 일정 등록·조회']])+call('회원들이 스터디를 만들고 참여하며 모임 일정을 관리하는 새 REST API 프로젝트입니다.<br>기능에 필요한 데이터와 구체적인 동작은 직접 설계합니다.'))
add('JPA 과제 · 자율 설계','연관관계와 서비스 규칙 정하기',steps('Entity 구성·필드·API를 직접 설계','일대일·일대다/다대일·여러 회원과 여러 스터디의 관계를 JPA로 표현','관계 방향·FK와 가입 정보의 표현 방식을 결정하고 이유 정리','중복 참여·정원·탈퇴 등 서비스 규칙을 직접 정의')+call('여력이 있다면 재가입·스터디장 위임 등 원하는 기능을 확장해 봅니다.<br>선택한 관계와 규칙이 서비스 동작에 맞는지 설명할 수 있어야 합니다.'))
add('JPA 과제 · 제출','구현 내용과 설계 이유를 PR에 설명',steps('새 Spring Boot 프로젝트에서 JPA로 DB에 저장하고 기능 구현','기존 fork 저장소의 자율 이름 폴더에 추가하고 공용 저장소로 PR 제출','PR에 구현 기능·Entity 관계도·관계와 트랜잭션 설계 이유·직접 정한 규칙 작성')+call('프로젝트 구조·API·브랜치 이름은 자율입니다. 기존 프로젝트는 보존합니다.<br>로그인·프론트는 선택이며 테스트 코드 구현은 필수가 아닙니다.<br><a href="https://github.com/sesac-ddm-4-web/sesac-spring-boot-study">공용 저장소 ↗</a>'))

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-26-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1><div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.26</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JPA 연관관계와 Spring Security 기초"><title>11월 26일 · JPA 연관관계와 Spring Security 기초</title><style>'+css+'</style></head><body data-deck-revision="2026-11-26-v8-four-cases-security-concepts"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">{}</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
print(f'Created {len(S)} slides; {out.count("<svg")} native diagrams')
