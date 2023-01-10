# Intel(R) Extension for Scikit-learn example

This directory contains an example for running Intel(R) Extension for
Scikit-learn with Gramine, including the Makefile and a template for generating
the manifest.

# Generating the manifest

## Installing prerequisites

For generating the manifest and running the test scripts, please run the
following command to install the required packages (Ubuntu-specific):

```sh
# required for Ubuntu 18.04 as its default pip doesn't have scikit-learn package
python3 -m pip install --upgrade pip

python3 -m pip install scikit-learn-intelex==2023.0.1 pandas numpy
```

## Download datasets

Before run, please download MNIST dataset by the following command:

```sh
python3 scripts/download_dataset.py
```

## Building for Linux

Run `make` (non-debug) or `make DEBUG=1` (debug) in the directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the directory.

# Run Intel(R) Extension for Scikit-learn with Gramine

Without SGX:

```sh
gramine-direct ./sklearnex scripts/kmeans_example.py
gramine-direct ./sklearnex scripts/kmeans_perf_eval.py
```

With SGX:

```sh
gramine-sgx ./sklearnex scripts/kmeans_example.py
gramine-sgx ./sklearnex scripts/kmeans_perf_eval.py
```

You can also manually run included tests:

```sh
SGX=1 ./run_tests.sh
```
