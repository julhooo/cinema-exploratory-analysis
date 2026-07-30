SELECT releaseYear, sum(profit) AS profit,
       sum(budget) AS budget,
       sum(boxoffice) AS boxoffice
       

FROM films as t1

LEFT JOIN financial as t2
ON t1.tconst = t2.tconst

GROUP BY releaseYear
ORDER BY profit DESC
