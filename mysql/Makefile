ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
UID ?= $(shell id -u)
GID ?= $(shell id -g)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: mysqld.manifest
ifeq ($(SGX),1)
all: mysqld.manifest.sgx mysqld.sig
endif

mysqld.manifest: mysqld.manifest.template
	gramine-manifest \
        -Dlog_level=$(GRAMINE_LOG_LEVEL) \
        -Darch_libdir=$(ARCH_LIBDIR) \
        -Duid=$(UID) \
        -Dgid=$(GID) \
        -Dentrypoint=$(realpath $(shell sh -c "command -v mysqld")) \
         $< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
mysqld.manifest.sgx mysqld.sig: sgx_sign
	@:

.INTERMEDIATE: sgx_sign
sgx_sign: mysqld.manifest
	gramine-sgx-sign \
        --manifest $< \
        --output $<.sgx

.PHONY: clean
clean:
	$(RM) *.sig *.manifest.sgx *.manifest

.PHONY: distclean
distclean: clean
