run:
	FLASK_APP=codesevenapi/app.py FLASK_ENV=development flask run

format:
	isort **/*.py
	isort codesevenapi/**/*.py
	black **/*.py
	black codesevenapi/**/*.py

test:
	pytest tests/ -v 

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
	pip install -e .[dev] --upgrade --no-cache
	rm -rf *.egg-info