#!/bin/bash

# Run the migrations
python -m alembic upgrade head

# Run the API
uvicorn main:app --host 0.0.0.0 --port 8080
