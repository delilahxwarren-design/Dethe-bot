import discord
import random
import os
from discord.ext import tasks
from datetime import datetime

TOKEN = os.getenv("TOKEN")

KANAL_ID = 1501855557584162818

intents = discord.Intents.all()
client = discord.Client(intents=intents)

piosenki = [

    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
    "https://open.spotify.com/track/3LlAyCYU26dvFZBDUIMb7a",
    "https://open.spotify.com/track/1NtIMM4N0cFa1dNzN15chl",
    "https://open.spotify.com/track/62yJjFtgkhUrXktIoSjgP2",
    "https://open.spotify.com/track/213x4gsFDm04hSqIUkg88w",

    "https://open.spotify.com/track/2VxeLyX666F8uXCJ0dZF8B",
    "https://open.spotify.com/track/7rglLriMNBPAyuJOMGwi39",
    "https://open.spotify.com/track/6rLqjzGV5VMLDWEnuUqi8q",
    "https://open.spotify.com/track/5R8dQOPq8haW94K7mgERlO",

    "https://open.spotify.com/track/2qSkIjg1o9h3YT9RAgYN75",
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP",
    "https://open.spotify.com/track/1d7Ptw3qYcfpdLNL5REhtJ",

    "https://open.spotify.com/track/2takcwOaAZWiXQijPHIx7B",
    "https://open.spotify.com/track/0eGsygTp906u18L0Oimnem",
    "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P"
]

@client.event
async def on_ready():
    print(f"{client.user} online!")
    codzienna_piosenka.start()

@tasks.loop(minutes=1)
async def codzienna_piosenka():

    teraz = datetime.now()

    if teraz.hour == 20 and teraz.minute == 0:

        kanal = client.get_channel(KANAL_ID)

        if kanal:
            await kanal.send(
                f"🎶 Dzisiejsza piosenka od Dethe:\n{random.choice(piosenki)}"
            )

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "!ping":
        await message.channel.send("🏓 Pong!")

    if message.content == "!piosenka":
        await message.channel.send(
            f"🎵 Dethe poleca:\n{random.choice(piosenki)}"
        )

client.run(TOKEN)
