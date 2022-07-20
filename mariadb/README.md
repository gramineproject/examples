# MariaDB example

This example was tested with MariaDB version 10.7.3 and Ubuntu 20.04.

This directory contains an example for running MariaDB server in Gramine,
including the Makefile and a template for generating the manifest.

## Pre-requisites

- `curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash -s -- --mariadb-server-version="mariadb-10.7.3" --os-type=ubuntu --os-version=focal` to use
MariaDB package repository setup script.
- `sudo apt-get update` to update package cache.
- `sudo apt-get install mariadb-server` to install MariaDB server.
- `sudo mysql_secure_installation` to improve the security of your MariaDB installation. Fill
the details as below.
    - Enter current password for root (enter for none): --> enter
    - Switch to unix_socket authentication [Y/n] --> n
    - Change the root password? --> y
    - Remove anonymous users? [Y/n] --> y
    - Disallow root login remotely? --> y
    - Remove test database and access to it? --> y
    - Reload privilege tables now? --> y
- `systemctl stop mysqld` to stop the default MariaDB server. We will
  manually start MariaDB server.
- `sudo chown -R $USER:$USER /run/mysqld`
  to allow MariaDB server to create socket file `mysqld.sock`.
- `sudo chown -R $USER:$USER /var/lib/mysql` to allow
  running MariaDB server under the current non-root user.

## Build

Run `make` to build the non-SGX version and `make SGX=1` to build the SGX
version.

## Run

- Native: `mysqld`.
- Gramine without SGX: `gramine-direct mysqld`.
- Gramine with SGX: `gramine-sgx mysqld`.

## Test client connection

Run below commands from new terminal:

- `mysql -u root -p -h 127.0.0.1` to connect a client to MariaDB server.
- `mysql> exit` to disconnect the client.