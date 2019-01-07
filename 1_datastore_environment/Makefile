
# Variables
REQUIREMENTS_FILE=requirements.txt
TEST_PROJECT_ID=testprojectid
LOCAL_PROJECT_ID=localprojectid

# Ensure's virtual environment is activated
.PHONY: virtualenv
virtualenv:
ifndef VIRTUAL_ENV
	$(error Must be inside of a virtual env.)
endif

# Install python requirements
.PHONY: install
install: virtualenv
	pip install -Ur $(REQUIREMENTS_FILE)

# Run integration tests
.PHONY: integrations
integrations:
	DATASTORE_EMULATOR_HOST=localhost:8081 GOOGLE_CLOUD_PROJECT=$(TEST_PROJECT_ID)  nosetests

# Run the application locally
.PHONY: dev
dev: virtualenv
	 DATASTORE_EMULATOR_HOST=localhost:8081 GOOGLE_CLOUD_PROJECT=$(LOCAL_PROJECT_ID) python main.py

# Standup datastore emulator for local dev
.PHONY: dev-env
dev-env: virtualenv
	gcloud beta emulators datastore start --project=$(LOCAL_PROJECT_ID) --data-dir=../data

# Standup datastore emulator for integration tests
.PHONY: test-env
test-env: virtualenv
		gcloud beta emulators datastore start --project=$(TEST_PROJECT_ID) --data-dir=../data/
