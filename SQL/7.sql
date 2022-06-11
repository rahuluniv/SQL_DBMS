-- Question 7 rahulsin
SELECT Title FROM MovieData
WHERE Title NOT IN(SELECT Title FROM StreamedMovies) AND INSTR(Actors, Director)!=0