PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
STREAMLIT := $(VENV)/bin/streamlit

.PHONY: install format lint test run-app clean

install: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

format: $(VENV)/bin/activate
	$(VENV)/bin/isort mm_names tests streamlit_app.py
	$(VENV)/bin/black mm_names tests streamlit_app.py

lint: $(VENV)/bin/activate
	$(VENV)/bin/pylint mm_names streamlit_app.py

test: $(VENV)/bin/activate
	$(VENV)/bin/pytest

run-app: $(VENV)/bin/activate
	$(STREAMLIT) run streamlit_app.py

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache .streamlit/__pycache__
