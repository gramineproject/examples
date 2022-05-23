# Installation location of R. By default, Gramine will run the system R executable.
R_HOME ?= /usr/lib/R
R_EXEC = $(R_HOME)/bin/exec/R

SGX_SIGNER_KEY ?= ../../Pal/src/host/Linux-SGX/signer/enclave-key.pem

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

LD_LIBRARY_PATH := $(LD_LIBRARY_PATH):$(R_HOME)/lib
export LD_LIBRARY_PATH

.PHONY: all
all: R.manifest
ifeq ($(SGX),1)
all: R.manifest.sgx R.sig R.token
endif

R.manifest: R.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dr_home=$(R_HOME) \
		-Dr_exec=$(R_EXEC) \
		$< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
R.manifest.sgx R.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: R.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

R.token: R.sig
	gramine-sgx-get-token --output $@ --sig $<

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: check
check: all
	$(GRAMINE) ./R --slave --vanilla -f scripts/sample.r > OUTPUT 2> /dev/null
	@grep -q "success" OUTPUT && echo "[ Success 1/1 ]"
	@$(RM) OUTPUT

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig OUTPUT

.PHONY: distclean
distclean: clean
