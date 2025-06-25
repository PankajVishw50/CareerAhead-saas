.PHONY: runserver
runserver:
	poetry run python3 manage.py runserver localhost:7575 

.PHONY: runserver-all
runserver-all:
	poetry run python3 manage.py runserver 0.0.0.0:7575

runserver-debug:
	poetry run python3 manage.py runserver localhost:7576

run-gunicorn:
	poetry run python3 -m gunicorn \
		--pid pids/gunicorn-server.pid \
		$(ARGS)

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

.PHONY: test 
test:
	poetry run python3 manage.py test

.PHONY: run-celery-multi
run-celery-multi:
	poetry run celery multi start careerahead01 -A careerahead worker -l DEBUG -c 2 \
		--logfile=logs/celery.log \
		--pidfile=pids/celery.pid

run-celery-beat:
	poetry run celery -A careerahead beat -l DEBUG \
		--logfile=logs/celery-beat.log \
		--pidfile=pids/celery-beat.pid \
		--detach

.PHONY: run-all-except-gunicorn
run-all-except-gunicorn: stop-all run-celery-multi run-celery-beat

.PHONY: run-all
run-all: run-all-except-gunicorn run-gunicorn


load-dummy-data:
	poetry run python3 manage.py loaddata full_fixture.json

stop-celery-multi:
	poetry run celery multi stopwait careerahead01 \
		--pidfile=pids/celery.pid
	
stop-celery-beat:
	@if [ -f pids/celery-beat.pid ]; then \
		PID=$$(cat pids/celery-beat.pid); \
		if kill -0 $$PID 2>/dev/null; then \
			kill $$PID && echo "Celery Beat stopped"; \
		else \
			echo "No running process found with PID $$PID"; \
		fi; \
	else \
		echo "Celery Beat PID file not found"; \
	fi


stop-all: stop-celery-multi stop-celery-beat

# Utils rules
rm-pids:
	rm -f pids/*.pid

