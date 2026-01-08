import os
import discord
from discord.ext import commands
from googletrans import Translator

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f"Bot çalıştı: {bot.user}")

@bot.command()
async def tr(ctx, *, text):
    ceviri = translator.translate(text, dest='tr')
    await ctx.send(ceviri.text)

@bot.command()
async def en(ctx, *, text):
    ceviri = translator.translate(text, dest='en')
    await ctx.send(ceviri.text)

bot.run(TOKEN)
