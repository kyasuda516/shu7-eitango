DROP TABLE IF EXISTS `pool`;
DROP TABLE IF EXISTS `genres`;

-- genresテーブルを用意
CREATE TABLE `genres` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `limit` INT(11) NOT NULL,
  PRIMARY KEY (id)
  );

-- poolテーブルを用意
CREATE TABLE `pool` (
  `id` INT(11) NOT NULL,
  `genre_id` INT(11) NOT NULL,
  `word` TEXT NOT NULL,
  `ja` TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (genre_id) REFERENCES genres(id)
		ON DELETE CASCADE
    ON UPDATE CASCADE
  );