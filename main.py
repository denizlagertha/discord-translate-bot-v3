import os
import discord
from discord import app_commands
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

user_langs = {}  # user_id : target_language

@tree.command(name="lang", description="Hedef dili ayarla (örnek: /lang tr)")
async def set_lang(interaction: discord.Interaction, dil: str):
    user_langs[interaction.user.id] = dil.lower()
    await interaction.response.send_message(f"✔ Çeviri dili **{dil}** olarak ayarlandı!", ephemeral=True)

@tree.command(name="stop", description="Otomatik çeviriyi kapat")
async def stop_lang(interaction: discord.Interaction):
    user_langs.pop(interaction.user.id, None)
    await interaction.response.send_message("❌ Otomatik çeviri kapatıldı!", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for uid, lang in user_langs.items():
        # Başkalarının mesajını çevir (mesaj sahibine göndermiyoruz)
        if uid != message.author.id:
            try:
                text = GoogleTranslator(source="auto", target=lang).translate(message.content)
                user = await bot.fetch_user(uid)
                # Ephemeral olmadığı için DM yerine sessiz mention simülasyonu
                await user.send(f"💬 **{message.author.display_name}:** {text}")
            except:
                pass

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot giriş yaptı: {bot.user}")

bot.run(TOKEN)
