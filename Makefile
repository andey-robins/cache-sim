# Makefile
# a very simple makefile for installing python dependencies.

# Instructions:
# We recommend you to use virtual environment while working with python and if requires to install extra packages.
# Note: Do not include venv files while making the zip file if you are using venv.

######################################################################################

# this is a sample Makefile code with implementation of virtual environment. 

# Virtual Environment Name
VENV_NAME := venv

# Python Interpreter
# built with 3.12.0b3, PEP linting and some type checking may
# fail with <= 3.11
# PYTHON := python3.12
PYTHON := python3

# Paths
VENV_PATH := $(VENV_NAME)
REQUIREMENTS := requirements.txt

# Target for creating a virtual environment
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_NAME)

# Target for installing libraries
install: venv
	@echo "Activating virtual environment..."
	@. $(VENV_PATH)/bin/activate && \
		$(PYTHON) -m pip install -r $(REQUIREMENTS)
	@echo "Libraries installed successfully."

# Target for removing the virtual environment
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_NAME)
	@echo "Virtual environment removed."
	@echo "Removing zip archive..."
	@rm -rf sim_cache.zip
	@echo "Zip archive removed."

test:
	@echo "Running unittests with pytest..."
	@python3 -m unittest **/tests/*.py

run:
	@echo "Running sim_cache.py with debug0 config..."
	python3 sim_cache.py 16 1024 2 0 0 0 0 ./provided/traces/gcc_trace.txt
	@echo "---\nEnd of execution."

zip:
	zip -r mp1.zip sim_cache.py cache/ behavior/ helpers/ Makefile README.md LICENSE report.pdf
	@echo "Zip archive created as mp1.zip"

diffs-debug:
	@echo "Manually set debug to True in sim_cache.py"
	python3 sim_cache.py 16 1024 2 0 0 0 0 ./provided/traces/gcc_trace.txt > ./out/debug0_run.out
	diff ./out/debug0_run.out ./provided/debug_runs/debug0.txt -iw
	python3 sim_cache.py 16 1024 1 0 0 0 0 ./provided/traces/perl_trace.txt > ./out/debug1_run.out
	diff ./out/debug1_run.out ./provided/debug_runs/debug1.txt -iw
	python3 sim_cache.py 16 1024 2 0 0 1 0 ./provided/traces/gcc_trace.txt > ./out/debug2_run.out
	diff ./out/debug2_run.out ./provided/debug_runs/debug2.txt -iw
	python3 sim_cache.py 16 1024 2 8192 4 0 0 ./provided/traces/gcc_trace.txt > ./out/debug3_run.out
	diff ./out/debug3_run.out ./provided/debug_runs/debug3.txt -iw
	python3 sim_cache.py 16 1024 1 8192 4 0 0 ./provided/traces/go_trace.txt > ./out/debug4_run.out
	diff ./out/debug4_run.out ./provided/debug_runs/debug4.txt -iw
	python3 sim_cache.py 16 1024 2 8192 4 0 1 ./provided/traces/gcc_trace.txt > ./out/debug5_run.out
	diff ./out/debug5_run.out ./provided/debug_runs/debug5.txt -iw
	python3 sim_cache.py 16 1024 1 8192 4 0 1 ./provided/traces/compress_trace.txt > ./out/debug6_run.out
	diff ./out/debug6_run.out ./provided/debug_runs/debug6.txt -iw

diffs:
	python3 sim_cache.py 16 1024 2 0 0 0 0 ./provided/traces/gcc_trace.txt > ./out/validation0_run.out
	diff ./out/validation0_run.out ./provided/validation_runs/validation0.txt -iw
	python3 sim_cache.py 16 1024 1 0 0 0 0 ./provided/traces/perl_trace.txt > ./out/validation1_run.out
	diff ./out/validation1_run.out ./provided/validation_runs/validation1.txt -iw
	python3 sim_cache.py 16 1024 2 0 0 1 0 ./provided/traces/gcc_trace.txt > ./out/validation2_run.out
	diff ./out/validation2_run.out ./provided/validation_runs/validation2.txt -iw
	python3 sim_cache.py 16 1024 2 8192 4 0 0 ./provided/traces/gcc_trace.txt > ./out/validation3_run.out
	diff ./out/validation3_run.out ./provided/validation_runs/validation3.txt -iw
	python3 sim_cache.py 16 1024 1 8192 4 0 0 ./provided/traces/go_trace.txt > ./out/validation4_run.out
	diff ./out/validation4_run.out ./provided/validation_runs/validation4.txt -iw
	python3 sim_cache.py 16 1024 2 8192 4 0 1 ./provided/traces/gcc_trace.txt > ./out/validation5_run.out
	diff ./out/validation5_run.out ./provided/validation_runs/validation5.txt -iw
	python3 sim_cache.py 16 1024 1 8192 4 0 1 ./provided/traces/compress_trace.txt > ./out/validation6_run.out
	diff ./out/validation6_run.out ./provided/validation_runs/validation6.txt -iw


.PHONY: venv install clean

######################################################################################