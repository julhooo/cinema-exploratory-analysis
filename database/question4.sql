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

SELECT t1.releaseYear, t2.genres, sum(t1.averageRating)/count(*) AS meanRating

FROM films AS t1

LEFT JOIN genres AS t2
ON t2.tconst = t1.tconst

INNER JOIN profitablegenres AS t3
ON t2.genres = t3.genres

WHERE t1.releaseYear IS NOT 2026

GROUP BY t2.genres, t1.releaseYear

ORDER BY releaseYear