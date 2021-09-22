# OpenVINO benchmark

This directory contains a Makefile and a template manifest for the most recent version of OpenVINO
toolkit (as of this writing, version 2021.4). We use the `Benchmark C++ Tool` (benchmark_app) from
the OpenVINO distribution as a concrete application running under Gramine-SGX to estimate deep
learning inference performance. We test only the CPU backend (i.e., no GPU or FPGA).

## Software requirements

- OpenVINO: Please download latest OpenVINO toolkit (as of this writing, version 2021.4) for Linux
  from https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/download.html.
  For OpenVINO installation step-by-step instructions please refer to this
[link](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html).
- Python (version 3.6 or higher)
- Python virtual environment: `sudo apt-get install python3-venv`
- CMake (version 3.10 or higher)

## Supported models for Gramine-SGX

The following models have been tested with Gramine-SGX:

- bert-large-uncased-whole-word-masking-squad-0001 (FP16/FP32)
- bert-large-uncased-whole-word-masking-squad-int8-0001 (INT8)
- brain-tumor-segmentation-0001 (FP16/FP32)
- brain-tumor-segmentation-0002 (FP16/FP32)
- resnet-50-tf (FP16/FP32)
- ssd_mobilenet_v1_coco (FP16/FP32)

## Preparing the source

1. Set up OpenVINO environment variables by running:
    - root user: `source /opt/intel/openvino_2021/bin/setupvars.sh`
    - root user and set permanently: append `source /opt/intel/openvino_2021/bin/setupvars.sh` to
      `~/.bashrc`
    - regular user: `source /home/<USER>/intel/openvino_2021/bin/setupvars.sh`
2. Build: `make SGX=1`

## Running the benchmark in Gramine-SGX

The below commands are utilizing only socket 0.

### Throughput runs

Options `-nireq`, `-nstreams` and `-nthreads` should be set to the *number of logical cores on the
socket 0* for achieving maximum performance.

```bash
$ export THREADS_CNT=<number of logical cores on the socket 0>
$ KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 \
    gramine-sgx benchmark_app -i <image files> \
    -m model/<public | intel>/<model_dir>/<INT8 | FP16 | FP32>/<model_xml_file> \
    -d CPU -b 1 -t 20 \
    -nstreams THREADS_CNT -nthreads THREADS_CNT -nireq THREADS_CNT
```

For example, in a system with 36 physical cores per socket and 2 threads per core, please export
`THREADS_CNT` as below.
```bash
$ export THREADS_CNT=72
```

### Latency runs

```bash
$ KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 \
    gramine-sgx benchmark_app -i <image files> \
    -m model/<public | intel>/<model_dir>/<INT8 | FP16 | FP32>/<model_xml_file> \
    -d CPU -b 1 -t 20 -api sync
```

## Running the benchmark in non-SGX Gramine and natively

To run the benchmark in non-SGX Gramine, replace `gramine-sgx benchmark_app` with
`gramine-direct benchmark_app` in the above commands.

To run the benchmark natively (outside Gramine), replace `gramine-sgx benchmark_app` with
`./benchmark_app` in the above commands.

## Notes

- The models require ~3GB of disk space.
- After setting up OpenVINO environment variables if you want to re-build Gramine you need to unset
  `LD_LIBRARY_PATH`. Please make sure to set up OpenVINO environment variables after building
  Gramine again.
- Option `-i <image files>` is optional. The user may use this option to benchmark specific images
  rather than randomly generated ones.
- Please tune the batch size to get the best performance on your system.
- Models for bert-large can be found in `model/intel` directory; the rest of the models can be found
  in `model/public` directory.
- For bert-large and brain-tumor-segmentation models the enclave size must be set to 64/128 GB for
  throughput runs.
- In multi-socket systems for bert-large-uncased-whole-word-masking-squad-0001 and
  brain-tumor-segmentation-0001 FP32/FP16 models, add more NUMA nodes using `numactl --membind` if
  memory allocation fails (for throughput runs).

## Performance considerations

### CPU frequency scaling

Linux systems have CPU frequency scaling governor that helps the system to scale the CPU frequency
to achieve best performance or to save power based on the requirement. To achieve the best
performance, please set the CPU frequency scaling governor to `performance` mode.

```bash
for ((i=0; i<$(nproc); i++)); do
    echo 'performance' > /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor;
done
```

### Manifest options for performance

- Preheat manifest option pre-faults the enclave memory and moves the performance penalty to
  Gramine-SGX startup (before the workload starts executing). To use the preheat option, make sure
  that `sgx.preheat_enclave = true` is added to the manifest template.
- Skipping invalid user pointer checks when the application does not invoke system calls with
  invalid pointers (typical case) can help improve performance. To use this option, make sure that
  `libos.check_invalid_pointers = false` is added to the manifest template.

### Memory allocator libraries

TCMalloc and mimalloc are memory allocator libraries from Google and Microsoft that can help improve
performance significantly based on the workloads. Only one of these allocators can be used at the
same time.

#### TCMalloc

(Please update the binary location and name if different from default.)

- Install tcmalloc: `sudo apt-get install google-perftools`
- Modify the manifest template file:
    - Add `loader.env.LD_PRELOAD = "/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"`
    - Append below entries to `sgx.trusted_files`:
        - `"file:/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"`
        - `"file:/usr/lib/x86_64-linux-gnu/libunwind.so.8"`
- Save the manifest template and rebuild this example.

#### mimalloc

(Please update the binary location and name if different from default.)

- Install mimalloc using the steps from https://github.com/microsoft/mimalloc
- Modify the manifest template file:
    - Add the `/usr/local` FS mount point:
        - `fs.mount.usr_local.type = "chroot"`
        - `fs.mount.usr_local.path = "/usr/local"`
        - `fs.mount.usr_local.uri = "file:/usr/local"`
    - Add `loader.env.LD_PRELOAD = "/usr/local/lib/mimalloc-1.7/libmimalloc.so.1.7"`
    - Append below entry to `sgx.trusted_files`:
        - `"file:/usr/local/lib/mimalloc-1.7/libmimalloc.so.1.7"`
- Save the manifest template and rebuild this example.
