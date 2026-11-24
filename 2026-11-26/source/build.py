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
add('학습 순서','관계로 연결하고 접근 권한을 검사하기',linear('한 사용자의 단축 URL 관계를 매핑하고 그 데이터를 누가 사용할 수 있는지 검사합니다',[('DB와 객체','FK · 다대일 관계'),('관계의 설계','방향 · 주인 · 저장'),('요청의 접근','인증 · 인가 · 소유권')])+call('기존 프로젝트의 버전 관리를 따릅니다. <a href="UNDERSTANDING-WORKSHEET.md">이해 확인 작업지 ↗</a>에서 그림과 코드의 이유를 설명해 봅니다.'))
add('엔티티 매핑 복습','클래스·필드와 테이블·컬럼 연결',table([['매핑','이 예제의 의미'],['@Entity · @Table(name = "app_users")','AppUser 클래스를 app_users 테이블과 연결'],['@Id · @GeneratedValue','id를 PK로 지정하고 생성 전략 적용'],['@Column(name = "username")','username 필드와 컬럼 연결'],['public 또는 protected 기본 생성자','JPA가 객체를 만들 때 사용']])+call('다음 코드들은 jakarta.persistence를 사용한 발췌입니다.<br>컬럼의 nullable·unique 설정은 요청값 유효성 검사를 대신하지 않습니다.'))
add('연관관계가 필요한 이유','사용자 ID 대신 사용자 객체를 참조',table([['ID만 가진 객체','연관관계가 있는 객체'],['Long ownerId','AppUser owner'],['ID로 사용자를 별도 조회','link.getOwner().getUsername()으로 탐색'],['DB에는 owner_id 값 저장','DB에는 동일하게 owner_id 값 저장']])+call('DB는 FK로 연결하고 Java는 객체 참조로 연결합니다.<br>객체 탐색을 제공하는 것이며 SQL이 없어지거나 조회가 항상 한 번이라는 뜻은 아닙니다.'))
add('DB의 관계','owner_id로 어느 사용자의 링크인지 연결',relation_tables()+call('short_links.owner_id → app_users.id를 가리킵니다.<br>learner 사용자의 두 링크가 같은 사용자 행을 참조합니다. ID는 설명용입니다.'))
add('관계의 개수와 방향','다중성과 단방향·양방향',table([['다중성','단축 URL 서비스에서의 예'],['N:1 · @ManyToOne','여러 링크 → 사용자 한 명'],['1:N · @OneToMany','사용자 한 명 → 여러 링크'],['1:1 · @OneToOne','사용자 한 명 ↔ 별도 프로필 하나'],['N:M · @ManyToMany','여러 링크 ↔ 여러 태그']])+call('단방향은 한쪽에만 참조 필드가 있고, 양방향은 양쪽에 있습니다.<br>방향은 Java 객체의 탐색 방향이며 DB FK를 두 개 만든다는 뜻이 아닙니다.'))
add('다대일 단방향','FK를 AppUser 참조에 매핑하기',code('''// ShortLink 내부 · ID·code·originalUrl·기본 생성자·getter 생략
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "owner_id", nullable = false)
private AppUser owner;
''','link-owner')+table([['설정','의미'],['@ManyToOne','여러 링크가 사용자 한 명을 참조'],['@JoinColumn(name = "owner_id")','short_links의 FK 컬럼 이름'],['LAZY','관계 데이터는 실제로 필요할 때 조회하도록 설정']])+call('owner의 타입은 Long이 아니라 AppUser입니다.<br>optional=false는 필수 관계, nullable=false는 FK 컬럼의 null 불허 매핑입니다.'),kind='code-slide')
add('단방향 저장과 조회','기존 사용자에 새 링크 연결하기',code('''@Transactional
public Long createForUser(Long ownerId, String code, String url) {
    AppUser owner = userRepository.findById(ownerId).orElseThrow();
    ShortLink link = new ShortLink(owner, code, url);
    return linkRepository.save(link).getId();
}
// 조회한 링크에서 사용자 탐색: link.getOwner().getUsername()
''','save-unidirectional')+call('생성자는 owner·code·originalUrl을 설정한다고 가정합니다.<br>매핑 설명용 ownerId이며 실제 API는 인증 정보에서 사용자를 결정합니다.'),kind='code-slide')
add('양방향이 필요한 경우','사용자에서도 링크로 탐색하려면?',object_links(True)+call('AppUser.links를 추가하면 사용자 → 링크 탐색도 가능합니다.<br>단방향만으로도 매핑은 가능합니다. 역방향 탐색이 필요할 때 추가합니다.'))
add('역방향 매핑 · AppUser 내부','mappedBy는 반대쪽 필드 이름',code('''// AppUser 내부 · import와 다른 필드 생략
@OneToMany(mappedBy = "owner")
private List<ShortLink> links = new ArrayList<>();
''','inverse-links')+table([['표현','의미'],['mappedBy = "owner"','ShortLink.owner에 연결된 역방향 목록'],['owner_id','DB의 FK 컬럼 이름 · mappedBy 값이 아님']])+call('mappedBy가 있는 목록 자체는 FK 등록·수정의 기준이 아닙니다.'),kind='code-slide')
add('연관관계의 주인','FK를 갱신하는 기준은 ShortLink.owner',owning_side()+call('DB FK는 하나인데 Java 참조는 owner와 links 두 군데입니다.<br>이 N:1 양방향 매핑에서는 FK가 있는 쪽의 owner가 주인입니다.<br>“주인”은 FK 갱신 기준이며 실제 데이터를 소유한 사용자와 다른 용어입니다.'))
add('양방향 관계 관리','주인 필드와 역방향 목록을 함께 설정',code('''// 역방향만 변경하면 FK 설정이 끝나지 않습니다.
user.getLinks().add(link);

// AppUser 내부 · 새 링크 생성 전용 편의 메서드
public ShortLink addLink(String code, String url) {
    ShortLink link = new ShortLink(this, code, url); // owner = this
    links.add(link);
    return link;
}
// Service에서는 linkRepository.save(user.addLink(code, url));
''','association-helper')+call('ShortLink 생성자는 this.owner = Objects.requireNonNull(owner)로 연결합니다.<br>양쪽 참조를 맞추고 새 링크도 명시적으로 저장합니다. 소유권 이전은 별도 설계합니다.'),kind='code-slide')
add('다른 관계를 선택할 때','일대다 단방향과 일대일',table([['선택','설계에서 확인할 점'],['일대다 단방향','FK 직접 매핑 시 사용자 객체가 short_links의 FK를 관리'],['이 수업의 권장 출발점','FK가 있는 링크의 @ManyToOne부터 매핑'],['일대일 · 사용자와 프로필','FK + UNIQUE 제약으로 같은 상대의 중복 연결 방지'],['양방향 일대일','FK를 매핑한 쪽이 주인 · 반대편은 mappedBy']])+call('일대다 단방향은 매핑 방식에 따라 조인 테이블이나 추가 UPDATE가 필요할 수 있습니다.<br>관계의 개수뿐 아니라 FK 위치와 필요한 탐색 방향도 함께 정합니다.'))
add('다대다 관계','링크와 태그 사이에 연결 Entity 추가',many_to_many()+call('ShortLinkTag의 link·tag는 객체 참조이고, DB FK는 link_id·tag_id입니다.<br>연결한 시각(createdAt) 같은 속성이 필요하면 @ManyToMany보다 연결 Entity가 적합합니다.'))
add('관계 정리','매핑·조회·저장을 구분하기',steps('owner_id는 FK, owner는 객체 참조, mappedBy="owner"는 반대쪽 필드 이름','단방향부터 매핑하고 역방향 탐색이 필요하면 양방향 추가','관계가 있다고 저장·삭제가 자동 전파되지는 않음','응답은 DTO 사용 · 양방향 순환 참조와 LAZY·N+1 조회는 따로 확인'))
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
add('수업 정리','연관관계와 접근 권한을 함께 설명',steps('FK를 갱신하는 쪽과 Java 양쪽 참조를 구분','단방향부터 매핑하고 필요한 역방향 탐색만 추가','인증 결과로 현재 사용자를 확인하고 역할·소유권을 검사','세션 로그인에서는 비밀번호 검증과 CSRF 보호를 함께 이해'))
add('공식 자료','연관관계·인증·요청 인가 참고','<div class="references"><a href="https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/ManyToOne.html"><b>Jakarta ManyToOne ↗</b><span>다대일 매핑과 기본 설정</span></a><a href="https://docs.hibernate.org/orm/6.6/userguide/html_single/#associations"><b>Hibernate 연관관계 ↗</b><span>양방향 관계와 생명주기</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/architecture.html"><b>Security Servlet 구조 ↗</b><span>필터 체인과 MVC 앞의 처리</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/authorization/authorize-http-requests.html"><b>요청 인가 ↗</b><span>매처·권한·정책</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/features/authentication/password-storage.html"><b>비밀번호 저장 ↗</b><span>PasswordEncoder</span></a><a href="https://docs.spring.io/spring-security/reference/7.0/servlet/exploits/csrf.html"><b>CSRF ↗</b><span>세션·토큰·브라우저 요청</span></a></div>')
add('선택 적용','본인 서비스에서 관계와 접근 범위 정하기',steps('사용자와 단축 URL의 FK·객체 관계를 그려 보기','공개 이동과 로그인 필요한 관리 기능을 구분하기','현재 사용자만 본인 링크를 다루도록 구현 방향 정리'),note='새로운 필수 과제나 추가 제출을 요구하는 장표가 아닙니다. 기존 23일 과제의 제출 조건은 바꾸지 않습니다.')

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-26-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1><div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.26</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JPA 연관관계와 Spring Security 기초"><title>11월 26일 · JPA 연관관계와 Spring Security 기초</title><style>'+css+'</style></head><body data-deck-revision="2026-11-26-v2-concise-relations"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">{}</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
print(f'Created {len(S)} slides; {out.count("<svg")} native diagrams')
