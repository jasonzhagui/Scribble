LINTER = flake8
API_DIR = API
DB_DIR = db
REQ_DIR = .
PYDOC = python3 -m pydoc -w

export TEST_MODE = 1

FORCE:

tests: lint unit

unit: FORCE
	cd $(API_DIR); nosetests --with-coverage --cover-package=$(API_DIR)

lint: FORCE
	$(LINTER) *.py

docs: FORCE
	$(PYDOC) ./*.py
	git add ./*.html