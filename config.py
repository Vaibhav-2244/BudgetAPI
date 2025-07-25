# config.py
import os

class Config:
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVER = os.getenv('DB_SERVER')
    DATABASE = os.getenv('DB_DATABASE')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')

    print("🔍 ENV CHECK:")
    print("SERVER:", SERVER)
    print("DATABASE:", DATABASE)
    print("USERNAME:", USERNAME)
    print("PASSWORD:", "✔️" if PASSWORD else "❌")  # Don't print raw password

    CONNECTION_STRING = (
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
    )
