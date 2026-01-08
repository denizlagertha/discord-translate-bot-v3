import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

# Kullanıcı -> hedef dil kayıtları
user_lang = {}

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.command()
async def lang(ctx, code=None):
    """
    !lang tr
    !lang en
    !lang ru
    """
    if code is None:
        await ctx.send("🌍 Dil seç:\nÖrnek: `!lang tr`")
        return

    user_lang[ctx.author.id] = code.lower()
    await ctx.send(f"✔️ Senin mesajların **{code.upper()}** diline çevrilecek.")

@bot.event
async def on_message(message):
    # Bot kendi mesajını görmezden gelir
    if message.author == bot.user:
        return

    # Kullanıcı bir dil ayarlamadıysa hiçbir şey yapma
    if message.author.id not in user_lang:
        await bot.process_commands(message)
        return

    target = user_lang[message.author.id]

    try:
        translated = GoogleTranslator(source='auto', target=target).translate(message.content)

        # Orijinal mesajın hemen altına görünür, embed değil
        if translated.lower() != message.content.lower():
            await message.channel.send(
                f"🗣️ {message.author.display_name} → **{target.upper()}**: {translated}",
                reference=message
            )
    except Exception as e:
        print("Çeviri hatası:", e)

    await bot.process_commands(message)

bot.run(TOKEN)
