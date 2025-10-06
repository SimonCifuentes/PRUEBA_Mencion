import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv('DB_URL', 'sqlite:///./app.db')
SECRET_TOKEN = os.getenv('SECRET_TOKEN', 'secreto123')
