import json
import math

# =========================
# CONFIGURAÇÕES
# =========================
ITENS_POR_SLIDE = 12

# =========================
# CARREGAR JSON
# =========================
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# ACHATAR LISTA (lista dentro de lista)
# =========================
produtos = []
for grupo in data:
    for item in grupo:
        produtos.append(item)

print("Total de produtos encontrados:", len(produtos))

# =========================
# CALCULAR SLIDES
# =========================
total_slides = math.ceil(len(produtos) / ITENS_POR_SLIDE)
print("Total de slides:", total_slides)

# =========================
# GERAR HTML
# =========================
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ofertas do Açougue</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    background: black;
    color: white;
    overflow: hidden;
}

.slide {
    display: none;
    padding: 40px;
}

.titulo {
    font-size: 50px;
    text-align: center;
    margin-bottom: 30px;
}

.produto {
    font-size: 32px;
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
}

.ativo {
    display: block;
}
</style>

</head>
<body>

<div class="titulo">Ofertas do Açougue</div>
"""

# =========================
# GERAR SLIDES
# =========================
indice = 0

for s in range(total_slides):

    html += f'<div class="slide" id="slide{s}">'

    for i in range(ITENS_POR_SLIDE):

        if indice >= len(produtos):
            break

        nome = produtos[indice]["nome"]
        preco = produtos[indice]["preco"]

        html += f"""
        <div class="produto">
            <div>{nome}</div>
            <div>{preco}</div>
        </div>
        """

        indice += 1

    html += "</div>"

# =========================
# SCRIPT DE TROCA DE SLIDE
# =========================
html += f"""
<script>

let slideAtual = 0;
let totalSlides = {total_slides};

function mostrarSlide() {{

    let slides = document.getElementsByClassName("slide");

    for (let i = 0; i < slides.length; i++) {{
        slides[i].classList.remove("ativo");
    }}

    slides[slideAtual].classList.add("ativo");

    slideAtual++;

    if (slideAtual >= totalSlides) {{
        slideAtual = 0;
    }}
}}

mostrarSlide();
setInterval(mostrarSlide, 10000);

</script>

</body>
</html>
"""

# =========================
# SALVAR SITE
# =========================
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Site gerado com sucesso!")