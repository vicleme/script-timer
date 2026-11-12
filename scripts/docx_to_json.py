#!/usr/bin/env python3
"""Convert a script written in a .docx into the JSON that Script Timer imports.

Usage:  python scripts/docx_to_json.py script.docx output.json

Standard library only. It reads the section that starts at the paragraph
"Roteiro" and stops at the paragraph starting with "Referências":
- a paragraph containing "(tempo estimado: ...)" or "(tempo medido: ...)"
  opens a new block (the text before the parenthesis is the block title);
- a paragraph "Label: line" becomes a spoken line, if the label is a key
  of CHARACTERS.

The markers above match the Portuguese docx template this project was built
around. For another group, language or template, edit only the constants
below.
"""
import json
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

TITLE = 'Papo de Dados: Economia da inferência'
LIMIT_MIN = 20  # time limit, in minutes

SECTION_START = 'Roteiro'        # paragraph that opens the script section
SECTION_END = 'Referências'      # paragraph prefix that closes it
BLOCK_MARKER = r'\(tempo (?:estimado|medido): [^)]*\)'  # opens a block
OPTIONAL_WORD = 'opcional'       # in a block title => optional block
OPTIONAL_NOTE = r'\s*\(entra se sobrar tempo\)'  # removed from the title

# docx label (lowercase) -> (name in the app, role, voice pitch)
CHARACTERS = {
    'apresentador 1': ('Lucas', 'Apresentador 1', 1.0),
    'apresentador 2': ('Timóteo', 'Apresentador 2', 1.15),
    'economista': ('João Pedro', 'Economista', 0.85),
    'engenheiro ambiental': ('Ivan', 'Engenheiro ambiental', 0.95),
    'pesquisador': ('Victor F.', 'Pesquisador', 1.2),
    'engenheiro de mlops/finops': ('Leme', 'Engenheiro de MLOps/FinOps', 0.75),
}


def paragraphs(path):
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    for p in root.iter(W + 'p'):
        yield ''.join(t.text or '' for t in p.iter(W + 't')).strip()


def convert(path):
    blocks, block, inside = [], None, False
    for p in paragraphs(path):
        if not inside:
            inside = (p == SECTION_START)
            continue
        if p.startswith(SECTION_END):
            break
        m = re.search(BLOCK_MARKER, p)
        if m:
            title = p[:m.start()].strip()
            optional = OPTIONAL_WORD in title.lower()
            title = re.sub(OPTIONAL_NOTE, '', title)
            block = {'title': title, 'optional': optional, 'lines': []}
            blocks.append(block)
            continue
        m = re.match(r'^([^:]{3,40}):\s*(.+)$', p)
        if m and block is not None and m.group(1).strip().lower() in CHARACTERS:
            name = CHARACTERS[m.group(1).strip().lower()][0]
            block['lines'].append({'who': name, 'text': m.group(2).strip()})
    return {
        'title': TITLE,
        'limit': LIMIT_MIN,
        'characters': [{'name': n, 'role': r, 'pitch': t} for n, r, t in CHARACTERS.values()],
        'blocks': blocks,
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    data = convert(sys.argv[1])
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    lines = sum(len(b['lines']) for b in data['blocks'])
    print(f"{len(data['blocks'])} blocks, {lines} lines, "
          f"{len(data['characters'])} characters -> {sys.argv[2]}")
