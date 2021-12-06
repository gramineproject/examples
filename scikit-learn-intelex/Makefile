ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

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
		-Denv_user_uid=$(shell id -u) \
		-Denv_user_gid=$(shell id -g) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		$< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# see the helloworld example for details on this workaround.
sklearnex.manifest.sgx sklearnex.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: sklearnex.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

sklearnex.token: sklearnex.sig
	gramine-sgx-get-token --output $@ --sig $<

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig OUTPUT* TEST_STDOUT TEST_STDERR
	$(RM) -r __pycache__
	$(RM) -r scripts/__pycache__

.PHONY: distclean
distclean: clean
