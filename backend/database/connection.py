import os
from dotenv import load_dotenv
from databases import Database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not configured. "
        "Set it in Vercel Project Settings or your local .env file."
    )

database = Database(DATABASE_URL)
