import json
import re

# Palavras que DEFINITIVAMENTE são carnes
PALAVRAS_CARNE = [
    "ACEM", "ALCATRA", "CONTRA FILE", "CONTRAFILE", "PATINHO", "COXAO",
    "MUSCULO", "COSTELA", "PICANHA", "FRALDA", "CAPA", "FILE",
    "CARNE", "BIFE", "FIGADO", "RABADA",

    # Frango
    "FRANGO", "COXA", "SOBRECOXA", "ASA", "PEITO", "DORSO",

    # Porco
    "SUINO", "SUINA", "PERNIL", "LOMBO", "BACON", "TOUCINHO", "COSTELINHA",

    # Linguiça e embutidos de açougue
    "LINGUICA", "TOSCANA", "CALABRESA",

    # Outros comuns
    "CUPIM", "PALETA", "OSSOBUCO"
]


def eh_carne(nome):
    nome = nome.upper()

    for palavra in PALAVRAS_CARNE:
        if palavra in nome:
            return True

    return False


# Carregar produtos
with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)


# Filtrar apenas carnes
produtos_filtrados = []
for p in produtos:
    nome = p["nome"]

    if eh_carne(nome):
        produtos_filtrados.append(p)


# Salvar apenas carnes
with open("produtos_filtrados.json", "w", encoding="utf-8") as f:
    json.dump(produtos_filtrados, f, indent=2, ensure_ascii=False)


print(f"{len(produtos_filtrados)} produtos de carne encontrados.")