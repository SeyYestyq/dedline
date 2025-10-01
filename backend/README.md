# Deadline 2.0 Backend

Backend для приложения управления дедлайнами с интеграцией Telegram Bot.

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

1. Убедитесь, что PostgreSQL запущен
2. Создайте базу данных `tasks` в pgAdmin
3. Выполните SQL скрипт из `../sql/init.sql` для создания таблиц

### 3. Настройка переменных окружения

Создайте файл `.env` в папке `backend/`:

```env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql://postgres:postgres123@127.0.0.1:5432/tasks
WEB_APP_URL=https://your-app.vercel.app
```

### 4. Запуск сервера

```bash
python run.py
```

API будет доступен по адресу: http://localhost:8000
Документация API: http://localhost:8000/docs

## API Endpoints

### GET /api/tasks/{telegram_id}
Получить задачи пользователя с категоризацией по срочности.

### PATCH /api/tasks/{task_id}/complete
Отметить задачу как выполненную.

### GET /api/subjects/{telegram_id}
Получить статистику по предметам пользователя.

## Структура базы данных

Таблица `tasks`:
- `id` - уникальный идентификатор
- `telegram_id` - ID пользователя в Telegram
- `subject` - название предмета
- `task_type` - тип задания (КР, Тест, Доклад, и т.д.)
- `task_number` - номер задания
- `points` - количество баллов
- `deadline_start` - начало периода
- `deadline_end` - дедлайн
- `description` - описание
- `first_reminder` - дата первого напоминания
- `second_reminder` - дата второго напоминания
- `status` - статус (pending/completed)
- `created_at` - дата создания

## Тестирование

Для тестирования подключения к базе данных:

```bash
python load_data.py
```

Для тестирования API:

```bash
python -c "from main import app; from fastapi.testclient import TestClient; client = TestClient(app); print(client.get('/api/tasks/123456789').json())"
```
