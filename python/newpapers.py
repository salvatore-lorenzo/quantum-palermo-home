import json
import os
import sys
from pathlib import Path

import discord

intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

client = discord.Client(intents=intents)

# Replace with your specific Discord Channel ID (as an integer)
TARGET_CHANNEL_ID = 1351613136830074930

# How many past messages to print at startup
LAST_MESSAGES = 20

# Only messages posted by this bot are saved
ARXIV_BOT_NAME = "arxiv-bot"

# File where arxiv-bot messages are saved (one JSON object per line), next to this script
MESSAGES_FILE = Path(__file__).with_name("newpapers_messages.jsonl")

# File holding the bot token, next to this script (gitignored: the token must never be committed)
TOKEN_FILE = Path(__file__).with_name("discord_token.txt")


def load_saved_ids():
  # IDs of messages already in the file, so restarts don't save them twice
  if not MESSAGES_FILE.exists():
    return set()
  with MESSAGES_FILE.open(encoding="utf-8") as f:
    return {json.loads(line)["id"] for line in f if line.strip()}


saved_ids = load_saved_ids()


def save_message(m):
  # Keep only arxiv-bot posts, and skip the ones already in the file
  if m.author.name != ARXIV_BOT_NAME or m.id in saved_ids:
    return
  record = {
    "id": m.id,
    "date": m.created_at.astimezone().isoformat(timespec="seconds"),
    "author": str(m.author),
    "content": m.content,
    "embeds": [{"title": e.title, "url": e.url, "description": e.description} for e in m.embeds],
  }
  with MESSAGES_FILE.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
  saved_ids.add(m.id)


@client.event
async def on_ready():
  print(f"Logged in as {client.user}")

  # Print and save the last messages already in the target channel, oldest first
  try:
    channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
    messages = [m async for m in channel.history(limit=LAST_MESSAGES)]
    for m in reversed(messages):
      print(f"[{m.created_at.astimezone():%Y-%m-%d %H:%M}] {m.author}: {m.content}")
      # Bot/feed posts often carry the text in embeds rather than in content
      for e in m.embeds:
        print(f"    {e.title or ''} {e.url or ''}".rstrip())
      save_message(m)
  finally:
    await client.close()  # disconnect, so client.run() returns and the script ends, even after an error



@client.event
async def on_message(message):
  # Ignore messages sent by the bot itself
  if message.author == client.user:
    return

  # Check if the message is from the target channel
  if message.channel.id == TARGET_CHANNEL_ID:
    print(f"New message from {message.author}: {message.content}")
    save_message(message)

    # Put the code you want to run here
    # E.g., call a function, write to a file, or process data
    #mio_script_custom(message.content)


def mio_script_custom(contenuto):
  print(f"Eseguendo lo script con il testo: {contenuto}")


def load_token():
  # The DISCORD_BOT_TOKEN environment variable wins over the token file
  token = os.environ.get("DISCORD_BOT_TOKEN")
  if not token and TOKEN_FILE.exists():
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
  if not token:
    sys.exit(f"Discord bot token missing: set DISCORD_BOT_TOKEN or put it in {TOKEN_FILE}")
  return token


client.run(load_token())