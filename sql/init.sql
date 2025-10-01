-- Основная таблица с задачами
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    subject VARCHAR(255) NOT NULL,           -- Название предмета
    task_type VARCHAR(100) NOT NULL,         -- Тип: КР, Тест, Доклад, Рабочая тетрадь
    task_number VARCHAR(50),                 -- Номер: КР 1, КР 2, и т.д.
    points INTEGER,                          -- Количество баллов
    deadline_start DATE NOT NULL,            -- Начало периода
    deadline_end DATE NOT NULL,              -- Конец периода (дедлайн)
    description TEXT,                        -- Описание задания
    first_reminder DATE NOT NULL,            -- Дата первого напоминания
    second_reminder DATE NOT NULL,           -- Дата второго напоминания
    status VARCHAR(50) DEFAULT 'pending',    -- pending/completed
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для быстрого поиска
CREATE INDEX idx_tasks_user_deadline ON tasks(telegram_id, deadline_end);
CREATE INDEX idx_tasks_reminders ON tasks(first_reminder, second_reminder);
CREATE INDEX idx_tasks_status ON tasks(status);