# iperf3

This directory contains the Makefile and the template manifest for the most
recent version of iperf as of this writing (3.16).

# Prerequisites

`iperf` has no prerequisites.

# Quick Start

```sh
# build iperf and the final manifest
make SGX=1

# To run the original iperf server, use:
make start-native-server 

# To run the iperf server in non-SGX Gramine, use:
make start-gramine-server

# To run the iperf server in Gramine-SGX, use:
make SGX=1 start-gramine-server 

# To get measurements with the iperf client, run in another terminal:
LD_LIBRARY_PATH=./iperf/src/.libs ./iperf/src/.libs/iperf3 -c localhost -p 5201
```