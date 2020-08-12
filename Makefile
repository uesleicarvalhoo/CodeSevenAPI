run:
	FLASK_APP=codesevenapi/app.py FLASK_ENV=development flask run

install:
	pip3 install -r requirements.txt

install-dev:
	pip3 install -r requirements-dev.txt

format:
	isort */**.py
	black */**.py