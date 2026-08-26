.PHONY: generate validate test

generate:
	python scripts/generate.py

validate: generate
	python scripts/validate.py

test: validate
	pytest

deps:
	pip install -r requirements.txt
