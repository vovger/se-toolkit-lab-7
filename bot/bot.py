#!/usr/bin/env python
import sys
import argparse
from telegram.ext import Application, CommandHandler
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
    output = get_response(cmd, args)
    print(output)
    sys.exit(0)

def run_bot():
    """Run Telegram bot in normal mode."""
    if not settings.bot_token:
        print("Error: BOT_TOKEN not set. Please configure .env.bot.secret")
        sys.exit(1)
    app = Application.builder().token(settings.bot_token).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handlers.start())))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handlers.help())))
    app.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(handlers.health())))
    app.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(handlers.labs())))
    app.add_handler(CommandHandler("scores", lambda u, c: u.message.reply_text(
        handlers.scores(c.args[0] if c.args else "")
    )))
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
