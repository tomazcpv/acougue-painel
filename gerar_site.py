import json
import math
import re

arquivo_txt = "ITENSMGV.txt"
arquivo_json = "produtos.json"

ITENS_POR_SLIDE = 12

# Apenas carnes que queremos mostrar
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

    # Extrai o nome procurando o bloco de texto no meio da linha
    resultado = re.search(r'[A-ZÇÃÉÍÓÚÂÊÔÀ ]{3,}', linha.upper())

    if not resultado:
        continue

    nome = resultado.group().strip()

    # Extrai preço (normalmente fica antes do nome)
    numeros = re.findall(r'\d{4,6}', linha)
    if not numeros:
        continue

    preco_str = numeros[0]

    # Filtra apenas carnes
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

print("\nProdutos encontrados:")
for p in produtos:
    print("-", p["nome"])