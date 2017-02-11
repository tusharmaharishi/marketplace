#!/bin/bash

mysql -uroot -p'$3cureUS' -h db
drop database cs4501;
create database cs4501 character set utf8;
grant all on cs4501.* to 'www'@'%';
exit;
exit;
