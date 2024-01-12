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
all: $(IPERF_DIR)/src/.libs/iperf3 iperf3.manifest
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

.PHONY: start-native-server
start-native-server: all
	LD_LIBRARY_PATH=$(IPERF_DIR)/src/.libs $(IPERF_DIR)/src/.libs/iperf3 -s

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

# Note that command-line arguments are hardcoded in the manifest file.
.PHONY: start-gramine-server
start-gramine-server: all
	$(GRAMINE) iperf3

################################## CLEANUP ####################################

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest iperf3

.PHONY: distclean
distclean: clean
	$(RM) -r $(IPERF_DIR)
