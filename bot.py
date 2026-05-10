import discord
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

piosenki = [

    # Imagine Dragons
    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
    "https://open.spotify.com/track/3LlAyCYU26dvFZBDUIMb7a",
    "https://open.spotify.com/track/1NtIMM4N0cFa1dNzN15chl",
    "https://open.spotify.com/track/62yJjFtgkhUrXktIoSjgP2",
    "https://open.spotify.com/track/213x4gsFDm04hSqIUkg88w",
    "https://open.spotify.com/track/5qaEfEh1AtSdrdrByCP7qR",
    "https://open.spotify.com/track/6Qn5zhYkTa37e91HC1D7lb",
    "https://open.spotify.com/track/6hPkbAV3ZXpGZBGUvL6jVM",
    "https://open.spotify.com/track/2U0Z1Q82FTnKqbluvlX7Iq",
    "https://open.spotify.com/track/7MXVkk9YMctZqd1Srtv4MB",

    # Lady Gaga
    "https://open.spotify.com/track/2VxeLyX666F8uXCJ0dZF8B",
    "https://open.spotify.com/track/7rglLriMNBPAyuJOMGwi39",
    "https://open.spotify.com/track/6rLqjzGV5VMLDWEnuUqi8q",
    "https://open.spotify.com/track/5R8dQOPq8haW94K7mgERlO",
    "https://open.spotify.com/track/0SiywuOBRcynK0uKGWdCnn",
    "https://open.spotify.com/track/4XNrMwGx1SqP01sqkGTDmo",
    "https://open.spotify.com/track/6uNdeba8z3oM8D5nYTYT23",
    "https://open.spotify.com/track/1HHeOs6zRdF8s9eF0AA1oN",
    "https://open.spotify.com/track/6M9fJXoQSN1cOYxen5Jf8b",
    "https://open.spotify.com/track/2rbDhOo9Fh61Bbu23T2qCk",

    # Sabrina Carpenter
    "https://open.spotify.com/track/2qSkIjg1o9h3YT9RAgYN75",
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP",
    "https://open.spotify.com/track/1d7Ptw3qYcfpdLNL5REhtJ",
    "https://open.spotify.com/track/3qhlB30KknSejmIvZZLjOD",
    "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
    "https://open.spotify.com/track/0HqZX76SFLDz2aW8aiqi7G",
    "https://open.spotify.com/track/6VsvKPJ4xjVNKpI8VVZ3SV",
    "https://open.spotify.com/track/0MMyJUC3WNnFS1lit5pTjk",
    "https://open.spotify.com/track/4uUG5RXrOk84mYEfFvj3cK",
    "https://open.spotify.com/track/7B3z0ySL9Rr0XvZEAjWZzM",

    # Rock
    "https://open.spotify.com/track/2takcwOaAZWiXQijPHIx7B",
    "https://open.spotify.com/track/0eGsygTp906u18L0Oimnem",
    "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P",
    "https://open.spotify.com/track/58ge6dfP91o9oXMzq3XkIS",
    "https://open.spotify.com/track/3AJwUDP919kvQ9QcozQPxg",
    "https://open.spotify.com/track/5ghIJDpPoe3CfHMGu71E6T",
    "https://open.spotify.com/track/2nLtzopw4rPReszdYBJU6h",
    "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
    "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3",
    "https://open.spotify.com/track/1mea3bSkSGXuIRvnydlB5b"
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
        await message.channel.send(
            f"🎶 Dethe poleca:\n{random.choice(piosenki)}"
        )

client.run(TOKEN)
