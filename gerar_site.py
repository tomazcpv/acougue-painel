import json
import math

# =========================
# CONFIG
# =========================
ITENS_POR_SLIDE = 12
TEMPO_SLIDE_MS = 10000  # 10s

NOME_ACOUGUE = "Aliança Supermercado"
TEXTO_PROMO = "PROMOÇÃO DO DIA"
TEXTO_RODAPE = "Preços sujeitos a alteração sem aviso prévio."

MOSTRAR_RELOGIO = True

# Paleta (sólida)
COR_FUNDO = "#0b0b0b"
COR_TOPO = "#7a0000"
COR_CARD = "#121212"
COR_CARD_PROMO = "#1a0b0b"
COR_LINHA = "#2a2a2a"
COR_TEXTO = "#ffffff"
COR_DESTAQUE = "#ffd700"  # amarelo
COR_SUBTEXTO = "#d7d7d7"


# =========================
# CARREGAR produtos.json
# =========================
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# Achatar (se vier como lista de listas)
produtos = []
if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
    for grupo in data:
        for item in grupo:
            produtos.append(item)
else:
    produtos = data

total_produtos = len(produtos)
total_slides = math.ceil(total_produtos / ITENS_POR_SLIDE)

print("Total de produtos:", total_produtos)
print("Total de slides:", total_slides)


def chunk(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]


def render_coluna(itens):
    linhas = ""
    for p in itens:
        nome = p.get("nome", "")
        preco = p.get("preco", "")
        linhas += f"""
          <div class="linha">
            <div class="nome">{nome}</div>
            <div class="preco">{preco}</div>
          </div>
        """
    return linhas


# =========================
# MONTAR SLIDES
# =========================
slides_html = ""
for idx, bloco in enumerate(chunk(produtos, ITENS_POR_SLIDE)):
    if not bloco:
        continue

    promo = bloco[0]           # 1º item = promoção
    tabela = bloco[1:]         # resto vai pra tabela (11)

    # divide tabela em 2 colunas (pra ficar grande e organizado)
    metade = math.ceil(len(tabela) / 2) if len(tabela) > 0 else 0
    col1 = tabela[:metade]
    col2 = tabela[metade:]

    promo_nome = promo.get("nome", "")
    promo_preco = promo.get("preco", "")

    slides_html += f"""
    <section class="slide {'ativo' if idx == 0 else ''}">
      <div class="layout">

        <div class="promo">
          <div class="promo-badge">{TEXTO_PROMO}</div>
          <div class="promo-nome">{promo_nome}</div>
          <div class="promo-preco">{promo_preco}</div>
          <div class="promo-detalhe">Aproveite! Oferta válida enquanto durar o estoque.</div>
        </div>

        <div class="card-tabela">
          <div class="tabela">
            <div class="coluna">
              {render_coluna(col1)}
            </div>
            <div class="coluna">
              {render_coluna(col2)}
            </div>
          </div>
        </div>

      </div>
    </section>
    """


# =========================
# HTML FINAL
# =========================
html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{NOME_ACOUGUE} - Painel de Preços</title>

<style>
  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    background: {COR_FUNDO};
    color: {COR_TEXTO};
    font-family: Arial, Helvetica, sans-serif;
    overflow: hidden;
  }}

  .topo {{
    height: 120px;
    background: {COR_TOPO};
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 48px;
  }}

  .brand {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .titulo {{
    font-size: 56px;
    font-weight: 900;
    letter-spacing: 0.5px;
    line-height: 1;
  }}

  .subtitulo {{
    font-size: 20px;
    color: {COR_SUBTEXTO};
    font-weight: 700;
  }}

  .logo {{
    height: 78px;
    width: auto;
    border-radius: 12px;
    background: rgba(255,255,255,0.10);
    padding: 6px;
  }}

  .conteudo {{
    height: calc(100vh - 120px - 54px);
    padding: 22px 48px;
  }}

  .slide {{
    display: none;
    height: 100%;
  }}

  .slide.ativo {{
    display: block;
  }}



.layout {{
  height: 100%;
  display: grid;
  grid-template-columns: 0.30fr 0.70fr; /* 30% promo / 70% tabela */
  gap: 22px;
}}

  /* PROMOÇÃO */
  .promo {{
    height: 100%;
    background: {COR_CARD_PROMO};
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.50);
    display: flex;
    flex-direction: column;
    justify-content: center;
    border: 2px solid rgba(255, 215, 0, 0.22);
  }}

  .promo-badge {{
    display: inline-block;
    align-self: flex-start;
    padding: 10px 16px;
    border-radius: 999px;
    background: rgba(255, 215, 0, 0.12);
    color: {COR_DESTAQUE};
    font-weight: 900;
    letter-spacing: 1px;
    font-size: 22px;
    margin-bottom: 18px;
  }}

  .promo-nome {{
    font-size: 42px;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 18px;
  }}

  .promo-preco {{
    font-size: 66px;
    font-weight: 900;
    color: {COR_DESTAQUE};
    line-height: 1;
    margin-bottom: 18px;
  }}

  .promo-detalhe {{
    font-size: 18px;
    color: {COR_SUBTEXTO};
    font-weight: 700;
  }}

  /* TABELA */
  .card-tabela {{
    height: 100%;
    background: {COR_CARD};
    border-radius: 26px;
    padding: 24px 28px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.50);
  }}

  .tabela {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px 40px;
    height: 100%;
    align-content: start;
  }}

  .coluna {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .linha {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 10px 0;
    border-bottom: 1px solid {COR_LINHA};
  }}

  .nome {{
    font-size: 32px;
    font-weight: 850;
    max-width: 72%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }}

  .preco {{
    font-size: 36px;
    font-weight: 900;
    color: {COR_DESTAQUE};
    padding-left: 16px;
    white-space: nowrap;
  }}

  .rodape {{
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px;
    color: {COR_SUBTEXTO};
    background: rgba(255,255,255,0.04);
    font-size: 18px;
    font-weight: 700;
  }}

  .relogio {{
    font-variant-numeric: tabular-nums;
  }}
</style>
</head>

<body>
  <header class="topo">
    <div class="brand">
      <div class="titulo">{NOME_ACOUGUE}</div>
      <div class="subtitulo">Painel de preços</div>
    </div>
    <img src="logo.png" class="logo" alt="Logo">
  </header>

  <main class="conteudo">
    {slides_html}
  </main>

  <footer class="rodape">
    <div>{TEXTO_RODAPE}</div>
    <div class="relogio" id="relogio"></div>
  </footer>

<script>
  const TEMPO = {TEMPO_SLIDE_MS};
  let idx = 0;
  const slides = document.querySelectorAll(".slide");

  function mostrar(i) {{
    slides.forEach(s => s.classList.remove("ativo"));
    slides[i].classList.add("ativo");
  }}

  function avancar() {{
    if (slides.length === 0) return;
    idx = (idx + 1) % slides.length;
    mostrar(idx);
  }}

  if (slides.length > 0) mostrar(0);
  setInterval(avancar, TEMPO);

  // Relógio
  const mostrarRelogio = {str(MOSTRAR_RELOGIO).lower()};
  const el = document.getElementById("relogio");

  function tick() {{
    if (!mostrarRelogio) {{
      el.textContent = "";
      return;
    }}
    const now = new Date();
    const h = String(now.getHours()).padStart(2, "0");
    const m = String(now.getMinutes()).padStart(2, "0");
    el.textContent = h + ":" + m;
  }}
  tick();
  setInterval(tick, 1000);
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html gerado com promoção à esquerda + tabela à direita.")