# Intel(R) Extension for Scikit-learn example

This directory contains an example for running Intel(R) Extension for
Scikit-learn with Gramine, including the Makefile and a template for generating
the manifest.

**NOTE**: This example works only on post-v1.3.1 Gramine, due to the manifest
file requiring special Python-templates handling. This example will work
correctly on Gramine v1.4 once the latter is released.

This example was tested with the following configuration:
- scikit-learn-intelex v2023.0.1
- scikit-learn v1.2.0
- pandas v1.5.2
- daal4py v2023.0.1
- daal v2023.0.1
- scipy v1.10.0
- numpy v1.24.1

# Generating the manifest

## Installing prerequisites

For generating the manifest and running the test scripts, please run the
following command to install the required packages (Ubuntu-specific):

```sh
# required for Ubuntu 18.04 as its default pip doesn't have scikit-learn package
python3 -m pip install --upgrade pip

python3 -m pip install scikit-learn-intelex==2023.0.1 pandas
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

**NOTE**: `kmeans_perf_eval.py` can exceed the process's maximum number of
mappings in Linux. You may need to increase the value in
`/proc/sys/vm/max_map_count`:

```
# the value is just an example
sudo sysctl vm.max_map_count=1310720
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
