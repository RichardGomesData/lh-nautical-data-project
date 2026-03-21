WITH custos_recentes AS (
    SELECT 
        stg_custos_importacao_tratado.id_produto,
        stg_custos_importacao_tratado.preco_usd
    FROM stg_custos_importacao_tratado
    WHERE (stg_custos_importacao_tratado.id_produto, stg_custos_importacao_tratado.data_inicio) IN (
        SELECT 
            id_produto, 
            MAX(data_inicio)
        FROM stg_custos_importacao_tratado
        GROUP BY id_produto
    )
),

base_calculo AS (
    SELECT
        stg_vendas.id_produto,
        stg_vendas.valor_total,
        custos_recentes.preco_usd,
        cambio_diario.taxa_cambio
    FROM stg_vendas
    LEFT JOIN custos_recentes
        ON stg_vendas.id_produto = custos_recentes.id_produto
    LEFT JOIN cambio_diario
        ON stg_vendas.data_venda = cambio_diario.data
)

SELECT
    id_produto,

    SUM(valor_total) AS receita_total,

    SUM(
        CASE 
            WHEN (preco_usd * taxa_cambio - valor_total) > 0
            THEN (preco_usd * taxa_cambio - valor_total)
            ELSE 0
        END
    ) AS prejuizo_total,

    SUM(
        CASE 
            WHEN (preco_usd * taxa_cambio - valor_total) > 0
            THEN (preco_usd * taxa_cambio - valor_total)
            ELSE 0
        END
    ) * 1.0 / SUM(valor_total) AS percentual_prejuizo

FROM base_calculo

GROUP BY id_produto
ORDER BY percentual_prejuizo DESC
LIMIT 1;