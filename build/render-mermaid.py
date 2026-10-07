#!/usr/bin/env python3
"""Replace mermaid fences with rendered SVG, so the diagrams survive into the PDF.

Pandoc passes a mermaid fence through as a code block, and mermaid.js only runs
in a browser. Rendering each diagram once up front keeps one source of truth for
both outputs.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

source = pathlib.Path(sys.argv[1])
cache = pathlib.Path(sys.argv[2])
cache.mkdir(parents=True, exist_ok=True)

text = source.read_text()
pattern = re.compile(r'^```mermaid\n(.*?)^```\n', re.MULTILINE | re.DOTALL)


def render(match):
    diagram = match.group(1)
    name = hashlib.sha1(diagram.encode()).hexdigest()[:12]
    svg = cache / f'{name}.svg'
    if not svg.exists():
        definition = cache / f'{name}.mmd'
        definition.write_text(diagram)
        subprocess.run(
            ['npx', '-y', '@mermaid-js/mermaid-cli', '-i', str(definition),
             '-o', str(svg), '-b', 'transparent'],
            check=True, stdout=subprocess.DEVNULL)
        print(f'  rendered {name}', file=sys.stderr)
    body = svg.read_text()
    # Drop the XML declaration so the SVG can be inlined in HTML.
    body = re.sub(r'^<\?xml[^>]*\?>\s*', '', body)
    return f'\n<figure class="diagram">\n{body}\n</figure>\n\n'


source.write_text(pattern.sub(render, text))
