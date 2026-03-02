# acougue-painel

Painel (GitHub Pages) para exibir preços do açougue em uma TV/monitor.

## Como funciona (100% online)
- A TV abre: `https://tomazcpv.github.io/acougue-painel/`
- A página **busca `produtos.json` automaticamente** e atualiza a tabela:
  - preços/itens: em até **60s**
- A página também checa `version.txt`:
  - se você mudar **layout/código** (index.html, CSS, imagens etc.), a TV **recarrega sozinha** em até **30s**

## Atualizar preços
1. Atualize o arquivo `ITENSMGV.txt` (export do sistema)
2. Ajuste a lista `carnes_permitidas.txt` (itens que devem aparecer)
3. Rode:
   - `atualizar_painel.bat`

O script:
- gera `produtos.json`
- atualiza `version.txt`
- faz `git commit` + `git push`

## Arquivos importantes
- `index.html` — página do painel (carrega dados dinamicamente)
- `produtos.json` — dados finais em “slides”
- `gerar_produtos_json.py` — gera o `produtos.json` filtrado a partir do TXT
- `version.txt` — “sinal” para forçar reload do site nas TVs
