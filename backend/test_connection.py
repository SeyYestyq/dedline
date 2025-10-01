# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password="postgres123",
        port=5432,
        database="tasks"
    )
    if conn:
        print("Connected to the PostgreSQL database")
        conn.close()
        print("Connection closed")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
