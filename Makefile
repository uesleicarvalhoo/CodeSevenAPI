run:
	FLASK_APP=codesevenapi/app.py FLASK_ENV=development flask run

format:
	isort **/*.py
	isort codesevenapi/**/*.py
	black codesevenapi/***/**/*.py
	black **/*.py
	black codesevenapi/**/*.py
	black codesevenapi/***/**/*.py

install:
	pip install -e .[dev] --upgrade --no-cache

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	rm -rf *.egg-info

test:
	FLASK_ENV=test pytest tests/ -v
