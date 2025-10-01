# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from database import get_db

app = FastAPI()

# CORS для Telegram WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/tasks/{telegram_id}")
async def get_categorized_tasks(telegram_id: int):
    """Получить задачи с автоматической категоризацией"""
    
    conn = get_db()
    cur = conn.cursor()
    
    # Получить все незавершенные задачи
    cur.execute("""
        SELECT 
            id,
            subject,
            task_type,
            task_number,
            points,
            deadline_start,
            deadline_end,
            description,
            first_reminder,
            second_reminder,
            status
        FROM tasks 
        WHERE telegram_id = %s 
        AND status = 'pending'
        ORDER BY deadline_end ASC
    """, (telegram_id,))
    
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    
    # Преобразуем кортежи в словари
    task_list = []
    for task in tasks:
        task_dict = {
            'id': task[0],
            'subject': task[1],
            'task_type': task[2],
            'task_number': task[3],
            'points': task[4],
            'deadline_start': task[5],
            'deadline_end': task[6],
            'description': task[7],
            'first_reminder': task[8],
            'second_reminder': task[9],
            'status': task[10]
        }
        task_list.append(task_dict)
    
    # Категоризация
    now = date.today()
    urgent = []      # < 7 дней
    current = []     # 7-21 день
    upcoming = []    # > 21 день
    
    for task in task_list:
        deadline = task['deadline_end']
        days_left = (deadline - now).days
        
        # Добавляем информацию о днях
        task['days_left'] = days_left
        
        # Форматируем название задачи
        task_name = f"{task['task_type']}"
        if task['task_number']:
            task_name += f" {task['task_number']}"
        if task['points']:
            task_name += f" ({task['points']} б.)"
        task['formatted_name'] = task_name
        
        # Категоризация
        if days_left < 0:
            task['urgency'] = 'overdue'
            urgent.append(task)
        elif days_left <= 7:
            task['urgency'] = 'urgent'
            urgent.append(task)
        elif days_left <= 21:
            task['urgency'] = 'current'
            current.append(task)
        else:
            task['urgency'] = 'upcoming'
            upcoming.append(task)
    
    return {
        'urgent': urgent,
        'current': current,
        'upcoming': upcoming,
        'total': len(task_list)
    }

@app.patch("/api/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    """Отметить задачу выполненной"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE tasks 
        SET status = 'completed' 
        WHERE id = %s
    """, (task_id,))
    
    if cur.rowcount > 0:
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Задача отмечена как выполненная"}
    else:
        cur.close()
        conn.close()
        return {"error": "Задача не найдена"}

@app.get("/api/subjects/{telegram_id}")
async def get_subjects_summary(telegram_id: int):
    """Получить сводку по предметам"""
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            subject,
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
            SUM(COALESCE(points, 0)) as total_points,
            MIN(deadline_end) as nearest_deadline
        FROM tasks 
        WHERE telegram_id = %s
        GROUP BY subject
        ORDER BY nearest_deadline ASC
    """, (telegram_id,))
    
    subjects = cur.fetchall()
    cur.close()
    conn.close()
    
    # Преобразуем кортежи в словари
    subject_list = []
    for subject in subjects:
        subject_dict = {
            'subject': subject[0],
            'total_tasks': subject[1],
            'completed': subject[2],
            'pending': subject[3],
            'total_points': subject[4],
            'nearest_deadline': subject[5].isoformat() if subject[5] else None
        }
        subject_list.append(subject_dict)
    
    return {'subjects': subject_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)