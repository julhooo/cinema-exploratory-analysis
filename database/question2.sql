WITH genresProfit AS(
    SELECT releaseYear, genres, 
           sum(profit) AS profit

    FROM films as t1

    LEFT JOIN genres as t2
    ON t1.tconst = t2.tconst

    LEFT JOIN financial as t3
    ON t1.tconst = t3.tconst

    GROUP BY releaseYear, genres
),

profitablegenres AS(
    SELECT genres, sum(profit) AS totalProfit

    FROM genresProfit

    GROUP BY genres

    ORDER BY totalProfit DESC

    LIMIT 8
)

SELECT t1.*

FROM genresProfit AS t1

INNER JOIN profitablegenres AS t2
ON t1.genres = t2.genres

WHERE releaseYear IS NOT 2026
