# PyTorch and the pre-trained model must be installed on the system. See README for details.

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

# PyTorch uses the Pillow backend; detect where Pillow was installed
PILLOW_PATH ?= $(shell pip3 show pillow | grep Location: | cut -d" " -f2)/

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: alexnet-pytorch.py.manifest
ifeq ($(SGX),1)
all: alexnet-pytorch.py.manifest.sgx alexnet-pytorch.py.sig
endif

alexnet-pytorch.py.manifest: alexnet-pytorch.py.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Dpillow_path=$(PILLOW_PATH) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		$< > $@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
alexnet-pytorch.py.manifest.sgx alexnet-pytorch.py.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: alexnet-pytorch.py.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest

.PHONY: distclean
distclean: clean
	$(RM) *.pt result.txt
