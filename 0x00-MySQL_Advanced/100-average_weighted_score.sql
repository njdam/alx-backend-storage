--SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
--	that computes and store the average weighted score for a student.

-- Requirements:
--	Procedure ComputeAverageScoreForUser is taking 1 input:
--		user_id, a users.id value
--		(you can assume user_id is linked to an existing users)

-- Tips:
--	[Calculate-Weighted-Average]
--	(https://intranet.alxswe.com/rltoken/QHx92mlF43zF6GTEil-Cyw)

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_weighted_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
        INTO total_weighted_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    IF total_weight = 0 THEN
        UPDATE users
            SET users.average_score = 0
            WHERE users.id = user_id;
    ELSE
        UPDATE users
            SET users.average_score = total_weighted_score / total_weight
            WHERE users.id = user_id;
    END IF;
END $$
DELIMITER ;
