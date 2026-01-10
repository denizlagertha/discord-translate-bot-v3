import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

LANG = {}  # Server language

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# TÜM DİLLER
language_options = {
    "English": "en", "Turkish": "tr", "German": "de", "Spanish": "es",
    "French": "fr", "Russian": "ru", "Arabic": "ar", "Hindi": "hi",
    "Japanese": "ja", "Korean": "ko", "Chinese (Simplified)": "zh-CN",
    "Vietnamese": "vi", "Portuguese": "pt", "Italian": "it",
    "Dutch": "nl", "Polish": "pl", "Ukrainian": "uk", "Romanian": "ro",
    "Hungarian": "hu", "Swedish": "sv",
    "Norwegian": "no", "Danish": "da", "Finnish": "fi", "Thai": "th",
    "Malay": "ms", "Indonesian": "id"
}

def translate(text, target):
    url = (
        "https://translate.googleapis.com/translate_a/single"
        f"?client=gtx&sl=auto&tl={target}&dt=t&q={requests.utils.quote(text)}"
    )
    r = requests.get(url)
    try:
        return r.json()[0][0][0]
    except:
        return "⚠️ Translation failed"

@client.tree.command(name="setlang", description="Set server language")
@app_commands.choices(lang=[
    app_commands.Choice(name=k, value=v) for k, v in language_options.items()
])
async def setlang(interaction: discord.Interaction, lang: app_commands.Choice[str]):
    LANG[interaction.guild_id] = lang.value
    await interaction.response.send_message(
        f"🌍 Language set to **{lang.name}**!", ephemeral=True
    )

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
client.run(os.getenv("TOKEN"))
