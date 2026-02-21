import json

ARQUIVO_TXT = "ITENSMGV.txt"
ARQUIVO_JSON = "dados.json"

def categorizar(nome):
    nome = nome.upper()

    bovinos = ["PATINHO", "ALCATRA", "PICANHA", "MAMINHA", "COXAO", "FRALDINHA", "COSTELA"]
    suinos = ["SUINO", "BISTECA", "PERNIL", "LOMBO"]
    aves = ["FRANGO", "ASA", "COXA", "SOBRECOXA"]

    for item in bovinos:
        if item in nome:
            return "Bovino"

    for item in suinos:
        if item in nome:
            return "Suino"

    for item in aves:
        if item in nome:
            return "Aves"

    return "Outros"


def ler_txt():
    produtos = []

    with open(ARQUIVO_TXT, "r", encoding="latin1") as f:
        for linha in f:
            nome = linha[18:60].strip()
            preco = linha[9:14].strip()

            if nome and preco.isdigit():
                preco = float(preco) / 10

                produtos.append({
                    "nome": nome + " KG",
                    "preco": f"{preco:.2f}",
                    "categoria": categorizar(nome)
                })

    return produtos


produtos = ler_txt()

with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(produtos, f, indent=2, ensure_ascii=False)

print("Arquivo dados.json gerado!")