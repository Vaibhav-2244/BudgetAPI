# config.py

import pyodbc

class Config:
    
    import os
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVER = os.getenv('DB_SERVER')  #budgetserver123.databases.windows.net
    DATABASE = os.getenv('DB_DATABASE') #budgetingdb
    USERNAME = os.getenv('DB_USERNAME')  #budgetadmin
    PASSWORD = os.getenv('DB_PASSWORD') #budget@123
    
    CONNECTION_STRING = (
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
    )

