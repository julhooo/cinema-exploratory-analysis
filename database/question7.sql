--diretores que mais aparecem
WITH relevantDirectors AS (
    SELECT t3.crewName AS Director, count(*) AS Movies, sum(averageRating)/count(*) AS Mean_Rate

    FROM films AS t1

    LEFT JOIN directors AS t2
    ON t1.tconst = t2.tconst

    LEFT JOIN crew AS t3
    ON t2.nconst = t3.nconst

    GROUP BY t2.nconst

    ORDER BY Movies DESC, Mean_Rate DESC
)

SELECT * FROM relevantDirectors

LIMIT 10
