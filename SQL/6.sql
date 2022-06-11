-- Question 6 rahulsin
SELECT Mov_d.Director 
FROM (SELECT Title,S.Director
FROM (SELECT Director FROM MovieData)P,MovieData S WHERE P.Director =S.Director)Mov_d,StreamedMovies str_m
WHERE Disney=1 AND Mov_d.Title = str_m.Title GROUP BY Mov_d.Director HAVING COUNT(*) >=2