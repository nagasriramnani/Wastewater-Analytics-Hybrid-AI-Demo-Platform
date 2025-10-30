.PHONY: setup fmt lint typecheck test run clean

# Create virtual environment and install dependencies
setup:
	python -m venv venv
	. venv/Scripts/activate && pip install --upgrade pip && pip install -r requirements.txt

# Format code
fmt:
	black .
	isort .

# Lint code
lint:
	ruff check .

# Type checking
typecheck:
	mypy app

# Run tests
test:
	pytest -v

# Run Streamlit app
run:
	streamlit run app/streamlit_app.py

# Clean generated files
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache



