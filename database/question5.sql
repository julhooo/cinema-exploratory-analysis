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

SELECT t3.genres, (sum(budget)/count(*)) AS budget

FROM films AS t1

LEFT JOIN financial AS t2
ON t1.tconst = t2.tconst

LEFT JOIN genres AS t3
ON t1.tconst = t3.tconst

INNER JOIN profitablegenres AS t4
ON t3.genres = t4.genres

GROUP BY t3.genres

ORDER BY budget