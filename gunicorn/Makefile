# Copyright (C) 2024 Gramine contributors
# SPDX-License-Identifier: BSD-3-Clause

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: gunicorn.manifest
ifeq ($(SGX),1)
all: gunicorn.manifest.sgx gunicorn.sig
endif

gunicorn.manifest: gunicorn.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v gunicorn")) \
		-Dpython_exe_path=$(realpath $(shell sh -c "command -v python3")) \
		$< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`)
gunicorn.manifest.sgx gunicorn.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: gunicorn.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

.PHONY: clean
clean:
	$(RM) -rf *.token *.sig *.manifest *.manifest.sgx __pycache__

.PHONY: distclean
distclean: clean
