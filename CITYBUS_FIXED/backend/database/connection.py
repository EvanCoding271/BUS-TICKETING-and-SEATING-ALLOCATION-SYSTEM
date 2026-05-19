from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. "
                       "Add it in your .env file or Vercel project settings.")
database = Database(DATABASE_URL)
