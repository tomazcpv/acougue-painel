import json
import math
import html as html_lib

# =========================
# CONFIG
# =========================
ITENS_POR_SLIDE = 10            # recomendo 9~11 pra ficar bem grande na TV
TEMPO_SLIDE_MS = 10000          # 10s

NOME_ACOUGUE = "Aliança Supermercado"
CATEGORIA_TEXTO = "Bovino / Suíno / Aves"
TEXTO_PROMO = "OFERTA DO DIA"

# Se quiser, dá pra esconder o logo (mas você pediu para colocar)
MOSTRAR_LOGO = True

# =========================
# CARREGAR produtos.json
# =========================
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# Achatar listas (se vier como lista de listas)
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

def esc(x: str) -> str:
    return html_lib.escape(x or "")

# =========================
# MONTAR SLIDES (promo = 1º item)
# =========================
slides_html = ""
for idx, bloco in enumerate(chunk(produtos, ITENS_POR_SLIDE)):
    if not bloco:
        continue

    promo = bloco[0]        # 1º item do slide vira oferta grande
    tabela = bloco[1:]      # resto vira lista

    linhas_lista = ""
    for p in tabela:
        nome = esc(p.get("nome", ""))
        preco = esc(p.get("preco", ""))
        linhas_lista += f"""
          <div class="linha">
            <div class="linha-conteudo">
              <span class="item-nome">{nome}</span>
              <span class="item-preco">{preco}</span>
            </div>
            <div class="seta"></div>
          </div>
        """

    promo_nome = esc(promo.get("nome", ""))
    promo_preco = esc(promo.get("preco", ""))

    slides_html += f"""
    <section class="slide {'ativo' if idx == 0 else ''}">
      <div class="layout">

        <!-- LISTA (70%) -->
        <div class="lista">
          <div class="lista-header">
            <div class="lista-titulo">{CATEGORIA_TEXTO}</div>
          </div>

          <div class="lista-body">
            {linhas_lista}
          </div>
        </div>

        <!-- PROMOÇÃO (30%) -->
        <div class="promo">
          <div class="promo-box">
            <div class="promo-topo">
              {"<img src='logo.png' class='promo-logo' alt='Logo'>" if MOSTRAR_LOGO else ""}
              <div class="promo-badge">{TEXTO_PROMO}</div>
            </div>

            <div class="promo-nome">{promo_nome}</div>

            <div class="promo-preco-wrap">
              <div class="promo-rs">R$</div>
              <div class="promo-preco">{promo_preco.replace("R$","").strip()}</div>
            </div>

            <!-- Se no futuro você quiser imagem do produto, a gente coloca aqui -->
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
<title>{NOME_ACOUGUE}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
  :root {{
    --bg: #070707;
    --red1: #b10000;
    --red2: #7a0000;
    --red3: #4d0000;
    --white: #ffffff;
    --shadow: rgba(0,0,0,0.55);
    --yellow: #ffd700;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    background: var(--bg);
    color: var(--white);
    font-family: Arial, Helvetica, sans-serif;
    overflow: hidden;
  }}

  /* Slide + animação */
  .slide {{
    position: absolute;
    inset: 0;
    opacity: 0;
    transform: translateX(18px);
    transition: opacity 700ms ease, transform 700ms ease;
    pointer-events: none;
  }}
  .slide.ativo {{
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }}

  /* Layout 70/30 */
  .layout {{
    height: 100vh;
    display: grid;
    grid-template-columns: 70% 30%;
  }}

  /* LISTA (lado esquerdo 70%) com fundo imagem */
  .lista {{
    position: relative;
    padding: 26px 34px;
    background:
      linear-gradient(90deg, rgba(0,0,0,0.70), rgba(0,0,0,0.40)),
      url("bg.jpg");
    background-size: cover;
    background-position: center;
  }}

  /* Overlay extra para leitura */
  .lista::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.65), rgba(0,0,0,0.45));
    pointer-events: none;
  }}

  .lista > * {{
    position: relative;
    z-index: 1;
  }}

  .lista-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }}

  .lista-titulo {{
    font-size: 46px;
    font-weight: 900;
    text-shadow: 0 6px 16px var(--shadow);
    padding: 6px 14px;
    border-radius: 10px;
    background: rgba(177,0,0,0.65);
    border: 2px solid rgba(255,255,255,0.14);
    display: inline-block;
  }}

  .lista-body {{
    margin-top: 8px;
  }}

  /* Linha estilo referência (barra vermelha + seta) */
  .linha {{
    position: relative;
    margin: 10px 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 10px 18px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.10);
    background: linear-gradient(180deg, var(--red1), var(--red2));
  }}

  .linha-conteudo {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    gap: 16px;
  }}

  .item-nome {{
    font-size: 36px;
    font-weight: 900;
    letter-spacing: 0.4px;
    text-shadow: 0 4px 10px var(--shadow);
    max-width: 72%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Preço com borda branca + sombra (bem TV) */
  .item-preco {{
    font-size: 38px;
    font-weight: 900;
    color: var(--white);
    text-shadow:
      0 3px 10px rgba(0,0,0,0.55),
      0 0 1px rgba(255,255,255,0.9);
    -webkit-text-stroke: 1px rgba(255,255,255,0.70);
    white-space: nowrap;
  }}

  /* Seta no fim (triângulo) */
  .seta {{
    position: absolute;
    top: 0;
    right: 0;
    width: 0;
    height: 0;
    border-top: 33px solid transparent;
    border-bottom: 33px solid transparent;
    border-left: 30px solid rgba(255,255,255,0.18);
    filter: drop-shadow(0 6px 10px rgba(0,0,0,0.35));
  }}

  /* PROMO (lado direito 30%) */
  .promo {{
    background: #f6f6f6;
    padding: 22px 18px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .promo-box {{
    width: 100%;
    height: 100%;
    border-radius: 18px;
    background: #ffffff;
    border: 3px solid rgba(177,0,0,0.35);
    box-shadow: 0 16px 28px rgba(0,0,0,0.30);
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .promo-topo {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }}

  .promo-logo {{
    height: 74px;
    width: auto;
    border-radius: 12px;
    padding: 6px;
    background: rgba(0,0,0,0.04);
  }}

  .promo-badge {{
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #b10000;
    border: 2px solid rgba(177,0,0,0.25);
    border-radius: 999px;
    padding: 10px 12px;
    background: rgba(177,0,0,0.06);
    text-align: center;
    white-space: nowrap;
  }}

  .promo-nome {{
    margin-top: 8px;
    font-size: 40px;
    font-weight: 900;
    color: #b10000;
    text-align: center;
    line-height: 1.05;
  }}

  .promo-preco-wrap {{
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 6px;
  }}

  .promo-rs {{
    font-size: 42px;
    font-weight: 900;
    color: #b10000;
  }}

  .promo-preco {{
    font-size: 92px;
    font-weight: 900;
    color: #b10000;
    letter-spacing: 1px;
    text-shadow: 0 6px 14px rgba(0,0,0,0.20);
  }}

  /* Responsivo mínimo (caso abra no PC) */
  @media (max-width: 1200px) {{
    .item-nome {{ font-size: 28px; }}
    .item-preco {{ font-size: 30px; }}
    .promo-preco {{ font-size: 72px; }}
    .promo-nome {{ font-size: 32px; }}
    .lista-titulo {{ font-size: 36px; }}
  }}
</style>
</head>

<body>
{slides_html}

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

  // inicia
  if (slides.length > 0) mostrar(0);
  setInterval(avancar, TEMPO);
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html gerado (layout referência + 1 coluna + promo 30% / lista 70%).")