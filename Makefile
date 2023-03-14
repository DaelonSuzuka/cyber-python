# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# **************************************************************************** #

# load the pypi credentials
ifneq (,$(wildcard .env))
include .env
# export them for twine
export
endif

# **************************************************************************** #
# Targets

# run the application
run: venv
	$(VENV_PYTHON) main.py

# **************************************************************************** #

ZIG := zig build lib
ZIGFLAGS := -Doptimize=ReleaseFast -Dcpu=baseline


# generate cyber/lib.py from src/cyber/cyber.h
bindings: venv
	$(VENV_PYTHON) tools/generate_bindings.py

pull_libs: venv
	$(VENV_PYTHON) tools/download_libs.py

# build cyber for the current platform in debug mode
build_lib:
	cd src/cyber && $(ZIG)
	cp src/cyber/zig-out/lib/* cyber/lib

# build cyber for all platforms in release mode
build_libs:
	cd src/cyber && $(ZIG) $(ZIGFLAGS) -Dtarget=x86_64-windows-gnu
	cd src/cyber && $(ZIG) $(ZIGFLAGS) -Dtarget=x86_64-linux-gnu
#	cd src/cyber && $(ZIG) $(ZIGFLAGS) -Dtarget=x86_64-macos.12.none
#	cd src/cyber && $(ZIG) $(ZIGFLAGS) -Dtarget=aarch64-macos.12.none
	cp src/cyber/zig-out/lib/cyber.dll cyber/lib/cyber.dll
	cp src/cyber/zig-out/lib/libcyber.so cyber/lib/libcyber.so
#	cp src/cyber/zig-out/lib/libcyber.dylib cyber/lib/libcyber.dylib
#	cp src/cyber/zig-out/lib/libcyber.dylib cyber/lib/libcyber-arm64.dylib

# **************************************************************************** #

# reinstall this package to the virtualenv
reload: venv
	$(VENV_PYTHON) -m pip install -e .

# build the package
build: venv
	$(VENV_PYTHON) -m build

# upload the built package to pypi using twine
publish: venv
	$(VENV_PYTHON) -m twine upload dist/* -u __token__

#
tox: venv
	$(VENV_PYTHON) -m tox

#
tests: venv
	$(VENV_PYTHON) -m pytest

coverage: venv
	$(VENV_PYTHON) -m pytest --cov

# remove build artifacts
clean:
	-$(RM) build
	-$(RM) dist
	-$(RM) qtstrap.egg-info

# **************************************************************************** #
# python venv settings
VENV_NAME := .venv
REQUIREMENTS := requirements.txt

ifeq ($(OS),Windows_NT)
	VENV_DIR := $(VENV_NAME)
	VENV_CANARY_DIR := $(VENV_DIR)/canary
	VENV_CANARY_FILE := $(VENV_CANARY_DIR)/$(REQUIREMENTS)
	VENV_TMP_DIR := $(VENV_DIR)/tmp
	VENV_TMP_FREEZE := $(VENV_TMP_DIR)/freeze.txt
	VENV := $(VENV_DIR)/Scripts
	PYTHON := python
	VENV_PYTHON := $(VENV)/$(PYTHON)
	VENV_PYINSTALLER := $(VENV)/pyinstaller
	RM := rm
else
	VENV_DIR := $(VENV_NAME)
	VENV_CANARY_DIR := $(VENV_DIR)/canary
	VENV_CANARY_FILE := $(VENV_CANARY_DIR)/$(REQUIREMENTS)
	VENV_TMP_DIR := $(VENV_DIR)/tmp
	VENV_TMP_FREEZE := $(VENV_TMP_DIR)/freeze.txt
	VENV := $(VENV_DIR)/bin
	PYTHON := python3
	VENV_PYTHON := $(VENV)/$(PYTHON)
	VENV_PYINSTALLER := $(VENV)/pyinstaller
	RM := rm -rf 
endif

# Add this as a requirement to any make target that relies on the venv
.PHONY: venv
venv: $(VENV_DIR) $(VENV_CANARY_FILE)

# Create the venv if it doesn't exist
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Update the venv if the canary is out of date
$(VENV_CANARY_FILE): $(REQUIREMENTS)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r $(REQUIREMENTS)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	-cp $(REQUIREMENTS) $(VENV_CANARY_FILE)

# forcibly update the canary file
canary: $(VENV_CANARY_DIR)
	cp $(REQUIREMENTS) $(VENV_CANARY_FILE)

# update requirements.txt to match the state of the venv
freeze_reqs: venv
	$(VENV_PYTHON) -m pip freeze > $(REQUIREMENTS)

# try to update the venv - expirimental feature, don't rely on it
update_venv: venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install --upgrade -r $(REQUIREMENTS)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	-cp $(REQUIREMENTS) $(VENV_CANARY_FILE)

# remove all packages from the venv
clean_venv:
	$(RM) $(VENV_CANARY_DIR)
	mkdir $(VENV_TMP_DIR)
	$(VENV_PYTHON) -m pip freeze > $(VENV_TMP_FREEZE)
	$(VENV_PYTHON) -m pip uninstall -y -r $(VENV_TMP_FREEZE)
	$(RM) $(VENV_TMP_DIR)

# clean the venv and rebuild it
reset_venv: clean_venv update_venv

# **************************************************************************** #
# expirimental, probably not reliable

# If the first argument is "pip"...
ifeq (pip,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "pip"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# forward pip commands to the venv
pip: venv
	$(VENV_PYTHON) -m pip $(RUN_ARGS)
