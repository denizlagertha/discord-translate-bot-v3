import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
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
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=auto|{target}"
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        return data["responseData"]["translatedText"]
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
