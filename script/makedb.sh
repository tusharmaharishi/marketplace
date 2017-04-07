#!/bin/bash

sleep 20

if [[ -e /app/db/cs4501 ]] ; then
    mysql -uroot -p'$3cureUS' -h db -Bse \
    "drop database if exists cs4501;
    create database cs4501 character set utf8;
    grant all on *.* to 'www'@'%'; \
    ";
else
    mysql -uroot -p'$3cureUS' -h db -Bse \
    "drop user if exists 'www'@'%';
    flush privileges;
    drop database if exists cs4501;
    create user 'www'@'%' identified by '\$3cureUS';
    create database cs4501 character set utf8;
    grant all on *.* to 'www'@'%'; \
    ";
fi

echo "Successfully created 'cs4501' table with root user 'www'@'%'"