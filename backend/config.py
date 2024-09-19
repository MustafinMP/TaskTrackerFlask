import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
INVITE_LINK_SALT = os.environ.get('INVITE_LINK_SALT')
MIN_DEADLINE_GAP = timedelta(minutes=5)


mode = 'local'
HOST = 'localhost' if mode == 'local' else '192.168.0.14'

