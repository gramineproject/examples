ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

SGX_SIGNER_KEY ?= ../../Pal/src/host/Linux-SGX/signer/enclave-key.pem

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: sklearnex.manifest
ifeq ($(SGX),1)
all: sklearnex.manifest.sgx sklearnex.sig sklearnex.token
endif

sklearnex.manifest: sklearnex.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		$< >$@

sklearnex.manifest.sgx: sklearnex.manifest
	@test -s $(SGX_SIGNER_KEY) || \
	    { echo "SGX signer private key was not found, please specify SGX_SIGNER_KEY!"; exit 1; }
	gramine-sgx-sign \
		--key $(SGX_SIGNER_KEY) \
		--manifest $< \
		--output $@

sklearnex.sig: sklearnex.manifest.sgx

sklearnex.token: sklearnex.sig
	gramine-sgx-get-token --output $@ --sig $<

.PHONY: check
check: all
	./run-tests.sh > TEST_STDOUT 2> TEST_STDERR
	@grep -q "Success 1/2" TEST_STDOUT
	@grep -q "Success 2/2" TEST_STDOUT

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig OUTPUT* TEST_STDOUT TEST_STDERR
	$(RM) -r __pycache__

.PHONY: distclean
distclean: clean
