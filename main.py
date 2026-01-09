import os
import discord
import requests
from discord.ext import commands
from discord import app_commands

# -------- KEEP ALIVE (Fake Web Server) ----------
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------------

TOKEN = os.getenv("TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Sunucuya göre dil saklama
server_lang = {}

# Dil seçme komutu
@client.tree.command(name="setlang", description="Set server translation language")
@app_commands.describe(language="Target language code (en, tr, es, de, fr etc)")
async def setlang(interaction: discord.Interaction, language: str):
    server_lang[interaction.guild_id] = language
    await interaction.response.send_message(
        f"Translation language set to: **{language}**",
        ephemeral=True
    )

# Sağ tık çeviri
@client.tree.context_menu(name="Translate")
async def translate(interaction: discord.Interaction, message: discord.Message):
    lang = server_lang.get(interaction.guild_id, "en")

    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    payload = {"from": "auto", "to": lang, "text": message.content}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        result = response.json()

        translated = result.get("trans", None)

        if not translated:
            raise Exception("No translation returned")

        await interaction.response.send_message(
            f"**Translated ({lang}):**\n{translated}",
            ephemeral=True
        )

    except Exception:
        await interaction.response.send_message(
            "Translation failed.",
            ephemeral=True
        )

@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is online!")

# Start fake web server, then bot
keep_alive()
client.run(TOKEN)
