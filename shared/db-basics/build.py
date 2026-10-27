"""Render the local DB handout; Python markdown-it-py is an authoring dependency."""
from pathlib import Path
from markdown_it import MarkdownIt

R = Path(__file__).resolve().parent
body = MarkdownIt('commonmark', {'html': False}).enable('table').render(
    (R / 'README.md').read_text())
style = '''
:root{color-scheme:light;--ink:#16251f;--green:#087f5b;--line:#d9e2da}
*{box-sizing:border-box}body{margin:0;background:#e9ede7;color:var(--ink);font-family:system-ui,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.75}
main{max-width:1120px;margin:28px auto;background:#fcfdf9;padding:30px 52px 60px;border-radius:12px}
nav{display:flex;gap:24px;flex-wrap:wrap;font-size:15px}a{color:var(--green);overflow-wrap:anywhere}a:focus-visible{outline:3px solid #72aee6;outline-offset:3px}
h1{font-size:36px;line-height:1.3;margin:30px 0 16px}h2{font-size:26px;margin:40px 0 15px;border-top:1px solid var(--line);padding-top:24px}
p,li{font-size:18px}table{width:100%;border-collapse:collapse;font-size:17px;margin:20px 0;table-layout:fixed}th,td{text-align:left;vertical-align:top;padding:12px;border:1px solid var(--line);overflow-wrap:anywhere}th{color:var(--green);background:#edf5ee}
pre{padding:20px;background:#f0f4ee;border-radius:8px;overflow-x:auto;font-size:15px;line-height:1.6}code{font-family:Consolas,"SFMono-Regular",monospace;overflow-wrap:anywhere}p code,td code{font-size:.9em}
@media(max-width:650px){main{margin:0;padding:20px 16px;border-radius:0}h1{font-size:28px}h2{font-size:22px}p,li{font-size:16px}table{font-size:14px}th,td{padding:8px}pre{padding:12px;font-size:13px}}
'''
page = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>상품 한 개로 시작하는 DB 기초</title><style>' + style + '</style></head>'
        '<body><main><nav aria-label="자료 이동"><a href="../../">전체 수업 자료</a>'
        '<a href="../../2026-11-14/">14일 수업</a><a href="../../2026-11-16/">16일 수업</a>'
        '<a href="STUDENT-WORKSHEET.md">멘티 작업지</a></nav>' + body + '</main></body></html>')
(R / 'index.html').write_text(page)
print('Built DB basics handout:', len(page.encode()), 'bytes')
