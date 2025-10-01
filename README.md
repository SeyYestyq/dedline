# Telegram Mini App - Дедлайны

Telegram Mini App для управления дедлайнами без регистрации.

## 🛠️ Технологический стек

**Backend:**
- Python 3.10+
- FastAPI
- PostgreSQL
- python-telegram-bot

**Frontend:**
- React 18
- Vite
- Telegram WebApp SDK

## 📦 Установка и запуск

### 1. Настройка базы данных

1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE tasks;
```

3. Выполните схему:
```bash
psql -d tasks -f sql/init.sql
```

### 2. Backend

1. Перейдите в папку backend:
```bash
cd backend
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения в `config.py`:
```python
BOT_TOKEN = 'your_bot_token_here'
DATABASE_URL = 'postgresql://postgres:postgres123@127.0.0.1:5432/tasks'
WEB_APP_URL = 'https://your-app.vercel.app'
```

5. Загрузите тестовые данные:
```bash
python load_tasks.py
```

6. **Запустите API сервер:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

7. В отдельном терминале запустите бота:
```bash
python bot.py
```

### 3. Frontend

1. Перейдите в папку frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. **Запустите dev сервер:**
```bash
npm run dev
```

## 🚀 Быстрый запуск

### Команды для запуска проекта:

**Терминал 1 - Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Терминал 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Откройте в браузере:** http://localhost:5173

### Проверка работы:

- **Backend API:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173

## 🤖 Настройка Telegram бота

1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Укажите имя бота
4. Получите токен и вставьте в `config.py`
5. Настройте команды:
```
start - Открыть приложение с дедлайнами
stats - Показать статистику
```

## 🚀 Деплой

### Backend на Railway
1. Зарегистрируйтесь на railway.app
2. Создайте новый проект
3. Добавьте PostgreSQL из Marketplace
4. Деплой backend:
```bash
cd backend
railway login
railway init
railway up
```

### Frontend на Vercel
1. Установите Vercel CLI:
```bash
npm install -g vercel
```

2. Деплой:
```bash
cd frontend
vercel login
vercel
```

## 📱 Использование

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Нажмите кнопку "Открыть дедлайны"
4. Приложение откроется внутри Telegram

## ✨ Функции

- ✅ Без регистрации - Telegram ID используется автоматически
- ✅ Автоматическая категоризация - задачи делятся по срочности
- ✅ Напоминания в боте - уведомления за 15 и 5 дней
- ✅ Два вида отображения - по задачам и по предметам
- ✅ Прогресс по предметам - визуализация выполнения
- ✅ Бесплатный хостинг - Railway + Vercel
