.PHONY: install run test demo lint clean

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

demo:
	python scripts/demo.py

lint:
	ruff check .

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache output
