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
def get_connection(dic=False):
    try:
        conn = mysql.connector.connect(**db_config)
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
        cursor = conn.cursor(dictionary=dic)
        return conn,cursor
    except Error as e:
        print(f"Error connecting to MySQL platform: {e}")
        return None
    
def closed_connection():
    conn,cursor=get_connection()
    cursor.close()
    conn.close()

## Create Tables

def custome_query(qr):
    _,cursor = get_connection()
    
    cursor.execute(qr)

    closed_connection