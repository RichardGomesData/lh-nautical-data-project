# Questão 7 - Previsão de demanda


import pandas as pd
import numpy as np
import json
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import duckdb
from IPython.display import Image, display

"""### Caminho base do projeto"""

BASE_PATH = Path().resolve()

while BASE_PATH.name != "lh-nautical-data-project":
    BASE_PATH = BASE_PATH.parent

print(f"BASE PATH: {BASE_PATH}")

"""Caminhos para as pastas do projeto."""

DATA_PATH = BASE_PATH / "data"

RAW_PATH = DATA_PATH / "raw"
STAGING_PATH = DATA_PATH / "staging"
INTERMEDIATE_PATH = DATA_PATH / "intermediate"
MARTS_PATH = DATA_PATH / "marts"

SQL_PATH = BASE_PATH / "sql"
IMAGES_PATH = BASE_PATH / "imagens"

"""Para descobrir o id do produto "Motor de Popa Yamaha Evo Dash 155HP"

"""

df_produtos = pd.read_csv(MARTS_PATH / "dim_produto.csv")
df_produtos.head()

df_produtos[
    df_produtos["nome_produto"].str.contains("Yamaha Evo Dash", case=False, na=False)
]

"""Série temporal por dias, considerando apenas "Motor de Popa Yamaha Evo Dash 155HP" que tem o ID 54"""

df = pd.read_csv(RAW_PATH / "vendas_2023_2024.csv")

df["sale_date"] = pd.to_datetime(df["sale_date"], format="mixed", dayfirst=True)

df = df.sort_values("sale_date")

produto_id = 54

df_produto = df[df["id_product"] == produto_id].copy()

df_diario = (
    df_produto
    .groupby("sale_date")["qtd"]
    .sum()
    .reset_index()
)

df_diario.head(10)

"""Corrigindo a falta de dias na série temporal criando calendário completo"""

calendario = pd.DataFrame({
    "sale_date": pd.date_range(
        start=df_diario["sale_date"].min(),
        end=df_diario["sale_date"].max(),
        freq="D"
    )
})

"""Um merge para juntar com as vendas"""

df_diario = calendario.merge(df_diario, on="sale_date", how="left")

"""Preencher dias sem venda com 0"""

df_diario["qtd"] = df_diario["qtd"].fillna(0)
df_diario["qtd"] = df_diario["qtd"].astype(int)

df_diario

"""Separando TREINO e TESTE"""

df_treino = df_diario[df_diario["sale_date"] < "2024-01-01"].copy()
df_teste  = df_diario[df_diario["sale_date"] >= "2024-01-01"].copy()

df_treino.tail(), df_teste.head()

"""Para criar previsão com média móvel de 7 dias"""

df_diario["media_7d"] = df_diario["qtd"].shift(1).rolling(window=7).mean()

"""Filtrar previsões apenas do teste"""

df_resultado = df_diario[df_diario["sale_date"] >= "2024-01-01"].copy()

df_resultado.head()

"""Calcula MAE"""

mae = (df_resultado["qtd"] - df_resultado["media_7d"]).abs().mean()

mae

"""Questão 7.2 - Validação

Utilizando seu modelo treinado, qual é a soma total da
previsão de vendas (arredondada para número inteiro)

para o Motor de Popa Yamaha Evo Dash 155HP' durante a
primeira semana de Janeiro de 2024 (01/01 a 07/01)?

Resposta: 3

Primeira semana de janeiro
"""

df_semana_1 = df_resultado[
    (df_resultado["sale_date"] >= "2024-01-01") &
    (df_resultado["sale_date"] <= "2024-01-07")
]

"""Somando previsões"""

soma_previsao = df_semana_1["media_7d"].sum()

"""Arredondando para inteiro (como pedido)"""

soma_previsao_arredondada = round(soma_previsao)

soma_previsao, soma_previsao_arredondada

"""Questão 7.3 - Explique:
1. Como o baseline foi construído?
2. Como evitou data leakage?
3. Uma limitação do modelo proposto.

1. Como o baseline foi construído?

Construi o modelo usando a média móvel de 7 dias. Para cada dia do período de teste (janeiro de 2024), a previsão foi calculada como a média das vendas observadas nos 7 dias anteriores. Esse método só considera o comportamento mais recente da série temporal. Ele serve como caso de uso simples, apenas uma referência de previsão da demanda.

2. Como evitou data leakage?

Evitei o data leakage garantindo que, para cada previsão, fossem utilizados apenas dados históricos anteriores à data prevista, usando da função shift(1).

3. Uma limitação do modelo proposto

Esse tipo de modelo não captura padrões mais complexos, como tendências de longo prazo, sazonalidade ou fatores externos (como promoções ou mudanças de mercado). Por ser baseado apenas na média recente.
"""