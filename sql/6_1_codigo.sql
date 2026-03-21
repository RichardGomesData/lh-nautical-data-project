WITH RECURSIVE calendario AS (

    SELECT DATE(MIN(data_corrigida)) AS data
    FROM (
        SELECT 
            CASE 
                WHEN sale_date LIKE '__-__-____' 
                THEN SUBSTR(sale_date, 7, 4) || '-' || SUBSTR(sale_date, 4, 2) || '-' || SUBSTR(sale_date, 1, 2)
                ELSE sale_date
            END AS data_corrigida
        FROM vendas_2023_2024
    )

    UNION ALL

    SELECT DATE(data, '+1 day')
    FROM calendario
    WHERE data < (
        SELECT DATE(MAX(data_corrigida))
        FROM (
            SELECT 
                CASE 
                    WHEN sale_date LIKE '__-__-____' 
                    THEN SUBSTR(sale_date, 7, 4) || '-' || SUBSTR(sale_date, 4, 2) || '-' || SUBSTR(sale_date, 1, 2)
                    ELSE sale_date
                END AS data_corrigida
            FROM vendas_2023_2024
        )
    )

),

vendas_diarias AS (

    SELECT 
        DATE(
            CASE 
                WHEN sale_date LIKE '__-__-____' 
                THEN SUBSTR(sale_date, 7, 4) || '-' || SUBSTR(sale_date, 4, 2) || '-' || SUBSTR(sale_date, 1, 2)
                ELSE sale_date
            END
        ) AS data,
        SUM(total) AS total_dia
    FROM vendas_2023_2024
    GROUP BY data

),

base_completa AS (

    SELECT 
        c.data,
        COALESCE(v.total_dia, 0) AS total_dia
    FROM calendario c
    LEFT JOIN vendas_diarias v
        ON c.data = v.data

),

media_por_dia AS (

    SELECT 
        CASE STRFTIME('%w', data)
            WHEN '0' THEN 'Domingo'
            WHEN '1' THEN 'Segunda-feira'
            WHEN '2' THEN 'Terça-feira'
            WHEN '3' THEN 'Quarta-feira'
            WHEN '4' THEN 'Quinta-feira'
            WHEN '5' THEN 'Sexta-feira'
            WHEN '6' THEN 'Sábado'
        END AS dia_semana,
        AVG(total_dia) AS media_vendas
    FROM base_completa
    GROUP BY dia_semana

)

SELECT 
    dia_semana,
    ROUND(media_vendas, 2) AS media_vendas
FROM media_por_dia
ORDER BY media_vendas asc;