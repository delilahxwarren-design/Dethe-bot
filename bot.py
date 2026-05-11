import discord
import random
import os
import asyncio

from discord.ext import tasks
from datetime import datetime

TOKEN = os.getenv("TOKEN")

# =========================================
# KONFIG
# =========================================

KANAL_SPOTIFY = 1501855557584162818

ROLA_BUTELKA = "BUTELKA"

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# SPOTIFY
# =========================================

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

# =========================================
# READY
# =========================================

@client.event
async def on_ready():

    print(f"{client.user} online!")

    if not codzienny_utwor.is_running():
        codzienny_utwor.start()

# =========================================
# CODZIENNY UTWÓR
# =========================================

@tasks.loop(minutes=1)
async def codzienny_utwor():

    teraz = datetime.now()

    if teraz.hour == 21 and 30 <= teraz.minute <= 32:

        kanal = client.get_channel(
            KANAL_SPOTIFY
        )

        if kanal:

            await kanal.send(
                f"🎶 Dzisiejszy utwór od Dethe:\n"
                f"{random.choice(utwory)}"
            )

            # anty duplikat
            await asyncio.sleep(180)

# =========================================
# MESSAGE
# =========================================

@client.event
async def on_message(message):

    if message.author.bot:
        return

    # =====================================
    # PING
    # =====================================

    if message.content.lower() == "!ping":

        await message.channel.send(
            "🏓 Pong!"
        )

        return

    # =====================================
    # UTWÓR
    # =====================================

    if message.content.lower() in [
        "!utwór",
        "!utwor"
    ]:

        await message.channel.send(
            f"🎵 Dethe poleca:\n"
            f"{random.choice(utwory)}"
        )

        return

    # =====================================
    # BUTELKA
    # =====================================

    if message.content.lower() == "!butelka":

        members = [
            member for member in message.guild.members
            if not member.bot
        ]

        if len(members) < 2:

            await message.channel.send(
                "❌ Za mało osób."
            )

            return

        osoba1 = random.choice(members)

        osoba2 = random.choice(members)

        while osoba2 == osoba1:
            osoba2 = random.choice(members)

        await message.channel.send(
            f"🍾 Butelka wskazuje:\n\n"
            f"👉 {osoba1.mention}\n"
            f"❤️ {osoba2.mention}"
        )

        return

client.run(TOKEN)
