from sqlalchemy import create_engine

DB_USER = 'dbowner'
DB_PASSWORD = 'Secret5555'
DB_HOST = '127.0.0.1'
DB_NAME = 'order_db'

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
