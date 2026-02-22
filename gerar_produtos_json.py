import json
import math
import re

ARQUIVO_TXT = "ITENSMGV.txt"
SAIDA_JSON = "produtos.json"
ITENS_POR_SLIDE = 12

def formatar_preco_centavos(preco_5dig: str) -> str:
    # preco_5dig exemplo: "04290" -> 42.90
    valor = int(preco_5dig) / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

produtos = []

with open(ARQUIVO_TXT, "r", encoding="latin-1") as f:
    for linha in f:
        if len(linha) < 30:
            continue

        # Nome (campo fixo: começa no 18)
        nome = linha[18:68].strip()
        if not nome:
            continue

        # Preço (campo fixo: 5 dígitos em 10:15)
        preco_raw = linha[10:15]
        if not preco_raw.isdigit():
            continue

        produtos.append({
            "nome": f"{nome} KG",
            "preco": formatar_preco_centavos(preco_raw)
        })

print("Produtos lidos do TXT:", len(produtos))
print("Exemplos (primeiros 5):")
for p in produtos[:5]:
    print("-", p["nome"], p["preco"])

# Divide em slides (listas de 12)
slides = []
for i in range(0, len(produtos), ITENS_POR_SLIDE):
    slides.append(produtos[i:i + ITENS_POR_SLIDE])

with open(SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print("OK! produtos.json gerado.")
print("Slides:", len(slides))