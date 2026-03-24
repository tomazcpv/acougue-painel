import json
import re
import unicodedata

ARQUIVO_TXT = "ITENSMGV.txt"
ARQUIVO_LISTA = "carnes_permitidas.txt"
SAIDA_JSON = "produtos.json"
ITENS_POR_SLIDE = 12

def normalizar(txt: str) -> str:
    """
    Remove acentos e sujeiras para comparação interna.
    """
    if not txt: return ""
    txt = txt.upper().strip()
    # Remove acentos
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    # Mantém apenas letras e números
    txt = re.sub(r"[^A-Z0-9]+", " ", txt)
    # Remove KG isolado
    txt = re.sub(r"\bKG\b", "", txt).strip()
    return re.sub(r"\s+", " ", txt).strip()

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

# Abrimos com latin-1 para ler corretamente o arquivo MGV
with open(ARQUIVO_TXT, "r", encoding="latin-1") as f:
    for linha in f:
        if len(linha) < 70: continue

        # 1. Extração bruta do nome (posição 18 a 68)
        nome_bruto = linha[18:68]
        
        # 2. LIMPEZA DOS ZEROS: 
        # No MGV, o nome termina e começam os zeros de preenchimento.
        # Vamos remover apenas os zeros que estão no FINAL do campo de nome.
        nome_limpo = re.sub(r"0+$", "", nome_bruto.strip()).strip()
        
        # 3. Remover a unidade KG se existir no texto original
        nome_exibicao = re.sub(r"\bKG\b", "", nome_limpo, flags=re.IGNORECASE).strip()
        nome_exibicao = re.sub(r"\s+", " ", nome_exibicao)

        # 4. Preço (posições 10 a 15)
        preco_raw = linha[10:15]

        if not nome_exibicao or not preco_raw.isdigit(): continue

        total_lidos += 1
        nome_norm = normalizar(nome_exibicao)

        if permitido(nome_norm, permitidos):
            # Usamos o nome normalizado como CHAVE para evitar duplicados (mesmo com acentos diferentes)
            chave_unica = nome_norm
            valor_atual = int(preco_raw)

            # Só adiciona se for o maior preço para aquele nome
            if chave_unica not in melhores_precos or valor_atual > melhores_precos[chave_unica]["valor_num"]:
                melhores_precos[chave_unica] = {
                    "nome": nome_exibicao,
                    "preco": formatar_preco_centavos(preco_raw),
                    "valor_num": valor_atual
                }

# Converte o dicionário para a lista de produtos
produtos_filtrados = [
    {"nome": v["nome"], "preco": v["preco"]} 
    for v in melhores_precos.values()
]

# Opcional: Ordenar por nome antes de gerar os slides
produtos_filtrados.sort(key=lambda x: x["nome"])

# ----------- GERAR SLIDES -----------
slides = []
for i in range(0, len(produtos_filtrados), ITENS_POR_SLIDE):
    slides.append(produtos_filtrados[i:i + ITENS_POR_SLIDE])

with open(SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)

print(f"Total lidos no arquivo: {total_lidos}")
print(f"Produtos aceitos (após filtros e unificação): {len(produtos_filtrados)}")