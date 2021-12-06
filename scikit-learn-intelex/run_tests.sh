#!/usr/bin/env bash

set -e

if test -n "$SGX"
then
    GRAMINE=gramine-sgx
else
    GRAMINE=gramine-direct
fi

# === Kmeans example ===
echo -e "\n\nRunning kmeans_example.py:"
$GRAMINE ./sklearnex scripts/kmeans_example.py > OUTPUT
grep -q "Kmeans example finished" OUTPUT && echo "[ Success 1/2 ]"
rm OUTPUT

# === Kmeans perf eval ===
echo -e "\n\nRunning kmeans_perf_eval.py:"
$GRAMINE ./sklearnex scripts/kmeans_perf_eval.py > OUTPUT
grep -q "Kmeans perf evaluation finished" OUTPUT && echo "[ Success 2/2 ]"
rm OUTPUT
