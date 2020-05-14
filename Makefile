requirements-dev:
	poetry export --dev -f requirements.txt > requirements_dev.txt

requirements:
	poetry export -f requirements.txt > requirements.txt

update-env-vars-template:
	cp .env .env.template
	cp .poetry.env .poetry.env.template

pyshell:
	poetry shell

totoro-server:
	python manage.py runserver_plus

django-shell:
	python manage.py shell_plus --bpython

migrations:
	python manage.py makemigrations
	python manage.py migrate

static:
	python manage.py collectstatic

update-requirements:
	make requirements
	make requirements-dev

docker-django-shell:
	docker-compose exec order-service python manage.py shell_plus --bpython

docker-totoro-server:
	docker-compose up --build

docker-detached-totoro-server:
	docker-compose up -d --build

docker-run-tests:
	docker-compose exec web py.test

docker-totoro-server-down:
	docker-compose down
