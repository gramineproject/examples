# MySQL example

This example was tested with MySQL version 8.0.35 and Ubuntu 20.04.

This directory contains an example for running MySQL server in Gramine,
including the Makefile and a template for generating the manifest.

## Pre-requisites

- `sudo apt-get install mysql-server` to install MySQL server.
- `sudo sed -i "s|^\(log_error.*\)|#\1|g" /etc/mysql/mysql.conf.d/mysqld.cnf`
  to see the MySQL logs on console instead of log file.
- `sudo systemctl stop mysql.service` to stop the default MySQL service. We
  will manually run MySQL process.
- `sudo mkdir /var/run/mysqld && sudo chown -R $USER:$USER /var/run/mysqld`
  to allow MySQL server to create socket file `mysqld.sock`.
- `sudo chown -R $USER:$USER /var/lib/mysql-files` to allow running MySQL
  server under the current non-root user.
- `mysqld --initialize-insecure --datadir=/tmp/mysql-data` to initialize data
  directory. For details on '--initialize-insecure', please see the
  https://dev.mysql.com/doc/mysql-linuxunix-excerpt/5.7/en/data-directory-initialization.html
  page.

## Build

Run `make` to build the non-SGX version and `make SGX=1` to build the SGX
version.

## Run

Execute any one of the following commands to run the workload:

- Natively: `mysqld --datadir /tmp/mysql-data`.
- Gramine w/o SGX: `gramine-direct mysqld --datadir /tmp/mysql-data`.
- Gramine with SGX: `gramine-sgx mysqld --datadir /tmp/mysql-data`.

## Testing client connection and running Sysbench

Run below commands from new terminal:

- `mysql -P 3306 --protocol=tcp -u root` to connect a client to MySQL server.
- `mysql> exit` to disconnect the client.

Run Sysbench:

- `sudo apt install -y sysbench` to install Sysbench.
- `sudo mysqladmin -h 127.0.0.1 -P 3306 create sbtest` to create test database.

- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 prepare`
  to create records in test database.
- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 run`
  to run the Sysbench benchmarks.
- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 cleanup`
  to delete the records from test database.
