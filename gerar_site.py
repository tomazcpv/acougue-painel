import json
import unicodedata

# Lista MUITO específica de carnes
CARNES = [
    "ACEM", "ALCATRA", "PICANHA", "CONTRA FILE", "CONTRAFILE", "FILE",
    "PATINHO", "COXAO", "MUSCULO", "COSTELA", "FRALDA", "CAPA",
    "CUPIM", "PALETA", "OSSOBUCO", "RABADA", "BIFE", "CARNE",

    # Frango
    "FRANGO", "COXA", "SOBRECOXA", "ASA", "PEITO",

    # Porco
    "SUINO", "PERNIL", "LOMBO", "BACON", "TOUCINHO", "COSTELINHA",

    # Linguiça
    "LINGUICA", "TOSCANA", "CALABRESA"
]


def normalizar(texto):
    texto = texto.upper()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def eh_carne(nome):
    nome = normalizar(nome)

    for carne in CARNES:
        if carne in nome:
            return True

    return False


# Carregar produtos
with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)


# Filtrar
produtos_filtrados = []
for p in produtos:
    nome = p["nome"]

    if eh_carne(nome):
        produtos_filtrados.append(p)


# Salvar
with open("produtos_filtrados.json", "w", encoding="utf-8") as f:
    json.dump(produtos_filtrados, f, indent=2, ensure_ascii=False)


print(f"{len(produtos_filtrados)} carnes encontradas.")