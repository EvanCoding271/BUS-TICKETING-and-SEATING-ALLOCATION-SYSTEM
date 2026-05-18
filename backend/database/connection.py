from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
	raise RuntimeError('DATABASE_URL environment variable is required for backend startup')
database = Database(DATABASE_URL)

