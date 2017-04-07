#!/bin/bash
set -e

docker rm -f exp model es kafka batch web &> /dev/null || {
    echo "Failed to remove some container(s)"
    echo "Try docker ps -a"
}

docker stop mysql mysql-cmdline &> /dev/null {
    echo "Failed to stop mysql container(s)"
    echo "Try docker ps -a"
}

docker start mysql mysql-cmdline &> /dev/null || {
    echo "Failed to start mysql container(s)."
    exit 1
}

sleep 2

docker exec -it mysql-cmdline bash -c \
"mysql -uroot -p'\$3cureUS' -h db -Bse \"drop database cs4501;
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%'; \"; " &> /dev/null || {
    echo "Failed to clear mysql database."
    exit 2
}

echo "Successfully reset mysql database"

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "Successfully deleted migrations"