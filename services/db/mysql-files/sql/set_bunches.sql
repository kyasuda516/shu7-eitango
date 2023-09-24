DELIMITER //
DROP PROCEDURE IF EXISTS `temp_procedure`//
CREATE PROCEDURE temp_procedure()
BEGIN
  DECLARE i TINYINT(3) DEFAULT 0;

  WHILE i <= 6 DO
    CALL update_bunch(i);
    SET i = i + 1;
  END WHILE;
END//
DELIMITER ;

CALL temp_procedure();

DROP PROCEDURE `temp_procedure`;