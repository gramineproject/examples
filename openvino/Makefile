# Copyright (C) 2024 Gramine contributors
# SPDX-License-Identifier: BSD-3-Clause

SHELL := /bin/bash # use bash syntax to activate virtual environment and to download models

OPENVINO_DIR ?= $(INTEL_OPENVINO_DIR)

THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

INFERENCE_ENGINE_CPP_SAMPLES_BUILD ?= $(THIS_DIR)inference_engine_cpp_samples_build

MODEL_DIR ?= $(THIS_DIR)/model

INTEL_MODELS = \
	bert-large-uncased-whole-word-masking-squad-0001 \
	bert-large-uncased-whole-word-masking-squad-int8-0001

PUBLIC_MODELS = \
	resnet-50-tf \
	brain-tumor-segmentation-0001 \
	brain-tumor-segmentation-0002 \
	ssd_mobilenet_v1_coco

VENV_DIR ?= $(THIS_DIR)/openvino

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: benchmark_app benchmark_app.manifest $(VENV_DIR)/.INSTALLATION_OK intel_models public_models
ifeq ($(SGX),1)
all: benchmark_app.manifest.sgx benchmark_app.sig
endif

.PHONY: intel_models
intel_models: $(VENV_DIR)/.INSTALLATION_OK
	@source $(VENV_DIR)/bin/activate \
	&& cd $(OPENVINO_DIR)/deployment_tools/open_model_zoo/tools/downloader \
	&& for model in $(INTEL_MODELS); do \
		if [ ! -d $(abspath $(MODEL_DIR))/intel/$$model ]; then \
			python3 ./downloader.py --name $$model -o $(abspath $(MODEL_DIR)); \
			python3 ./converter.py --name $$model -d $(abspath $(MODEL_DIR)) -o $(abspath $(MODEL_DIR)); \
		fi; \
	done \
	&& deactivate

.PHONY: public_models
public_models: $(VENV_DIR)/.INSTALLATION_OK
	@source $(VENV_DIR)/bin/activate \
	&& cd $(OPENVINO_DIR)/deployment_tools/open_model_zoo/tools/downloader \
	&& for model in $(PUBLIC_MODELS); do \
		if [ ! -d $(abspath $(MODEL_DIR))/public/$$model ]; then \
			python3 ./downloader.py --name $$model -o $(abspath $(MODEL_DIR)); \
			python3 ./converter.py --name $$model -d $(abspath $(MODEL_DIR)) -o $(abspath $(MODEL_DIR)); \
		fi; \
	done \
	&& deactivate

.PRECIOUS: $(VENV_DIR)/.INSTALLATION_OK
$(VENV_DIR)/.INSTALLATION_OK:
	mkdir -p model
	python3 -m venv $(VENV_DIR) \
	&& source $(VENV_DIR)/bin/activate \
	&& pip install --upgrade pip \
	&& pushd $(OPENVINO_DIR)/deployment_tools/open_model_zoo/tools/downloader \
	&& python3 -mpip install -r ./requirements.in \
	&& popd \
	&& pushd $(OPENVINO_DIR)/deployment_tools/model_optimizer \
	&& pip3 install -r requirements.txt \
	&& popd \
	&& deactivate \
	&& touch $@

benchmark_app.manifest: benchmark_app.manifest.template | benchmark_app
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dopenvino_dir=$(abspath $(OPENVINO_DIR)) \
		-Dinference_engine_cpp_samples_build=$(abspath $(INFERENCE_ENGINE_CPP_SAMPLES_BUILD)) \
		$< > $@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
benchmark_app.manifest.sgx benchmark_app.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: benchmark_app.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

benchmark_app: $(OPENVINO_DIR)
	mkdir -p $(INFERENCE_ENGINE_CPP_SAMPLES_BUILD)
	cd $(INFERENCE_ENGINE_CPP_SAMPLES_BUILD) \
	&& cmake -DCMAKE_BUILD_TYPE=Release $(OPENVINO_DIR)/inference_engine/samples/cpp \
	&& make
	ln -s $(INFERENCE_ENGINE_CPP_SAMPLES_BUILD)/intel64/Release/benchmark_app $@

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig benchmark_app

.PHONY: distclean
distclean: clean
	$(RM) -r $(MODEL_DIR) $(VENV_DIR) $(INFERENCE_ENGINE_CPP_SAMPLES_BUILD)
