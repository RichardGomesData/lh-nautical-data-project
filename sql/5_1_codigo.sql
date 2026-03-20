WITH vendas_produtos AS (
    SELECT 
        stg_vendas.id_cliente,
        stg_vendas.id_venda,
        stg_vendas.quantidade,
        stg_vendas.valor_total,
        stg_produtos.categoria_produt
    FROM stg_vendas
    LEFT JOIN stg_produtos
        ON stg_vendas.id_produto = stg_produtos.id_produto
),

clientes_metricas AS (
    SELECT
        id_cliente,
        SUM(valor_total) AS faturamento_total,
        COUNT(id_venda) AS frequencia,
        SUM(valor_total) * 1.0 / COUNT(id_venda) AS ticket_medio,
        COUNT(DISTINCT categoria_produt) AS diversidade
    FROM vendas_produtos
    GROUP BY id_cliente
),

clientes_elite AS (
    SELECT *
    FROM clientes_metricas
    WHERE diversidade >= 3
    ORDER BY ticket_medio DESC, id_cliente ASC
    LIMIT 10
),

top_clientes_vendas AS (
    SELECT vendas_produtos.*
    FROM vendas_produtos
    INNER JOIN clientes_elite
        ON vendas_produtos.id_cliente = clientes_elite.id_cliente
)

SELECT
    categoria_produt,
    SUM(quantidade) AS qtd_total
FROM top_clientes_vendas
GROUP BY categoria_produt
ORDER BY qtd_total DESC;