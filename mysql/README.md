# MySQL example
This example is tested with MySQL version 8.0.29.

This directory contains an example for running Mysql server in Gramine, including
the Makefile and a template for generating the manifest.

# Pre-requisites

- `sudo apt-get install mysql-server` to install MySQL server.
- Comment out the log line `log_error = /var/log/mysql/error.log` in the config file 
 `/etc/mysql/mysql.conf.d/mysqld.cnf` to see the log on console.
- `systemctl stop mysql.service` to stop the default MySQL service .We will manually
 run MySQL process.
- `sudo mkdir /var/run/mysqld && sudo chown -R <current_user>:<current_user> /var/run/mysqld` 
to allow MySQL server to create socket file `mysqld.sock`.
- `sudo chown -R <current_user>:<current_user> /var/lib/mysql-files` to allow MySQL server for 
internal usage.
- `sudo chown -R <current_user>:<current_user> /var/lib/mysql-keyring` to allow MySQL server for 
internal usage.
- `mysqld --initialize-insecure --datadir=mysql-data/` to initialize data directory.

# Build

Run `make` to build the non-SGX version and `make SGX=1` to build the SGX
version.

# Run

Execute any one of the following commands to run the workload:

- Natively: `mysqld --datadir /tmp/mysql`.
- Gramine w/o SGX: `gramine-direct mysqld -u root --datadir /tmp/mysql`.
- Gramine with SGX: `gramine-sgx mysqld -u root --datadir /tmp/mysql`.

# Testing client connection and running sysbench benchmarking

Run below command from new terminal:

- `mysql -P 3306 --protocol=tcp -uroot` to connect a client to MySQL server.
- `mysql> exit` to disconnect the client.

Run Sysbench benchmarking:

- `sudo apt install -y sysbench` to install sysbench.
- `sudo mysqladmin -h 127.0.0.1 -P 3306 create sbtest` to create test database.

- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 prepare` to
 create records in test database.
- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 run` to
 run the sysbench benchmarks.
- `sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 cleanup` to
delete the records from test database.
