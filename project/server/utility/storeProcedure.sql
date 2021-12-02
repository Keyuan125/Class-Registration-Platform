DELIMITER //
DROP PROCEDURE IF EXISTS findRecommendation;
CREATE PROCEDURE findRecommendation(sUIN INT, tempSubject VARCHAR(10))
BEGIN

	DECLARE done INT DEFAULT 0;
	DECLARE c INT;
	DECLARE s, n VARCHAR(50);
	DECLARE g DOUBLE(10, 2);

	
	
	DECLARE course CURSOR FOR SELECT CRN, SubNum, Name, GPA FROM tempCourses;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;


	CREATE TABLE IF NOT EXISTS tempCourses AS
	(SELECT C.CRN, CONCAT(C.Subject, " ", C.Number) AS SubNum, C.Name, MAX(avgGPA) AS GPA
	from CoursesNew C INNER JOIN GPAsNew G on C.Subject = 
	G.CourseSubject and C.Number = G.CourseNumber WHERE 
	C.Subject = "CS" GROUP BY C.CRN, C.Subject, C.Number, C.Name HAVING MAX(avgGPA) < 3.2 LIMIT 10)

	UNION

	(SELECT C.CRN, CONCAT(C.Subject, " ", C.Number) AS SubNum, C.Name, MIN(avgGPA) AS GPA
	from CoursesNew C INNER JOIN GPAsNew G on C.Subject = 
	G.CourseSubject and C.Number = G.CourseNumber WHERE 
	C.Subject = "CS" GROUP BY C.CRN, C.Subject, C.Number, C.Name HAVING MIN(avgGPA) > 3.8 LIMIT 10);

	

	DROP TABLE toTake;

	CREATE TABLE IF NOT EXISTS toTake AS

	select L.CSN from 

	(select CSN, SEPSN from
	(select CSN, PSN, Sum(CEPSN >= 1) as SEPSN from
	(select CSN, PSN, Count(EPSN) as CEPSN from 

	(select distinct Prerequisite.CourseSubNum as CSN, 
	Prerequisite.PreSubNum as PSN, Prerequisite.EquPreSubNum as EPSN 
	from Students join Enrollments on Students.UIN = Enrollments.UIN 
	join (select concat(Subject, ' ', Number) as SubNum, CRN from Courses) T on T.CRN = Enrollments.CRN 
	join Prerequisite on T.SubNum = Prerequisite.EquPreSubNum where Students.UIN = sUIN) M 

	GROUP BY CSN, PSN) N
	GROUP BY CSN, PSN) K) P


	join


	(select CourseSubNum AS CSN,  Count(PreSubNum)  as CPSN
	from (select distinct CourseSubNum, PreSubNum from Prerequisite) A join 

	(select distinct Prerequisite.CourseSubNum as CSN 
	from Students join Enrollments on Students.UIN = Enrollments.UIN 
	join (select concat(Subject, ' ', Number) as SubNum, CRN from Courses) T on T.CRN = Enrollments.CRN 
	join Prerequisite on T.SubNum = Prerequisite.EquPreSubNum where Students.UIN = sUIN) M 

	on M.CSN = A.CourseSubNum

	GROUP BY CourseSubNum) L


	on P.CSN = L.CSN
	Where P.SEPSN = L.CPSN;



	CREATE TABLE IF NOT EXISTS FinalTable (
        CRN INT,
        SubNum VARCHAR(50),
        Name VARCHAR(50),
        GPA DOUBLE(10, 2),
        allow INT
    );


	OPEN course;

	read_loop: LOOP
		FETCH course INTO c, s, n, g;
		IF done = 1 THEN
			LEAVE read_loop;
		ELSEIF s in (SELECT * FROM toTake) THEN
			INSERT INTO FinalTable VALUES(c, s, n, g, 1);
		ELSE
			INSERT INTO FinalTable VALUES(c, s, n, g, 0);
		END IF;
	END LOOP read_loop;

	CLOSE course;

	SELECT * FROM FinalTable;

END;
//
DELIMITER ;
