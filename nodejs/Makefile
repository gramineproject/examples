# Copyright (C) 2024 Gramine contributors
# SPDX-License-Identifier: BSD-3-Clause

THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
NODEJS_DIR ?= /usr/bin

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: nodejs.manifest
ifeq ($(SGX),1)
all: nodejs.manifest.sgx nodejs.sig
endif

nodejs.manifest: nodejs.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dnodejs_dir=$(NODEJS_DIR) \
		-Dnodejs_usr_share_dir=$(wildcard /usr/share/nodejs) \
		$< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
nodejs.manifest.sgx nodejs.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: nodejs.manifest helloworld.js
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: check
check: all
	$(GRAMINE) ./nodejs helloworld.js > OUTPUT
	@grep -q "Hello World" OUTPUT && echo "[ Success 1/1 ]"
	@rm OUTPUT

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig OUTPUT

.PHONY: distclean
distclean: clean
