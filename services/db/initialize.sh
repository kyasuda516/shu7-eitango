#!/bin/bash
set -eu

sql_files=/var/lib/mysql-files/sql
stmt=""
stmt="${stmt}  source ${sql_files}/set_procedures.sql;"
stmt="${stmt}  source ${sql_files}/define_masters.sql;"
stmt="${stmt}  $(sed s/%tableName%/pos_config/g ${sql_files}/_update_master.sql)"
stmt="${stmt}  $(sed s/%tableName%/pool/g ${sql_files}/_update_master.sql)"
stmt="${stmt}  source ${sql_files}/set_bunches.sql;"
stmt="${stmt}  source ${sql_files}/set_events.sql;"

stmt="${stmt}  REVOKE ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* FROM \`${MYSQL_USER}\`@\`%\`;"
stmt="${stmt}  GRANT SELECT ON \`${MYSQL_DATABASE}\`.* TO \`${MYSQL_USER}\`@\`%\`;"

mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE -e "${stmt}"