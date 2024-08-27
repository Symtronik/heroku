import os
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

DATABASE_URL = os.environ("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.on_event("startup")
def on_startup():
    create_table()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
