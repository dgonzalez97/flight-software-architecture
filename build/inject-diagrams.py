#!/usr/bin/env python3
"""Put the rendered diagrams into the page pandoc produced.

Each diagram's identifiers are renamed on the way in. Every diagram mermaid
emits calls itself `my-svg`, scopes its whole stylesheet to `#my-svg`, and
numbers its gradients from `color-0`, so inlining several into one page would
make the rules of one apply to another.
"""
import pathlib
import re
import sys

page = pathlib.Path(sys.argv[1])
cache = pathlib.Path(sys.argv[2])
html = page.read_text()


def isolate(svg, prefix):
    identifiers = sorted(set(re.findall(r'\bid="([^"]+)"', svg)), key=len, reverse=True)
    for identifier in identifiers:
        quoted = re.escape(identifier)
        renamed = f'{prefix}-{identifier}'
        svg = re.sub(rf'\bid="{quoted}"', f'id="{renamed}"', svg)
        svg = re.sub(rf'url\(#{quoted}\)', f'url(#{renamed})', svg)
        svg = re.sub(rf'(href=")#{quoted}"', rf'\g<1>#{renamed}"', svg)
        # Stylesheet selectors, which carry no quotes around the identifier.
        svg = re.sub(rf'#{quoted}(?![\w-])', f'#{renamed}', svg)
    return svg


def place(match):
    name = match.group(1)
    svg = (cache / f'{name}.svg').read_text()
    svg = re.sub(r'^<\?xml[^>]*\?>\s*', '', svg)
    return f'<figure class="diagram">{isolate(svg, name)}</figure>'


html, count = re.subn(r'<p>KFSWDIAGRAM([0-9a-f]+)</p>', place, html)
page.write_text(html)
print(f'  placed {count} diagrams')
