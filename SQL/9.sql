-- Question 9 rahulsin
SELECT *
FROM(
SELECT 'PrimeVideo',Title,MAX(Revenue)FROM(SELECT MOV.Title,MOV.Revenue FROM MovieData MOV,StreamedMovies STREAM WHERE MOV.Title = STREAM.Title AND STREAM.PrimeVideo = 1)UNION
SELECT 'Disney', Title,MAX(Revenue)FROM(SELECT MOV.Title,MOV.Revenue FROM MovieData MOV,StreamedMovies STREAM WHERE MOV.Title = STREAM.Title AND STREAM.Disney = 1)UNION
SELECT 'Netflix',Title,MAX(Revenue)FROM(SELECT MOV.Title,MOV.Revenue FROM MovieData MOV,StreamedMovies STREAM WHERE MOV.Title = STREAM.Title AND STREAM.Netflix = 1)UNION
SELECT 'Hulu',Title,MAX(Revenue)FROM(SELECT MOV.Title,MOV.Revenue FROM MovieData MOV,StreamedMovies STREAM WHERE MOV.Title = STREAM.Title AND STREAM.Hulu = 1))
