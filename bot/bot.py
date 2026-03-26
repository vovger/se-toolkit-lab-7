#!/usr/bin/env python
import sys
import argparse
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import handlers
from config import settings

def get_response(command: str, args: list[str]) -> str:
    """Route command to handler and return text response."""
    cmd = command.lstrip("/").lower()
    if cmd == "start":
        return handlers.start()
    if cmd == "help":
        return handlers.help()
    if cmd == "health":
        return handlers.health()
    if cmd == "labs":
        return handlers.labs()
    if cmd == "scores":
        lab = args[0] if args else ""
        return handlers.scores(lab)
    return "Unknown command. Try /help."

def test_mode(command: str):
    """Print handler output for given command."""
    parts = command.strip().split()
    if not parts:
        print("No command provided")
        sys.exit(1)
    cmd = parts[0]
    args = parts[1:]
    
    # Check if it's a slash command
    if cmd.startswith("/"):
        output = get_response(cmd, args)
    else:
        # Natural language - use LLM router
        output = handlers.route_to_llm(command)
    
    print(output)
    sys.exit(0)

def run_bot():
    """Run Telegram bot in normal mode."""
    if not settings.bot_token:
        print("Error: BOT_TOKEN not set. Please configure .env.bot.secret")
        sys.exit(1)
    
    app = Application.builder().token(settings.bot_token).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handlers.start())))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handlers.help())))
    app.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(handlers.health())))
    app.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(handlers.labs())))
    app.add_handler(CommandHandler("scores", lambda u, c: u.message.reply_text(
        handlers.scores(c.args[0] if c.args else "")
    )))
    
    # Message handler for natural language
    async def handle_message(update, context):
        user_message = update.message.text
        response = handlers.route_to_llm(user_message)
        await update.message.reply_text(response)
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Keyboard buttons
    keyboard = [
        [KeyboardButton("/start"), KeyboardButton("/help")],
        [KeyboardButton("/health"), KeyboardButton("/labs")],
        [KeyboardButton("/scores lab-01"), KeyboardButton("/scores lab-04")],
        [KeyboardButton("Which lab has the lowest pass rate?"), KeyboardButton("Show me top 5 students in lab 04")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    async def start_with_keyboard(update, context):
        await update.message.reply_text(
            handlers.start(),
            reply_markup=reply_markup
        )
    
    app.add_handler(CommandHandler("start", start_with_keyboard))
    
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Run in test mode with command", nargs="?", const="", default=None)
    args = parser.parse_args()
    if args.test is not None:
        test_mode(args.test if args.test else "/start")
    else:
        run_bot()
