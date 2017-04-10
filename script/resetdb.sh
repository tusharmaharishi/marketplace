#!/bin/bash
set -e

echo "Removing container(s)..."

cmd="$(docker ps -a -q)"

if [[ ${#cmd} -gt 25 ]]; then
    docker rm -f exp model es kafka batch web &> /dev/null || {
        echo "Failed to remove other container(s)"
        echo "Try docker ps -a"
        exit 1
    }
fi

echo "Restarting mysql container(s)..."

docker stop mysql mysql-cmdline &> /dev/null || {
    echo "Failed to stop mysql container(s)"
    echo "Try docker ps -a"
    exit 1
}

yes | find . -path "../*/migrations/*.py" -not -name "__init__.py" -delete
yes | find . -path "../*/migrations/*.pyc"  -delete

echo "Successfully deleted old migrations"

docker start mysql mysql-cmdline &> /dev/null || {
    echo "Failed to start mysql container(s)."
    exit 1
}

sleep 2

echo "Dropping old database..."

docker exec -it mysql-cmdline bash -c \
"mysql -uroot -p'\$3cureUS' -h db -Bse \"
drop user if exists 'www'@'%';
flush privileges;
drop database if exists cs4501;
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%'; \"; " &> /dev/null || {
    echo "Failed to clear mysql database"
    exit 2
}

echo "Successfully cleared mysql database"