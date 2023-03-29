FROM python:3.10

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY devops/poetry.lock devops/pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

# Execute the backend
EXPOSE 8080
COPY devops/entrypoint.sh .
CMD ./entrypoint.sh
