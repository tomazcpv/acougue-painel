import json
import math

arquivo_txt = "ITENSMGV.txt"
arquivo_json = "produtos.json"

ITENS_POR_SLIDE = 12

# SOMENTE carnes reais
CARNES = [
    # Bovino
    "PICANHA",
    "ALCATRA",
    "MAMINHA",
    "FRALDA",
    "PATINHO",
    "ACEM",
    "ACÉM",
    "COXAO",
    "COXÃO",
    "CONTRA",
    "CUPIM",
    "COSTELA",
    "MUSCULO",
    "MÚSCULO",
    "PALETA",

    # Frango
    "FRANGO",
    "PEITO",
    "ASA",
    "COXA",
    "SOBRECOXA",

    # Suíno
    "SUINO",
    "SUÍNO",
    "PERNIL",
    "LOMBO",
    "BISTECA",
    "BACON",

    # Embutidos
    "LINGUI",
    "LINGUIÇA",
    "TOSCANA",
    "CALABRESA"
]

def eh_carne(nome):
    nome = nome.upper()

    for carne in CARNES:
        if carne in nome:
            return True

    return False


def formatar_preco(valor):
    try:
        valor = float(valor)
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"


produtos = []

with open(arquivo_txt, "r", encoding="latin-1") as f:
    linhas = f.readlines()

for linha in linhas:

    partes = linha.strip().split()

    if len(partes) < 2:
        continue

    preco_str = partes[-1]
    nome = " ".join(partes[:-1])

    # FILTRO DE CARNE
    if eh_carne(nome):

        preco_str = preco_str.replace(",", ".")

        produto = {
            "nome": nome + " KG",
            "preco": formatar_preco(preco_str)
        }

        produtos.append(produto)

# Divide em slides
slides = []
total_slides = math.ceil(len(produtos) / ITENS_POR_SLIDE)

for i in range(total_slides):
    inicio = i * ITENS_POR_SLIDE
    fim = inicio + ITENS_POR_SLIDE
    slides.append(produtos[inicio:fim])

# Salva JSON
with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print("OK!")
print("Produtos encontrados:", len(produtos))
print("Slides:", total_slides)