import json
import math
import re

arquivo_txt = "ITENSMGV.txt"
arquivo_json = "produtos.json"

ITENS_POR_SLIDE = 12

# Carnes verdadeiras
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
    "LOMBO",
    "PERNIL",
    "BISTECA",
    "FRANGO",
    "COXA",
    "SOBRECOXA",
    "ASA",
    "PEITO",
    "BACON",
    "LINGUIÇA",
    "LINGUICA",
    "CALABRESA",
    "SALSICHA"
]

# Coisas que NÃO são açougue
PROIBIDOS = [
    "PIZZA",
    "EMPADA",
    "EMPANADO",
    "EMPANADINHO",
    "ENROLADO",
    "ENROLADINHO",
    "MASSA",
    "PÃO",
    "PAO",
    "BOLO",
    "TORTA",
    "FATIA",
    "FAROFA",
    "BALA",
    "DOCE",
    "SEMENTE",
    "TEMPERO",
    "PIMENTA",
    "ORÉGANO",
    "OREGANO",
    "QUEIJO",
    "QJO",
    "AZEITONA",
    "MILHO",
    "BETERRABA",
    "BATATA",
    "CEBOLA",
    "ALHO",
    "VERDURA",
    "LEGUME",
    "FRUTA"
]


def eh_carne(nome):
    nome = nome.upper()

    # Se tiver algo proibido → ignora
    for p in PROIBIDOS:
        if p in nome:
            return False

    # Se tiver carne → aceita
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

    # Nome
    resultado = re.search(r'[A-ZÇÃÉÍÓÚÂÊÔÀ ]{3,}', linha.upper())
    if not resultado:
        continue

    nome = resultado.group().strip()

    # Preço
    numeros = re.findall(r'\d{4,6}', linha)
    if not numeros:
        continue

    preco_str = numeros[0]

    if eh_carne(nome):
        produtos.append({
            "nome": nome + " KG",
            "preco": formatar_preco(preco_str)
        })

# Divide slides
slides = []
total_slides = math.ceil(len(produtos) / ITENS_POR_SLIDE)

for i in range(total_slides):
    slides.append(produtos[i*ITENS_POR_SLIDE:(i+1)*ITENS_POR_SLIDE])

# Salva
with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print("OK!")
print("Produtos encontrados:", len(produtos))

print("\nLista final:")
for p in produtos:
    print("-", p["nome"])