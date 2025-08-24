# Gunicorn example

This directory contains an example for running Gunicorn in Gramine, including the Makefile and a
template for generating the manifest. Gunicorn is a webserver to deploy Flask applications in
Python. Although Flask comes with an internal webserver, this is widely considered to be not
viable for production. Common practice in production is to put Flask behind a real webserver that
communicates via the WSGI protocol. A common choice for that webserver is Gunicorn. For more
documentation, refer to https://docs.gunicorn.org/en/stable/.

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
gramine-direct gunicorn
```

With SGX:
```
gramine-sgx gunicorn
```

Because these commands will start the Gunicorn server in the foreground, you will need to open
another console to run the client.

Once the server has started, you can test it with `curl`.

```
curl http://127.0.0.1:8000/hello
```
