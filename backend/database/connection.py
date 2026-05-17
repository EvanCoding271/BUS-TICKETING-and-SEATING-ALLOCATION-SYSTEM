<<<<<<< HEAD
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
database = Database(DATABASE_URL)
=======
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
database = Database(DATABASE_URL)
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0
