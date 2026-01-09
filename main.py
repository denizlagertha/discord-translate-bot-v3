import os
import discord
from discord.ext import commands
from discord import app_commands
from deepl import Translator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPL_KEY = os.getenv("DEEPL_API_KEY")

translator = Translator(DEEPL_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild_lang = {}  # per-server language memory


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)


# /setlang
@bot.tree.command(name="setlang", description="Select your translation target language")
@app_commands.describe(language="Target language code (example: TR, EN, DE)")
async def setlang(interaction: discord.Interaction, language: str):
    guild_lang[interaction.guild_id] = language.upper()
    await interaction.response.send_message(
        f"✔ Translation language set to **{language.upper()}**",
        ephemeral=True
    )


# Context Menu: Translate
@bot.tree.context_menu(name="Translate Message")
async def translate_message(interaction: discord.Interaction, message: discord.Message):
    if interaction.guild_id not in guild_lang:
        await interaction.response.send_message(
            "⚠ No language set. Use **/setlang <code>** first.",
            ephemeral=True
        )
        return
    
    target = guild_lang[interaction.guild_id]

    try:
        result = translator.translate_text(message.content, target_lang=target)
        translated = result.text
    except Exception as e:
        await interaction.response.send_message(
            f"Translation failed: {e}",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"**Translated to {target}:**\n{translated}",
        ephemeral=True
    )


bot.run(TOKEN)
