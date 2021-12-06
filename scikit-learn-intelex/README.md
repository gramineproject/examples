# Python example

This directory contains an example for running Intel(R) Extension for Scikit-learn* with Gramine, including
the Makefile and a template for generating the manifest.

# Generating the manifest

## Installing prerequisites

For generating the manifest and running the test scripts, please run the following
command to install the required packages (Ubuntu-specific):

```
sudo apt-get install scikit-learn-intelex pandas numpy
```

## Download datasets

Before run, please download MNIST dataset by the following command:

```    
python scripts/download_dataset.py
```

## Building for Linux

Run `make` (non-debug) or `make DEBUG=1` (debug) in the directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the directory.

## Building with a local Python/oneDAL installation

By default, the `make` command creates the manifest for the Python3.9 and oneDAL binaries from
the system installation. If you have a local installation, you may create the
manifest with the `ONEDAL_LIBS` variable. For example (default paths are below):

```
make PYTHON_VERSION=python3.9 ONEDAL_LIBS=/usr/local/lib SGX=1
```

# Run Python with Gramine

Here's an example of running Python scripts under Gramine:

Without SGX:
```
gramine-direct ./python scripts/kmeans_example.py
gramine-direct ./python scripts/kmeans_perf_eval.py
```

With SGX:
```
gramine-sgx ./python scripts/kmeans_example.py
gramine-sgx ./python scripts/kmeans_perf_eval.py
```

You can also manually run included tests:
```
SGX=1 ./run-tests.sh
```
