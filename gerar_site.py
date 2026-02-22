import json
import math

# ==============================
# LISTA OFICIAL (180 ITENS)
# ==============================

CARNES_PERMITIDAS = [
"LINGUIÇA BRAGANÇA",
"CALABRESA PERDIGÃO",
"SALSICHA SADIA",
"SALSICHA AURORA KG",
"SALSICHA PERDIGÃO KG",
"CALABRESA SADIA",
"LINGUIÇA TOSCANA SADIA",
"LINGUIÇA TOSCANA AURORA",
"BACON",
"LINGUIÇA PERDIGÃO NA BRASA",
"LINGUIÇA FINA MISTA",
"SALSICHA RESFRIADA SEARA",
"SALSICHA PIF PAF",
"PICANHA",
"MAMINHA",
"MIOLO DE ALCATRA",
"ALCATRA EM PEÇA",
"CONTRA FILE",
"CONTRA FILE EM PEÇA",
"LAGARTO",
"ALCATRA COM MAMINHA",
"CHULETA DE CONTRA FILE",
"FILE MIGNOM",
"CAPA DE FILE",
"ACEM",
"PALETA",
"PEITO BOVINO",
"COSTELA DE RIPA",
"COSTELA PONTA DE AGULHA",
"COSTELA DE PEITO",
"FRANGO INTEIRO",
"COXA SOBRECOXA",
"SOBRECOXA",
"ASA DE FRANGO",
"MEIO DA ASA",
"PERNIL SEM OSSO",
"PERNIL COM OSSO",
"LOMBO SUINO",
"BISTECA",
"PATINHO",
"CUPIM",
"FRALDINHA",
"MUSCULO",
"COSTELA BOVINA",
"PICANHA SUÍNA",
"PANCETA",
"SHORT RIB BOVINO"
]

# ==============================
# NORMALIZAR
# ==============================

def norm(txt):
    return txt.upper().strip()

# ==============================
# CARREGAR JSON
# ==============================

with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data[0], list):
    produtos = data[0]
else:
    produtos = data

permitidos = [norm(x) for x in CARNES_PERMITIDAS]

# ==============================
# FILTRAR
# ==============================

filtrados = []

for p in produtos:
    nome = norm(p["nome"])
    if nome in permitidos:
        filtrados.append(p)

# ==============================
# SLIDES
# ==============================

itens_por_slide = 12
total_slides = math.ceil(len(filtrados)/itens_por_slide)

slides_html = ""

for s in range(total_slides):
    inicio = s*itens_por_slide
    fim = inicio+itens_por_slide
    bloco = filtrados[inicio:fim]

    slides_html += f'<div class="slide">'

    slides_html += "<table>"

    for item in bloco:
        slides_html += f"""
        <tr>
            <td>{item['nome']}</td>
            <td class="preco">{item['preco']}</td>
        </tr>
        """

    slides_html += "</table>"
    slides_html += "</div>"

# ==============================
# HTML
# ==============================

html = f"""
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="60">

<style>

body {{
    margin:0;
    font-family: Arial;
    background:#111;
    color:white;
    overflow:hidden;
}}

.slide {{
    display:none;
    padding:40px;
}}

table {{
    width:100%;
    font-size:32px;
}}

td {{
    padding:10px;
}}

.preco {{
    text-align:right;
    color:yellow;
}}

h1 {{
    text-align:center;
    font-size:50px;
}}

</style>

</head>

<body>

<h1>OFERTAS DO AÇOUGUE</h1>

{slides_html}

<script>

let slide = 0;
let slides = document.getElementsByClassName("slide");

function mostrar() {{

    for (let i=0; i<slides.length; i++)
        slides[i].style.display="none";

    slides[slide].style.display="block";

    slide++;
    if (slide>=slides.length)
        slide=0;
}}

mostrar();
setInterval(mostrar,10000);

</script>

</body>
</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("Slides gerados:", total_slides)
print("Itens encontrados:", len(filtrados))