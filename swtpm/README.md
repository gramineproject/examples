# swtpm

This directory contains a Makefile and a manifest template for running swtpm.
See https://github.com/stefanberger/swtpm/.

**NOTE**: Currently works only with PR https://github.com/gramineproject/gramine/pull/1210.
See also https://github.com/stefanberger/swtpm/issues/792.

## Installing

1. Install `libtpms` like this:
   https://github.com/stefanberger/libtpms/wiki#build-a-package-on-ubuntu
   - Version used: `git checkout v0.9.6`

2. Install `swtpm` like this: https://github.com/stefanberger/swtpm/wiki#compile-on-ubuntu-2104
   - Don't install `libtpms-dev` since we've done it already in step 1
   - Version used: `git checkout v0.8.0`

Now swtpm tools are installed. We run only `swtpm` executable with Gramine.

## Configuration of `swtpm`

`swtpm` executable can be run in several modes. We hard-code the following configuration
(command-line options) to run with Gramine:
```sh
$ swtpm socket --tpm2 --tpmstate dir=/myvtpm2 --seccomp action=none \
    --server type=tcp,port=2321,disconnect --ctrl type=tcp,port=2320 \
    --flags not-need-init,startup-clear
```

This configuration means:
- run `swtpm` in TPM2 mode,
- save all TPM state under `/myvtpm2/` dir (transparently encrypted by Gramine),
- don't use seccomp (Gramine doesn't support it, and it's not needed in Gramine env anyway),
- listen for client connections on TCP/IP port 2321 (in contrast to CUSE or chardev),
- create a control channel on TCP/IP port 2320,
- additional flags for the initial state of TPM.

For more information, see `man swtpm`.

## Building

- `make clean; make` for Gramine without SGX (`gramine-direct`).
- `make clean; make SGX=1` for Gramine with SGX (`gramine-sgx`).

You can add `DEBUG=1` for verbose Gramine logs.

Notice that `gramine-direct` uses a dummy encryption key for TPM files, hard-coded in the manifest.
Whereas `gramine-sgx` uses the MRENCLAVE-based sealing encryption key for TPM files (and is
therefore secure). To make sure the correct key is used, we require a `make clean` step. For details
on how the key is chosen, see Makefile and manifest template.

## Quick tests of swtpm with Gramine

### 1. Self-test

The test idea is taken from https://github.com/stefanberger/swtpm/wiki/Useful-scripts-for-TPM,
Section "Trigger a self-test on a TPM 2 listening on command port 2321 with the disconnect flag".

```sh
# swtpm server in one window
gramine-sgx swtpm

# client script in another window
bash -c "exec 100<>/dev/tcp/localhost/2321; \
    echo -en '\x80\x01\x00\x00\x00\x0b\x00\x00\x01\x43\x01' >&100; \
    od -tx1 <&100"

## output must be like this:
##   0000000 80 01 00 00 00 0a 00 00 00 00
```

### 2. Hashing in PCR 17

The test idea is taken from the unit test:
https://github.com/stefanberger/swtpm/blob/346b3d62/tests/_test_tpm2_hashing.

```sh
# swtpm server in one window
gramine-sgx swtpm

# client scripts in another window

## 1 step: init TPM to known state
swtpm_ioctl --tcp localhost:2320 -i

## 2 step: startup TPM2
bash -c "exec 100<>/dev/tcp/localhost/2321; \
    echo -en '\x80\x01\x00\x00\x00\x0c\x00\x00\x01\x44\x00\x00' >&100; \
    od -tx1 <&100"

## output must be like this:
##   0000000 80 01 00 00 00 0a 00 00 00 00

## 3 step: check TPM Established flag (must be 0)
swtpm_ioctl --tcp localhost:2320 -e

## 4 step: ask TPM to hash string "1234" in PCR 17
swtpm_ioctl --tcp localhost:2320 -h 1234

## 5 step: read PCR 17
bash -c "exec 100<>/dev/tcp/localhost/2321; \
    echo -en '\x80\x01\x00\x00\x00\x14\x00\x00\x01\x7e\x00\x00\x00\x01\x00\x0b\x03\x00\x00\x02' >&100; \
    od -tx1 <&100"

## output must be like this:
##   0000000 80 01 00 00 00 3e 00 00 00 00 00 00 00 2c 00 00
##   0000020 00 01 00 0b 03 00 00 02 00 00 00 01 00 20 fc a5
##   0000040 d6 49 bf b0 c9 22 fd 33 0f 79 b2 00 43 28 9d af
##   0000060 d6 0d 01 a4 c4 37 3c f2 8a db 56 c9 b4 54

## 6 step: check TPM Established flag (must be 1)
swtpm_ioctl --tcp localhost:2320 -e

## 7 step: shutdown TPM
swtpm_ioctl --tcp localhost:2320 -s
```
