DELIMITER //

DROP EVENT IF EXISTS `update_bunch_daily`//
CREATE EVENT `update_bunch_daily`
ON SCHEDULE EVERY 1 DAY
STARTS '2023-04-01 6:00:00'
DO
BEGIN
  DECLARE dayId TINYINT(3);
  SET dayId = DAYOFWEEK(NOW()) - 1;
  CALL update_bunch(dayId);
END//

DELIMITER ;