
# Questão 8 - Sistema de recomendação


import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

### Caminho base do projeto"""

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

"""### Carregar dataset"""

df_dataset = pd.read_csv(RAW_PATH/"vendas_2023_2024.csv")

df_dataset.head()

"""Criar matriz binária (usuário x produto)"""

matriz = (
    df_dataset.groupby(['id_client', 'id_product'])
    .size()
    .unstack(fill_value=0)
)

"""Converter para binário (1 = comprou, 0 = não comprou)"""

matriz = (matriz > 0).astype(int)

matriz.head()

"""Calculando produto x produto

Transpondo, agora linhas = produtos, colunas = clientes
"""

matriz_produto = matriz.T

"""Calcular similaridade de cosseno"""

similaridade = cosine_similarity(matriz_produto)

"""Transformar em DataFrame"""

df_similaridade = pd.DataFrame(
    similaridade,
    index=matriz_produto.index,
    columns=matriz_produto.index
)

df_similaridade.head()

"""Agora para descobrir o id do "GPS Garmin Vortex Maré Drift"
"""

df_produtos = pd.read_csv(RAW_PATH/"produtos_raw.csv")

df_produtos.head()

df_produtos[df_produtos['name'].str.contains("GPS Garmin", case=False, na=False)]

"""GPS Garmin Vortex Maré Drift tem o id 27"""

produto_id = 27

"""Pegar similaridades do produto"""

similares = df_similaridade.loc[produto_id]

"""Ordenar do maior para o menor"""

ranking = similares.sort_values(ascending=False)

"""Remover o próprio produto "GPS Garmin Vortex Maré Drift" (similaridade = 1)"""

ranking = ranking.drop(produto_id)

"""Top 5 produtos mais similares"""

top5 = ranking.head(5)

top5

"""Top 5 produtos mais similares com seus nomes"""

top5_df = top5.reset_index()
top5_df.columns = ['id_produto', 'similaridade']

top5_com_nome = top5_df.merge(
    df_produtos[['code', 'name']],
    left_on='id_produto',
    right_on='code',
    how='left'
)
top5_com_nome = top5_com_nome[['id_produto', 'name', 'similaridade']]

top5_com_nome

"""Questão 8.2 - Validação

Qual é o id _produto com MAIOR similaridade ao
"GPS Garmin Vortex Maré Drift"?

Resposta:
94
"""

top5.index[0]

"""O produto com a maior similaridade é o "Motor de Popa Volvo Magnum 276HP" que tem o id 94

com 0.869626 de similaridade.

Questão 8.3 - Explique:
1. Como a matriz foi construída?
2 . O que significa a similaridade de cosseno nesse
contexto?
3. Uma limitação desse método de recomendação.

Construi a matriz foi usando usuário × produto, onde cada linha representa um cliente e cada coluna um produto. Os valores são 1 se o cliente comprou o produto ao menos uma vez, 0 caso contrário, sem levar em conta a quantidade.

A similaridade mede o quanto dois produtos são comprados pelos mesmos clientes. Quanto mais próximo de 1, maior a semelhança no comportamento de compra.

Uma limitação é que o método considera apenas se houve ou não uma compra, se houvessem mais variaveis como quantidade de compra, contexto, características dos produtos e dos clientes, como demografia ou mesmo compras em sites de concorrentes poderia ser usado algo mais robusto como o KNN por exemplo.
"""