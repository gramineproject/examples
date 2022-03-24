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
all: pytorch.manifest
ifeq ($(SGX),1)
all: pytorch.manifest.sgx pytorch.sig pytorch.token
endif

%.manifest: %.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Dpillow_path=$(PILLOW_PATH) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		$< > $@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# we need to hack around.
pytorch.sig pytorch.manifest.sgx: sgx_outputs
	@:

.INTERMEDIATE: sgx_outputs
sgx_outputs: pytorch.manifest
	gramine-sgx-sign \
		--output pytorch.manifest.sgx \
		--manifest pytorch.manifest

%.token: %.sig
	gramine-sgx-get-token --output $@ --sig $<

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest

.PHONY: distclean
distclean: clean
	$(RM) *.pt result.txt
