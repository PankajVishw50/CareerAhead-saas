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