import json

# Palavras que indicam carne
CARNES = [
    "BOV", "PATINHO", "ACEM", "ALCATRA", "PICANHA", "CUPIM",
    "MAMINHA", "FRALDINHA", "COSTELA", "CARNE", "BIFE",

    "FRANGO", "COXA", "SOBRECOXA", "ASA", "PEITO",
    "FILE", "PÉ DE FRANGO", "PESCOÇO",

    "SUINO", "PERNIL", "LOMBO", "BISTECA",

    "LINGUIÇA", "CALABRESA", "TOSCANA",
    "SALSICHA", "BACON"
]

# Palavras proibidas
PROIBIDOS = [
    "BOLO", "PÃO", "PAO", "DOCE", "BISCOITO", "FARINHA",
    "QUEIJO", "MUSSARELA", "PRESUNTO", "PERU",
    "ALHO", "CEBOLA", "BATATA", "VERDURA",
    "TEMPERO", "OREGANO", "ALECRIM",
    "AÇUCAR", "ACUCAR", "AVEIA", "CACAU",
    "CHA", "COCO", "GRANOLA",
    "BALA", "DOCINHO",
    "PIZZA", "ESFIHA", "EMPADA",
    "BROA"
]

def eh_carne(nome):
    nome = nome.upper()

    for p in PROIBIDOS:
        if p in nome:
            return False

    for c in CARNES:
        if c in nome:
            return True

    return False


# Abre o JSON
with open("produtos.json", encoding="utf-8") as f:
    data = json.load(f)

# Corrige lista dupla
if isinstance(data[0], list):
    produtos = data[0]
else:
    produtos = data

# Filtra carnes
produtos_filtrados = []

for p in produtos:
    nome = p["nome"]

    if eh_carne(nome):
        produtos_filtrados.append(p)
        print("OK:", nome)
    else:
        print("REMOVIDO:", nome)

print("\nTotal carnes:", len(produtos_filtrados))


# Gera HTML
html = """
<html>
<head>
<meta charset="UTF-8">
<style>
body {
    font-family: Arial;
    background: black;
    color: white;
    font-size: 28px;
}
.produto {
    margin: 10px;
    padding: 10px;
    border-bottom: 1px solid gray;
}
.preco {
    float: right;
}
</style>
</head>
<body>
<h1>AÇOUGUE - OFERTAS</h1>
"""

for p in produtos_filtrados:
    html += f"""
    <div class='produto'>
        {p['nome']}
        <span class='preco'>{p['preco']}</span>
    </div>
    """

html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\nSite gerado com sucesso!")