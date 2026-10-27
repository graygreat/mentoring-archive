"""Render the assignment handout from the reviewable Markdown source, without dependencies."""
from pathlib import Path
import html,re
R=Path(__file__).resolve().parent

def inline(text):
    value=html.escape(text)
    value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',value)

def render(text):
    lines=text.splitlines(); out=[]; i=0; listing=False
    while i<len(lines):
        line=lines[i]
        if not line.strip():
            if listing:out.append('</ul>');listing=False
            i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]);i+=1
            out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                fields=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in fields):rows.append(fields)
                i+=1
            out.append('<div class="table-wrap"><table>')
            for n,row in enumerate(rows):
                tag='th' if n==0 else 'td';out.append('<tr>'+''.join(f'<{tag}>'+inline(v)+f'</{tag}>' for v in row)+'</tr>')
            out.append('</table></div>');continue
        if line.startswith('#'):
            n=len(line)-len(line.lstrip('#'));out.append(f'<h{n}>'+inline(line[n:].strip())+f'</h{n}>');i+=1;continue
        if line.startswith('- ') or re.match(r'^\d+\. ',line):
            if not listing:out.append('<ul>');listing=True
            out.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',line))+'</li>');i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ','```')):
            paragraph.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    if listing:out.append('</ul>')
    return '\n'.join(out)
style='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fcfdf9;color:#16251f;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.8}main{max-width:1100px;margin:auto;padding:48px 28px 80px}nav{display:flex;flex-wrap:wrap;gap:24px;padding-bottom:22px;border-bottom:1px solid #d9e2da}a{color:#087f5b;text-underline-offset:4px}h1{font-size:clamp(32px,5vw,48px);line-height:1.3;letter-spacing:-1.6px;margin:40px 0 24px}h2{font-size:27px;line-height:1.5;margin:54px 0 18px;padding-top:24px;border-top:1px solid #d9e2da}h3{font-size:21px}p,li{font-size:18px}li{margin:12px 0}code{background:#edf5ee;padding:2px 5px;border-radius:4px;font-size:.9em;overflow-wrap:anywhere}pre{padding:24px;border-radius:12px;background:#eaf1e9;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.7}pre code{padding:0;background:none}table{width:100%;border-collapse:collapse;font-size:16px;min-width:580px}th,td{text-align:left;padding:13px 16px;border-bottom:1px solid #d9e2da;vertical-align:top}th{background:#edf5ee}.table-wrap{overflow-x:auto}footer{margin-top:60px;padding-top:24px;border-top:1px solid #d9e2da;color:#627568}a:focus-visible{outline:3px solid #8bc1f7;outline-offset:5px}@media(max-width:600px){main{padding:28px 18px}p,li{font-size:16px}h2{font-size:23px}}'''
body=render((R/'README.md').read_text())
body=body.replace('<a href="./index.html">과제 안내</a> · ','')
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>단축 URL 웹 서비스 · 별도 과제</title><style>'+style+'</style></head><body><main><nav aria-label="자료 이동"><a href="../../">전체 수업 자료</a><a href="../../2026-11-12/">12일 수업</a><a href="./README.md">과제 원문</a></nav>'+body+'<footer>SPRING BOOT &amp; AI · 상품 관리 수업의 별도 적용 과제 · 마감 별도 공지</footer></main></body></html>'
(R/'index.html').write_text(page)
print('Built assignment handout:',len(page.encode()),'bytes')
