# Detección automática de entorno
INSIDE_DOCKER := $(shell [ -f /.dockerenv ] && echo yes || echo no)
HAS_VENV      := $(shell [ -f .venv/bin/python ] && echo yes || echo no)

ifeq ($(INSIDE_DOCKER),yes)
  PYTHON_INTERPRETER = python
else ifeq ($(HAS_VENV),yes)
  PYTHON_INTERPRETER = .venv/bin/python
endif

ifdef PYTHON_INTERPRETER

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME   = malnutrition-research
PYTHON_VERSION = 3.12.13

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -e .

## Delete all compiled Python files and clean up LaTeX auxiliary files in docs/
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo ">>> Cleaning up LaTeX auxiliary files in docs/..."
	@find docs/ -type f \( -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.lof" -o -name "*.lot" -o -name "*.synctex.gz" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.blg" -o -name "*.bbl" \) -delete
	@find docs/ -type d -name ".tmp" -exec rm -rf {} +

## Lint using ruff
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Run tests
.PHONY: test
test:
	$(PYTHON_INTERPRETER) -m pytest tests

## Set up Python interpreter environment using pyenv + venv
.PHONY: create_environment
create_environment:
	@echo ">>> Setting local pyenv version to $(PYTHON_VERSION)..."
	@pyenv local $(PYTHON_VERSION) || (echo "ERROR: Python $(PYTHON_VERSION) is not installed. Run 'pyenv install $(PYTHON_VERSION)' first." && exit 1)
	@echo ">>> Creating virtual environment in .venv..."
	@python -m venv .venv
	@echo ">>> Virtual environment created. Activate it with:"
	@echo "    source .venv/bin/activate"

#################################################################################
# DATA PIPELINE                                                                 #
#################################################################################

## Download raw ENDES data from INEI
.PHONY: ingest
ingest: requirements
	$(PYTHON_INTERPRETER) -m mnp.ingestion._ingest extract

## Audit local raw data integrity
.PHONY: audit
audit: requirements
	$(PYTHON_INTERPRETER) -m mnp.ingestion._ingest audit

## Run cleaning pipeline (raw → interim)
.PHONY: clean_data
clean_data: requirements
	$(PYTHON_INTERPRETER) -m mnp.pipeline.cleaning

## Run validation pipeline (interim → validated)
.PHONY: validate_data
validate_data: requirements
	$(PYTHON_INTERPRETER) -m mnp.pipeline.validation

## Full pipeline: ingest → clean → validate
.PHONY: pipeline
pipeline: ingest clean_data validate_data

## Make dataset (full local processing pipeline)
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) -m mnp.dataset make

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)

else

#################################################################################
# Sin entorno local: redirigir a Docker                                         #
#################################################################################

.DEFAULT_GOAL := help

## Start Docker container in the background
docker-up:
	@echo ">>> Starting Docker container..."
	docker compose up -d
	@echo ">>> Container is up! Jupyter Lab available at http://localhost:8888"

## Stop Docker container
docker-down:
	@echo ">>> Stopping Docker container..."
	docker compose down

## Open interactive shell inside Docker container
docker-shell:
	@echo ">>> Entering Docker container shell..."
	@docker compose exec malnutrition-research-workspace bash || docker compose run --rm malnutrition-research-workspace bash

## Rebuild Docker container
docker-build:
	@echo ">>> Building Docker container..."
	docker compose build

## Set up Python interpreter environment using pyenv + venv
create_environment:
	@echo ">>> Setting local pyenv version to 3.12.13..."
	@pyenv local 3.12.13 || (echo "ERROR: Run 'pyenv install 3.12.13' first." && exit 1)
	@echo ">>> Creating virtual environment in .venv..."
	@python -m venv .venv
	@echo ">>> Virtual environment created. Activate it with:"
	@echo "    source .venv/bin/activate"

# Redirigir el resto a Docker automáticamente
%:
	@docker compose run --rm malnutrition-research-workspace make $@

endif
