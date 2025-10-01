# -*- coding: utf-8 -*-
import psycopg

try:
    conn = psycopg.connect(
        host="127.0.0.1",
        user="postgres",
        password="postgres123",
        port=5432,
        dbname="tasks"
    )
    if conn:
        print("Connected to the PostgreSQL database")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY deadline_end ASC")
        tasks = cursor.fetchall()
        
        if tasks:
            print(f"\nFound {len(tasks)} task(s):")
            print("-" * 80)
            for task in tasks:
                print(f"ID: {task[0]}")
                print(f"Telegram ID: {task[1]}")
                print(f"Subject: {task[2]}")
                print(f"Task Type: {task[3]}")
                print(f"Task Number: {task[4]}")
                print(f"Points: {task[5]}")
                print(f"Deadline Start: {task[6]}")
                print(f"Deadline End: {task[7]}")
                print(f"Description: {task[8]}")
                print(f"First Reminder: {task[9]}")
                print(f"Second Reminder: {task[10]}")
                print(f"Status: {task[11]}")
                print(f"Created At: {task[12]}")
                print("-" * 80)
        else:
            print("No tasks found in the database")
            
        cursor.close()
        conn.close()
        print("Connection closed")
except Exception as e:
    print(e)