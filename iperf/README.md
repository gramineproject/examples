# iperf

This directory contains the Makefile and the template manifest for the most
recent version of `iperf` as of this writing (3.16).

# Prerequisites

`iperf` has no prerequisites ([source](https://github.com/esnet/iperf?tab=readme-ov-file#prerequisites)).

# Building instructions

## Building for Linux

Run `make` in the root directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the root directory.

# Execution instructions

Run `iperf` server natively:
```
LD_LIBRARY_PATH=./install ./install/iperf3 -s
```

Run `iperf` server in Gramine without SGX:
```
gramine-direct iperf3
```

Run `iperf` server in Gramine with SGX:
```
gramine-sgx iperf3
```

To get measurements with the `iperf` client, run in another terminal:
```
LD_LIBRARY_PATH=./install ./install/iperf3 -c localhost -p 5201
```

# Useful iperf options
## Generic options (both for server and client):
- `-p, --port`: server port to listen on/connect to
- `--forceflush`: force flushing output at every interval
- `-d, --debug[=#]`: emit debugging output (optional "=" and debug level: 1-4. Default is 4 - all messages)

## Server-specific options:
- `-s, --server`: run in server mode
- `-1, --one-off`: handle one client connection then exit
- `--idle-timeout #`: restart idle server after # seconds in case it got stuck (default - no timeout)

## Client-specific options:
- `-c, --client <host>`: run in client mode, connecting to <host>
- `-t, --time #`: time in seconds to transmit for (default 10 secs)
- `-n, --bytes #[KMG]`: number of bytes to transmit (instead of -t)
- `-P, --parallel #`: number of parallel client streams to run
- `-N, --no-delay`: set TCP/SCTP no delay, disabling Nagle's Algorithm

# Notes
- Tested in `Ubuntu 22.04.3 LTS`.
- In the execution instructions, we use port `5201` for the client.
This is the default port used by `iperf`.