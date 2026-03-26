FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy only pyproject.toml first
COPY bot/pyproject.toml ./

# Install dependencies (without lock file)
RUN uv sync

# Copy bot code
COPY bot/ .

# Run bot
CMD ["uv", "run", "bot.py"]
