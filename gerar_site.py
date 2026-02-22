import json
import unicodedata

# Palavras que indicam carne
CARNES = [
    "ACEM", "ALCATRA", "PICANHA", "PATINHO", "COSTELA", "CUPIM",
    "FRANGO", "COXA", "SOBRECOXA", "ASA", "PEITO",
    "SUINO", "PERNIL", "LOMBO", "BACON",
    "LINGUICA", "TOSCANA", "CALABRESA",
    "BIFE", "CARNE", "FILE", "MAMINHA", "PALETA"
]

# Palavras proibidas (NUNCA são carne)
PROIBIDOS = [
    "BOLO",
    "QUEIJO",
    "ALECRIM",
    "BALA",
    "CEBOLA",
    "ALHO",
    "BATATA",
    "PÃO",
    "DOCE",
    "AÇUCAR",
    "ACUCAR",
    "AVEIA",
    "CACAU",
    "COCO",
    "FARINHA",
    "ARROZ",
    "FEIJAO",
    "TEMPERO",
    "ERVA",
    "CHA",
    "SEMENTE",
    "FATIADO",
    "RECHEADO"
]


def normalizar(texto):
    texto = texto.upper()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def eh_carne(nome):
    nome = normalizar(nome)

    # Se tiver palavra proibida → NÃO é carne
    for p in PROIBIDOS:
        if p in nome:
            return False

    # Se tiver palavra de carne → É carne
    for c in CARNES:
        if c in nome:
            return True

    return False


# Carregar produtos
with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)


produtos_filtrados = []

for p in produtos:
    nome = p["nome"]

    if eh_carne(nome):
        produtos_filtrados.append(p)


# Salvar
with open("produtos_filtrados.json", "w", encoding="utf-8") as f:
    json.dump(produtos_filtrados, f, indent=2, ensure_ascii=False)


print(f"{len(produtos_filtrados)} carnes encontradas.")