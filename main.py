import os
import discord
from discord.ext import commands
from discord import app_commands
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Sunucu dilini kaydetmek için hafif bellek
server_lang = {}  # server_id -> lang code

### RapidAPI çeviri ###
def translate_text(text, target):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "google-translate1.p.rapidapi.com",
        "content-type": "application/x-www-form-urlencoded"
    }

    data = {
        "q": text,
        "target": target
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        result = response.json()

        if "data" in result and "translations" in result["data"]:
            return result["data"]["translations"][0]["translatedText"]
        return None
    except:
        return None

### Slash komut: dil ayarla ###
@bot.tree.command(name="langset", description="Set your server's translation language")
@app_commands.describe(lang="Target language code. Example: tr, en, es, de")
async def langset(interaction: discord.Interaction, lang: str):
    server_lang[interaction.guild.id] = lang.lower()
    await interaction.response.send_message(
        f"✔ Translation language set to **{lang}**",
        ephemeral=True
    )

### Mesaj sağ tık çeviri ###
@bot.tree.context_menu(name="Translate (ephemeral)")
async def translate_context(interaction: discord.Interaction, message: discord.Message):

    # Dil seçilmemişse varsayılan TR
    target = server_lang.get(interaction.guild.id, "tr")

    translated = translate_text(message.content, target)

    if not translated:
        await interaction.response.send_message(
            "❌ Translation failed.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"**Translated → {target}:**\n{translated}",
        ephemeral=True
    )

### Bot açılınca senkron ###
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Ready: {bot.user}")

bot.run(TOKEN)
