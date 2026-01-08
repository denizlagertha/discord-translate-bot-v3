import os
import discord
from discord.ext import commands
from discord import app_commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# User language preferences {user_id: lang}
user_lang = {}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)

# /lang set your language
@bot.tree.command(name="lang", description="Set your translation target language")
@app_commands.describe(language="Language code like en, tr, es, ru, ar, etc")
async def setlang(interaction: discord.Interaction, language: str):
    user_lang[interaction.user.id] = language.lower()
    await interaction.response.send_message(
        f"Your translation language is now: **{language}**",
        ephemeral=True  # only user sees
    )

@bot.event
async def on_message(message):
    # ignore bots
    if message.author.bot:
        return

    # ignore if user has no language set
    if message.author.id not in user_lang:
        return

    target_lang = user_lang[message.author.id]

    # do NOT translate user's own messages
    # only translate others
    async for msg in message.channel.history(limit=5):
        pass

    # Find messages from others after user wrote something
    if message.author == message.author:
        await bot.process_commands(message)
        return

    try:
        translation = GoogleTranslator(source="auto", target=target_lang).translate(
            message.content
        )

        # Send ONLY visible to the user who enabled translation
        await message.channel.send(
            f"🔍 **Translated for {message.author.display_name}:**\n> {translation}",
            delete_after=15
        )

    except Exception as e:
        print("Translation error:", e)

    await bot.process_commands(message)
