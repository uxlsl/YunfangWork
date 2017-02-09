#！/bin/bash

yum install -y  gcc gcc-c++ autoconf  libxml*  httpd-manual  mysql-connector-odbc mysql-devel curl curl-devel openssl perl-DBI httpd mysql mysql-server php php-mysql postgresql postgresql-server php-postgresql php-pgsql php-devel
rpm -ivh 'http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm'
yum install -y zabbix-server-mysql zabbix-web-mysql zabbix-agent
