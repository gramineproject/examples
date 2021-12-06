ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

SGX_SIGNER_KEY ?= ../../Pal/src/host/Linux-SGX/signer/enclave-key.pem
ONEDAL_LIBS ?= /usr/local/lib
PYTHON_VERSION ?= python3.9

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: sklearnex.manifest
ifeq ($(SGX),1)
all: trusted_files.list sklearnex.manifest.template.patched sklearnex.manifest.sgx sklearnex.sig sklearnex.token
endif

trusted_files.list:
	echo "$(shell $(PYTHON_VERSION) utils/get_trusted_files.py)" > $@

sklearnex.manifest.template.patched: sklearnex.manifest.template trusted_files.list
	sed 's|PLACEHOLDER|$(shell cat trusted_files.list)|' $< > $@

sklearnex.manifest: sklearnex.manifest.template.patched
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Donedal_libs=$(ONEDAL_LIBS) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v $(PYTHON_VERSION)")) \
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
	$(RM) *.list *.manifest *.patched *.manifest.sgx *.token *.sig OUTPUT* *.PID TEST_STDOUT TEST_STDERR
	$(RM) -r __pycache__

.PHONY: distclean
distclean: clean
