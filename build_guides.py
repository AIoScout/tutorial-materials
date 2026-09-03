#!/usr/bin/env python3
"""Regenerate every student-guide HTML from its markdown source, preserving
each HTML file's existing head/nav/footer template. Covers the workshop
guides and Lab 0/1/2/5/6. Run from the repo root:  python3 build_guides.py [name ...]

Markdown dialect handled (matches the conventions of the existing guides):
headings, ---, blockquotes (multi-line, multi-paragraph), fenced code with
language tag, $$ math blocks, tables, ul/ol, image + optional *caption*,
**bold** / *italic* / `code`, "Check Point" headings -> .cph banner.
"""
import re, sys

PAIRS = [
    ('workshop/prelab.md', 'workshop/prelab.html'),
    ('workshop/labmanual.md', 'workshop/labmanual.html'),
    ('Lab0_EdgeAI_Vision_StudentGuide.md', 'Lab0_EdgeAI_Vision_StudentGuide.html'),
    ('Lab1_Motor_Motion_StudentGuide.md', 'Lab1_Motor_Motion_StudentGuide.html'),
    ('Lab2_Sensors_StudentGuide.md', 'Lab2_Sensors_StudentGuide.html'),
    ('Lab5_Routing_StudentGuide.md', 'Lab5_Routing_StudentGuide.html'),
    ('Lab6_Firebase_RFID_StudentGuide.md', 'Lab6_Firebase_RFID_StudentGuide.html'),
]

# emoji / variation selectors to strip (keeps ✔ U+2714 and ✓ U+2713)
STRIP = re.compile('[\U0001F000-\U0001FFFF☀-⛿️✅❌❗❓❕]')

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', s)
    return s

def convert(md):
    lines = STRIP.sub('', md).split('\n')
    out = []
    i = 0

    def flush_quote(qlines):
        """consecutive '> ' lines -> one blockquote; blank '>' splits paragraphs"""
        out.append('<blockquote>')
        para = []
        for q in qlines:
            if q == '':
                if para:
                    out.append('<p>' + '\n'.join(inline(x) for x in para) + '</p>')
                    para = []
            else:
                para.append(q)
        if para:
            out.append('<p>' + '\n'.join(inline(x) for x in para) + '</p>')
        out.append('</blockquote>')

    while i < len(lines):
        line = lines[i]
        if line.startswith('#### ') or line.startswith('### ') or line.startswith('## ') or line.startswith('# '):
            level, text = len(line) - len(line.lstrip('#')), line.lstrip('#').strip()
            if text.startswith('Check Point'):
                out.append('<div class="cph">' + inline(text) + '</div>')
            else:
                out.append(f'<h{level}>' + inline(text) + f'</h{level}>')
        elif line.strip() == '---':
            out.append('<hr />')
        elif line.startswith('>'):
            qlines = []
            while i < len(lines) and lines[i].startswith('>'):
                qlines.append(lines[i][2:] if lines[i].startswith('> ') else lines[i][1:])
                i += 1
            i -= 1
            flush_quote(qlines)
        elif line.startswith('```'):
            lang = line[3:].strip()
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].startswith('```'):
                code.append(esc(lines[j]))
                j += 1
            cls = f' class="language-{lang}"' if lang else ''
            out.append(f'<pre><code{cls}>' + '\n'.join(code) + '</code></pre>')
            i = j
        elif line.strip() == '$$':
            j = i + 1
            math = []
            while j < len(lines) and lines[j].strip() != '$$':
                math.append(esc(lines[j]))
                j += 1
            out.append('<p>$$\n' + '\n'.join(math) + '\n$$</p>')
            i = j
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(cells)
                i += 1
            i -= 1
            header, body = rows[0], rows[2:]  # rows[1] is the separator
            t = ['<div class="wrap-list"><table>', '<thead>', '<tr>']
            t += ['<th>' + inline(c) + '</th>' for c in header]
            t += ['</tr>', '</thead>', '<tbody>']
            for r in body:
                t.append('<tr>')
                t += ['<td>' + inline(c) + '</td>' for c in r]
                t.append('</tr>')
            t += ['</tbody>', '</table></div>']
            out.append('\n'.join(t))
        elif re.match(r'^!\[(.*)\]\((.*)\)$', line):
            m = re.match(r'^!\[(.*)\]\((.*)\)$', line)
            cap = ''
            if i + 1 < len(lines) and re.match(r'^\*.*\*$', lines[i + 1] or ''):
                cap = lines[i + 1][1:-1]
                i += 1
            out.append('<p><img alt="' + esc(m.group(1)) + '" src="' + esc(m.group(2)) + '" />')
            if cap:
                out.append('<em>' + inline(cap) + '</em>')
            out.append('</p>')
        elif line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append('<li>' + inline(lines[i][2:]) + '</li>')
                i += 1
            i -= 1
            out.append('<ul>')
            out += items
            out.append('</ul>')
        elif re.match(r'^\d+\. ', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                items.append('<li>' + inline(re.sub(r'^\d+\. ', '', lines[i])) + '</li>')
                i += 1
            i -= 1
            out.append('<ol>')
            out += items
            out.append('</ol>')
        elif line.strip() == '':
            pass
        else:
            out.append('<p>' + inline(line) + '</p>')
        i += 1
    return '\n'.join(out)

def rebuild(md_path, html_path):
    src = open(html_path).read()
    head, rest = src.split('<article class="article">', 1)
    _, tail = rest.split('</article>', 1)
    body = convert(open(md_path).read())
    open(html_path, 'w').write(head + '<article class="article">\n' + body + '\n</article>' + tail)
    print(f'rebuilt {html_path}: {body.count("<p>")} paragraphs, {body.count("<table")} tables, '
          f'{body.count("<pre")} code blocks, {body.count("cph")} checkpoints')

if __name__ == '__main__':
    todo = PAIRS
    if len(sys.argv) > 1:
        keys = sys.argv[1:]
        todo = [p for p in PAIRS if any(k in p[0] for k in keys)]
    for md, html in todo:
        rebuild(md, html)
