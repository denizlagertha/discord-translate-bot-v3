import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcı -> Hedef Dil sözlüğü
user_lang = {}

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.command()
async def lang(ctx, language):
    """
    Örnek:
    !lang tr
    !lang ru
    !lang vi
    """
    user_lang[ctx.author.id] = language.lower()
    await ctx.send(f"🌍 Dil ayarlandı: **{language}**")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Kullanıcının ayarladığı dil var mı?
    lang = user_lang.get(message.author.id)
    if lang:
        try:
            translated = GoogleTranslator(target=lang).translate(message.content)
            if translated.lower() != message.content.lower():
                await message.channel.send(
                    f"🔁 **{message.author.name}** → {lang}:\n{translated}"
                )
        except:
            pass

    await bot.process_commands(message)

bot.run(TOKEN)
