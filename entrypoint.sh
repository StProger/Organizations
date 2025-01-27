#!/bin/bash

alembic upgrade head
uvicorn --factory app.application.api.main:create_app --reload --host 0.0.0.0 --port 8000