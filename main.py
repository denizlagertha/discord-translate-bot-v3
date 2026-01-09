import os
import discord
from discord import app_commands
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# sunucuya göre dil tut
user_lang = {}

class TranslateButton(discord.ui.View):
    def __init__(self, original, target_lang):
        super().__init__(timeout=None)
        self.original = original
        self.target_lang = target_lang

    @discord.ui.button(label="Çevir ✨", style=discord.ButtonStyle.primary)
    async def translate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        translated = GoogleTranslator(source="auto", target=self.target_lang).translate(self.original)
        await interaction.response.send_message(
            f"**Çeviri ({self.target_lang}):** {translated}",
            ephemeral=True
        )

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash komutları senkron: {len(synced)}")
    except Exception as e:
        print(e)
    print(f"Giriş yapıldı: {bot.user}")

@bot.tree.command(name="lang", description="Çeviri dilini ayarla")
@app_commands.describe(code="ör: tr, en, fr, es")
async def set_lang(interaction: discord.Interaction, code: str):
    user_lang[interaction.user.id] = code.lower()
    await interaction.response.send_message(
        f"✔ Çeviri dili **{code}** olarak ayarlandı!",
        ephemeral=True
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for uid, lang in user_lang.items():
        if uid != message.author.id:  # kendi mesajını çevirme!
            try:
                view = TranslateButton(message.content, lang)
                await message.channel.send(
                    f"💬 **Yeni mesaj! Çevirmek ister misin?**",
                    view=view
                )
            except Exception as e:
                print("Hata:", e)
                pass

    await bot.process_commands(message)

bot.run(TOKEN)
