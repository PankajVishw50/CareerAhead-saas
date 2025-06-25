FROM python:3.12.3-bullseye AS base 

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE="careerahead.settings"
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /careerahead-saas-backend
RUN mkdir -p pids

# Add Poetry to path
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
  apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml ./poetry.lock ./ 



# Development Image
FROM base AS dev

RUN apt-get install -y vim curl less tree htop net-tools

RUN poetry sync --all-groups
COPY . .

CMD ["sh", "-c", "make rm-pids; make run-all-except-gunicorn; make run-gunicorn ARGS='--reload --worker-class util.uvicornworker.RestartableUvicornWorker'"]

# Production Image
FROM base AS prod

RUN poetry sync --only main --compile
COPY . .

CMD ["make", "run-all"]
