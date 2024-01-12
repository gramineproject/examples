# iperf

This directory contains the Makefile and the template manifest for the most
recent version of `iperf` as of this writing (3.16).

# Prerequisites

`iperf` has no prerequisites.

# Execution instructions

```sh
# build iperf and the final manifest
make SGX=1

# To run the original iperf server, use:
LD_LIBRARY_PATH=./install ./install/iperf3 -s

# To run the iperf server in non-SGX Gramine, use:
gramine-direct iperf3

# To run the iperf server in Gramine-SGX, use:
gramine-sgx iperf3

# To get measurements with the iperf client, run in another terminal:
LD_LIBRARY_PATH=./install ./install/iperf3 -c localhost -p 5201
```

# Notes
Tested in `Ubuntu 22.04.3 LTS`.