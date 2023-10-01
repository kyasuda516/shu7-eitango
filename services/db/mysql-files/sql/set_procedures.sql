-- ステートメント区切りを//に変更
DELIMITER //

-- update_bunchプロシージャを定義
DROP PROCEDURE IF EXISTS `update_bunch`//
CREATE PROCEDURE `update_bunch`(IN dayId TINYINT(3))
root: BEGIN
  DECLARE tableName VARCHAR(7);

  -- トランザクション前の準備（トラの途中で終了した場合にエラー内容が出力されるように）
  -- 参考元：https://qiita.com/itmammoth/items/54309d4cb4150f45f1d6
  DECLARE EXIT HANDLER FOR SQLEXCEPTION     -- , SQLWARNING    -- これを入れていると警告のときでさえ止まる
  BEGIN
    GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
    SELECT @sqlstate, @errno, @text;
    ROLLBACK;
  END;

  START TRANSACTION;

  -- bunchテーブルの名前を設定
  IF dayId NOT BETWEEN 0 AND 6 THEN
    SIGNAL SQLSTATE '45000' 
      SET MESSAGE_TEXT = "Specify a number from 0 to 6 for 'dayId'.", MYSQL_ERRNO = 999;
    LEAVE root;
  END IF;
  SET tableName = CONCAT('bunch', dayId);  -- Note: 数値は文字列に暗黙的に変換される
  
  -- tmpテーブルを用意
  DROP TABLE IF EXISTS `tmp`;
  CREATE TABLE 
    `tmp`
  -- 作成するテーブルは次の出力内容にもとづく。
  AS (
    -- ここで定義するtはほぼbunchだが、カードやジャンルがidで表された、いわば骨状態。
    WITH `t` AS (
      SELECT 
        `id`,
        `genre_id`
      FROM
        -- ここで定義するshuffled_poolは、ジャンルごとにシャッフルされているpoolで、
        -- そしてシャッフルされたあとジャンルごとに連番（1始まり）がつけられている。
        (
          SELECT 
            `id`,
            `genre_id`,
            ROW_NUMBER() OVER (PARTITION BY `genre_id` ORDER BY RAND()) AS `num_in_genre`
          FROM
            `pool`
        ) AS `shuffled_pool`
      WHERE
        `num_in_genre` <= (SELECT `limit` FROM `genres` WHERE `genres`.`id`=`shuffled_pool`.`genre_id` LIMIT 1)
      ORDER BY
        `genre_id`
    )
    -- 骨状態のbunchに中身をつけて出力する。
    SELECT 
      `t`.`id`,
      `genres`.`name` AS `genre`,
      `pool`.`word`,
      `pool`.`ja`
    FROM
      `t` JOIN `pool` ON `t`.`id` = `pool`.`id`
          JOIN `genres` ON `t`.`genre_id` = `genres`.`id` 
  );

  -- tmpテーブルのidを連番に振り直す(0始まり)
  SET @n:=-1;
  UPDATE `tmp` SET id=@n:=@n+1;
  
  -- bunchテーブルを削除
  SET @temp_query = CONCAT('DROP TABLE IF EXISTS `', tableName, '`');
  PREPARE stmt FROM @temp_query;     -- Note: プロシージャ内のローカル変数ではなく、ユーザー定義変数を使わないと無理だった。
  EXECUTE stmt;
  
  -- tmpテーブルをbunchに名称変更
  SET @temp_query = CONCAT('RENAME TABLE `tmp` TO `', tableName, '`');
  PREPARE stmt FROM @temp_query;
  EXECUTE stmt;

  -- 変数の解放
  SET @temp_query = NULL;
  DEALLOCATE PREPARE stmt;

  COMMIT;
  -- SELECT 'Success!' AS result FROM DUAL;   -- ログ削減のためにカット
END//

-- ステートメント区切りを;に戻す
DELIMITER ;