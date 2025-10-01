# -*- coding: utf-8 -*-
"""
Скрипт для запуска проекта Deadline 2.0
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Запуск Deadline 2.0 Backend...")
    print("📊 API будет доступен по адресу: http://localhost:8000")
    print("📚 Документация API: http://localhost:8000/docs")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
