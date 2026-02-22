import json
import math

ITENS_POR_SLIDE = 12

# =========================
# CARREGAR JSON
# =========================
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# Achatar listas
produtos = []
for grupo in data:
    for item in grupo:
        produtos.append(item)

total_produtos = len(produtos)
total_slides = math.ceil(total_produtos / ITENS_POR_SLIDE)

# =========================
# GERAR SLIDES HTML
# =========================
slides_html = ""

indice = 0
for s in range(total_slides):
    slides_html += '<div class="slide">\n'
    slides_html += '<div class="tabela">\n'

    for i in range(ITENS_POR_SLIDE):
        if indice >= total_produtos:
            break

        nome = produtos[indice]["nome"]
        preco = produtos[indice]["preco"]

        slides_html += f"""
        <div class="linha">
            <div class="nome">{nome}</div>
            <div class="preco">{preco}</div>
        </div>
        """

        indice += 1

    slides_html += '</div>\n'
    slides_html += '</div>\n'

# =========================
# HTML FINAL
# =========================
html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Ofertas do Açougue</title>

<style>
body {{
    margin: 0;
    background: #0f0f0f;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    overflow: hidden;
}}

.topo {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 40px;
    background: #7a0000;
}}

.topo h1 {{
    margin: 0;
    font-size: 52px;
}}

.logo {{
    height: 70px;
}}

.slide {{
    display: none;
    padding: 30px 60px;
}}

.slide.ativo {{
    display: block;
}}

.tabela {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 40px;
}}

.linha {{
    display: flex;
    justify-content: space-between;
    font-size: 32px;
    padding: 8px 0;
    border-bottom: 1px solid #333;
}}

.nome {{
    max-width: 70%;
}}

.preco {{
    font-weight: bold;
    color: #ffd700;
}}

.rodape {{
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background: #111;
    color: #aaa;
    font-size: 18px;
}}
</style>
</head>

<body>

<div class="topo">
    <h1>OFERTAS DO AÇOUGUE</h1>
    <!-- Se tiver logo, coloque logo.png na pasta e descomente abaixo -->
    <!-- <img src="logo.png" class="logo"> -->
</div>

{slides_html}

<div class="rodape">
    Preços sujeitos a alteração sem aviso prévio
</div>

<script>
let indice = 0;
let slides = document.getElementsByClassName("slide");

function mostrarSlide() {{
    for (let i = 0; i < slides.length; i++) {{
        slides[i].classList.remove("ativo");
    }}

    slides[indice].classList.add("ativo");
    indice++;

    if (indice >= slides.length) {{
        indice = 0;
    }}
}}

mostrarSlide();
setInterval(mostrarSlide, 10000);
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Site gerado com layout bonito!")
print("Produtos:", total_produtos)
print("Slides:", total_slides)