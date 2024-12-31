.PHONY: install dev-up dev-down dev-publish dev-consume run lint test build docker-run

install:
	poetry install

dev-up:
	docker-compose up -d

dev-down:
	docker-compose down

run:
	PUBSUB_EMULATOR_HOST=localhost:8085 \
	poetry run worker

lint:
	black .

test:
	pytest .

build:
	docker build -t async_worker_svc .

docker-run:
	docker run -it --rm --name async_worker_svc -e PUBSUB_EMULATOR_HOST=0.0.0.0:8085 --network host async_worker_svc bash

dev-publish:
	@python scripts/publish.py $(filter-out $@,$(MAKECMDGOALS))

dev-consume:
	@python scripts/consume.py