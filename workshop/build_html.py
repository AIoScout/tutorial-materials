#!/usr/bin/env python3
"""Regenerate workshop/*.html from workshop/*.md, preserving the existing
head/nav/footer template of each HTML file (markdown module unavailable)."""
import re, sys

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', s)
    return s

def convert(md):
    lines = md.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('# '):
            out.append('<h1>' + inline(line[2:]) + '</h1>')
        elif line.startswith('## '):
            out.append('<h2>' + inline(line[3:]) + '</h2>')
        elif line.startswith('### '):
            out.append('<h3>' + inline(line[4:]) + '</h3>')
        elif line.strip() == '---':
            out.append('<hr />')
        elif line.startswith('> '):
            out.append('<blockquote>')
            out.append('<p>' + inline(line[2:]) + '</p>')
            out.append('</blockquote>')
        elif line.startswith('```'):
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].startswith('```'):
                code.append(esc(lines[j]))
                j += 1
            out.append('<pre><code>' + '\n'.join(code) + '</code></pre>')
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
            if i + 1 < len(lines) and re.match(r'^\*.*\*$', lines[i + 1]):
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
    print('rebuilt', html_path, '-', body.count('<p>'), 'paragraphs,', body.count('<table'), 'tables')

if __name__ == '__main__':
    rebuild('workshop/prelab.md', 'workshop/prelab.html')
    rebuild('workshop/labmanual.md', 'workshop/labmanual.html')
