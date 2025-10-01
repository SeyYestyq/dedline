import psycopg

def get_db():
    return psycopg.connect(
        host="127.0.0.1",
        user="postgres",
        password="postgres123",
        port=5432,
        dbname="tasks"
    )
