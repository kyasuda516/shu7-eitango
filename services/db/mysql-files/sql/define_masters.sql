DROP TABLE IF EXISTS `pool`;
DROP TABLE IF EXISTS `pos_config`;

-- pos_configテーブルを用意
CREATE TABLE `pos_config` (
  `id` INT(11) NOT NULL,
  `pos` VARCHAR(128) NOT NULL,
  `limit` INT(11) NOT NULL,
  PRIMARY KEY (id)
  );

-- poolテーブルを用意
CREATE TABLE `pool` (
  `id` INT(11) NOT NULL,
  `pos_id` INT(11) NOT NULL,
  `word` TEXT NOT NULL,
  `ja` TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (pos_id) REFERENCES pos_config(id)
		ON DELETE CASCADE
    ON UPDATE CASCADE
  );