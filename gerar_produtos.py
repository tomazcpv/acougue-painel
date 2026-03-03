import json
import math
import re
import unicodedata

ARQUIVO_TXT = "ITENSMGV.txt"
ARQUIVO_LISTA = "carnes_permitidas.txt"
SAIDA_JSON = "produtos.json"
ITENS_POR_SLIDE = 12


def normalizar(txt: str) -> str:
    """
    Normaliza para comparar:
    - maiúsculas
    - remove acentos
    - troca pontuação por espaço
    - remove "KG" no final (se existir)
    - remove espaços duplicados
    """
    txt = txt.upper().strip()
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")  # remove acentos
    txt = re.sub(r"[^A-Z0-9]+", " ", txt)  # pontuação -> espaço
    txt = re.sub(r"\bKG\b$", "", txt).strip()  # remove KG no final
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def carregar_permitidos(caminho: str) -> list[str]:
    permitidos = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            permitidos.append(normalizar(linha))

    # Ordena do maior pro menor para reduzir matches ruins
    permitidos.sort(key=len, reverse=True)
    return permitidos


def permitido(nome_normalizado: str, permitidos: list[str]) -> bool:
    """
    Match por palavra inteira (evita FILE bater em FILEZINHO, PE bater em PEITO, etc.)
    """
    # cria uma versão com espaços nas pontas pra facilitar boundary
    texto = f" {nome_normalizado} "

    for p in permitidos:
        # p pode ter espaço; usamos " boundary " com espaços
        alvo = f" {p} "
        if alvo in texto:
            return True

    return False


def formatar_preco_centavos(preco_5dig: str) -> str:
    valor = int(preco_5dig) / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ----------- carregar lista permitida -----------
permitidos = carregar_permitidos(ARQUIVO_LISTA)
print("Itens permitidos (lista):", len(permitidos))

# ----------- ler TXT e montar lista -----------
produtos_filtrados = []
total_lidos = 0
exemplos_rejeitados = []

with open(ARQUIVO_TXT, "r", encoding="latin-1") as f:
    for linha in f:
        if len(linha) < 30:
            continue

        # Nome (campo fixo: começa em 18)
        nome = linha[18:68].strip()
        if not nome:
            continue

        # Preço (5 dígitos: 10:15) -> 04290 = R$ 42,90
        preco_raw = linha[10:15]
        if not preco_raw.isdigit():
            continue

        total_lidos += 1

        nome_norm = normalizar(nome)

        if permitido(nome_norm, permitidos):
            produtos_filtrados.append({
                "nome": f"{nome.strip()} KG",
                "preco": formatar_preco_centavos(preco_raw)
            })
        else:
            if len(exemplos_rejeitados) < 25:
                exemplos_rejeitados.append(nome.strip())

print("Produtos lidos do TXT:", total_lidos)
print("Produtos aprovados (na lista):", len(produtos_filtrados))
if exemplos_rejeitados:
    print("\nExemplos rejeitados (amostra):")
    for x in exemplos_rejeitados:
        print("-", x)

# ----------- dividir em slides -----------
slides = []
for i in range(0, len(produtos_filtrados), ITENS_POR_SLIDE):
    slides.append(produtos_filtrados[i:i + ITENS_POR_SLIDE])

with open(SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print("\nOK! produtos.json gerado (filtrado).")
print("Slides:", len(slides))