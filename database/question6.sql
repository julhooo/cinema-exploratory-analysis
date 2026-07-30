WITH revenue_year AS (
    SELECT releaseYear AS Year, primaryTitle AS Title, profit AS Profit

    FROM films AS t1

    LEFT JOIN financial AS t2
    ON t1.tconst = t2.tconst
),

enumerating AS (
    SELECT *,
    row_number() OVER (PARTITION BY Year ORDER BY Profit DESC) AS rn

    FROM revenue_year
)

SELECT Year, Title, Profit

FROM enumerating

WHERE rn <= 3