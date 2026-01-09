import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

LANG = {}  # Server language

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Language Codes
language_options = {
    "English": "en",
    "Turkish": "tr",
    "German": "de",
    "Spanish": "es",
    "French": "fr",
    "Russian": "ru"
}

def translate(text, target):
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {"text": text, "target_language": target}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "deep-translate1.p.rapidapi.com"
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == 200:
        return r.json()["data"]["translations"]["translatedText"]
    else:
        return "translation failed"


@client.tree.command(name="setlang", description="Set server language")
@app_commands.choices(lang=[
    app_commands.Choice(name=k, value=v) for k, v in language_options.items()
])
async def setlang(interaction: discord.Interaction, lang: app_commands.Choice[str]):
    LANG[interaction.guild_id] = lang.value
    await interaction.response.send_message(f"🌍 Language set to **{lang.name}**!", ephemeral=True)

@client.tree.context_menu(name="Translate message")
async def translate_context(interaction: discord.Interaction, message: discord.Message):
    target = LANG.get(interaction.guild_id, "en")
    translated = translate(message.content, target)
    await interaction.response.send_message(f"🔤 **{translated}**", ephemeral=True)


@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is online!")

keep_alive()
client.run(TOKEN)
