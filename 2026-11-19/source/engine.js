

const SLIDES=JSON.parse(document.getElementById('deck-data').textContent);
let index=0,lastFocus=null;
const els=[...document.querySelectorAll('.slide')],$=id=>document.getElementById(id);
const clean=s=>s.replace(/<[^>]*>/g,' ');
function scale(){const w=$('workspace').clientWidth,h=$('workspace').clientHeight;$('stage').style.transform='scale('+Math.max(.1,Math.min((w-24)/1280,(h-24)/720))+')'}
function show(n){index=Math.max(0,Math.min(els.length-1,n));els.forEach((el,i)=>{el.classList.toggle('active',i===index);el.setAttribute('aria-hidden',i===index?'false':'true')});$('counter').textContent=String(index+1).padStart(2,'0')+' / '+els.length;$('current-title').textContent=clean(SLIDES[index].title);$('progress').style.width=((index+1)/els.length*100)+'%';$('prev').disabled=index===0;$('next').disabled=index===els.length-1;history.replaceState(null,'','#slide-'+(index+1))}
function openToc(){lastFocus=document.activeElement;$('toc').classList.add('open');renderToc();$('toc-search').focus()}
function closeToc(){$('toc').classList.remove('open');lastFocus?.focus()}
function renderToc(){const q=$('toc-search').value.toLowerCase();$('toc-list').replaceChildren();SLIDES.forEach((s,i)=>{if(!(clean(s.title)+' '+s.ch).toLowerCase().includes(q))return;const b=document.createElement('button');b.className='toc-item'+(i===index?' selected':'');const no=document.createElement('small');no.textContent=String(i+1).padStart(2,'0');const box=document.createElement('div'),t=document.createElement('b'),c=document.createElement('span');t.textContent=clean(s.title);c.textContent=s.ch;box.append(t,c);b.append(no,box);b.onclick=()=>{show(i);closeToc()};$('toc-list').appendChild(b)})}
async function full(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{}}
$('prev').onclick=()=>show(index-1);$('next').onclick=()=>show(index+1);$('toc-button').onclick=openToc;$('fullscreen').onclick=full;$('print').onclick=()=>window.print();$('toc-search').oninput=renderToc;
$('toc').querySelector('.close').onclick=closeToc;$('toc').addEventListener('click',e=>{if(e.target===$('toc'))closeToc()});$('blackout').onclick=()=>$('blackout').classList.remove('open');
window.addEventListener('keydown',e=>{if(e.key==='Escape'){closeToc();closeSource();$('blackout').classList.remove('open');return}if($('source').classList.contains('open')){trapSource(e);return}if($('toc').classList.contains('open')){if(e.key==='Tab'){const f=[...$('toc').querySelectorAll('button,input,a[href]')],first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}return}if(/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(index+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(index-1)}if(e.key==='Home')show(0);if(e.key==='End')show(els.length-1);if(e.key.toLowerCase()==='o')openToc();if(e.key.toLowerCase()==='f')full();if(e.key.toLowerCase()==='b')$('blackout').classList.toggle('open')});
window.addEventListener('resize',scale);window.addEventListener('hashchange',()=>{const n=Number(location.hash.replace('#slide-',''));if(n>0)show(n-1)});
show(Math.max(0,Number(location.hash.replace('#slide-',''))-1)||0);scale();



const SOURCES=JSON.parse(document.getElementById('source-data').textContent);
let sourceFocus=null;
function openSource(key){sourceFocus=document.activeElement;$('source-title').textContent=key;$('source-path').textContent=(key.endsWith('Test.java')?'src/test/java/':'src/main/java/')+'com/example/product/'+key;$('source-code').textContent=SOURCES[key];$('source').classList.add('open');$('source').querySelector('.close').focus()}
function closeSource(){if(!$('source').classList.contains('open'))return;$('source').classList.remove('open');sourceFocus?.focus()}
function trapSource(e){if(e.key!=='Tab')return;const f=[...$('source').querySelectorAll('button,[tabindex="0"]')],first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}
$('source').querySelector('.close').onclick=closeSource;$('source').addEventListener('click',e=>{if(e.target===$('source'))closeSource()});
document.querySelectorAll('[data-source-key]').forEach(b=>b.onclick=()=>openSource(b.dataset.sourceKey));
$('copy-source').onclick=async()=>{try{await navigator.clipboard.writeText($('source-code').textContent);$('copy-source').textContent='복사 완료';setTimeout(()=>$('copy-source').textContent='코드 복사',1500)}catch{$('copy-source').textContent='본문을 선택해 복사하세요'}};
