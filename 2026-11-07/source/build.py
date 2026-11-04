from pathlib import Path
import html,json,re
from code_examples import SOURCES
R=Path(__file__).resolve().parent
OUT=R.parent
S=[]
def esc(s):return html.escape(str(s))
def call(s):return '<div class="callout">'+s+'</div>'
def table(rows):return '<table class="lesson-table">'+''.join('<tr>'+''.join(f'<{("th" if i==0 else "td")}>{x}</{("th" if i==0 else "td")}>' for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
def steps(*xs):return '<ol class="steps">'+''.join('<li>'+x+'</li>' for x in xs)+'</ol>'
def cards(*xs):return '<div class="cols'+(' three' if len(xs)==3 else '')+'">'+''.join('<div class="card"><div class="eyebrow">'+a+'</div><h3>'+b+'</h3><p>'+c+'</p></div>' for a,b,c in xs)+'</div>'
def add(ch,title,body='',note='',kind='',source=None):S.append(dict(ch=ch,title=title,body=body,note=note.strip(),kind=kind,source=source))
def section(n,title):add(title,title,'<div class="section-number">'+n+'</div>',kind='section')
# The verified reference source is retained without turning the deck into a code listing.
TODAY_KEYS=('ProductApplication.java','Product.java','ProductRepository.java','MemoryProductRepository.java','ProductNotFoundException.java','ProductService.java','ProductServiceTest.java','TimingAspect.java','ProductWiringTest.java')
TODAY_SOURCES={key:SOURCES[key] for key in TODAY_KEYS}
PROJECT='https://github.com/graygreat/mentoring-archive/blob/main/assignments/personal-project/README.md'
SOURCE_BUTTONS='<div class="inline-list">'+''.join('<button type="button" data-source-key="'+esc(key)+'">'+esc(key)+' ↗</button> ' for key in TODAY_SOURCES)+'</div>'
add('세 번째 수업','책으로 읽고<br>내 프로젝트로 적용하기','<div class="cover-bottom"><span>2026.11.07 SAT · 8시간</span><strong>상품 객체 · 객체 연결 · 테스트</strong><span>책 함께 읽기 → 개인 과제 → 11명 발표</span></div>',kind='cover')
add('주말 수업 운영','앞 4교시는 책 · 뒤 4교시는 개인 과제',table([['교시','진행'],['1–2','CH 09 객체·저장·조회 + CH 12 추상화·테스트 일부'],['3–4','책의 요청 처리 코드 읽기 · MVC 역할 표시 활동'],['5–6','개인 프로젝트 구현 · 각 45분'],['7–8','발표 준비 15분 + 발표·질문 75분']])+call('매 교시 활동 45분 + 휴식·정리 15분 · 점심 별도'),note='총 8교시×60분입니다. 개인 활동 4교시는 구현·발표 준비105분과 발표·질문75분, 휴식·정리60분으로240분입니다. 핵심 개념 6교시는 앞 2교시의 책·코어 학습과 뒤 4교시의 개인 적용이며, MVC는 3~4교시에 배정합니다. 강사 코딩 시연 없이 책 본문을 읽고 학생이 작성합니다.')
add('프로젝트 구분','책의 상품 관리와 개인 프로젝트를 나눕니다',cards(('함께 배우기','product-api/','교재 상품 관리 · 9일 REST API로 계속 확장'),('혼자 적용하기','personal-project/','나만의 소장품 관리 · 오늘 객체와 테스트부터 시작')),note='sesac-spring-boot-study 저장소 안에 두 폴더를 보존합니다. 개인 프로젝트를 만든다고 공통 product-api를 지우거나 대체하지 않습니다. 5일 greeting-api도 유지합니다.')
section('01','CH 09 · 상품 객체와 저장·조회')
add('책에서 읽을 곳','상품을 어떤 값으로 표현하나요?',table([['책에서 찾기','함께 확인할 질문'],['List를 이용한 상품 관리','상품 여러 개를 어디에 보관하나요?'],['데이터 구조 정의','상품 한 개에 필요한 값은 무엇인가요?'],['상품 추가·프로젝트 구조','객체를 만들고 보관하는 일은 어디에 있나요?']])+call('쪽수는 소지한 책에서 표시합니다. 오늘은 객체·저장·조회 부분을 먼저 봅니다.'),note='출판사 목차의 CH09 앞부분을 함께 찾습니다. DTO와 HTTP 입력·응답의 구체 구현은9일에 이어 읽습니다. 책 전체9장을 오늘 모두 끝냈다는 뜻이 아닙니다.')
add('함께 작성한 뒤 점검','상품 객체와 저장 결과를 확인합니다',steps('Product의 이름·가격과 잘못된 값 처리 찾기','저장한 상품의 id로 같은 상품 조회하기','상품이 없을 때와 여러 개일 때 목록 확인하기','List와 수업 참고 Map의 차이는 짧게 기록하기'),note='공통 product-api는 기존 Java 핵심 계약을 유지합니다. 참고 코드의 Map 구현은 교재 List 코드를 그대로 재현한 것이 아닙니다. id 연속성은 요구하지 않으며 HTTP 상태를 테스트하지 않습니다.')
section('02','CH 12 · 추상화와 테스트 일부')
add('책에서 읽을 곳','구현을 바꿔도 사용하는 코드는 같게',table([['읽을 부분','코드에서 찾을 것'],['클래스 추상화하기','Repository 인터페이스와 메모리 구현'],['리팩토링과 테스트 코드','Service가 생성자로 필요한 객체를 받는 곳'],['모킹과 단위 테스트','정상·실패 입력의 기대 결과를 비교하는 방법']])+call('12장 일부를 먼저 연결합니다. 모든 테스트 기법을 오늘 구현하지 않습니다.'),note='생성자 DI와 인터페이스를 책 코드에서 찾고 필요한 부분만 먼저 읽습니다. 실제 메모리 Repository는 mock이 아닙니다. 모킹 도구의 추가 도입은 필수가 아닙니다.')
add('보충 확인 · 책 코드와 연결','MVC와 AOP는 두 질문으로 확인',cards(('요청 처리','어떤 메서드를 호출할까요?','책의 Controller에서 담당 요청을 찾고 DispatcherServlet 흐름을 말해보기'),('공통 처리','호출 시간을 어디서 잴까요?','주입된 상품 Service의 시간 로그를 보고 직접 new 호출과 비교하기')),note='MVC·AOP는 해당 장의 코드 읽기와 연결하는 수업 보충 활동입니다. HTTP Controller 작성은9일이며 오늘 새 API를 만들지 않습니다. AOP는 보충 참고 코드의 주입 테스트·로그로 확인하고 0ms도 정상입니다. MVC는 책의 요청 흐름과 역할을 표시하는 활동으로 진행합니다.')
add('공통 프로젝트 완료 확인','책을 덮기 전에 결과를 설명해 봅시다',steps('Product → Repository → Service의 역할 설명','상품 등록·목록·단건 조회 테스트 실행','잘못된 이름·가격과 없는 id 처리 확인','product-api를 남겨 9일 Controller·DTO로 확장'),note='공통 ProductServiceTest와 ProductWiringTest를 보존합니다. AOP 확인 로그와 생성자 연결을 확인하고 다음 개인 과제로 전환합니다. 미완료자는 기본 등록·조회·규칙 테스트부터 완료하며 과제를 복사한 답안으로 대신하지 않습니다.')
section('03','개인 프로젝트 · 나만의 소장품 관리')
add('개인 과제 · 테마 선택','같은 기술로 내 데이터를 관리합니다',table([['정할 것','오늘의 개인 과제'],['테마','책 · 게임 · 운동용품 등 본인이 고르기'],['객체','CollectionItem · id, name, price'],['폴더','sesac-spring-boot-study/personal-project/']])+call('<a href="'+PROJECT+'" target="_blank" rel="noopener">개인 프로젝트 요구사항 전체 ↗</a>'),note='이 요구사항은 수업용 개인 과제이며 교재 원문 조건이 아닙니다. 화면·HTTP·DB는 만들지 않습니다. 클래스의 주제·이름은 본인 테마에 맞춰도 되지만 id/name/price의 의미와 필수 동작은 지킵니다.')
add('개인 과제 · 필수 기능','등록하고, 목록과 한 개를 조회합니다',steps('이름·가격을 가진 소장품 등록','등록한 소장품 전체 목록과 id 단건 조회','Repository 인터페이스·메모리 구현 분리','Service는 생성자로 Repository를 받기'),note='개인용 Domain·Repository·Service를 직접 작성합니다. 책과 공통 코드를 참고할 수 있지만 본인 테마로 옮긴 설계 이유를 설명합니다. 구현 정답은 제공하지 않습니다. 없는 id는 Java 예외 등 정한 방식으로 처리하고 README에 적습니다.')
add('개인 과제 · 완료 기준','동작과 실패를 테스트로 보여주세요',table([['상황','확인할 결과'],['정상 등록·목록·단건','입력한 이름·가격과 등록 결과가 일치'],['잘못된 입력','빈 이름·공백 이름·음수 가격 거부'],['조회할 id 없음','정한 실패 처리 확인'],['최소 3개 테스트','정상·실패를 포함하고 실행 결과 통과']])+call('이름 앞뒤 공백은 제거하고 가격 0은 허용합니다. HTTP·DB·프론트는 필수가 아닙니다.'),note='입력 정리·실패 후 저장 상태를 추가 테스트하면 좋습니다. 정상 등록·조회, 빈 이름 거부, 음수 가격 거부를 포함해 최소3개를 작성합니다. 테스트마다 새 메모리 저장소를 사용합니다. 실패 후 id가 연속인지 여부는 채점하지 않습니다.')
add('개인 활동 · 4교시','105분 구현·준비 + 75분 발표·질문',table([['교시','활동 45분'],['5','개인 객체·저장소·Service 구현'],['6','단위 테스트·오류 수정·실행 확인'],['7','발표 준비 15분 + 앞 5명 발표·질문 30분'],['8','뒤 6명 발표·질문 36분 + 공통 피드백 9분']])+call('각 교시 뒤 휴식·정리 15분 · 개인 과제와 발표로 4시간 확보'),note='11명 전원에게 발표 순서를 정합니다. 발표 준비까지105분, 발표66분+공통피드백9분=75분, 휴식60분으로 총240분입니다. 발표 시작을 늦춰 휴식이나 마지막 학생 시간을 줄이지 않습니다.')
add('11명 전원 발표','한 사람당 발표 4분 + 질문 2분',table([['발표 4분','보여줄 것'],['1분','내 테마와 객체·클래스 역할'],['1분','등록·조회 성공 결과'],['1분','잘못된 입력 테스트 한 개'],['1분','직접 내린 결정 또는 해결한 오류']])+call('발표 PPT 없이 IDE·테스트·실행 화면으로 설명합니다.'),note='발표11명×4분=44분, 질문11명×2분=22분입니다. 공통피드백9분을 더해75분입니다. 도중 장시간 디버깅 대신 재현 상황과 다음 할 일을 설명하도록 합니다.')
add('질문과 피드백','친구 코드에서 한 가지를 확인합니다',steps('이름·가격 규칙을 어느 클래스가 지키나요?','Service가 구현 클래스 대신 인터페이스를 받는 이유는?','테스트가 실패하면 어느 입력부터 확인할까요?','미완료라면 동작한 부분과 막힌 부분을 나눠 설명하기'),note='사람마다 새 기능 개수를 경쟁시키지 않습니다. 기본 요구의 동작·설계 설명·테스트 근거로 피드백합니다. 미완료 학생도 발표 기회를 보장하고 현재 완료한 기능과 다음 작업을 기록합니다.')
add('GitHub 제출','책 코드와 개인 코드를 각각 기록합니다',table([['작업','브랜치'],['공통 코어 코드','practice/product-core'],['공통 README·검증 기록','docs/product-core'],['개인 과제 코드·테스트·README','assignment/personal-core']])+call('같은 개인 저장소에서 Issue → 브랜치 → 확인 → PR(main) → 병합'),note='공통필수Issue·PR2개는기존대로유지합니다. 개인과제는Issue·PR각1개를추가하고제목은[개인 과제] 소장품 관리 코어와 테스트로합니다. 공통제목은[실습] 상품 객체·저장소·Service와 테스트,[문서] 상품 객체 구조와 테스트 기록입니다. main pull 후 작업하고 Closes #실제번호를 사용합니다. ')
add('제출 전 체크','README에는 실행할 방법과 결과만',steps('product-api와 personal-project 폴더 모두 보존','각 README에 테마·환경·테스트 명령·완료 기능 기록','테스트 결과와 실제 병합 PR 링크 제출','Wrapper 포함 · build/·IDE 파일·비밀값 제외'),note='루트 README에 두 프로젝트 링크를 추가하고 greeting-api 링크는 보존합니다. 루트 .gitignore에 !product-api/gradle/wrapper/gradle-wrapper.jar와 !personal-project/gradle/wrapper/gradle-wrapper.jar 예외를 유지합니다. 발표 화면의 예상 결과를 실제 테스트를 실행한 것처럼 기록하지 않습니다.')
add('다음 수업','9일에는 상품 기능을 HTTP로 연결',cards(('공통 product-api','CH 09 · DTO와 상품 API','오늘 객체와 테스트를 보존한 채 Controller·JSON·Postman으로 확장'),('개인 personal-project','14일에 같은 프로젝트 확장','9·12일에 배운 요청·검증을 적용해 CRUD 만들기')),note='9일 전 개인 HTTP 서버 구현을 필수 숙제로 추가하지 않습니다. 개인 프로젝트를 끝내지 못했으면7일코어를정리해14일에이어사용합니다.14일에는개인과제·발표4교시를다시확보합니다.')
add('수업 자료','책과 과제 안내를 다시 확인','<div class="references"><a href="https://www.yes24.com/product/goods/124434554" target="_blank" rel="noopener"><b>교재 목차 ↗</b><span>CH 09 상품 관리 · CH 12 객체지향과 테스트</span></a><a href="'+PROJECT+'" target="_blank" rel="noopener"><b>개인 프로젝트 과제 ↗</b><span>7일 코어 · 14일 REST CRUD · 발표 기준</span></a></div>'+SOURCE_BUTTONS,note='책의 쪽수와 실제 절 위치는 수업 중 소지한 판본에서 표시합니다. 책에 없는 MVC·AOP 동작과 수업 참고코드는 보충자료로 구분합니다. 마지막 자료 화면의 파일명 버튼9개를 누르면 각 예제의 전체 코드가 열립니다. 필요할 때만 참고합니다.')
# Emit a self-contained, read-only deck. No private notes or local editing drafts are shipped.
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson3-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.07</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 9·12장과 함께 배우는 IoC·DI·AOP·MVC 구조와 상품 객체 실습"><title>11월 7일 · 객체 연결과 MVC 구조</title><style>'+css+'</style></head><body data-deck-revision="2026-11-07-v7-book-led"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(TODAY_SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(t in out for t in ['강사 시연','contenteditable=','localStorage'])
assert not re.search(r'wiki|위키',''.join(slides),re.I)
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
# Full source examples are canonical for verification, but are not a downloadable starter project.
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',out.count('class="diagram"'),'SVG diagrams;',len(out.encode()),'bytes')
