import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Hedef dilleri kullanıcı bazında tutuyoruz
user_lang = {}

@bot.event
async def on_ready():
    print(f"Bot aktif ✔ Giriş yaptı: {bot.user}")

@bot.command()
async def setlang(ctx, lang):
    """
    Kullanıcı kendi çeviri dilini seçer ör:
    !setlang tr
    !setlang ru
    !setlang en
    """
    user_lang[ctx.author.id] = lang.lower()
    await ctx.reply(f"🌍 Çeviri dilin kaydedildi: **{lang}**", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Kullanıcı kayıtlı değilse işlem yapma
    for uid, lang in user_lang.items():
        # Sadece mesaj sahibi olmayanlar için çevir
        if message.author.id != uid:
            try:
                translated = GoogleTranslator(source='auto', target=lang).translate(message.content)
                if translated.lower() != message.content.lower():
                    user = await bot.fetch_user(uid)
                    await user.send(f"💬 **{message.author.name} dedi ki:**\n{message.content}\n\n🔁 Çeviri (**{lang}**):\n**{translated}**")
            except Exception:
                pass

    await bot.process_commands(message)
