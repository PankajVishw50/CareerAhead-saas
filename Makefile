
BASE_DOCKER_COMPOSE=./docker-compose.yml
DEV_DOCKER_COMPOSE=./docker-compose-dev.yml
PROD_DOCKER_COMPOSE=./docker-compose-prod.yml
DEBUG_DOCKER_COMPOSE=./docker-compose-debug.yml

BACKEND_DOCKER=./backend/Dockerfile
FRONTEND_DOCKER=./frontend/Dockerfile

prefix-prod:
	docker compose -f ${BASE_DOCKER_COMPOSE} -f ${PROD_DOCKER_COMPOSE} $(ARGS)

prefix-dev:
	docker compose -f ${BASE_DOCKER_COMPOSE} -f ${DEV_DOCKER_COMPOSE} $(ARGS)

prefix-debug:
	$(MAKE) prefix-dev ARGS="-f ${DEBUG_DOCKER_COMPOSE} $(ARGS)"

prefix-all:
	docker compose -f ${BASE_DOCKER_COMPOSE} \
		-f ${PROD_DOCKER_COMPOSE} \
		-f ${DEV_DOCKER_COMPOSE} \
		-f ${DEBUG_DOCKER_COMPOSE} \
		$(ARGS)


%-up-build:
	$(MAKE) prefix-$(*) ARGS="up --build -d"

%-restart:
	$(MAKE) prefix-$(*) ARGS="restart"

%-up:
	$(MAKE) prefix-$(*) ARGS="up -d $(ARGS)"

clean-prod:
	$(MAKE) prefix-prod ARGS="down"

clean-dev:
	$(MAKE) prefix-dev ARGS="down"

clean-debug:
	$(MAKE) prefix-debug ARGS="down"

clean-indvidually: clean-dev clean-prod clean-debug

clean:
	$(MAKE) prefix-all ARGS="down"


%-bash:
	$(MAKE) prefix-all ARGS="exec $* bash"

%-sh:
	$(MAKE) prefix-all ARGS="exec $* sh"

logs:
	$(MAKE) prefix-all ARGS="logs -f $(ARGS)"
	
logs-d:
	$(MAKE) prefix-all ARGS="logs"

primary-logs:
	$(MAKE) prefix-all ARGS="logs -f backend frontend"

secondary-logs:
	$(MAKE) prefix-all ARGS="logs -f rabbitmq postgres redis backend_db_setup nginx frontend-builder"

%-logs:
	$(MAKE) prefix-all ARGS="logs -f $*"
