# Intel(R) Extension for Scikit-learn* example

This directory contains an example for running Intel(R) Extension for Scikit-learn* with Gramine, including
the Makefile and a template for generating the manifest.

# Generating the manifest

## Installing prerequisites

First, please set environment variable that is corresponding to your Python's binaries.
That Python is going to be used for preparation and building:

```
export PYTHON_VERSION=python3
```

For generating the manifest and running the test scripts, please run the following
command to install the required packages (Ubuntu-specific):

```
${PYTHON_VERSION} -m pip install scikit-learn-intelex pandas numpy
```

## Download datasets

Before run, please download MNIST dataset by the following command:

```
${PYTHON_VERSION} scripts/download_dataset.py
```

## Building for Linux

Run `make` (non-debug) or `make DEBUG=1` (debug) in the directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the directory.

# Run Intel(R) Extension for Scikit-learn* with Gramine

Here's an example of running Python scripts under Gramine:

Without SGX:

```
gramine-direct ./sklearnex scripts/kmeans_example.py
gramine-direct ./sklearnex scripts/kmeans_perf_eval.py
```

With SGX:

```
gramine-sgx ./sklearnex scripts/kmeans_example.py
gramine-sgx ./sklearnex scripts/kmeans_perf_eval.py
```

You can also manually run included tests:

```
SGX=1 ./run-tests.sh
```
