# API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# DB
from services.mobile_signal.models import MobileSignal
from core.db.connection import DbSession

# Import all the routers
from services.mobile_signal.views import router as ms_router

# DB
MobileSignal
DbSession.create_tables()

description = """
Fastapi core to create complete APIs in record time!
"""

app = FastAPI(
    title="Fastapi Core",
    description=description,
    version="0.0.1",
    contact={
        "name": "Adrian",
        "email": "adriansacristancontractor@gmail.com",
    },
    docs_url="/core_docs",
    responses={404: {"description": "Not found"}}
)


# Routers
app.include_router(ms_router)


origins = [
    "http://localhost:3000/",
    "http://localhost:3000",
]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main_route():
    return {"message": "Welcome to the Fastapi core API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

