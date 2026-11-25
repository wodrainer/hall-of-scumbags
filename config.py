import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DB_PATH', os.path.join(BASE_DIR, 'data', 'database.db'))

SECRET_KEY = os.environ.get('SECRET_KEY', 'sxd')
PASSWORD = os.environ.get('PASSWORD', 'xd')