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
	poetry run celery multi start careerahead01 -A careerahead worker -l DEBUG -c 2 \
		--logfile=logs/celery.log \
		--pidfile=logs/celery.pid

run-celery-beat:
	poetry run celery -A careerahead beat -l DEBUG \
		--logfile=logs/celery-beat.log \
		--pidfile=logs/celery-beat.pid \
		--detach

.PHONY: run-all
run-all: stop-all run-celery-multi run-celery-beat runserver

stop-celery-multi:
	poetry run celery multi stopwait careerahead01 \
		--pidfile=logs/celery.pid

stop-celery-beat:
	@if [ -f logs/celery-beat.pid ]; then \
		PID=$$(cat logs/celery-beat.pid); \
		if kill -0 $$PID 2>/dev/null; then \
			kill $$PID && echo "Celery Beat stopped"; \
		else \
			echo "No running process found with PID $$PID"; \
		fi; \
	else \
		echo "Celery Beat PID file not found"; \
	fi


stop-all: stop-celery-multi stop-celery-beat