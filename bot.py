import discord
import random

TOKEN = "TU_TOKEN"

intents = discord.Intents.all()

client = discord.Client(intents=intents)

piosenki = [
    "🎵 Linkin Park - Numb",
    "🎵 Eminem - Lose Yourself",
    "🎵 Arctic Monkeys - 505"
]

@client.event
async def on_ready():
    print(f"{client.user} online!")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "!ping":
        await message.channel.send("🏓 Pong!")

    if message.content == "!piosenka":
        await message.channel.send(random.choice(piosenki))

client.run(TOKEN)
