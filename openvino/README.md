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

The following models have been enabled and tested with Gramine-SGX:

- resnet-50-tf (FP16/FP32)
- ssd_mobilenet_v1_coco (FP16/FP32)
- bert-large-uncased-whole-word-masking-squad-0001 (FP16/FP32)
- bert-large-uncased-whole-word-masking-squad-int8-0001 (INT8)
- brain-tumor-segmentation-0001 (FP16/FP32)
- brain-tumor-segmentation-0002 (FP16/FP32)

## Preparing the source

1. Set up OpenVINO environment variables by running:
    - root user: `source /opt/intel/openvino_2021/bin/setupvars.sh`
    - root user and set permanently: Append `source /opt/intel/openvino_2021/bin/setupvars.sh` to `~/.bashrc`
    - regular user: `source /home/<USER>/intel/openvino_2021/bin/setupvars.sh`
2. Build: `make SGX=1`

## Running the benchmark

Options `-nireq`, `-nstreams` and `-nthreads` should be set to the
`number of physical cores * 2` (take into account hyperthreading) for achieving maximum
performance.

### Throughput runs

#### Gramine-SGX

```bash
$ export OPTIMAL_VALUE=<number of physical cores * 2>
$ KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 \
    gramine-sgx benchmark_app -i <image files> \
    -m model/<public | intel>/<model_dir>/<INT8 | FP16 | FP32>/<model_xml_file> \
    -d CPU -b 1 -t 20 \
    -nstreams OPTIMAL_VALUE -nthreads OPTIMAL_VALUE -nireq OPTIMAL_VALUE
```
For example, in a system with 36 physical cores, please export `OPTIMAL_VALUE` as below.
```bash
$ export OPTIMAL_VALUE=72
```

#### Native

To run the benchmark in a native baremetal (outside Gramine), replace `gramine-sgx benchmark_app`
with `./benchmark_app` in the above command.

### Latency runs

#### Gramine-SGX

```bash
$ KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 \
    gramine-sgx benchmark_app -i <image files> \
    -m model/<public | intel>/<model_dir>/<INT8 | FP16 | FP32>/<model_xml_file> \
    -d CPU -b 1 -t 20 -api sync
```

#### Native

To run the benchmark in a native baremetal (outside Gramine), replace `gramine-sgx benchmark_app`
with `./benchmark_app` in the above command.

## Notes

- The models require ~3GB of disk space.
- After setting up OpenVINO environment variables if you want to build Gramine after
cleaning you need to unset `LD_LIBRARY_PATH`. Please make sure to set up OpenVINO environment
variables after building Gramine again.
- To get `number of physical cores`, do `lscpu | grep 'Core(s) per socket'`.
- Option `i <image files>` is optional. A user may use this option as required.
- Please tune batch size to get best performance in your system.
- Model files for bert-large can be found in `model/intel` directory and for rest of
the models these are stored in `model/public` directory.
- Based on the precision for bert-large and brain-tumor-segmentation models the enclave
size must be set to 64/128 GB for capturing throughput.
- In multi-socket systems for bert-large-uncased-whole-word-masking-squad-0001 and
brain-tumor-segmentation-0001 FP32/FP16 models please expand memory nodes usage with
`numactl --membind` if memory allocation fails for capturing throughput.

## Performance considerations

### Scale the CPU frequency

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
gramine-sgx startup (before the workload starts executing). To use preheat option, add
`sgx.preheat_enclave = true` to the manifest template.
- Skipping invalid user pointer checks when the application does not invoke system calls with
invalid pointers (typical case) can help improve performance. To use this option, add
`libos.check_invalid_pointers = false` to the
manifest template.

### Memory allocator libraries

TCMalloc and mimalloc are memory allocator libraries from Google and Microsoft that can help
improve performance significantly based on the workloads. At any point, only one of these
allocators can be used.

#### TCMalloc

Please update the binary location and name if different from default.
- Install tcmalloc : `sudo apt-get install google-perftools`
- Add these in the manifest template:
    - `loader.env.LD_PRELOAD = "/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"`
    - Append below entries to `sgx.trusted_files`:
        - `"file:/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"`
        - `"file:/usr/lib/x86_64-linux-gnu/libunwind.so.8"`
- Save the manifest template and rebuild this example.

#### mimalloc

Please update the binary location and name if different from default.
- Install mimalloc using the steps from https://github.com/microsoft/mimalloc
- Add these in the manifest template:
    - `fs.mount.usr_local.type = "chroot"`
    - `fs.mount.usr_local.path = "/usr/local"`
    - `fs.mount.usr_local.uri = "file:/usr/local"`
    - `loader.env.LD_PRELOAD = "/usr/local/lib/mimalloc-1.7/libmimalloc.so.1.7"`
    - Append below entry to `sgx.trusted_files`:
        - `"file:/usr/local/lib/mimalloc-1.7/libmimalloc.so.1.7"`
- Save the manifest template and rebuild this example.
