Discord Translate Bot
This is a simple Discord bot that translates any selected message into a chosen language.
Users can set the server language, and then right‑click any message to translate it.

Features
Slash command /setlang to set the translation target language

Right‑click message -> “Translate message”

Keeps language setting per server

Hosted for free on Render

Requirements
You need:

A Discord bot token

A RapidAPI key (Deep Translate)

A computer with Python 3.10 or higher

A GitHub account (optional but recommended)

A Render.com account for hosting

How to Install Locally
1. Clone or download this repository
git clone https://github.com/<your-username>/<repository-name>
Or click Download ZIP, extract it anywhere.

2. Open a terminal inside the project folder
3. Install required libraries
pip install -r requirements.txt
4. Create an environment file
Create a file named .env or set environment variables manually.

TOKEN=your_discord_bot_token
RAPIDAPI_KEY=your_rapidapi_key
5. Run the bot
python main.py
Getting API Keys
Discord Bot Token
Go to 

Create a New Application

Go to Bot tab → Add Bot

Under TOKEN click Reset Token and copy it

Turn on the following intents:

Message Content Intent

Add the Bot to Your Server
Developer Portal → OAuth2 → URL Generator

Select:

applications.commands

bot

Bot Permissions:

Read Messages/View Channels

Send Messages

Copy the URL, paste into a browser, and invite the bot

RapidAPI Key (Deep Translate)
Go to 

Search: Deep Translate

Subscribe to the free plan

Copy the x-rapidapi-key

Put that key in your .env

How to Deploy on Render (Free Hosting)
1. Create a GitHub repository
Upload all your project files there.

2. Go to 
Create an account

Click New Web Service

Choose your GitHub repository

3. Configure settings
Runtime: Python

Build Command:

pip install -r requirements.txt
Start Command:

python main.py
4. Add Environment Variables in Render
Under “Environment”

TOKEN=your_discord_bot_token
RAPIDAPI_KEY=your_rapidapi_key
5. Deploy
Click Deploy.
Render will build automatically and run your bot 24/7.

Usage
Set server language
Use slash command:
/setlang

Choose one of the available options.

Translate messages
Right‑click any message
Apps → Translate message
You will receive the translation privately.

Supported Languages
You can add or remove languages, but the default list includes:

English

Turkish

French

Spanish

German

Russian
(and more if added manually)

Troubleshooting
Bot is offline

Check TOKEN is correct

Ensure bot is invited to the server

Translation failed

Check RapidAPI key usage

Free plan has limits

Slash commands not appearing

Wait a minute for Discord to sync

Make sure bot has applications.commands permission

