# Development Plan for Telegram Bot

## Architecture
The bot will follow a testable handler architecture:
- `bot.py` – entry point; handles Telegram polling and `--test` mode.
- `handlers/` – command handlers that receive parsed arguments and return plain text.
- `services/` – clients for LMS API and LLM API.
- `config.py` – load environment variables with defaults.

## Commands Implementation
- `/start` → welcome message.
- `/help` → list of commands.
- `/health` → check backend status (call `GET /health`).
- `/labs` → list available labs (call `GET /items`).
- `/scores <lab>` → get scores for a lab (parse from items).
- For Task 3, a catch-all handler will use LLM to route intents.

## Integration with Backend
Use `httpx` to call LMS API with `api-key` header. Base URL and key come from `.env.bot.secret`.

## Integration with LLM
For Task 3, we'll implement intent routing by sending user input to Qwen Code API with a prompt asking to classify the intent and extract parameters.

## Testing & Deployment
- Test mode: `uv run bot.py --test "/command"` prints output.
- On VM: run with `nohup` and log to file.
- Autochecker will test via `--test` mode.
