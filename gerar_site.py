import json
import math

arquivo_txt = "ITENSMGV.txt"
arquivo_json = "produtos.json"

ITENS_POR_SLIDE = 12

# Carnes permitidas
CARNES = [
    "PATINHO",
    "ACEM",
    "ACÉM",
    "PICANHA",
    "ALCATRA",
    "MAMINHA",
    "FRALDA",
    "COSTELA",
    "CUPIM",
    "LINGUIÇA",
    "LINGUICA",
    "CALABRESA",
    "FRANGO",
    "COXA",
    "SOBRECOXA",
    "PEITO",
    "ASA",
    "PERNIL",
    "LOMBO",
    "BISTECA",
    "BACON",
    "SALSICHA"
]

def eh_carne(nome):
    nome = nome.upper()
    for carne in CARNES:
        if carne in nome:
            return True
    return False

def formatar_preco(preco_str):
    try:
        valor = int(preco_str) / 100
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

produtos = []

with open(arquivo_txt, "r", encoding="latin-1") as f:
    linhas = f.readlines()

for linha in linhas:

    # Nome do produto começa na posição 18 e vai até 60
    nome = linha[18:60].strip()

    # Preço fica entre posição 10 e 16
    preco_str = linha[10:16].strip()

    if not nome:
        continue

    if eh_carne(nome):

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