import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.command()
async def translate(ctx, *, text):
    """
    Kullanım:
    !translate hello
    """
    try:
        translated = GoogleTranslator(source='auto', target='tr').translate(text)
        await ctx.send(f"Çeviri 🌍 ➡️ 🇹🇷:\n**{translated}**")
    except Exception as e:
        await ctx.send("❌ Hata oluştu.")
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        translated = GoogleTranslator(source='auto', target='tr').translate(message.content)
        if translated.lower() != message.content.lower():
            await message.channel.send(f"🌍 **{message.author.name}:** {translated}")
    except:
        pass

    await bot.process_commands(message)

bot.run(TOKEN)
