-- Question 5 rahulsin
SELECT COUNT(*) netfllix_drama
FROM StreamedMovies 
WHERE EXISTS(SELECT * FROM MovieData WHERE Genre LIKE '%Drama%')AND Netflix=1 

