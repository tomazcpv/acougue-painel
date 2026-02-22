import json
import math

# =========================
# CONFIG
# =========================
ITENS_POR_SLIDE = 10          # menos itens pra ficar grande e legível
TEMPO_SLIDE_MS = 10000       # 10s

NOME_ACOUGUE = "Aliança Supermercado"
TEXTO_PROMO = "OFERTA DO DIA"
TEXTO_RODAPE = "Preços sujeitos a alteração sem aviso prévio."

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

total_produtos = len(produtos)
total_slides = math.ceil(total_produtos / ITENS_POR_SLIDE)

print("Total de produtos:", total_produtos)
print("Total de slides:", total_slides)


def chunk(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]


# =========================
# MONTAR SLIDES
# =========================
slides_html = ""
for idx, bloco in enumerate(chunk(produtos, ITENS_POR_SLIDE)):
    if not bloco:
        continue

    promo = bloco[0]      # 1º item = oferta grande
    tabela = bloco[1:]   # resto = lista

    linhas_lista = ""
    for p in tabela:
        nome = p.get("nome", "")
        preco = p.get("preco", "")
        linhas_lista += f"""
          <div class="linha">
            <span class="item-nome">{nome}</span>
            <span class="item-preco">{preco}</span>
          </div>
        """

    slides_html += f"""
    <section class="slide {'ativo' if idx == 0 else ''}">
      <div class="layout">

        <!-- LISTA (70%) -->
        <div class="lista">
          <div class="categoria">Bovino / Suíno / Aves</div>
          {linhas_lista}
        </div>

        <!-- PROMOÇÃO (30%) -->
        <div class="promo">
          <div class="promo-logo">
            <img src="logo.png" alt="Logo">
          </div>
          <div class="promo-nome">{promo.get("nome","")}</div>
          <div class="promo-preco">{promo.get("preco","")}</div>
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

<style>
body {{
  margin: 0;
  background: #000;
  color: #fff;
  font-family: Arial, Helvetica, sans-serif;
  overflow: hidden;
}}

.slide {{ display: none; height: 100vh; }}
.slide.ativo {{ display: block; }}

.layout {{
  display: grid;
  grid-template-columns: 70% 30%;
  height: 100vh;
}}

.lista {{
  background: url('bg.jpg') center/cover no-repeat, #8b0000;
  padding: 30px 40px;
}}

.categoria {{
  font-size: 42px;
  font-weight: 900;
  margin-bottom: 20px;
}}

.linha {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to right, #b30000, #7a0000);
  margin-bottom: 10px;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 32px;
  font-weight: 800;
}}

.item-preco {{
  color: #fff;
  font-size: 34px;
}}

.promo {{
  background: #fff;
  color: #000;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}

.promo-logo img {{
  max-width: 160px;
  margin-bottom: 20px;
}}

.promo-nome {{
  font-size: 36px;
  font-weight: 900;
  color: #c00;
  text-align: center;
  margin-bottom: 20px;
}}

.promo-preco {{
  font-size: 72px;
  font-weight: 900;
  color: #c00;
}}
</style>
</head>

<body>

{slides_html}

<script>
let idx = 0;
const slides = document.querySelectorAll(".slide");

function trocar() {{
  slides.forEach(s => s.classList.remove("ativo"));
  slides[idx].classList.add("ativo");
  idx = (idx + 1) % slides.length;
}}

trocar();
setInterval(trocar, {TEMPO_SLIDE_MS});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Site gerado com layout de 1 coluna + oferta grande.")