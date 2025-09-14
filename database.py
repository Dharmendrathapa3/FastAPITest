import mysql.connector
from fastapi import HTTPException
from mysql.connector import Error



# MySQL connection config - update with your details
db_config = {
    'host': 'localhost',
    'database': 'My_Portfolio',
    'user': 'root',
    'password': 'Surkhet@123'
}

# Helper function for DB connection
def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL platform: {e}")
        return None

## Create Tables

def custome_query(qr):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute(qr)
    conn.commit()
    cursor.close()
    conn.close()