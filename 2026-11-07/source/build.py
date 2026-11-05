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
add('2026.11.07','상품 관리 · 객체지향<br>테스트 · MVC','<div class="cover-bottom"><span>교재 9장 · 12장</span><strong>상품 관리와 개인 프로젝트</strong><span>개인 과제: 취미 위시리스트와 예산 추천</span></div>',kind='cover')
add('수업 내용','수업 내용',steps('교재 9장 · 상품 객체와 저장·조회','교재 12장 · 추상화와 테스트','MVC 요청 처리와 AOP 확인','개인 프로젝트 구현 및 준비','결과 발표와 코드 확인'))
section('01','CH 09 · 상품 관리 애플리케이션')
add('교재 수업','CH 12 · 객체지향과 테스트',call('9장 상품 객체·저장·조회와 12장 추상화·테스트는 책을 보며 설명합니다.'),note='교재 9장 앞부분과 12장 일부를 함께 읽습니다. DTO와 HTTP API 구현은 9일에 이어갑니다. 책의 실제 코드와 현재 product-api를 비교하며 필요한 질문에 답합니다. 확인하지 않은 쪽수나 책의 세부 규칙을 만들지 않습니다.')
add('보충 내용','MVC · AOP',cards(('MVC','요청 처리 흐름','책의 요청 주소와 Controller 메서드 연결 확인'),('AOP','공통 처리','Service 호출 전후의 시간 로그와 프록시 확인')),note='MVC는 책의 Controller에서 요청을 담당하는 메서드를 찾고 DispatcherServlet의 역할을 연결합니다. AOP는 수업 참고 구현을 이용해 주입된 Service 호출과 직접 만든 객체 호출을 비교합니다. 개인 과제의 기본 완료 조건에 새 HTTP 서버나 AOP 구현을 강제하지 않습니다.')
section('02','개인 과제 · 취미 위시리스트')
add('과제 주제와 데이터','취미 위시리스트와 예산 추천','<p>사고 싶은 물건을 등록하고, 각 물건의 가격을 예산과 비교해<br>구매 후보를 추천하는 프로젝트입니다.</p>'+table([['항목','요구사항'],['주제','구매하고 싶은 책·게임·운동용품·캠핑장비 등에서 선택'],['데이터','CollectionItem: id, name, price'],['의미','name은 아이템 이름, price는 원 단위 정수 가격'],['프로젝트','개인 저장소의 personal-project/']]),note='공통 product-api와 기존 greeting-api는 보존합니다. 오늘 요구사항은 교재 원문을 옮긴 것이 아니라 배운 이론을 적용하는 개인 과제입니다. 수업용 완성 정답 코드는 제공하지 않습니다.')
add('필수 기능','등록 · 목록 · 단건 조회 · 추천',steps('위시리스트에 아이템 등록','전체 목록과 등록한 id의 아이템 조회','예산 안에서 살 수 있는 아이템을 최대 3개 추천','Repository 인터페이스와 메모리 구현 분리','Service는 생성자로 Repository를 받기'),note='Service는 Repository 인터페이스를 사용합니다. HTTP·DB·프론트는 기본 과제의 필수 범위가 아닙니다. 기능을 Java 객체와 테스트로 먼저 완성합니다.')
add('입력 규칙','이름 · 가격 · id 처리',table([['입력','규칙'],['이름','null·빈 문자열·공백만 있는 이름 거부 · 앞뒤 공백 제거'],['가격','0 이상의 정수 · 무료 아이템 0원 허용'],['id','프로그램에서 부여 · 등록 결과의 실제 id로 조회'],['없는 id','찾을 수 없다는 예외로 구분']])+call('실패한 등록 뒤에는 기존 목록이 바뀌지 않아야 합니다.'),note='id가 항상 1부터 시작하거나 연속이라는 가정으로 테스트하지 않습니다. 이 규칙은 도메인 객체가 지키고 Service와 테스트에서 확인합니다.')
add('추천 규칙','예산별 아이템 추천',steps('예산은 0 이상 · 음수 예산은 거부','개별 가격이 예산 이하인 구매 후보만 선택','가격 오름차순 · 같은 가격은 등록 순서 유지','정렬한 결과에서 최대 3개 반환','조건에 맞는 아이템이 없으면 빈 목록 반환')+call('추천 조회가 원본 목록을 정렬하거나 변경하면 안 됩니다.'),note='예산 0이면 무료 아이템만 추천합니다. 추천 로직은 Service에서 처리하고 저장·조회는 Repository에 맡깁니다. 추천 결과와 원본 보존을 함께 테스트합니다.')
add('입출력 예시','예산 추천 결과',table([['등록 순서','이름','가격'],['1','노트','12,000원'],['2','무료 샘플','0원'],['3','펜','5,000원'],['4','스티커','5,000원'],['5','게임','8,000원']])+call('개별 가격 5,000원 이하 → 무료 샘플 · 펜 · 스티커<br>예산 0원 → 무료 샘플'),note='표의 번호는 등록 순서를 나타내며 실제 id 값을 고정하지 않습니다. 같은 가격인 펜과 스티커는 등록 순서를 유지합니다. 정렬과 최대 3개 제한이 둘 다 적용되어야 합니다.')
add('테스트 완료 기준','정상 · 실패 · 추천 테스트',steps('정상 등록·목록·실제 id의 단건 조회','빈 이름·음수 가격·음수 예산 거부','예산 경계·가격 정렬·같은 가격의 순서·최대 3개','빈 결과·가격 0·조회 전후 원본 보존')+call('최소 4개의 단위 테스트를 작성합니다.<br>Spring이 연결한 Service도 통합 테스트나 실제 빈 실행으로 확인합니다.'),note='독립 단위 테스트는 새 메모리 저장소를 생성자에 전달해 매번 분리된 상태에서 실행합니다. Spring 컨테이너가 객체를 연결하는 확인은 직접 new로 만든 Service의 테스트와 구분합니다. 서버를 띄우지 않는 컨텍스트 테스트나 실제 빈을 실행해 연결을 확인할 수 있습니다.')
add('개인 구현','구현 및 준비 · 150분',steps('객체·Repository·Service와 추천 기능 구현','정상·실패·경계 조건 테스트','README에 실행 방법과 실제 결과 기록','발표할 코드·테스트·실행 화면 준비'),note='구현과 발표 준비에 150분을 사용합니다. 발표 순서와 진행은 현장 상황에 맞추며 고정 발표·질문 타이머를 자료에 두지 않습니다. 미완료 교육생도 완료 범위와 막힌 지점을 설명합니다.')
add('완료 후 선택','추가 과제',cards(('검색','이름 부분 검색','공백·빈 검색어·결과 없음 처리와 테스트'),('상태','즐겨찾기 또는 구매 완료','상태 변경과 조회 조건을 추가하고 테스트'),('AOP','실행 시간 로그','공통 처리를 분리하고 주입된 Service 호출 로그 확인'))+call('원하는 기능을 선택해 추가하고 기존 테스트는 유지합니다.'),note='기본 과제를 먼저 완료한 교육생이 수행합니다. 검색어 처리와 상태 변경 규칙은 직접 정해 README에 적습니다. AOP를 적용했다면 프록시를 거친 호출과 직접 new로 만든 객체의 차이를 설명하고 실제 로그를 확인합니다.')
add('완료 후 선택','AI를 활용한 프론트 개발',table([['항목','구현할 내용'],['화면','등록 폼 · 전체 목록 · 예산 입력 · 추천 결과'],['기술','순수 HTML·CSS·JavaScript · 외부 라이브러리/CDN 사용 안 함'],['데이터','샘플 데이터 화면부터 작성하거나 HTTP API를 추가해 fetch 연동']])+call('프롬프트는 자율입니다. 백엔드 로직은 직접 작성합니다.<br>샘플 화면은 샘플임을 표시하고, 실제 연동은 요청·응답을 확인합니다.'),note='브라우저가 Java Service를 직접 호출하는 구조가 아닙니다. 실제 연동을 선택하면 책 9장의 REST 부분을 자율적으로 참고해 HTTP API를 추가한 뒤 fetch로 연결합니다. Controller는 입력·응답, Service는 업무 로직을 맡습니다. API 경로와 요청·응답 계약은 README에 직접 정합니다. AI가 작성한 프론트도 실행해 정상·실패 결과를 확인하고 코드의 동작을 설명합니다.')
add('개인 발표','발표 내용',steps('선택한 주제와 구현한 기능','등록·조회·추천의 실제 실행 결과','잘못된 입력 또는 실패 테스트','클래스 역할과 생성자 주입 구조','직접 결정한 규칙·해결한 문제·미완료 범위')+call('발표용 PPT 대신 코드·테스트·실행 화면을 보여줍니다.'))
add('이론 적용 체크리스트','다른 교육생과 코드 확인',steps('□ Domain: 빈 이름·음수 가격을 객체가 거부하는가?','□ Repository: 메모리 저장·id 조회가 분리되어 있는가?','□ Service: 추천 로직을 처리하고 Repository 인터페이스를 사용하는가?','□ DI: 생성자로 Repository를 받고 Spring의 객체 연결도 확인했는가?','□ 테스트: 새 저장소로 정상·실패·추천 결과를 비교하는가?')+call('다른 교육생의 코드와 테스트 결과를 열어 각 항목의 근거를 확인합니다.'),note='추가 기능이 많다는 이유로 기본 설계와 테스트가 빠진 것을 통과시키지 않습니다. AOP를 추가했다면 공통 로그와 프록시 호출을, HTTP·프론트를 추가했다면 Controller와 Service의 역할 및 실제 요청·응답을 함께 확인합니다. 미완료자는 완료한 부분과 다음 작업을 구분해 설명합니다.')
add('제출 확인','코드 · 테스트 · README',steps('개인 저장소에 코드·테스트·README 반영','README에 주제·실행 명령·완료 기능·실제 결과 기록','테스트 결과와 PR 링크 준비','Wrapper 포함 · build/·IDE 파일·비밀값 제외')+call('브랜치 이름은 자율입니다.'),note='같은 개인 저장소 sesac-spring-boot-study를 사용합니다. 공통 product-api와 개인 personal-project를 보존합니다. Issue와 PR에 실제 구현 범위와 검증 결과를 적고 자체 확인 후 main에 병합합니다. 브랜치 이름과 작업 단위는 교육생이 정합니다.')
add('다음 수업','REST API',cards(('공통 product-api','CH 09 · DTO와 상품 API','기존 객체·테스트를 유지하고 Controller·JSON·Postman으로 확장'),('개인 personal-project','위시리스트 API로 확장','9·12일의 요청·검증을 배운 뒤 같은 기능을 HTTP로 연결')),note='기본 개인 과제에서 HTTP를 미리 구현할 필요는 없습니다. 먼저 끝낸 교육생의 프론트·API 연동은 선택 선행 과제입니다.')
# Emit a self-contained, read-only deck. No private notes or local editing drafts are shipped.
css=(R/'theme.css').read_text();slides=[]
for i,d in enumerate(S):
 src='' if not d['source'] else '<button class="source-button" data-source-key="'+esc(d['source'])+'">파일 전체 코드 ↗</button>'
 slides.append('<section class="slide '+d['kind']+(' active' if i==0 else '')+'" data-index="'+str(i)+'" data-slide-id="lesson3-'+str(i)+'" aria-label="'+esc(re.sub('<[^>]*>',' ',d['title']))+'" aria-hidden="'+('false' if i==0 else 'true')+'"><div class="topline"><span class="brand">SPRING BOOT &amp; AI</span><span class="chapter-tag">'+esc(d['ch'])+'</span></div><h1>'+d['title']+'</h1>'+src+'<div class="content">'+d['body']+'</div><footer class="foot"><span>2026.11.07</span><span>'+f'{i+1:02} / {len(S):02}'+'</span></footer></section>')
meta=[{k:d[k] for k in ('ch','title')} for d in S]
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="교재 상품 관리·객체지향·테스트와 취미 위시리스트 개인 과제"><title>11월 7일 · 상품 관리·객체지향·테스트</title><style>'+css+'</style></head><body data-deck-revision="2026-11-07-v8-plain-assignment"><main id="workspace" aria-label="강의 슬라이드"><div id="stage">'+''.join(slides)+(R/'controls.html').read_text()+'<script type="application/json" id="deck-data">'+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="source-data">'+json.dumps(TODAY_SOURCES,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+(R/'engine.js').read_text()+'</script></body></html>'
assert not any(t in out for t in ['강사 시연','contenteditable=','localStorage'])
assert not re.search(r'wiki|위키',''.join(slides),re.I)
(OUT/'index.html').write_text(out)
(R/'slide-index.json').write_text(json.dumps([{'n':i+1,'title':d['title'],'chapter':d['ch'],'source':d['source']} for i,d in enumerate(S)],ensure_ascii=False,indent=2))
# Full source examples are canonical for verification, but are not a downloadable starter project.
(R/'metadata-private.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Created',len(S),'slides;',sum(d['source'] is not None for d in S),'file-code pages;',out.count('class="diagram"'),'SVG diagrams;',len(out.encode()),'bytes')
