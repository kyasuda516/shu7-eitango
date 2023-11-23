DELETE FROM `%tableName%`;
LOAD DATA INFILE '/var/lib/mysql-files/csv/%tableName%.csv'
  INTO TABLE `%tableName%` 
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
  LINES TERMINATED BY '\r\n' 
  IGNORE 1 LINES;