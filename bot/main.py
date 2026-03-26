import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv('.env.bot.secret')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
LMS_API_KEY = os.getenv("LMS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для лабораторной работы №7.\n\n"
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - список команд\n"
        "/status - проверить статус API"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📚 Команды бота:\n\n"
        "/start - показать приветствие\n"
        "/help - показать эту справку\n"
        "/status - проверить подключение к LMS API\n\n"
        "Подробнее в документации лабораторной работы."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка статуса API"""
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{LMS_API_BASE_URL}/health",
                timeout=5
            )
            if response.status_code == 200:
                await update.message.reply_text("✅ LMS API работает нормально")
            else:
                await update.message.reply_text(f"⚠️ API вернул статус: {response.status_code}")
    except httpx.TimeoutException:
        await update.message.reply_text("❌ Таймаут подключения к API. Убедитесь, что сервер запущен.")
    except httpx.ConnectError:
        await update.message.reply_text(f"❌ Не удалось подключиться к {LMS_API_BASE_URL}")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
        print("Убедитесь, что файл .env.bot.secret настроен правильно")
        return

    print(f"🤖 Запуск бота...")
    print(f"📡 API URL: {LMS_API_BASE_URL}")
    
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    
    # Запускаем бота
    print("✅ Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
