# Gunicorn example

This directory contains an example for running Gunicorn in Gramine, including the
Makefile and a template for generating the manifest.

# Generating the manifest

## Installing prerequisites

Please run the following command to install Gunicorn and its dependencies on Ubuntu 22.04:
```
sudo apt-get install python3 python3-flask gunicorn
```

## Building for Linux

Run `make` (non-debug) or `make DEBUG=1` (debug) in the directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the directory.

# Running Gunicorn with Gramine

Here's an example of running Gunicorn under Gramine:

Without SGX:
```
gramine-direct gunicorn --workers 1 --timeout 600 main:app
```

With SGX:
```
gramine-sgx gunicorn --workers 1 --timeout 600 main:app
```
