import discord
import random
import os
import asyncio
from discord.ext import tasks
from datetime import datetime
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

KANAL_ID = 1501855557584162818
ROLA_BUTELKA = "BUTELKA"

# KEEP ALIVE 💜
app = Flask('')

@app.route('/')
def home():
    return "Dethe żyje 💜"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

utwory = [

    # Imagine Dragons
    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
    "https://open.spotify.com/track/3LlAyCYU26dvFZBDUIMb7a",
    "https://open.spotify.com/track/1NtIMM4N0cFa1dNzN15chl",
    "https://open.spotify.com/track/62yJjFtgkhUrXktIoSjgP2",

    # Lady Gaga
    "https://open.spotify.com/track/6rLqjzGV5VMLDWEnuUqi8q",
    "https://open.spotify.com/track/5R8dQOPq8haW94K7mgERlO",
    "https://open.spotify.com/track/0SiywuOBRcynK0uKGWdCnn",

    # Sabrina Carpenter
    "https://open.spotify.com/track/2qSkIjg1o9h3YT9RAgYN75",
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP",

    # Rock
    "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P",
    "https://open.spotify.com/track/58ge6dfP91o9oXMzq3XkIS",
    "https://open.spotify.com/track/2nLtzopw4rPReszdYBJU6h"
]

@client.event
async def on_ready():
    print(f"{client.user} online!")
    codzienny_utwor.start()

@tasks.loop(minutes=1)
async def codzienny_utwor():

    teraz = datetime.now()

    if teraz.hour == 21 and 30 <= teraz.minute <= 32:

        kanal = client.get_channel(KANAL_ID)

        if kanal:
            await kanal.send(
                f"🎶 Dzisiejszy utwór od Dethe:\n{random.choice(utwory)}"
            )

            await asyncio.sleep(180)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # PING
    if message.content == "!ping":
        await message.channel.send("🏓 Pong!")

    # LOSOWY UTWÓR
    if message.content == "!utwór":
        await message.channel.send(
            f"🎵 Dethe poleca:\n{random.choice(utwory)}"
        )

    # BUTELKA
    if message.content == "!butelka":

        members = [
            member for member in message.channel.members
            if not member.bot and any(role.name == ROLA_BUTELKA for role in member.roles)
        ]

        if len(members) < 2:
            await message.channel.send(
                "❌ Za mało osób z rolą BUTELKA!"
            )
            return

        osoba = random.choice(members)

        await message.channel.send("🍾 Dethe kręci butelką...")
        await asyncio.sleep(1)

        await message.channel.send("3️⃣")
        await asyncio.sleep(1)

        await message.channel.send("2️⃣")
        await asyncio.sleep(1)

        await message.channel.send("1️⃣")
        await asyncio.sleep(1)

        wybor = random.choice([
            "❓ PYTANIE",
            "🔥 WYZWANIE"
        ])

        await message.channel.send(
            f"🍾 Butelka wskazuje: {osoba.mention}\n\n{wybor}"
        )

client.run(TOKEN)
