# iperf

This directory contains the Makefile and the template manifest for the most
recent version of `iperf` as of this writing (3.16).

# Prerequisites

`iperf` has no prerequisites
([source](https://github.com/esnet/iperf/tree/3.16?tab=readme-ov-file#prerequisites)).

# Building instructions

We build `iperf` from source because Ubuntu 22.04 has `iperf3` v3.9 in its
package repositories which is built with `TCP_CONGESTION` requirement (i.e.,
with `iperf3_cv_header_tcp_congestion="yes"` config option). Using the Ubuntu
package would fail with the following error:
```
iperf3: error - unable to set TCP_CONGESTION: ...
```

Thus we build `iperf` manually. In this case, it is built without
`TCP_CONGESTION`, and can successfully execute under Gramine[^1].

[^1]: Starting from version 3.10, `iperf` supports environments that do not
implement congestion control algorithm. Thus, iperf 3.10+ prebuilt packages
should work under Gramine without problems. See [release
notes](https://github.com/esnet/iperf/blob/3.16/RELNOTES.md#iperf-310-2021-05-26)
for details.


## Building for Linux

Run `make` in the current directory.

## Building for SGX

Run `make SGX=1` (non-debug) or `make SGX=1 DEBUG=1` (debug) in the current
directory.

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

(The options may be version-dependent. Below are the options for v3.16.)

## Generic options (both for server and client):
- `-p, --port`: server port to listen on/connect to
- `--forceflush`: force flushing output at every interval
- `-d, --debug[=#]`: emit debugging output (optional "=" and debug level: 1-4)

## Server-specific options:
- `-s, --server`: run in server mode
- `-1, --one-off`: handle one client connection then exit
- `--idle-timeout #`: restart idle server after # seconds in case it got stuck

## Client-specific options:
- `-c, --client <host>`: run in client mode, connecting to `<host>`
- `-t, --time #`: time in seconds to transmit for (default 10 secs)
- `-n, --bytes #[KMG]`: number of bytes to transmit (instead of -t)
- `-P, --parallel #`: number of parallel client streams to run
- `-N, --no-delay`: set TCP/SCTP no delay, disabling Nagle's Algorithm

# Notes
- Tested on Ubuntu 22.04.
- In the execution instructions, we use port `5201` for the client.
  This is the default port used by `iperf`.
