import pyodbc

def test_db_connection():
    try:
        # Directly assigned values
        SERVER = 'budgetserver123.database.windows.net'
        DATABASE = 'budgetingdb'
        USERNAME = 'budgetadmin'
        PASSWORD = 'budget@123'

        CONNECTION_STRING = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
            f'Trusted_Connection=no;'
        )

        print("Attempting to connect to the database...")
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Test query - list tables
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
        tables = cursor.fetchall()

        print("\n✅ Successfully connected! Tables in DB:")
        for table in tables:
            print(f" - {table[0]}")

        cursor.close()
        conn.close()

    except Exception as e:
        print("\n❌ Failed to connect to the database.")
        print("Error:", e)

if __name__ == "__main__":
    test_db_connection()
