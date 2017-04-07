#!/bin/bash
set -e

docker rm -f exp model es kafka batch web &> /dev/null || {
    echo "Some container(s) cannot be removed."
    echo "Try docker ps -a"
}

docker rm -f mysql mysql-cmdline &> /dev/null {
    echo "There was an error removing mysql container(s)."
    echo "Try docker ps -a"
}

docker start mysql mysql-cmdline &> /dev/null || {
    echo "There was an error starting docker container(s)."
    exit 1
}

sleep 2

docker exec -it mysql-cmdline bash -c \
"mysql -uroot -p'\$3cureUS' -h db -Bse \"drop database cs4501;
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%'; \"; " &> /dev/null || {
    echo "There was an error clearing mysql database."
    exit 2
}

docker stop mysql-cmdline &> /dev/null || {
    echo "There was an error stopping mysql-cmdline container."
    exit 3
}
echo "Database was reset successfully."

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "Migrations were deleted successfully."