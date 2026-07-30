SELECT primaryTitle AS Title, releaseYear AS Year, numVotes AS Votes, boxoffice AS Boxoffice

FROM films AS t1

LEFT JOIN financial AS t2
ON t1.tconst = t2.tconst

ORDER BY numVotes DESC

LIMIT 10