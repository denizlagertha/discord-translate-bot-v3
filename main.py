import os
import discord
from discord.ext import commands
from googletrans import Translator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.command()
async def translate(ctx, *, text):
    """
    Örnek:
    !translate hello
    """
    try:
        translated = translator.translate(text, dest="tr")
        await ctx.send(f"Çeviri 🇬🇧 ➡️ 🇹🇷:\n**{translated.text}**")
    except Exception as e:
        await ctx.send("❌ Hata oluştu.")
        print(e)

@bot.event
async def on_message(message):
    # Botun kendi mesajlarını görmezden gelmesi
    if message.author == bot.user:
        return

    # Otomatik çeviri örneği
    try:
        translated = translator.translate(message.content, dest="tr")
        if translated.text.lower() != message.content.lower():
            await message.channel.send(f"🌍 **{message.author.name}:** {translated.text}")
    except:
        pass

    await bot.process_commands(message)

bot.run(TOKEN)
