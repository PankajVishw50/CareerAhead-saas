.PHONY: runserver
runserver:
	python3 manage.py runserver localhost:7575 
	
.PHONY: check 
check:
	python3 manage.py check

.PHONY: shell 
shell:
	python3 manage.py shell

.PHONY: createsuperuser
createsuperuser:
	python3 manage.py createsuperuser

.PHONY: makemigrations
makemigrations:
	python3 manage.py makemigrations

.PHONY: migrate
migrate:
	python3 manage.py migrate

.PHONY: makemigrate
makemigrate: makemigrations migrate

.PHONY: collectstatic
collectstatic: 
	poetry run python3 manage.py collectstatic