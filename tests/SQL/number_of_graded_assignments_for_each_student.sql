-- Write query to get number of graded assignments for each student:
SELECT COUNT(*)
FROM assignments 
WHERE student_id = 1 AND state = 'GRADED'