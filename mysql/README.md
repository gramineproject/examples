# Mysql example
# This example is tested with mysql Ver 8.0.29

This directory contains an example for running Mysql-Server in Gramine, including
the Makefile and a template for generating the manifest.

# Prerequisites Steps

## Install mysql-server on baremetal:
    sudo apt-get install mysql-server

## Comment log in /etc/mysql/mysql.conf.d/mysqld.cnf to see the logs on console:
    #log_error = /var/log/mysql/error.log

## Stop mysql service, we need to manually run mysql with mysqld:
    systemctl stop mysql.service
    sudo mkdir /var/run/mysqld && sudo chown -R <current_user>:<current_user> /var/run/mysqld
    sudo chown -R <current_user>:<current_user> /var/lib/mysql-files
    sudo chown -R <current_user>:<current_user> /var/lib/mysql-keyring

## Prepare new data directory:
    sudo mkdir /tmp/mysql && sudo chown -R <current_user>:<current_user> /tmp/mysql

## Add the following 2 lines to /etc/apparmor.d/usr.sbin.mysqld:
    /tmp/mysql r,
    /tmp/mysql/** rwk,

## Restart apparmor:
    sudo service apparmor restart

## Initialize mysql:
    mysqld --initialize-insecure --datadir=/tmp/mysql
    sudo rm /tmp/mysql/undo*

# Generating the manifest

## Installing prerequisites

## Building for Linux

Run `make` (non-debug) or `make DEBUG=1` (debug) in the directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the directory.

# Run Mysql with Gramine

Here's an example of running Mysql under Gramine:

Without SGX:
```
gramine-direct mysqld -u root --datadir /tmp/mysql
```

With SGX:
```
gramine-sgx mysqld -u root --datadir /tmp/mysql
```
