#!/usr/bin/env python3
"""Render every mermaid fence to SVG and leave a marker in its place.

Pandoc passes a mermaid fence through as a code block, and mermaid.js only runs
in a browser, so each diagram is rendered once up front and the result serves
both outputs.

The SVG is not written into the markdown, because pandoc reflows raw HTML and
mermaid sets white-space: break-spaces on its labels, so an inserted newline
pushes a label out of the box that clips it. A marker survives that untouched,
and inject-diagrams.py puts the SVG in after pandoc has finished.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

source = pathlib.Path(sys.argv[1])
cache = pathlib.Path(sys.argv[2])
config = (pathlib.Path(__file__).parent / 'mermaid.json').read_bytes()
cache.mkdir(parents=True, exist_ok=True)

text = source.read_text()
pattern = re.compile(r'^```mermaid\n(.*?)^```\n', re.MULTILINE | re.DOTALL)


def render(match):
    diagram = match.group(1)
    name = hashlib.sha1(diagram.encode() + config).hexdigest()[:12]
    svg = cache / f'{name}.svg'
    if not svg.exists():
        definition = cache / f'{name}.mmd'
        definition.write_text(diagram)
        subprocess.run(
            ['npx', '-y', '@mermaid-js/mermaid-cli', '-i', str(definition),
             '-o', str(svg), '-b', 'transparent',
             '-c', str(pathlib.Path(__file__).parent / 'mermaid.json')],
            check=True, stdout=subprocess.DEVNULL)
        print(f'  rendered {name}', file=sys.stderr)
    return f'\n\nKFSWDIAGRAM{name}\n\n'


def isolate(svg, prefix):
    """Make one diagram's identifiers unique to it.

    Every diagram mermaid emits calls itself `my-svg`, scopes its whole
    stylesheet to `#my-svg`, and numbers its gradients from `color-0`. Inlining
    several into one page makes those collide: the rules of one diagram apply to
    another, and labels disappear. Renaming each identifier keeps the diagrams
    independent of each other.
    """
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


source.write_text(pattern.sub(render, text))
