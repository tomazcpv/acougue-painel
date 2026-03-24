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
    Remove acentos, espaços duplos e unidade KG para comparar de forma justa.
    """
    if not txt: return ""
    txt = txt.upper().strip()
    # Remove acentos
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    # Remove pontuação e KG isolado
    txt = re.sub(r"[^A-Z0-9]+", " ", txt)
    txt = re.sub(r"\bKG\b", "", txt).strip()
    # Remove espaços duplos
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def carregar_permitidos(caminho: str) -> list[str]:
    permitidos = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha: continue
                permitidos.append(normalizar(linha))
    except FileNotFoundError:
        return []
    permitidos.sort(key=len, reverse=True)
    return permitidos

def permitido(nome_normalizado: str, permitidos: list[str]) -> bool:
    texto = f" {nome_normalizado} "
    for p in permitidos:
        alvo = f" {p} "
        if alvo in texto: return True
    return False

def formatar_preco_centavos(preco_5dig: str) -> str:
    valor = int(preco_5dig) / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ----------- PROCESSAMENTO -----------

permitidos = carregar_permitidos(ARQUIVO_LISTA)
melhores_precos = {} 
total_lidos = 0

with open(ARQUIVO_TXT, "r", encoding="latin-1") as f:
    for linha in f:
        if len(linha) < 30: continue

        nome_bruto = linha[18:68].strip()
        preco_raw = linha[10:15]

        if not nome_bruto or not preco_raw.isdigit(): continue

        total_lidos += 1
        nome_norm = normalizar(nome_bruto)

if permitido(nome_norm, permitidos):
            # 1. NOME DE EXIBIÇÃO:
            # - Remove o KG
            # - Remove sequências de 3 ou mais zeros seguidos (limpa o final do campo fixo)
            # - Remove espaços extras
            nome_exibicao = re.sub(r"\bKG\b", "", nome_bruto, flags=re.IGNORECASE).strip()
            nome_exibicao = re.sub(r"0{3,}", "", nome_exibicao) # Remove 3 ou mais zeros seguidos
            nome_exibicao = re.sub(r"\s+", " ", nome_exibicao).strip()

            # 2. CHAVE DE COMPARAÇÃO (para unificar SALSICHA SEARA e Salsicha Seara)
            chave_unica = normalizar(nome_exibicao)

            valor_atual = int(preco_raw)

            # 3. LÓGICA DE UNIFICAÇÃO (Mantém o maior preço)
            if chave_unica not in melhores_precos or valor_atual > melhores_precos[chave_unica]["valor_num"]:
                melhores_precos[chave_unica] = {
                    "nome": nome_exibicao,
                    "preco": formatar_preco_centavos(preco_raw),
                    "valor_num": valor_atual
                }

# Monta a lista final para o JSON
produtos_filtrados = [
    {"nome": v["nome"], "preco": v["preco"]} 
    for v in melhores_precos.values()
]

# ----------- GERAR SLIDES E SALVAR -----------
slides = []
for i in range(0, len(produtos_filtrados), ITENS_POR_SLIDE):
    slides.append(produtos_filtrados[i:i + ITENS_POR_SLIDE])

with open(SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print(f"Total lidos: {total_lidos}")
print(f"Total após unificar acentos e preços: {len(produtos_filtrados)}")
print("Sucesso! Verifique o arquivo produtos.json.")