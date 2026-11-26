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
 inner=box(10,15,390,90,'studies · 스터디','id(PK) · title')+box(630,15,505,90,'study_meetings · 모임 일정','id(PK) · title · study_id(FK)')
 for y,a,b in [(155,'201 · Java','501 · 연관관계 복습 · 201'),(215,'202 · SQL','502 · 쿼리 연습 · 201'),(275,'','503 · SQL 문제 풀이 · 202')]:
  inner+=text(35,y,a,24,anchor='start')+text(650,y,b,23,anchor='start')
 inner+=arrow(610,148,420,148)+'<path d="M610,208 H520 V155 H420" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 return svg('study_id가 201인 두 모임 일정은 Java 스터디에 연결됩니다. 숫자는 설명용 식별자입니다',inner,310,'relation-tables')
def object_studies():
 inner=box(10,75,365,135,'Study 객체','id=201 · Java')+box(745,10,390,110,'StudyMeeting 객체','연관관계 복습 · study')+box(745,190,390,110,'StudyMeeting 객체','쿼리 연습 · study')
 inner+='<path d="M730,65 H560 V125 H390" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M730,245 H590 V165 H390" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M390,95 H500 V25 H730" fill="none" stroke="#9b4d25" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+=text(525,290,'meetings는 역방향 탐색 · DB FK는 study_id 하나',23,'#9b4d25')
 return svg('모임 일정의 study 참조와 스터디의 meetings 목록으로 양쪽에서 탐색합니다',inner,325,'bidirectional')
def ownership_conflict():
 inner=box(10,15,300,115,'Java 스터디 · 201','모임의 study가 가리킴')+box(430,75,340,125,'StudyMeeting · 501','study = Java(201)')
 inner+=box(10,205,300,115,'SQL 스터디 · 202','meetings에 모임 501 포함')+box(840,95,295,125,'DB의 study_id','201 또는 202?')
 inner+='<path d="M415,125 H355 V75 H325" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+='<path d="M325,260 H385 V175 H415" fill="none" stroke="#9b4d25" stroke-width="3" marker-end="url(#arrow)"/>'
 inner+=text(560,260,'목록에도 같은 모임을 참조',22,'#9b4d25')+arrow(785,140,825,140)
 return svg('모임의 study는 Java 스터디를 가리키지만 SQL 스터디의 meetings에도 같은 모임이 있어 두 Java 참조가 불일치합니다. DB study_id는 한 값만 저장합니다',inner,325,'owning-conflict')
def many_to_many():
 inner=box(10,75,285,120,'Member','id · nickname')+box(390,40,370,190,'StudyMember','id · member · study')+box(850,75,285,120,'Study','id · title')
 inner+=text(575,185,'joinedAt · 가입한 시각',22,'#52665a')
 inner+=arrow(375,135,310,135,'N:1')+arrow(775,135,835,135,'N:1')
 inner+=text(574,295,'회원 한 명이 여러 스터디 · 스터디 하나에 여러 회원',24,'#087f5b')
 return svg('Member와 Study의 다대다 관계를 StudyMember의 두 다대일 관계로 나눕니다',inner,325,'many-to-many')
def profile_relation():
 inner=box(10,20,420,105,'members','id(PK) · nickname')+box(735,20,400,105,'member_profiles','id(PK) · member_id(FK · UNIQUE)')
 inner+=text(35,190,'101 · 서연',25,anchor='start')+text(760,190,'301 · 101',25,anchor='start')+arrow(715,175,450,175,'member_id → id')
 inner+=text(574,270,'다른 프로필 행에 member_id=101을 다시 저장하면 UNIQUE 위반',23,'#9b4d25')
 return svg('프로필 테이블에 회원 FK를 두고 UNIQUE로 회원당 프로필 최대 한 행을 보장합니다',inner,300,'one-to-one')
add('2026.11.26 · 4시간','JPA 연관관계와<br>Spring Security 기초',steps('ManyToOne · OneToMany · OneToOne · ManyToMany 비교','스터디 서비스 예시로 FK·주인·코드 확인','보안 개념과 요청 흐름 · 스터디 서비스 과제'),kind='cover')
add('학습 순서','스터디 서비스로 배우는 네 가지 관계',linear('모임 일정·스터디·회원·프로필의 관계를 살펴보고 보안 개념으로 이어갑니다',[('JPA 네 가지 관계','예시 · FK · 주인 · 코드'),('Security 기초','인증 · 인가 · 요청 흐름'),('프로젝트 과제','스터디 모집 · 모임 관리')])+call('<a href="UNDERSTANDING-WORKSHEET.md">이해 확인 작업지 ↗</a> · 관계 이해용 예시이며, 과제의 Entity 구성과 서비스 규칙은 자율입니다.'))
add('관계 읽기','내 객체 하나가 상대 몇 개와 연결될까?',table([['매핑','관계의 개수','스터디 서비스의 예'],['@ManyToOne','여러 모임이 같은 스터디를 참조','모임 일정 → 스터디'],['@OneToMany','스터디 하나에 모임 여러 개','스터디 → 모임 일정 목록'],['@OneToOne','회원 하나에 프로필 최대 하나','회원 ↔ 별도 프로필'],['@ManyToMany','양쪽 모두 여러 개와 연결','회원 ↔ 스터디']])+call('PK는 각 행의 고유한 키, FK는 연결할 행의 키를 참조하는 값입니다.<br>Java는 객체 참조, DB는 FK로 연결합니다. 코드는 jakarta.persistence를 사용한 발췌입니다.'))
add('① ManyToOne · 다대일','여러 모임 일정이 스터디 하나를 참조',relation_tables()+call('연관관계 복습과 쿼리 연습은 study_id=201이므로 같은 Java 스터디에 연결됩니다.<br>모임 일정 한 행에는 스터디 하나의 ID를 저장하면 됩니다. 숫자는 설명용 ID입니다.'))
add('① ManyToOne · 다대일','StudyMeeting.study가 study_id를 매핑',code("""// StudyMeeting 내부 · 다른 필드·기본 생성자·getter 생략
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "study_id", nullable = false)
private Study study;
""",'meeting-study')+table([['확인','이 예시의 답'],['FK는 어느 테이블에 있는가?','study_meetings.study_id'],['어느 관계 필드가 FK를 매핑하는가?','StudyMeeting.study · 이 관계의 주인'],['이후 양방향으로 만든다면?','@ManyToOne인 study가 FK 등록·수정의 기준']])+call('주인은 사람이나 Entity 전체가 아니라 FK 값을 결정하는 관계 필드입니다.<br>스터디장이 모임을 관리한다는 업무 의미와 구분합니다.'),kind='code-slide')
add('① ManyToOne · 다대일','스터디 객체를 연결한 뒤 모임 일정 저장',code("""// Service의 @Transactional 메서드 내부 · 이미 저장된 스터디
Study study = studyRepository.findById(studyId).orElseThrow();
StudyMeeting meeting = new StudyMeeting(study, "연관관계 복습");
meetingRepository.save(meeting);
String title = meeting.getStudy().getTitle(); // "Java"
""",'save-meeting')+call('생성자는 this.study = Objects.requireNonNull(study)와 title을 설정한다고 가정합니다.<br>스터디 ID가 201이면 모임의 study_id에 201이 저장됩니다. new만으로 저장되지는 않습니다.<br>LAZY는 필요할 때 조회하도록 설정하는 것이며 SQL 횟수나 N+1 해결을 보장하지 않습니다.'),kind='code-slide')
add('① ManyToOne · 다대일','다대일 단방향부터 시작하는 이유',table([['출발점','스터디 서비스에서의 의미'],['StudyMeeting.study만 먼저 작성','모임의 소속 스터디를 연결·저장·탐색할 수 있음'],['FK와 관계 필드가 직접 대응','study_meetings.study_id ↔ StudyMeeting.study'],['처음에는 한쪽 참조만 관리','양쪽 객체의 내용이 어긋나는 실수를 줄임']])+code("""// StudyMeetingRepository에 직접 선언하는 조회 메서드
List<StudyMeeting> findByStudyId(Long studyId);
""",'find-meetings-by-study')+call('목록 필드가 없어도 Repository로 해당 스터디의 모임들을 조회할 수 있습니다.<br>스터디 객체에서 목록으로 직접 탐색할 필요가 생기면 @OneToMany(mappedBy = "study")를 추가합니다.'),kind='code-slide')
add('② OneToMany · 일대다','스터디에서도 모임 일정 목록으로 탐색',object_studies()+call('study.getMeetings()로 스터디 → 모임 일정 탐색을 추가합니다.<br>앞의 StudyMeeting.study는 유지합니다. Java 참조는 두 방향, DB FK는 study_id 하나입니다.'))
add('② OneToMany · 일대다','두 객체가 다른 소속을 가리킨다면?',ownership_conflict()+call('같은 모임 501인데 meeting.study는 Java, SQL.meetings 목록도 이 모임을 가리킵니다.<br>두 참조가 서로 다르지만 DB의 study_id에는 한 값만 저장할 수 있어 기준이 필요합니다.'))
add('② OneToMany · 일대다','모임의 소속 설정과 스터디 목록 추가',code("""// 생성자는 meeting.study만 설정 · javaStudy.meetings는 처음에 빈 목록
StudyMeeting meeting = new StudyMeeting(javaStudy, "연관관계 복습"); // ①
javaStudy.getMeetings().add(meeting); // ②
""",'set-both-references')+table([['작업 후','meeting.study','javaStudy.meetings'],['① 후','Java 스터디','빈 목록'],['② 후','Java 스터디','해당 모임 포함']])+call('①은 주인 meeting.study를 설정합니다. 저장할 때 FK의 기준이며, 현재 Java 목록은 비어 있습니다.<br>②는 목록에 추가하는 작업입니다. 이 목록만으로 FK를 결정하지 않습니다.<br>javaStudy는 저장된 스터디입니다. 두 줄은 객체 상태 설정이며 새 모임 저장은 별도로 필요합니다.'),kind='code-slide')
add('② OneToMany · 일대다','양방향 목록은 mappedBy로 연결',code("""// Study 내부 · java.util.List, ArrayList 사용
@OneToMany(mappedBy = "study")
private List<StudyMeeting> meetings = new ArrayList<>();
""",'inverse-meetings')+table([['이름','무엇을 가리키는가?'],['study','상대 StudyMeeting의 Java 관계 필드 이름'],['study_id','DB 컬럼 이름 · mappedBy 값이 아님'],['mappedBy = "study"','FK 변경 기준은 반대편 StudyMeeting.study라는 뜻']])+call('이 N:1 양방향 매핑에서 Study.meetings는 역방향입니다.<br>목록 변경만으로 FK가 바뀌지는 않습니다. Study의 일반 속성 수정까지 금지하는 뜻은 아닙니다.'),kind='code-slide')
add('② OneToMany · 일대다','양쪽 객체 참조를 맞추고 저장',code("""// Study 내부 · 새 모임 일정 생성 전용 편의 메서드
public StudyMeeting addMeeting(String title) {
    StudyMeeting meeting = new StudyMeeting(this, title); // meeting.study 설정
    meetings.add(meeting);                              // 내 목록에도 추가
    return meeting;
}
// Service의 @Transactional 메서드 내부 · 저장된 study
StudyMeeting created = study.addMeeting("연관관계 복습");
meetingRepository.save(created);
""",'association-helper')+call('목록에만 추가하면 study_id 설정이 끝나지 않습니다. 주인 필드도 설정해야 합니다.<br>반대로 주인을 바꿔도 이미 읽은 목록이 자동 수정되지는 않으므로 양쪽을 맞춥니다.<br>이 예시에는 cascade가 없어서 새 모임 일정도 명시적으로 저장합니다.'),kind='code-slide')
add('② OneToMany · 일대다','일대다 단방향은 별도의 매핑 방식',code("""// 대안 모델의 Study 내부 · StudyMeeting.study는 없는 경우
@OneToMany
@JoinColumn(name = "study_id")
private List<StudyMeeting> meetings = new ArrayList<>();
""",'one-to-many-unidirectional')+table([['앞의 양방향 매핑','이 단방향 대안'],['StudyMeeting.study가 FK 쓰기 관리','Study.meetings가 모임 테이블의 FK 쓰기 관리'],['목록에 mappedBy="study"','목록에 @JoinColumn · mappedBy 없음']])+call('두 설정을 같은 필드에 동시에 적용하는 예제가 아닙니다. FK 위치는 모두 모임 테이블입니다.<br>추가 UPDATE 등이 생길 수 있어 이 수업은 다대일을 먼저 매핑하고 필요한 역방향만 추가합니다.'),kind='code-slide')
add('③ OneToOne · 일대일','회원 한 명에 별도 프로필 하나',profile_relation()+call('이 예시는 프로필 테이블에 member_id를 둡니다. FK는 회원을 연결하고 UNIQUE는 중복을 막습니다.<br>UNIQUE는 회원당 프로필이 최대 하나임을 보장하며, 모든 회원에게 프로필을 자동 생성하지는 않습니다.'))
add('③ OneToOne · 일대일','프로필의 member 필드가 FK를 매핑',code("""// MemberProfile 내부 · 다른 필드·기본 생성자 생략
@OneToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "member_id", unique = true, nullable = false)
private Member member;

// Member 내부 · 역방향 탐색이 필요할 때만 추가
@OneToOne(mappedBy = "member", fetch = FetchType.LAZY)
private MemberProfile profile;
""",'one-to-one-mapping')+call('이 예시의 주인은 MemberProfile.member입니다. 반대쪽은 mappedBy="member"를 사용합니다.<br>일대일 FK를 어느 테이블에 둘지 먼저 정한 뒤 판단합니다.<br>역방향 일대일의 실제 LAZY 동작은 구현체·설정에 따라 달라질 수 있습니다.'),kind='code-slide')
add('③ OneToOne · 일대일','프로필 저장과 중복 연결 결과',code("""// Service의 @Transactional 메서드 내부
Member member = memberRepository.findById(memberId).orElseThrow();
MemberProfile profile = new MemberProfile(member, "백엔드를 공부합니다");
profileRepository.save(profile);
String nickname = profile.getMember().getNickname(); // "서연"
""",'one-to-one-save')+call('생성자는 member·자기소개를 설정한다고 가정합니다. 새 프로필은 명시적으로 저장합니다.<br>이미 member_id=101인 프로필이 있는데 다른 프로필도 101에 연결하면 DB UNIQUE 제약에 걸립니다.<br>역방향 profile까지 사용한다면 Java 양쪽 참조도 직접 맞춰야 합니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','회원과 스터디는 서로 여러 개 연결',table([['연결 테이블의 member_id','study_id','읽는 방법'],['101 · 서연','201 · Java','서연이 Java 스터디에 참여'],['102 · 민수','201 · Java','민수도 Java 스터디에 참여'],['102 · 민수','202 · SQL','민수는 SQL 스터디에도 참여']])+call('회원 한 명이 스터디 여러 개, 스터디 하나에도 회원 여러 명이 연결됩니다.<br>DB에서는 두 테이블 사이에 연결 테이블이 필요합니다. ID는 설명용입니다.'))
add('④ ManyToMany · 다대다','단순 연결은 @ManyToMany로 매핑 가능',code("""// Member 내부 · Study는 이미 저장된 Entity라고 가정
@ManyToMany
@JoinTable(name = "member_study_pairs",
    joinColumns = @JoinColumn(name = "member_id"),
    inverseJoinColumns = @JoinColumn(name = "study_id"))
private Set<Study> studies = new HashSet<>();
""",'many-to-many-direct')+call('이 설정에서는 Member.studies가 연결 테이블의 쓰기 관리 기준입니다.<br>양방향이 필요하면 Study 쪽에 @ManyToMany(mappedBy = "studies")를 추가할 수 있습니다.<br>가입한 시각 같은 추가 속성을 직접 다뤄야 한다면 연결 Entity가 더 적합합니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','가입을 Entity로 만들면 다대일 두 개',many_to_many()+call('StudyMember.member → Member, StudyMember.study → Study로 각각 @ManyToOne을 매핑합니다.<br>가입 한 건을 객체로 다루므로 joinedAt 같은 속성도 저장할 수 있습니다.<br>이후 코드는 직접 @ManyToMany를 쓰는 앞 방식 대신 선택하는 설계입니다.'))
add('④ ManyToMany · 다대다','가입 Entity의 식별자와 중복 제약',code("""// StudyMember 선언 · 뒤 장표에서 필드가 이어집니다.
@Entity
@Table(name = "study_members", uniqueConstraints =
    @UniqueConstraint(columnNames = {"member_id", "study_id"}))
public class StudyMember {
    @Id @GeneratedValue
    private Long id;
    // 관계 필드·joinedAt·기본 생성자·getter는 다음 장표 또는 생략
}
""",'study-member-identity')+call('별도 id로 가입 한 건을 구분합니다. (member_id, study_id)의 UNIQUE로 같은 스터디의 중복 참여를 막습니다.<br>@Table 제약은 실제 DB 스키마에도 반영되어 있어야 합니다. 요청값 검사와는 별개입니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','가입 Entity가 FK 두 개를 각각 매핑',code("""// 앞 장표의 StudyMember 클래스 내부
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "member_id", nullable = false)
private Member member;

@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "study_id", nullable = false)
private Study study;

private LocalDateTime joinedAt;
""",'study-member-fields')+call('StudyMember.member와 StudyMember.study가 각각 자기 관계의 주인입니다.<br>하나의 Entity에도 주인 관계 필드가 여러 개 있을 수 있습니다. 기본 생성자·import는 생략했습니다.'),kind='code-slide')
add('④ ManyToMany · 다대다','저장할 대상은 스터디 가입 한 건',code("""// Service의 @Transactional 메서드 내부
Member member = memberRepository.findById(memberId).orElseThrow();
Study study = studyRepository.findById(studyId).orElseThrow();
StudyMember joined = new StudyMember(member, study, LocalDateTime.now());
studyMemberRepository.save(joined);

List<StudyMember> rows = studyMemberRepository.findByMemberId(memberId);
// 각 row.getStudy().getTitle()로 회원이 참여한 스터디 이름을 읽습니다.
""",'study-member-save')+call('생성자는 member·study·joinedAt을 설정하며 Repository는 JpaRepository를 확장한다고 가정합니다.<br>조회 메서드는 List&lt;StudyMember&gt; findByMemberId(Long memberId)입니다.<br>양방향 목록은 필요할 때 추가합니다. 새 스터디까지 자동 저장·삭제된다고 가정하지 않습니다.'),kind='code-slide')
add('관계별 정리','개수·FK·주인을 나눠 확인',table([['매핑 사례','FK·연결 정보','이 예시의 쓰기 관리 기준'],['N:1 양방향','study_meetings.study_id','StudyMeeting.study'],['1:N 단방향 대안','study_meetings.study_id','Study.meetings'],['1:1 · 프로필에 FK','member_profiles.member_id + UNIQUE','MemberProfile.member'],['N:M → 가입 Entity','study_members의 member_id·study_id','StudyMember.member · StudyMember.study']])+call('관계의 실제 개수에 맞게 매핑합니다. 일대일·다대다를 무조건 다대일 하나로 바꾸지는 않습니다.<br>일대다 관계는 다대일 단방향부터 시작하고, 필요한 역방향 탐색을 추가합니다.<br>양쪽 Java 참조는 개발자가 맞추고, DTO와 LAZY·N+1 조회도 따로 확인합니다.'))
add('객체지향 설계','객체의 책임과 참조 방향',table([['객체·계층','스터디 종료 기능에서 맡을 일'],['Study','자기 상태와 종료 가능 여부 판단'],['StudyMeeting','자기 일정의 취소 조건 판단·상태 변경'],['Service','필요한 객체 조회·권한 확인 조율·작업 순서·트랜잭션 경계'],['Repository','조건에 맞는 객체 조회와 저장']])+call('연결을 저장하는 방법을 봤으니, 이제 각 객체에 어떤 일을 맡길지 봅니다.<br>이 책임 분리는 하나의 설계 예시입니다. 맡은 일을 하려면 누구를 알아야 할지 생각합니다.<br>FK 쓰기 기준인 연관관계의 주인과 업무 책임은 별개입니다.<br>이 예시의 Entity에는 HTTP 요청 처리나 Repository 조회 코드를 넣지 않습니다.'))
add('객체지향 설계','상태 변경과 캡슐화',code("""// StudyMeeting 내부 · 필드·enum 선언 등은 생략한 개념 예시
public void cancelIfUpcoming(LocalDateTime now) {
    if (status == MeetingStatus.SCHEDULED && startsAt.isAfter(now)) {
        status = MeetingStatus.CANCELLED;
    }
}
""",'meeting-encapsulation')+call('예시 규칙: 예정 상태이며 시작 시각이 현재보다 뒤인 모임만 취소합니다.<br>호출하는 쪽은 동작을 요청하고, 모임 객체가 자기 상태·시각을 보고 변경 여부를 판단합니다.<br>여러 곳의 setStatus 대신 규칙을 메서드에 모읍니다. 캡슐화는 허용할 변경 방법도 정하는 일입니다.<br>Java 상태 변경의 DB 반영은 영속 상태·트랜잭션도 확인합니다.'),kind='code-slide')
def study_close_flow():
    inner=box(10,5,350,85,'Study.close(now)','스터디 종료 요청')+box(615,5,520,85,'각 StudyMeeting','cancelIfUpcoming(now)')
    inner+=arrow(380,48,595,48,'목록의 모임에 요청')
    return svg('스터디가 목록의 각 모임에 취소 판단을 요청하고 자기 상태를 종료로 바꾸는 설계 예시',inner,100,'object-collaboration')
add('객체지향 설계','양방향 참조와 객체의 동작',study_close_flow()+code("""// Study 내부 · 종료 가능 상태 검사는 별도 구현한다고 가정
public void close(LocalDateTime now) {
    for (StudyMeeting meeting : meetings) {
        meeting.cancelIfUpcoming(now);
    }
    status = StudyStatus.CLOSED;
}
""",'study-close-collaboration')+call('스터디가 모임들을 직접 사용해 종료를 수행하는 설계라면 meetings 참조가 유용합니다.<br>각 모임은 자기 취소 규칙을 판단합니다. 양방향이 항상 더 객체지향적인 것은 아닙니다.<br>Service가 필요한 데이터 조회와 트랜잭션을 준비합니다. 모임이 많다면 별도 처리도 검토합니다.'),kind='code-slide')
add('객체지향 설계','목록 조회와 객체 탐색의 선택',table([['필요한 동작','설계 선택'],['화면의 목록·검색·페이징','Repository에서 목적에 맞게 조회'],['Study가 모임들을 직접 다루는 동작 수행','Study.meetings 역방향 참조 검토'],['Service가 모임들을 조회해 각 메서드 호출','양방향 없이도 종료 기능 구현 가능']])+call('객체의 책임을 먼저 정하고 필요한 참조만 둡니다. 양방향이면 양쪽 참조도 맞춥니다.<br>양방향 자체가 객체지향성이나 조회 SQL 감소를 보장하지는 않습니다.<br>어느 설계든 트랜잭션 경계와 실제 SQL을 확인합니다.<br>기능을 만들었다면 이제 누가 사용하고, 누가 수정할 수 있는지 확인해야 합니다.'))
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

def mvc_interceptor_position():
    inner=text(574,20,'정상 동기 요청 · DispatcherServlet이 MVC 내부 순서를 조율',23,'#087f5b')
    inner+=box(10,35,300,85,'Filter','Servlet 앞의 공통 처리')+box(420,35,300,85,'DispatcherServlet','MVC 요청 처리 시작')+box(830,35,305,85,'HandlerMapping','handler·Interceptor 선택')
    inner+=arrow(330,78,400,78)+arrow(740,78,810,78)
    inner+=box(735,180,400,85,'preHandle','선택된 handler 실행 전')+box(10,180,510,85,'HandlerAdapter','선택된 Controller 호출')
    inner+=arrow(980,135,980,165)+arrow(715,222,540,222,'true면 계속')
    return svg('Filter 뒤의 DispatcherServlet이 HandlerMapping으로 handler와 Interceptor를 선택하고 preHandle을 거쳐 HandlerAdapter로 Controller를 호출합니다',inner,280,'mvc-interceptor-position')

def simple_security_flow():
    inner=box(10,10,1125,75,'SecurityFilterChain · 여러 보안 Filter의 묶음')
    nodes=[('인증 정보 확인','로그인한 사용자인가?'),('접근 허용 확인','이 요청을 해도 되는가?'),('MVC 업무 처리','Controller · Service')]
    for i,(name,desc) in enumerate(nodes):
        x=10+i*410
        inner+=box(x,155,305,110,name,desc)
        if i<2:inner+=arrow(x+325,210,x+390,210)
    inner+='<path d="M160,100 V140" fill="none" stroke="#087f5b" stroke-width="3" marker-end="url(#arrow)"/>'
    return svg('보안 필터들이 인증 정보와 접근 허용 여부를 확인하고 요청을 허용하면 MVC 업무 처리를 계속하는 개념 흐름',inner,290,'simple-security-flow')

def sec_sso_flow():
    inner=box(10,10,320,105,'앱 A에 접근','A의 로그인 시작')+box(410,10,320,105,'중앙 인증 서버 · IdP','처음에는 로그인 필요')+box(810,10,325,105,'앱 A','인증 응답 검증 · A 세션')
    inner+=arrow(350,60,390,60)+arrow(750,60,790,60)
    inner+=box(10,200,320,105,'앱 B에 접근','B의 로그인 시작')+box(410,200,320,105,'같은 IdP','기존 로그인 상태 재사용')+box(810,200,325,105,'앱 B','인증 응답 검증 · B 세션')
    inner+=arrow(350,250,390,250)+arrow(750,250,790,250)
    inner+=text(574,160,'브라우저가 로그인 경로로 이동하고 각 앱으로 돌아오는 흐름',22,'#087f5b')
    return svg('앱 A 로그인 후 앱 B도 같은 IdP로 이동하여 기존 인증 상태를 활용하고 각 앱은 자기 세션과 권한을 관리합니다',inner,325,'sso-flow')

add('Security 기초','인증과 인가',table([['구분','확인하는 질문','스터디 서비스 예시'],['인증','누구인가?','서연 회원으로 로그인했는지 확인'],['인가','이 요청을 허용할까?','해당 스터디의 모임을 수정할 권한 확인']])+call('기능을 만들었다면 누가 사용하고 수정할 수 있는지도 정해야 합니다.<br>개발자가 접근 규칙을 설정하면 Spring Security가 로그인과 요청별 확인을 돕습니다.<br>로그인에 성공해도 모든 스터디의 모임을 수정할 수 있는 것은 아닙니다.'))
add('로그인 상태','쿠키와 세션으로 로그인 상태 이어가기',sec_session_flow()+call('브라우저는 쿠키에 세션 ID를 보관하고, 전송 조건에 맞는 요청에 보냅니다.<br>서버는 세션에 인증 결과를 보관하고, 다음 요청의 세션 ID로 사용자를 확인합니다.'))
add('Filter','Filter는 요청·응답을 처리하는 중간 단계',sec_filter_roundtrip()+call('Controller마다 같은 확인을 반복하지 않도록, 앞단에서 요청을 공통으로 처리할 수 있습니다.<br>chain.doFilter는 다음 필터 또는 Servlet으로 처리를 이어갑니다.<br>필터에서 응답을 끝내면 Controller까지 가지 않을 수도 있습니다.'))
add('Filter와 Interceptor','Filter와 HandlerInterceptor의 실행 위치',mvc_interceptor_position()+table([['구분','처리 범위'],['Filter','Servlet 표준 · 매핑된 요청·응답의 공통 처리'],['HandlerInterceptor','Spring MVC · 선택된 handler 앞뒤의 공통 처리']]))
add('MVC Interceptor','HandlerInterceptor의 세 가지 시점',table([['메서드','언제 무엇을 하는가?'],['preHandle','대상 선택 후 실행 전. true면 계속, false면 중단하며 응답은 직접 처리'],['postHandle','정상 반환 후 뷰 렌더링 전. REST 응답 본문은 이미 처리되어 본문 수정에 쓰지 않음'],['afterCompletion','MVC 완료 뒤 정리·로그. 자신의 preHandle이 true였을 때 호출']])+call('정상 동기 요청의 예시입니다. 모임 API의 처리 메서드 이름·수행 시간 로그 등에 활용합니다.<br>인증·인가는 Spring Security를 우선 검토합니다. Interceptor만으로 보안을 대체하지 않습니다.'))
add('Spring Security','Spring Security의 요청 확인 순서',simple_security_flow()+call('경로에 맞는 SecurityFilterChain 하나를 선택하고, 안의 여러 Filter를 순서대로 실행합니다.<br>그림은 주요 역할만 묶었습니다. 허용되지 않은 요청은 MVC 업무 처리 전에 끝날 수 있습니다.'))
add('SSO','SSO는 여러 서비스의 반복 로그인을 줄입니다',sec_sso_flow()+call('SSO는 같은 중앙 인증 서버의 로그인 상태를 활용해 반복 로그인을 줄이는 구성입니다.<br>앱 A와 B는 인증 결과를 확인하고 각자의 로그인 상태와 접근 권한을 관리합니다.'))
add('Security 자율 학습','Security는 기본 로그인부터 직접 학습','<div class="references"><a href="https://docs.spring.io/spring-security/reference/servlet/getting-started.html"><b>1. 기본 로그인 ↗</b><span>로그인 전·후 요청 비교</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html"><b>2. 세션과 로그인 상태 ↗</b><span>다음 요청에서도 사용자 확인</span></a><a href="https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html"><b>3. 경로별 접근 허용 ↗</b><span>공개·로그인·운영자 요청 구분</span></a></div>'+call('예: 스터디 조회는 공개, 참여는 로그인 필요, 모임 수정은 해당 스터디 운영자만 허용합니다.<br>운영자 여부처럼 데이터에 따른 권한도 확인합니다. 프로젝트 버전에 맞는 문서를 봅니다.<br>Security 구현은 이번 스터디 과제의 필수 조건이 아닙니다.'))

add('JPA 과제','스터디 모집·모임 관리 서비스',table([['핵심 기능','만들 서비스'],['회원·프로필','회원 정보와 자기소개 관리'],['스터디','스터디 개설과 목록·상세 조회'],['참여','스터디 참여·탈퇴와 참여 목록 조회'],['모임 일정','스터디별 일정 등록·조회']])+call('회원들이 스터디를 만들고 참여하며 모임 일정을 관리하는 새 REST API 프로젝트입니다.<br>기능에 필요한 데이터와 구체적인 동작은 직접 설계합니다.'))
add('JPA 과제 · 자율 설계','연관관계와 서비스 규칙 정하기',steps('Entity 구성·필드·API를 직접 설계','일대일·일대다/다대일·여러 회원과 여러 스터디의 관계를 JPA로 표현','관계 방향·FK와 가입 정보의 표현 방식을 결정하고 이유 정리','중복 참여·정원·탈퇴 등 서비스 규칙을 직접 정의')+call('여력이 있다면 재가입·스터디장 위임 등 원하는 기능을 확장해 봅니다.<br>선택한 관계와 규칙이 서비스 동작에 맞는지 설명할 수 있어야 합니다.'))
add('JPA 과제 · 제출','구현 내용과 설계 이유를 PR에 설명',steps('새 Spring Boot 프로젝트에서 JPA로 DB에 저장하고 기능 구현','기존 fork 저장소의 자율 이름 폴더에 추가하고 공용 저장소로 PR 제출','PR에 구현 기능·Entity 관계도·관계와 트랜잭션 설계 이유·직접 정한 규칙 작성')+call('프로젝트 구조·API·브랜치 이름은 자율입니다. 기존 프로젝트는 보존합니다.<br>로그인·프론트는 선택이며 테스트 코드 구현은 필수가 아닙니다.<br><a href="https://github.com/sesac-ddm-4-web/sesac-spring-boot-study">공용 저장소 ↗</a>'))

css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson-26-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1><div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.26</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JPA 연관관계와 Spring Security 기초"><title>11월 26일 · JPA 연관관계와 Spring Security 기초</title><style>'+css+'</style></head><body data-deck-revision="2026-11-26-v13-simple-security"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">{}</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
(OUT/'index.html').write_text(out)
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
print(f'Created {len(S)} slides; {out.count("<svg")} native diagrams')
