# Script Timer

🇧🇷 [Leia em português (pt-BR)](README.pt-BR.md)

Measure how long a script really takes to say out loud. Script Timer reads a multi-speaker script with your browser's built-in synthetic voices, animates one avatar per character, and reports total time, time per character and time per block, against a time limit you set.

Single HTML file. No server, no build step, no account, no dependencies.

## Features

- Multi-character scripts, one voice pitch per character (and an optional fixed voice per character).
- Live total, per-character and per-block timing, with a progress bar and "over / under limit" indicator.
- Optional blocks that only count when you tick "include optional blocks".
- Measure the whole script or a single block.
- Adjustable speed and pause between lines.
- Import / export JSON; the project is also saved in the browser's local storage.
- Light and dark themes.
- Optional Python script to turn a `.docx` script into the JSON the app imports.

## Quick start

1. Open `index.html` in Chrome or Edge (double-click works; no server needed).
2. Click **Importar JSON** (Import JSON) and pick a file from [`examples/`](examples/), or paste text in the format below and click **Gerar do texto** (Generate from text).
3. Adjust characters, time limit (minutes), speed and pause between lines.
4. Click **Iniciar** (Start). Use **Trecho** (Section) to time a single block.
5. **Copiar resultado** (Copy result) or **Exportar JSON** (Export JSON) to keep the numbers.

> The interface is currently in Brazilian Portuguese. Translating it is on the roadmap.

### Text format

```
## Opening
Ana: Hello, everyone!
Beto: Thanks for having me.

## Extra block [opcional]
Ana: Only included if there is time left.
```

- `## Title` opens a block; add `[opcional]` to mark it optional.
- `Name: line` is one spoken line. Lines without `Name:` continue the previous line.
- Characters are created automatically from the names that appear.

### JSON format

```json
{
  "title": "My script",
  "limit": 20,
  "characters": [{ "name": "Ana", "role": "Host", "pitch": 1.1 }],
  "blocks": [
    {
      "title": "Opening",
      "optional": false,
      "lines": [{ "who": "Ana", "text": "Hello, everyone!" }]
    }
  ]
}
```

`limit` is in minutes. Every `who` must match a character `name`. `pitch` goes from 0.6 to 1.5.

## Examples

| File | What it is |
| --- | --- |
| [`examples/papo-de-dados.json`](examples/papo-de-dados.json) | Full draft of a six-voice podcast script (in Portuguese), including one optional block. |
| [`examples/papo-de-dados-18min.json`](examples/papo-de-dados-18min.json) | Tighter cut of the same script, written to fit the 20-minute limit. |
| [`examples/voice-test.json`](examples/voice-test.json) | Single character reading the opening, to compare voices and speeds. |

## Converting a `.docx` script

```bash
python scripts/docx_to_json.py script.docx output.json
```

Python 3, standard library only. The converter expects the template this project was built around:

- the script section starts at a paragraph reading `Roteiro` and ends at a paragraph starting with `Referências`;
- a paragraph containing `(tempo estimado: ...)` or `(tempo medido: ...)` opens a block;
- a paragraph `Label: line` becomes a line when the label is listed in `CHARACTERS`.

For another group, language or template, edit the constants at the top of [`scripts/docx_to_json.py`](scripts/docx_to_json.py).

## Limitations

- Uses the browser's Web Speech API. Chrome and Edge are the supported browsers; available voices depend on your operating system and browser, and some voices are network-based.
- Synthetic speech is more regular than human speech: add a 5–10% margin to the measured time.
- A measurement is valid only for the speed and pause you chose.

## Project structure

```
.
├── index.html              # the app
├── examples/               # ready-to-import scripts
├── scripts/
│   └── docx_to_json.py     # .docx → JSON converter
├── README.md
├── README.pt-BR.md
└── LICENSE
```

## Roadmap

- [ ] English interface (with language switch)
- [ ] Keep the app and its examples in sync via a small test script

## License

[MIT](LICENSE)
