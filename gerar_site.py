import json
import math
import html as html_lib

# =========================
# CONFIG
# =========================
ITENS_POR_SLIDE = 21        # 1 promo + 10 bovinos + 10 suínos (ajuste se quiser)
TEMPO_SLIDE_MS = 10000      # 10s

NOME_EMPRESA = "Aliança Supermercado"
TEXTO_PROMO = "OFERTA DO DIA"

# Quantos itens por coluna (direita)
MAX_BOVINOS = 10
MAX_SUINOS = 10

def esc(s: str) -> str:
    return html_lib.escape(s or "")

# =========================
# Heurística de categoria
# =========================
def categoria(nome: str) -> str:
    n = (nome or "").upper()

    # SUÍNOS
    suinos_kw = [
        "SUIN", "SUÍN", "PORCO", "PERNIL", "BISTECA", "COSTELINHA", "PANCETA",
        "TOICINHO", "TORRESMO", "PAIO", "LINGUIÇA", "LINGUICA", "CUIBANA",
        "JOELHO", "ORELHA", "RABO SU", "PELE SU", "PRIME RIB SU", "TIBONE SU"
    ]
    # AVES (a referência não mostra "AVES", então eu NÃO vou criar 3ª coluna.
    # Itens de aves vão para "BOVINOS" por padrão, a não ser que você queira uma 3ª coluna depois.)
    aves_kw = [
        "FRANGO", "ASA", "COXA", "SOBRECOXA", "SASSAMI", "PERU",
        "PESCOÇO", "PÉ DE FRANGO", "PE DE FRANGO", "MOELA"
    ]

    if any(k in n for k in suinos_kw):
        return "SUINOS"
    if any(k in n for k in aves_kw):
        return "BOVINOS"  # fica na coluna da esquerda pra manter layout igual ao da imagem
    return "BOVINOS"

# =========================
# CARREGAR produtos.json
# =========================
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# Achatar listas
produtos = []
if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
    for grupo in data:
        for item in grupo:
            produtos.append(item)
else:
    produtos = data

def chunk(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i+n]

# =========================
# MONTAR SLIDES
# =========================
slides_html = ""

for idx, bloco in enumerate(chunk(produtos, ITENS_POR_SLIDE)):
    if not bloco:
        continue

    promo = bloco[0]
    resto = bloco[1:]

    bovinos = []
    suinos = []

    for p in resto:
        nome = p.get("nome", "")
        if categoria(nome) == "SUINOS":
            if len(suinos) < MAX_SUINOS:
                suinos.append(p)
        else:
            if len(bovinos) < MAX_BOVINOS:
                bovinos.append(p)

    def render_linhas(lista):
        out = ""
        for p in lista:
            nome = esc(p.get("nome", ""))
            preco = esc(p.get("preco", ""))
            out += f"""
            <div class="row">
              <div class="row-name">{nome}</div>
              <div class="row-price">{preco}</div>
            </div>
            """
        return out

    promo_nome = esc(promo.get("nome", ""))
    promo_preco = esc(promo.get("preco", ""))

    # preço sem "R$" duplicar na arte
    promo_preco_num = promo_preco.replace("R$", "").strip()

    slides_html += f"""
    <section class="slide {'active' if idx == 0 else ''}">
      <div class="screen">

        <!-- LADO ESQUERDO: OFERTA -->
        <aside class="left">
          <div class="wood-plaque">{TEXTO_PROMO}</div>

          <div class="promo-card">
            <div class="promo-title">{promo_nome}</div>

            <div class="promo-image">
              <!-- opcional: coloque promo.jpg na pasta -->
              <img src="promo.jpg" alt="" onerror="this.style.display='none'">
            </div>

            <div class="promo-price">
              <span class="rs">R$</span>
              <span class="big">{promo_preco_num}</span>
              <span class="unit">/KG</span>
            </div>
          </div>
        </aside>

        <!-- LADO DIREITO: LISTAS -->
        <main class="right">
          <div class="top-banner">
            <div class="banner-photo">
              <!-- opcional: coloque banner.jpg na pasta -->
              <img src="banner.jpg" alt="" onerror="this.style.display='none'">
            </div>
            <div class="brand">
              <img class="logo" src="logo.png" alt="Logo">
              <div class="brand-name">{NOME_EMPRESA}</div>
            </div>
          </div>

          <div class="tables">
            <section class="table-box">
              <div class="table-title">BOVINOS</div>
              <div class="table-body">
                {render_linhas(bovinos)}
              </div>
            </section>

            <section class="table-box">
              <div class="table-title">SUÍNOS</div>
              <div class="table-body">
                {render_linhas(suinos)}
              </div>
            </section>
          </div>
        </main>

      </div>
    </section>
    """

# =========================
# HTML FINAL
# =========================
html = f"""<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel - {NOME_EMPRESA}</title>

<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#000; font-family: Arial, Helvetica, sans-serif; overflow:hidden; }}

  /* Transição suave entre slides */
  .slide {{
    position: absolute;
    inset: 0;
    opacity: 0;
    transform: translateX(18px);
    transition: opacity 700ms ease, transform 700ms ease;
    pointer-events: none;
  }}
  .slide.active {{
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }}

  .screen {{
    width: 100vw;
    height: 100vh;
    display: grid;
    grid-template-columns: 30% 70%; /* como você pediu */
  }}

  /* Fundo madeira “fake” (não precisa imagem) */
  .wood {{
    background:
      linear-gradient(180deg, rgba(0,0,0,0.25), rgba(0,0,0,0.35)),
      repeating-linear-gradient(
        90deg,
        #3a2a1d 0px,
        #3a2a1d 22px,
        #2f2218 22px,
        #2f2218 44px
      );
  }}

  /* ======= ESQUERDA (OFERTA) ======= */
  .left {{
    padding: 22px;
  }}
  .left {{
    background:
      linear-gradient(180deg, rgba(0,0,0,0.25), rgba(0,0,0,0.45)),
      repeating-linear-gradient(
        90deg,
        #3a2a1d 0px,
        #3a2a1d 22px,
        #2f2218 22px,
        #2f2218 44px
      );
  }}

  .wood-plaque {{
    background: linear-gradient(180deg, #1a1a1a, #0f0f0f);
    border: 2px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 18px 16px;
    text-align: center;
    color: #fff;
    font-weight: 900;
    letter-spacing: 1px;
    font-size: 34px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.45);
    margin-bottom: 18px;
    text-transform: uppercase;
  }}

  .promo-card {{
    height: calc(100% - 92px);
    border-radius: 18px;
    background: radial-gradient(circle at 30% 20%, #fff3a3, #ffd400 60%, #f0b400);
    border: 3px solid rgba(255,255,255,0.40);
    box-shadow: 0 18px 28px rgba(0,0,0,0.55);
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .promo-title {{
    font-size: 44px;
    font-weight: 900;
    color: #b10000;
    text-align: center;
    text-transform: uppercase;
    line-height: 1.05;
    text-shadow: 0 2px 0 rgba(255,255,255,0.35);
  }}

  .promo-image {{
    display:flex;
    justify-content:center;
    align-items:center;
    padding: 10px 0;
  }}
  .promo-image img {{
    width: 88%;
    max-height: 320px;
    object-fit: contain;
    border-radius: 16px;
    box-shadow: 0 10px 18px rgba(0,0,0,0.30);
    background: rgba(255,255,255,0.35);
  }}

  .promo-price {{
    display:flex;
    align-items: baseline;
    justify-content: center;
    gap: 10px;
    padding-bottom: 8px;
  }}
  .promo-price .rs {{
    font-size: 42px;
    font-weight: 900;
    color: #b10000;
  }}
  .promo-price .big {{
    font-size: 92px;
    font-weight: 900;
    color: #b10000;
    letter-spacing: 1px;
    text-shadow: 0 8px 16px rgba(0,0,0,0.20);
  }}
  .promo-price .unit {{
    font-size: 26px;
    font-weight: 900;
    color: #222;
  }}

  /* ======= DIREITA (TABELAS) ======= */
  .right {{
    background:
      linear-gradient(180deg, rgba(0,0,0,0.20), rgba(0,0,0,0.35)),
      repeating-linear-gradient(
        90deg,
        #3a2a1d 0px,
        #3a2a1d 22px,
        #2f2218 22px,
        #2f2218 44px
      );
    padding: 18px 22px 22px 22px;
  }}

  .top-banner {{
    height: 120px;
    display: grid;
    grid-template-columns: 1fr 360px;
    gap: 18px;
    margin-bottom: 16px;
    align-items: stretch;
  }}

  .banner-photo {{
    border-radius: 14px;
    overflow: hidden;
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.12);
  }}
  .banner-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .brand {{
    border-radius: 14px;
    overflow: hidden;
    background: rgba(255,255,255,0.92);
    display:flex;
    align-items:center;
    justify-content:center;
    gap: 14px;
    padding: 10px 12px;
    border: 2px solid rgba(255,255,255,0.15);
  }}
  .brand .logo {{
    height: 82px;
    width: auto;
  }}
  .brand-name {{
    font-size: 24px;
    font-weight: 900;
    color: #111;
    text-align:center;
    line-height: 1.1;
  }}

  .tables {{
    height: calc(100% - 136px);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }}

  .table-box {{
    border-radius: 14px;
    overflow: hidden;
    border: 2px solid rgba(255,255,255,0.12);
    box-shadow: 0 14px 24px rgba(0,0,0,0.45);
    background: rgba(0,0,0,0.18);
    display:flex;
    flex-direction: column;
  }}

  .table-title {{
    padding: 12px 14px;
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    color: #fff;
    background: linear-gradient(180deg, rgba(0,0,0,0.55), rgba(0,0,0,0.25));
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
  }}

  .table-body {{
    padding: 12px 14px;
    display:flex;
    flex-direction: column;
    gap: 8px;
  }}

  .row {{
    display:flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 10px 12px;
    border-radius: 10px;
    background: rgba(0,0,0,0.22);
    border: 1px solid rgba(255,255,255,0.10);
  }}

  .row-name {{
    font-size: 26px;
    font-weight: 800;
    color: #fff;
    max-width: 72%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Preço com borda + sombra (bem legível na TV) */
  .row-price {{
    font-size: 30px;
    font-weight: 900;
    color: #fff;
    white-space: nowrap;
    text-shadow: 0 6px 14px rgba(0,0,0,0.55);
    -webkit-text-stroke: 1px rgba(255,255,255,0.55);
  }}

</style>
</head>
<body>

{slides_html}

<script>
  const TEMPO = {TEMPO_SLIDE_MS};
  let idx = 0;
  const slides = document.querySelectorAll(".slide");

  function show(i) {{
    slides.forEach(s => s.classList.remove("active"));
    slides[i].classList.add("active");
  }}

  function next() {{
    if (!slides.length) return;
    idx = (idx + 1) % slides.length;
    show(idx);
  }}

  if (slides.length) show(0);
  setInterval(next, TEMPO);
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html gerado no estilo da referência (madeira + oferta + duas colunas).")