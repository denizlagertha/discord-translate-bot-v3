import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# Sunucuya göre ayarlanmış diller
server_lang = {}

# ÇEVİRME FONKSİYONU
def translate(text, target):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    payload = {"from": "auto", "to": target, "text": text}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json().get("trans", "⚠️ Translation failed")

# Bot hazır
@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Bot ONLINE: {client.user}")

# 🌍 Dil Ayarlama Komutu
@client.tree.command(name="setlang", description="Set server translation language")
@app_commands.describe(code="Language code (en, tr, es, fr, de...)")
async def setlang(interaction: discord.Interaction, code: str):
    server_lang[interaction.guild_id] = code.lower()
    await interaction.response.send_message(f"🌐 Server language set to **{code}**!")

# 📌 Sağ tık menüsü
@client.tree.context_menu(name="Translate message")
async def translate_message(interaction: discord.Interaction, message: discord.Message):
    lang = server_lang.get(interaction.guild_id, "en")
    translated = translate(message.content, lang)
    await interaction.response.send_message(f"➡️ **{translated}**")

keep_alive()
client.run(TOKEN)
