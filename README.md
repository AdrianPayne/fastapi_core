# FastAPI Core
Core to build a Fastapi API!

# Features
## ORM (SQLModel)
Using SQLModel to use Pydantic and SQLAlchemist

## Migrations (Alembic)
To create a new migration file include the new models to the `core/db/models_db`

Migrations file automatically run when Docker run

## Encapsulation (Docker)
Easy to build and run everywhere, just:
```
docker-compose up
```

## Auth and user model

## Admin 
- PostgreSQL DB integration
- ORM using SQLModel
- Migrations with Alembic
- Base models with CRUD operations
- Auth with email/password and Google
- Email integration with X
- Test suit
- Encapsulated by Dockers
- CI/CD

# 🔧 Installation
Create a virtual environment and install the dependencies
```
python3 -m venv venv
source venv/bin/activate
cd config
poetry install
```

Install Dockers and run a PostgreSQL local DB
```
docker run --name fastapi-code-db -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -d postgres
```

# 🔌 Run (local)
## Using uvicorn
```
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
Check http://127.0.0.1:8080/

## Using Dockers
Build and run
```
docker-compose up
```

## Docs
The docs url is changed to avoid that automated scripts from cyber criminals get all the information
about our endpoints 🦹🏻

http://127.0.0.1:8000/core_docs

## DB
First, model the DB executing the migrations
```
python -m alembic upgrade head
```

Run X to populate DB with some data
```
TODO
```

To visualize, you can install and use PgAdmin
```
brew install --cask pgadmin4 
```

# 🧩 Extend the backend
## Readme
Here a cheatsheet to extend docs

[Makdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)

## Libraries
Add new libraries (with "add" command, new libraries will be installed too 😀)
```
cd config
poetry add <package>
```

## Models
We are using SQLModel for defining models and their methods. This is a library that mixes Poetry and SQLAlchemist.
### Define new models
[Pydantic field types](https://pydantic-docs.helpmanual.io😀/usage/types/)

Also it is probably you need to add any validator (some types as email already contains validators)
[Pydantic validators](https://pydantic-docs.helpmanual.io/usage/validators/)

> ⚠️ If you change properties of models used in DB, you should create a new migration file
```
python -m alembic revision --autogenerate -m "Your descriptiving comment about your change"
```
And then, you should refresh your DB with this new migration:
```
python -m alembic upgrade head    
```

Also, if you create new models, you should import them in `core/db/models_db.py`

### Define new methods
[SQLModel with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/)

# 🧪 Tests
Run tests with coverage
```
python -m pytest -vx --cov=core --cov-report term-missing --cov-fail-under=95
```


Using test client from fastapi library and unittest for test classes and asserts methods

Try to develop following TDD rules (writing tests before views, models and methods)

Call to method tearDown for deleting all the created objects in the DB.

# TODO
## Core
- [X] Terminar service example (endpoints, schemes, httperrors, dependencies)
- [X] Infra DEV (Docker, DB Settings, Migrations)
- [ ] CI 
  

- [ ] Autentificacion (Oauth2: access y refresh tokens & level access)
- [ ] Servicio de usuarios (modelo, endpoints de password reset, CRUD, Factories)
- [ ] [Fastapi admin](https://aminalaee.dev/sqladmin/)


- [ ] Integracion con email client (extender usuario)
- [ ] Auth con Google (extender User)
- [ ] Logs y Debug (Sentry)
- [ ] Check async is correct

Extra:
- [ ] Generate TS Client
- [ ] Cache
- [ ] Repository integration (G Storage)
- [ ] MongoDB client
