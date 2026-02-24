from fastapi import FastAPI
from .database.core import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .api.api import register_routes
import os
import errx
from errx import DisplayStyle

errx.bootstrap()

load_dotenv()
EMAIL_HOST = os.getenv("SMTP_HOST")
EMAIL_PORT = os.getenv("SMTP_PORT")
EMAIL_USERNAME = os.getenv("SMTP_USERNAME")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

app = FastAPI()

errx.install(app, return_json=False, display_style=DisplayStyle.NONE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    # allow_origins=["http://10.255.70.142:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


register_routes(app)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    print("Tables created")