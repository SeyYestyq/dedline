import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token_here')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres123@127.0.0.1:5432/tasks')
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://your-app.vercel.app')
