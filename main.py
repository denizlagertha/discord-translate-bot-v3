import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
import json

TOKEN = os.getenv("DISCORD_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sunucuya özel dil seçimi
server_lang = {}

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

# Slash komut: Çeviri dilini ayarla
@bot.tree.command(name="setlang", description="Set your translation language")
@app_commands.describe(lang="Language code (example: en, tr, fr, es)")
async def setlang(interaction: discord.Interaction, lang: str):
    server_lang[interaction.guild_id] = lang.lower()
    await interaction.response.send_message(
        f"Translation language set to: **{lang.lower()}**",
        ephemeral=True
    )

# Sağ tık çeviri menüsü
@bot.tree.context_menu(name="Translate")
async def translate(interaction: discord.Interaction, message: discord.Message):

    # Kendi mesajını çevirtmesin
    if message.author.id == interaction.user.id:
        return await interaction.response.send_message(
            "You can't translate your own message.",
            ephemeral=True
        )

    # Sunucu dili belirlenmemişse
    lang = server_lang.get(interaction.guild_id, "en")

    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

    payload = json.dumps({
        "q": message.content,
        "source": "auto",
        "target": lang
    })

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        translated = data["data"]["translations"]["translatedText"]

        await interaction.response.send_message(
            f"> {translated}",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            "Translation failed.",
            ephemeral=True
        )

bot.run(TOKEN)
