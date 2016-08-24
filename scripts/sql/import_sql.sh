#!/bin/bash

if [[ $# -ne 4 ]]; then
	echo "Usage: $0 <username> <password> <database> </path/to/sql_file.sql.gz>"
	exit 1
fi

echo "=> Starting MySQL Server"
/usr/bin/mysqld_safe > /dev/null 2>&1 &
PID=$!

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -u"$1" -p"$2" -e "status" > /dev/null 2>&1
RET=$?
done

echo "   Started with PID ${PID}"

echo "=> Importing SQL file"
gunzip -c "$4" | mysql -u"$1" -p"$2" "$3"

echo "=> Stopping MySQL Server"
mysqladmin -u"$1" -p"$2" shutdown

echo "=> Done!"
