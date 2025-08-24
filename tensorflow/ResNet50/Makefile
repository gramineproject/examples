# ResNet50 sample for TensorFlow

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
SGX_SIGNER_KEY ?= ../../../Pal/src/host/Linux-SGX/signer/enclave-key.pem

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: python.manifest
ifeq ($(SGX),1)
all: python.manifest.sgx python.sig python.token
endif

.PHONY: collateral
collateral:
	test -d models || git clone https://github.com/IntelAI/models.git
	test -f resnet50v1_5_int8_pretrained_model.pb || wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/resnet50v1_5_int8_pretrained_model.pb

python.manifest: python.manifest.template collateral
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		-Dpythondistpath=$(PYTHONDISTPATH) \
		$< >$@

python.manifest.sgx: python.manifest
	@test -s $(SGX_SIGNER_KEY) || \
	    { echo "SGX signer private key was not found, please specify SGX_SIGNER_KEY!"; exit 1; }
	gramine-sgx-sign \
		--key $(SGX_SIGNER_KEY) \
		--manifest $< \
		--output $@

python.sig: python.manifest.sgx

python.token: python.sig
	gramine-sgx-get-token --output $@ --sig $<

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig

.PHONY: distclean
distclean: clean
	$(RM) -r models/ resnet50v1_5_int8_pretrained_model.pb
