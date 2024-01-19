# Copyright (C) 2024 Gramine contributors
# SPDX-License-Identifier: BSD-3-Clause

ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

IPERF_DIR = iperf
IPERF_REPO = https://github.com/esnet/iperf.git
IPERF_VERSION = 3.16

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: install/iperf3 install/libiperf.so.0 iperf3.manifest
ifeq ($(SGX),1)
all: iperf3.manifest.sgx iperf3.sig
endif

$(IPERF_DIR)/configure:
	git clone $(IPERF_REPO)
	cd $(IPERF_DIR) && git checkout $(IPERF_VERSION) && ./configure && make

$(IPERF_DIR)/src/.libs/iperf3: $(IPERF_DIR)/configure
	cd $(IPERF_DIR) && ./configure && make

iperf3.manifest: iperf3.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		$< > $@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# see the helloworld example for details on this workaround.
iperf3.sig iperf3.manifest.sgx: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: iperf3.manifest $(IPERF_DIR)/src/.libs/iperf3
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

# for simplicity, copy iperf3 executable into our install directory
install/iperf3: $(IPERF_DIR)/src/.libs/iperf3
	mkdir -p install
	cp $< $@

# for simplicity, copy libiperf library into our install directory
install/libiperf.so.0: $(IPERF_DIR)/src/.libs/libiperf.so.0
	mkdir -p install
	cp $< $@

################################## CLEANUP ####################################

.PHONY: clean
clean:
	$(RM) -r *.token *.sig *.manifest.sgx *.manifest install

.PHONY: distclean
distclean: clean
	$(RM) -r $(IPERF_DIR)
