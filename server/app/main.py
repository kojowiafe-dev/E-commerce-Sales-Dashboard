from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


load_dotenv()
EMAIL_HOST = os.getenv("SMTP_HOST")
EMAIL_PORT = os.getenv("SMTP_PORT")
EMAIL_USERNAME = os.getenv("SMTP_USERNAME")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Tables created")