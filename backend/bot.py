import asyncio
from datetime import date
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler
from database import get_db
from config import BOT_TOKEN, WEB_APP_URL

async def start(update, context):
    """Команда /start"""
    keyboard = [[
        InlineKeyboardButton(
            "📚 Открыть дедлайны", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    ]]
    
    await update.message.reply_text(
        "👋 Привет! Нажми кнопку ниже, чтобы открыть свои дедлайны:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def stats(update, context):
    """Команда /stats"""
    user_id = update.effective_user.id
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
        FROM tasks WHERE telegram_id = %s
    """, (user_id,))
    
    stats = cur.fetchone()
    cur.close()
    conn.close()
    
    await update.message.reply_text(
        f"📊 Статистика:\n\n"
        f"📚 Всего: {stats[0]}\n"
        f"✅ Выполнено: {stats[1]}\n"
        f"⏳ Осталось: {stats[2]}"
    )

async def check_reminders():
    """Проверка напоминаний ежедневно"""
    bot = Bot(token=BOT_TOKEN)
    
    while True:
        try:
            today = date.today()
            conn = get_db()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT DISTINCT telegram_id, subject, task_type, task_number, 
                       points, deadline_end
                FROM tasks 
                WHERE status = 'pending'
                AND (first_reminder = %s OR second_reminder = %s)
            """, (today, today))
            
            reminders = cur.fetchall()
            
            for task in reminders:
                days_left = (task[5] - today).days
                task_name = task[2]
                if task[3]:
                    task_name += f" {task[3]}"
                
                await bot.send_message(
                    chat_id=task[0],
                    text=f"🔔 Напоминание!\n\n"
                         f"📚 {task[1]}\n"
                         f"📝 {task_name}\n"
                         f"⏰ Дедлайн через {days_left} дн."
                )
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"Ошибка: {e}")
        
        await asyncio.sleep(86400)  # 24 часа

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    
    # Запуск напоминаний в фоне
    asyncio.create_task(check_reminders())
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()