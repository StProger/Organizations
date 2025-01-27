DC = docker-compose
STORAGES_FILE = docker_compose/storages.yml
APP_FILE = docker_compose/app.yml
APP_CONTAINER = main-app
EXEC = docker exec -it
DB_CONTAINER = organizations-db
LOGS = docker logs
ENV_FILE = --env-file .env
ALEMBIC_REVISION = alembic revision --autogenerate
ALEMBIC_UPGRADE = alembic upgrade head


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql -U postgres

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV_FILE} up -d --build

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${ALEMBIC_UPGRADE}

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${ALEMBIC_REVISION} 