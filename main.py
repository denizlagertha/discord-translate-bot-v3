import os
import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

# Kullanıcıya özel hedef dil
user_lang = {}

# Slash komut: dil ayarla
@bot.tree.command(name="lang", description="Çeviri dilini ayarla (örnek: /lang tr)")
@app_commands.describe(code="Hedef dil kodu örn: tr, en, ar")
async def set_lang(interaction: discord.Interaction, code: str):
    user_lang[interaction.user.id] = code.lower()
    await interaction.response.send_message(
        f"✔ Çeviri dili `{code}` olarak ayarlandı.",
        ephemeral=True
    )

# Mesaj dinleyici
@bot.event
async def on_message(message):
    # Botları yok say
    if message.author.bot:
        return
    
    # Kendini çevirmesin
    if message.content.startswith("/") or message.content.startswith("!"):
        return

    for uid, lang in user_lang.items():
        # Sadece hedef dil belirleyen kullanıcıya buton koy
        if uid != message.author.id:
            view = TranslateView(message.content, lang)
            try:
                await message.channel.send(
                    content=f"🔤 **Çeviri için tıkla:**",
                    reference=message,
                    view=view,
                    silent=True
                )
            except:
                pass

class TranslateView(discord.ui.View):
    def __init__(self, text, lang):
        super().__init__(timeout=None)
        self.text = text
        self.lang = lang

    @discord.ui.button(label="Çeviriyi Göster", style=discord.ButtonStyle.primary)
    async def translate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        translated = translator.translate(self.text, dest=self.lang).text
        await interaction.response.send_message(
            f"🌍 **Çeviri:** {translated}",
            ephemeral=True
        )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} online!")

bot.run(TOKEN)
