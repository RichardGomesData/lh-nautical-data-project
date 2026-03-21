SELECT
    COUNT(*) AS total_linhas,

    COUNT(*) * 1.0 / COUNT(*) * 6 AS total_colunas,

    MIN(sale_date) AS data_min,
    MAX(sale_date) AS data_max,

    MIN(total) AS valor_min,
    MAX(total) AS valor_max,
    AVG(total) AS valor_medio

FROM vendas_2023_2024;