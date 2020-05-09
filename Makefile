requirements-dev:
	poetry export --dev -f requirements.txt > requirements_dev.txt

requirements:
	poetry export -f requirements.txt > requirements.txt

env-vars-template:
	cp .env .env.template

pyshell:
	poetry shell
