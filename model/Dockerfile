FROM tp33/django

RUN pip install "djangorestframework==3.5.3" \
	&& pip install "requests==2.13.0"

# Switching from mysql-connector to mysqlclient requires that
# the database engine be changed from 'ENGINE': 'mysql.connector.django' to
# 'ENGINE': 'django.db.backends.mysql'
