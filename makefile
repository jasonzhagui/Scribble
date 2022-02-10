include common.mk

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin main

dev_env: FORCE
	- ./setup.sh SCRIBBLE_HOME
	pip install -r $(REQ_DIR)/requirements-dev.txt

all_tests: FORCE
	cd $(API_DIR); make tests
	cd $(DB_DIR); make tests

all_docs: FORCE
	cd $(API_DIR); make docs
	cd $(DB_DIR); make docs

heroku_remote:
	heroku git:remote -a scribble-art

heroku_api_key:
	heroku auth:token
