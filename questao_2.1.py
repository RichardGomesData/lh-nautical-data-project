# Questão 2 - Produtos

import pandas as pd
from pathlib import Path
import unicodedata

BASE_PATH = Path().resolve()

while BASE_PATH.name != "lh-nautical-data-project":
    BASE_PATH = BASE_PATH.parent

print(f"BASE PATH: {BASE_PATH}")

DATA_PATH = BASE_PATH / "data"
RAW_PATH = DATA_PATH / "raw"

print(f"RAW PATH: {RAW_PATH}")


df_produtos = pd.read_csv(RAW_PATH / "produtos_raw.csv", encoding="utf-8")


# Parte 1 - Padronize os nomes das categorias d e produtos em: eletrônicos, propulsão e ancoragem.

df_produtos.shape

df_produtos.info()

df_produtos["actual_category"].unique()

df_produtos["actual_category_clean"] = (
    df_produtos["actual_category"]
    .str.lower()
    .str.strip()
)

df_produtos["actual_category_clean"].unique()

import unicodedata

def remover_acentos(texto):
    if isinstance(texto, str):
        return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    return texto

df_produtos["actual_category_clean"] = df_produtos["actual_category_clean"].apply(remover_acentos)

df_produtos["actual_category_clean"].unique()

# Remoção de espaços internos nas categorias


df_produtos["actual_category_clean"] = (
    df_produtos["actual_category_clean"]
    .str.replace(" ", "", regex=False)
)

df_produtos["actual_category_clean"].unique()

# Padronização das categorias

def padronizar_categoria(cat):
    if "eletro" in cat:
        return "eletronicos"
    elif "prop" in cat:
        return "propulsao"
    elif "ancor" in cat:
        return "ancoragem"
    else:
        return "outros"

df_produtos["category_final"] = df_produtos["actual_category_clean"].apply(padronizar_categoria)

df_produtos["category_final"].unique()


df_produtos[df_produtos["category_final"] == "outros"]["actual_category_clean"].unique()


def padronizar_categoria(cat):
    if "eletro" in cat or "eletru" in cat:
        return "eletronicos"
    elif "prop" in cat:
        return "propulsao"
    elif "ancor" in cat or "encor" in cat:
        return "ancoragem"
    else:
        return "outros"


df_produtos["category_final"] = df_produtos["actual_category_clean"].apply(padronizar_categoria)

df_produtos["category_final"].unique()


df_produtos = df_produtos[[
    "name",
    "price",
    "code",
    "category_final"
]].rename(columns={
    "name": "nome_produto",
    "price": "preco",
    "code": "codigo_produto",
    "category_final": "categoria"
})

df_produtos

df_produtos.info()


# Parte 2 - Converta os valores para o tipo numérico.


df_produtos["preco"] = (
    df_produtos["preco"]
    .str.replace("R$", "", regex=False)
    .str.strip()
    .astype(float)
)

print(df_produtos['preco'].dtype)


# Parte 3 - Remova as duplicatas.

# verificando os duplicados


duplicados_antes = df_produtos.duplicated().sum()
df_produtos = df_produtos.drop_duplicates()
duplicados_depois = df_produtos.duplicated().sum()
duplicados_removidos = duplicados_antes - duplicados_depois
duplicados_removidos

# Removendo os duplicados.

duplicados_removidos = df_produtos.duplicated().sum()
duplicados_removidos
