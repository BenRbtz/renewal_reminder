PROJECT_NAME = renewal_reminder

install:
	poetry install --no-dev

install-dev:
	poetry install

run-unit-tests:
	poetry run pytest tests/unit

run-component-tests:
	poetry run behave tests/component/renewal_reminder/features

dev-services-up:
	docker-compose --project-name ${PROJECT_NAME} -f docker/docker-compose.yaml up --build -d

dev-services-down:
	docker-compose -f docker/docker-compose.yaml down --remove-orphans
