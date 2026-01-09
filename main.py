import os
import discord
from discord.ext import commands
from discord import app_commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# user_id -> {'lang': 'xx', 'thread': thread_id}
user_settings = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="lang", description="Set your translation language")
async def set_lang(interaction: discord.Interaction, language: str):
    await interaction.response.defer(ephemeral=True)

    member = interaction.user

    # Create new private thread if needed
    thread = None
    if member.id in user_settings and user_settings[member.id]["thread"]:
        thread = interaction.channel.get_thread(user_settings[member.id]["thread"])

    if thread is None:
        try:
            thread = await interaction.channel.create_thread(
                name=f"{member.display_name}-translations",
                type=discord.ChannelType.private_thread
            )
        except discord.Forbidden:
            await interaction.followup.send("Botun thread açma izni yok!", ephemeral=True)
            return
        except Exception as e:
            await interaction.followup.send(f"Hata: {e}", ephemeral=True)
            return

    user_settings[member.id] = {"lang": language.lower(), "thread": thread.id}

    await interaction.followup.send(
        f"✔ Çeviri dili **{language}** olarak ayarlandı.\n"
        "🔒 Tüm çeviriler gizli threadine gönderilecek!",
        ephemeral=True
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Process slash commands
    await bot.process_commands(message)

    for user_id, info in user_settings.items():
        # Skip if author = user (kendi mesajını çevirme)
        if message.author.id == user_id:
            continue

        lang = info["lang"]
        thread_id = info["thread"]
        thread = message.channel.get_thread(thread_id)

        if not thread:
            continue

        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(message.content)
            await thread.send(f"💬 **{message.author.display_name}**:\n{translated}")
        except Exception as e:
            print("Translation error:", e)

bot.run(TOKEN)
