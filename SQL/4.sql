-- Question 4 rahulsin
SELECT COUNT(*) ATLEAST_THREE
FROM(SELECT Title FROM StreamedMovies WHERE Hulu=1 AND Disney=1 AND PrimeVideo=1 UNION 
SELECT Title FROM StreamedMovies WHERE Hulu=1 AND PrimeVideo=1 AND Netflix=1 UNION
SELECT Title FROM StreamedMovies WHERE Disney=1 AND PrimeVideo=1 AND Netflix=1)