import os
from dotenv import load_dotenv


load_dotenv()

dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

DATABASE_URL: str = 'postgresql://misha:bMAAO6l63J9I@projects.csradvigauhb.eu-west-2.rds.amazonaws.com:5432/DS2023'
