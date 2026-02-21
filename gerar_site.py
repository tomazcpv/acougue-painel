import json
import math

# Nome do arquivo TXT exportado pelo ERP/balança
arquivo_txt = "ITENSMGV.txt"

# Nome do JSON que será gerado
arquivo_json = "produtos.json"

# Quantidade de itens por slide
ITENS_POR_SLIDE = 14

# Lista de palavras que identificam carnes
CARNES = [
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
    "BISTECA",
    "LINGUI",
    "FRANGO",
    "PEITO",
    "ASA",
    "COXA",
    "SOBRECOXA",
    "SUINO",
    "SUÍNO",
    "PERNIL",
    "LOMBO",
    "BACON",
    "CARNE",
    "FILE",
    "FILÉ"
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

    # Último campo é o preço
    preco_str = partes[-1]

    # O resto é o nome
    nome = " ".join(partes[:-1])

    # Remove espaços extras
    nome = nome.strip()

    # Filtra apenas carnes
    if eh_carne(nome):

        # Troca vírgula por ponto
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

print("Arquivo produtos.json gerado com sucesso!")
print(f"{len(produtos)} produtos encontrados")
print(f"{total_slides} slides gerados")