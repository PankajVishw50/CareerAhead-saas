.PHONY: runserver
runserver:
	poetry run python3 manage.py runserver localhost:7575 

.PHONY: runserver-all
runserver-all:
	poetry run python3 manage.py runserver 0.0.0.0:7575
	
.PHONY: check 
check:
	poetry run python3 manage.py check

.PHONY: shell 
shell:
	poetry run python3 manage.py shell

.PHONY: shell_plus 
shell_plus:
	poetry run python3 manage.py shell_plus

.PHONY: createsuperuser
createsuperuser:
	poetry run python3 manage.py createsuperuser

.PHONY: makemigrations
makemigrations:
	poetry run python3 manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python3 manage.py migrate

.PHONY: makemigrate
makemigrate: makemigrations migrate

.PHONY: collectstatic
collectstatic: 
	poetry run python3 manage.py collectstatic

.PHONY: test 
test:
	poetry run python3 manage.py test

.PHONY: run-celery-multi
run-celery-multi:
	poetry run celery multi restart app -A careerahead worker -l info -c 2 \
		--logfile=logs/celery.log --pidfile=logs/celery.pid

.PHONY: run-all
run-all: run-celery-multi runserver