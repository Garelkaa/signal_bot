import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
LOGGING_LEVEL = 'DEBUG'
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_NAME = os.getenv("POSTGRES_NAME")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def get_db_url() -> str:
    return f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_NAME}'
