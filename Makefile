requirements-dev:
	poetry export --dev -f requirements.txt > requirements_dev.txt

requirements:
	poetry export -f requirements.txt > requirements.txt

env-vars-template:
	cp .env .env.template

pyshell:
	poetry shell

server:
	python manage.py runserver_plus

djshell:
	python manage.py shell_plus --bpython


i-djshell:
	python manage.py shell_plus --ipython

migrations:
	python manage.py makemigrations
	python manage.py migrate

static:
	python manage.py collectstatic

update-requirements:
	make requirements
	make requirements-dev
