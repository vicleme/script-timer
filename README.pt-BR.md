# Script Timer (Cronômetro de roteiro)

🇬🇧 [Read in English](README.md) (versão oficial)

Meça quanto tempo um roteiro realmente leva para ser falado. O Script Timer lê um roteiro com vários personagens usando as vozes sintéticas do próprio navegador, anima um bonequinho por personagem e mostra o tempo total, por personagem e por bloco, em relação a um limite que você define.

Um único arquivo HTML. Sem servidor, sem build, sem conta, sem dependências.

## Recursos

- Roteiros com vários personagens, com tom de voz por personagem (e voz fixa opcional).
- Tempo total, por personagem e por bloco em tempo real, com barra de progresso e indicação de folga ou excesso.
- Blocos opcionais, que só entram na conta se você marcar "incluir blocos opcionais".
- Medição do roteiro inteiro ou de um único bloco.
- Velocidade e pausa entre falas ajustáveis.
- Importar e exportar JSON; o projeto também fica salvo no armazenamento local do navegador.
- Tema claro e escuro.
- Script Python opcional que converte um roteiro `.docx` no JSON que o app importa.

## Início rápido

1. Abra o `index.html` no Chrome ou no Edge (basta dar dois cliques; não precisa de servidor).
2. Clique em **Importar JSON** e escolha um arquivo de [`examples/`](examples/), ou cole um texto no formato abaixo e clique em **Gerar do texto**.
3. Ajuste personagens, limite (em minutos), velocidade e pausa entre falas.
4. Clique em **Iniciar**. Use **Trecho** para cronometrar só um bloco.
5. **Copiar resultado** ou **Exportar JSON** para guardar os números.

### Formato do texto

```
## Abertura
Ana: Olá, pessoal!
Beto: Obrigado pelo convite.

## Bloco extra [opcional]
Ana: Só entra se sobrar tempo.
```

- `## Título` abre um bloco; acrescente `[opcional]` para marcá-lo como opcional.
- `Nome: fala` é uma fala. Linhas sem `Nome:` continuam a fala anterior.
- Os personagens são criados sozinhos, a partir dos nomes que aparecem.

### Formato do JSON

```json
{
  "title": "Meu roteiro",
  "limit": 20,
  "characters": [{ "name": "Ana", "role": "Apresentadora", "pitch": 1.1 }],
  "blocks": [
    {
      "title": "Abertura",
      "optional": false,
      "lines": [{ "who": "Ana", "text": "Olá, pessoal!" }]
    }
  ]
}
```

`limit` é em minutos. Cada `who` deve ser o `name` de um personagem. `pitch` vai de 0,6 a 1,5.

## Exemplos

| Arquivo | O que é |
| --- | --- |
| [`examples/papo-de-dados.json`](examples/papo-de-dados.json) | Rascunho completo de um roteiro de podcast com seis vozes, incluindo um bloco opcional. |
| [`examples/papo-de-dados-18min.json`](examples/papo-de-dados-18min.json) | Versão enxuta do mesmo roteiro, escrita para caber no limite de 20 minutos. |
| [`examples/voice-test.json`](examples/voice-test.json) | Um único personagem lendo a abertura, para comparar vozes e velocidades. |

## Convertendo um roteiro `.docx`

```bash
python scripts/docx_to_json.py roteiro.docx saida.json
```

Python 3, só biblioteca padrão. O conversor espera o modelo em que este projeto foi construído:

- a seção do roteiro começa no parágrafo `Roteiro` e termina no parágrafo que começa com `Referências`;
- um parágrafo com `(tempo estimado: ...)` ou `(tempo medido: ...)` abre um bloco;
- um parágrafo `Rótulo: fala` vira uma fala quando o rótulo está em `CHARACTERS`.

Para outro grupo, idioma ou modelo, edite as constantes no início de [`scripts/docx_to_json.py`](scripts/docx_to_json.py).

## Limitações

- Usa a Web Speech API do navegador. Chrome e Edge são os navegadores suportados; as vozes disponíveis dependem do sistema operacional e do navegador, e algumas vozes funcionam pela rede.
- Voz sintética é mais regular que fala humana: some uma margem de 5% a 10% ao tempo medido.
- A medição vale apenas para a velocidade e a pausa escolhidas.

## Estrutura do projeto

```
.
├── index.html              # o app
├── examples/               # roteiros prontos para importar
├── scripts/
│   └── docx_to_json.py     # conversor .docx → JSON
├── README.md
├── README.pt-BR.md
└── LICENSE
```

## Próximos passos

- [ ] Interface em inglês (com seletor de idioma)
- [ ] Script de teste para manter o app e os exemplos em sincronia

## Licença

[MIT](LICENSE)
