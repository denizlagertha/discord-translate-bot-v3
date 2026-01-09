import os
import requests
import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

TARGET_LANG = "tr"

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(e)

# Slash command to set target language
@bot.tree.command(name="setlang", description="Set your translate target language")
@app_commands.describe(code="Language code, e.g. tr, en, ar, de, fr")
async def setlang(interaction: discord.Interaction, code: str):
    global TARGET_LANG
    TARGET_LANG = code.lower()
    await interaction.response.send_message(
        f"Language set to **{TARGET_LANG}**",
        ephemeral=True
    )

# Message context menu: translate
@bot.tree.context_menu(name="Translate")
async def translate_message(interaction: discord.Interaction, message: discord.Message):
    if message.author.id == bot.user.id:
        return await interaction.response.send_message(
            "Can't translate bot messages.",
            ephemeral=True
        )

    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {
        "q": message.content,
        "source": "auto",
        "target": TARGET_LANG
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        translation = data["data"]["translations"]["translatedText"]

        await interaction.response.send_message(
            f"**Translation ({TARGET_LANG}):**\n{translation}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            "❌ Translation failed.",
            ephemeral=True
        )
        print(e)


bot.run(os.getenv("DISCORD_TOKEN"))
