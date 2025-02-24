## Inference on TensorFlow BERT and ResNet50 models

This directory contains steps and artifacts to run inference with TensorFlow BERT and ResNet50
sample workloads on Gramine. Specifically, both these examples use pre-trained models to run
inference.

### Bidirectional Encoder Representations from Transformers (BERT)

BERT is a method of pre-training language representations and then using that trained model for
downstream NLP tasks like 'question answering'. BERT is an unsupervised, deeply bidirectional system
for pre-training NLP.
In this BERT sample, we use **BERT-Large, Uncased (Whole Word Masking)** model and perform int8
inference. More details about BERT can be found at https://github.com/google-research/bert.

### Residual Network (ResNet)

ResNet50 is a convolutional neural network that is 50 layers deep.
In this ResNet50 (v1.5) sample, we use a pre-trained model and perform int8 inference.
More details about ResNet50 can be found at https://github.com/IntelAI/models/tree/icx-launch-public/benchmarks/image_recognition/tensorflow/resnet50v1_5.

## Pre-requisites

- Install unzip.
- Upgrade pip/pip3.
- Install TensorFlow using `pip install intel-tensorflow-avx512==2.4.0`.

## Build BERT or ResNet50 sample

- To build the non-SGX version, do `make PYTHONDISTPATH=path_to_python_dist_packages/`.
- To build the SGX version, do `make PYTHONDISTPATH=path_to_python_dist_packages/ SGX=1`.
- Typically, `path_to_python_dist_packages` is `/usr/local/lib/python3.6/dist-packages`, but can
change based on python's installation directory.
- To clean the sample, do `make clean`.
- To clean and remove downloaded models and datasets, do `make distclean`.

**WARNING:** Building BERT sample downloads about 5GB of data.

## Run inference on BERT model

- To run int8 inference on `gramine-sgx` (SGX version):
```
OMP_NUM_THREADS=36 KMP_AFFINITY=granularity=fine,verbose,compact,1,0 taskset -c 0-35 gramine-sgx \
./python models/models/language_modeling/tensorflow/bert_large/inference/run_squad.py \
--init_checkpoint=data/bert_large_checkpoints/model.ckpt-3649 \
--vocab_file=data/wwm_uncased_L-24_H-1024_A-16/vocab.txt \
--bert_config_file=data/wwm_uncased_L-24_H-1024_A-16/bert_config.json \
--predict_file=data/wwm_uncased_L-24_H-1024_A-16/dev-v1.1.json \
--precision=int8 \
--output_dir=output/bert-squad-output \
--predict_batch_size=32 \
--experimental_gelu=True \
--optimized_softmax=True \
--input_graph=data/fp32_bert_squad.pb \
--do_predict=True --mode=benchmark \
--inter_op_parallelism_threads=1 \
--intra_op_parallelism_threads=36
```
- To run int8 inference on `gramine-direct` (non-SGX version), replace `gramine-sgx` with
`gramine-direct` in the above command.
- To run int8 inference natively (outside Gramine), replace `gramine-sgx ./python` with
`python3` in the above command.

## Run inference on ResNet50 model

- To run inference on `gramine-sgx` (SGX version):
```
OMP_NUM_THREADS=36 KMP_AFFINITY=granularity=fine,verbose,compact,1,0 taskset -c 0-35 gramine-sgx \
./python models/models/image_recognition/tensorflow/resnet50v1_5/inference/eval_image_classifier_inference.py \
--input-graph=resnet50v1_5_int8_pretrained_model.pb \
--num-inter-threads=1 \
--num-intra-threads=36 \
--batch-size=32 \
--warmup-steps=50 \
--steps=500
```
- To run inference on `gramine-direct` (non-SGX version), replace `gramine-sgx` with
`gramine-direct` in the above command.
- To run inference natively (outside Gramine), replace `gramine-sgx ./python` with
`python3` in the above command.

## Notes on optimal performance

Above commands are for a 36-core system. Please set the following options accordingly for optimal
performance:

- Assuming that X is the number of cores per socket, set `OMP_NUM_THREADS=X`,
  `intra_op_parallelism_threads=X` for BERT and `num_intra_threads=X` for ResNet50.
- Specify the whole range of cores available on one of the sockets in `taskset`.
- If hyperthreading is enabled: use `KMP_AFFINITY=granularity=fine,verbose,compact,1,0`.
- If hyperthreading is disabled: use `KMP_AFFINITY=granularity=fine,verbose,compact`.
- Note that `OMP_NUM_THREADS` sets the maximum number of threads to
  use for OpenMP parallel regions, and `KMP_AFFINITY` binds OpenMP threads
  to physical processing units.
- The options `batch-size`, `warmup-steps` and `steps` can be varied for ResNet50 sample.
- To get the number of cores per socket, do `lscpu | grep 'Core(s) per socket'`.

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

### Memory allocator libraries

TCMalloc and mimalloc are memory allocator libraries from Google and Microsoft that can help
improve performance significantly based on the workloads. Only one of these
allocators can be used at the same time.

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
