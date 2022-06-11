-- Question 10 rahulsin
SELECT CAST(COUNT(*) AS NUMERIC) PERCENT
FROM (SELECT Director FROM MovieData GROUP BY Director HAVING Rating >8)