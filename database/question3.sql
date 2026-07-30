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

SELECT t1.releaseYear, t2.genres, 
       (1.*sum(t3.profit)/sum(t3.budget)) AS roi

FROM films AS t1

LEFT JOIN genres AS t2
ON t1.tconst = t2.tconst

LEFT JOIN financial AS t3
ON t1.tconst = t3.tconst

INNER JOIN profitablegenres AS t4
ON t2.genres = t4.genres

WHERE t1.releaseYear IS NOT 2026

GROUP BY t1.releaseYear, t2.genres

ORDER BY roi DESC