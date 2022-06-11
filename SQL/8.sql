-- Question 8 rahulsin
SELECT N.Year, MOV.QUANTITY
FROM(SELECT DISTINCT Year FROM StreamedMovies)N LEFT JOIN(SELECT Year,COUNT(*) QUANTITY FROM (SELECT Title FROM StreamedMovies WHERE PrimeVideo=1 INTERSECT SELECT Title FROM MovieData WHERE Genre LIKE '%Drama%'  )PRIME, 
StreamedMovies STREAM WHERE STREAM.Title=PRIME.Title GROUP BY Year)MOV ON MOV.Year= N.Year  