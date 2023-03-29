# Example service
The purpose of this service is to show a complete example of a service based in core features in order to be imitated 
to extend the backend

## 🔌 Run
```
uvicorn core.service_example.views:app --host 0.0.0.0 --port 8080 --reload
```

## 🧪 Tests
```
python -m pytest -vx --cov=core --cov-report term-missing --cov-fail-under=95
```