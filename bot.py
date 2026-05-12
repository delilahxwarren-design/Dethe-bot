import discord
import random
import os
import asyncio
import unicodedata

from discord.ext import tasks
from datetime import datetime

TOKEN = os.getenv("TOKEN")

# =========================================
# KONFIG
# =========================================

KANAL_SPOTIFY = 1501855557584162818
KANAL_PM = 1503525539766337656

KANAL_BUTELKA_DOM = 1503091932321022122

ROLA_PM = "GRACZPM"

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# =========================================
# BLOKADA DUPLIKATÓW
# =========================================

last_messages = set()

# =========================================
# SYSTEM PM
# =========================================

pm_aktywne = False
aktualna_kategoria = None
aktualna_litera = None

odpowiedzi = {}
punkty = {}
wykorzystane_kategorie = []
wiadomosci_graczy = []

MAX_RUND = 10

KATEGORIE = {
    "Państwo": "panstwa.txt",
    "Miasto": "miasta.txt",
    "Zwierzę": "zwierzeta.txt",
    "Imię": "imiona.txt",
    "Rzecz": "rzeczy.txt",
    "Jedzenie": "jedzenie.txt",
    "Kolor": "kolory.txt",
    "Zawód": "zawody.txt",
    "Roślina": "rosliny.txt",
    "Gra": "gry.txt",
    "Film": "filmy.txt",
    "Serial": "seriale.txt",
    "Sport": "sporty.txt",
    "Instrument": "instrumenty.txt",
    "Napój": "napoje.txt",
    "Słodycz": "slodycze.txt",
    "Fast food": "fastfood.txt",
    "Owoc": "owoce.txt",
    "Warzywo": "warzywa.txt",
    "Kwiat": "kwiaty.txt",
    "Mebel": "meble.txt"
}

LITERY = list("ABCDEFGHIJKLMNOPRSTUWYZ")

SMIESZNE_TEKSTY = [
    "🧠 Dethe szuka inteligentnych graczy...",
    "🍕 Ładowanie chaosu i pizzy...",
    "☠ System wykrył brak snu opiekunów.",
    "👁 PM.SYSTEM obserwuje wasze odpowiedzi.",
    "🌑 Chomik losujący kategorię właśnie się obudził.",
    "💀 Dethe próbuje przypomnieć sobie alfabet.",
    "🎮 Ładowanie chaosu...",
    "⚠ Opiekunowie nie odpowiadają za utratę IQ.",
    "🟣 Dethe otworzył księgę państw i miast.",
    "👻 System sprawdza czy gracze żyją.",
    "🍟 Dethe zgubił odpowiedzi i improwizuje.",
    "🧃 Trwa karmienie chomika serwerowego.",
    "🔮 Losowanie kategorii przez czarną magię.",
    "🌌 PM.SYSTEM wszedł w tryb nocnego chaosu.",
    "🛸 Obcy właśnie sprawdzają waszą ortografię.",
    "📚 Dethe udaje że zna wszystkie odpowiedzi.",
    "⚡ Serwer przeżył kolejne odpalenie gry.",
    "🎲 Dethe rzuca kostką przeznaczenia.",
    "🕷 Pająk w kodzie właśnie coś naprawił.",
    "🍩 Opiekunowie znowu zapomnieli spać.",
    "📡 Skanowanie mózgów graczy...",
    "🧠 IQ serwera chwilowo spadło do 3.",
    "🌪 System wykrył nadchodzący chaos.",
    "🎭 Dethe udaje profesjonalnego bota.",
    "🐸 Żaba od kodu daje wam jeszcze jedną szansę.",
    "💜 Fioletowy system aktywowany.",
    "🕯 Dethe przywołuje poprawne odpowiedzi.",
    "🚨 Alarm: gracze zaczynają myśleć.",
    "📦 Ładowanie losowych liter...",
    "🧿 PM.SYSTEM patrzy."
]

# =========================================
# NORMALIZACJA
# =========================================

def normalize(text):

    text = text.lower().strip()

    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    return text

# =========================================
# SPOTIFY
# =========================================

utwory = [

    "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
    "https://open.spotify.com/track/7MXVkk9YMctZqd1Srtv4MB",
    "https://open.spotify.com/track/5XeFesFbtLpXzIVDNQP22n",
    "https://open.spotify.com/track/0NdTUS4UiNYCNn5FgVqKQY",
    "https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m",
    "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62",
    "https://open.spotify.com/track/2NmsngXHeC1GQ9wWrzhOMf",
    "https://open.spotify.com/track/5yY9lUy8nbvjM1Uyo1Uqoc",
    "https://open.spotify.com/track/776AftMmFFAWUIEAb3lHhw",
    "https://open.spotify.com/track/1OcSfkeCg9hRC2sFKB4IMJ",
    "https://open.spotify.com/track/6rLqjzGV5VMLDWEnuUqi8q",
    "https://open.spotify.com/track/5R8dQOPq8haW94K7mgERlO",
    "https://open.spotify.com/track/2qSkIjg1o9h3YT9RAgYN75",
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP",
    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
    "https://open.spotify.com/track/62yJjFtgkhUrXktIoSjgP2"
]

last_song_day = None

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

    global last_song_day

    teraz = datetime.now()

    if teraz.hour == 21 and teraz.minute == 30:

        dzis = teraz.date()

        if last_song_day == dzis:
            return

        last_song_day = dzis

        kanal = client.get_channel(
            KANAL_SPOTIFY
        )

        if kanal:

            embed = discord.Embed(
                title="🎵 Dzisiejszy utwór od Dethe",
                description=random.choice(utwory),
                color=0x6a0dad
            )

            await kanal.send(embed=embed)

# =========================================
# MESSAGE
# =========================================

@client.event
async def on_message(message):

    global pm_aktywne
    global odpowiedzi
    global punkty
    global wiadomosci_graczy

    if message.author.bot:
        return

    if message.id in last_messages:
        return

    last_messages.add(message.id)

    if len(last_messages) > 1000:
        last_messages.clear()

    # =====================================
    # PING
    # =====================================

    if message.content.lower() == "!ping":

        await message.channel.send(
            "🏓 Pong!"
        )

        return

    # =====================================
    # BUTELKA
    # =====================================

    if message.content.lower() == "!butelka":

        rola_butelka = discord.utils.get(
            message.guild.roles,
            name="BUTELKA"
        )

        rola_gosc = discord.utils.get(
            message.guild.roles,
            name="GOSC"
        )

        if not rola_butelka:

            await message.channel.send(
                "❌ Nie znaleziono roli BUTELKA."
            )

            return

        # KANAŁ DOMOWNIKÓW

        if message.channel.id == KANAL_BUTELKA_DOM:

            members = [
                member for member in message.guild.members
                if (
                    not member.bot
                    and rola_butelka in member.roles
                    and (
                        rola_gosc is None
                        or rola_gosc not in member.roles
                    )
                )
            ]

        # RESZTA KANAŁÓW

        else:

            members = [
                member for member in message.guild.members
                if (
                    not member.bot
                    and rola_butelka in member.roles
                )
            ]

        if len(members) < 1:

            await message.channel.send(
                "❌ Brak osób do losowania."
            )

            return

        msg = await message.channel.send(
            "🍾 Dethe kręci butelką..."
        )

        for i in ["3", "2", "1"]:

            await asyncio.sleep(1)

            await msg.edit(
                content=
                f"🍾 Dethe kręci butelką...\n\n"
                f"⏳ {i}"
            )

        osoba = random.choice(members)

        typ = random.choice([
            "🟣 PRAWDA",
            "🔥 WYZWANIE"
        ])

        await asyncio.sleep(1)

        await msg.edit(
            content=
            f"╔════════════════╗\n"
            f"      DETHE\n"
            f"╚════════════════╝\n\n"
            f"🍾 Butelka wybrała:\n\n"
            f"👉 {osoba.mention}\n\n"
            f"{typ}"
        )

        return

    # =====================================
    # UTWÓR
    # =====================================

    if message.content.lower() in [
        "!utwór",
        "!utwor"
    ]:

        embed = discord.Embed(
            title="🎵 Dethe poleca",
            description=random.choice(utwory),
            color=0x6a0dad
        )

        await message.channel.send(embed=embed)

        return

client.run(TOKEN)
