import os
from pathlib import Path
from dotenv import load_dotenv
from databases import Database

# Load environmental configs safely
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable is required for backend startup')

# 🛠️ THE CRUCIAL VERCEL FIX: 
# Asyncpg requires 'postgresql://', but Supabase sometimes provides 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Ensure connection pooling strings don't crash serverless functions
database = Database(DATABASE_URL, min_size=1, max_size=5)

