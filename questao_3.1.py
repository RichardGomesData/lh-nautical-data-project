# Questão 3 - Custos de Importação

import pandas as pd
from pathlib import Path
import unicodedata
import json 


BASE_PATH = Path().resolve()

while BASE_PATH.name != "lh-nautical-data-project":
    BASE_PATH = BASE_PATH.parent

print(f"BASE PATH: {BASE_PATH}")

DATA_PATH = BASE_PATH / "data"
RAW_PATH = DATA_PATH / "raw"

print(f"RAW PATH: {RAW_PATH}")

# Leitura e carregamento dos dados dos custos de importação (custos_importacao.json)

with open(RAW_PATH / "custos_importacao.json", "r", encoding="utf-8") as f:
    custos_importacao_json = json.load(f)

custos_importacao = pd.json_normalize(custos_importacao_json)
custos_importacao.shape
custos_importacao.head(10)

# Compreendendo o conteúdo de "historic_data"

custos_importacao["historic_data"].iloc[0]

# Várias datas para apenas um único produto. Vai ser preciso "explodir" a coluna

custos_importacao_exploded = custos_importacao.explode("historic_data")
custos_importacao_exploded.head()

# Agora já dá pra separar em colunas, extraindo os campos do dicionário.

custos_importacao_exploded["start_date"] = custos_importacao_exploded["historic_data"].apply(lambda x: x["start_date"])
custos_importacao_exploded["usd_price"] = custos_importacao_exploded["historic_data"].apply(lambda x: x["usd_price"])
custos_importacao_exploded.head()


# Agora posso montar as colunas  finais para como foi pedido. 

custos_importacao_final = custos_importacao_exploded[[
    "product_id",
    "product_name",
    "category",
    "start_date",
    "usd_price"
]]

custos_importacao_final.head()

custos_importacao_final.info()

# Tive que corrigir o tipo da data de "start_date"

custos_importacao_final["start_date"] = pd.to_datetime(
    custos_importacao_final["start_date"],
    dayfirst=True
)

custos_importacao_final.info()
custos_importacao_final.head()
