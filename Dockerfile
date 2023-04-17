FROM python:3.11

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY config/poetry.lock config/pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

# Execute the backend
EXPOSE 8080
COPY config/entrypoint.sh .
CMD ./entrypoint.sh
