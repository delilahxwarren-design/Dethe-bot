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
KANAL_PM = 1503525539766337656

ROLA_BUTELKA = "BUTELKA"
ROLA_PM = "GRACZPM"

# =========================================
# PM SYSTEM
# =========================================

RUNDA_AKTYWNA = False
AKTUALNA_KATEGORIA = None
AKTUALNA_LITERA = None
ODPOWIEDZI = {}
PUNKTY = {}
RUNDA_NUMER = 0
MAX_RUND = 10

KATEGORIE = {
    "Jedzenie": "jedzenie.txt",
    "Miasto": "miasta.txt",
    "Państwo": "panstwa.txt",
    "Zwierzę": "zwierzeta.txt",
    "Film": "filmy.txt",
    "Gra": "gry.txt",
    "Kolor": "kolory.txt",
    "Zawód": "zawody.txt",
    "Roślina": "rosliny.txt",
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
WYKORZYSTANE_KATEGORIE = []

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

    global RUNDA_AKTYWNA
    global RUNDA_NUMER
    global AKTUALNA_KATEGORIA
    global AKTUALNA_LITERA
    global ODPOWIEDZI
    global PUNKTY
    global WYKORZYSTANE_KATEGORIE

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

    # =====================================
    # STOP PM
    # =====================================

    if message.content.lower() == "!stop":

        if message.channel.id != KANAL_PM:
            return

        RUNDA_AKTYWNA = False

        await message.channel.send(
            "🛑 Gra została zatrzymana."
        )

        return

    # =====================================
    # START PM
    # =====================================

    if message.content.lower() == "!start":

        if RUNDA_AKTYWNA:
            return

        if message.channel.id != KANAL_PM:
            return

        await message.channel.purge(limit=5)

        print("START DETHE-PM")

        if RUNDA_AKTYWNA:

            await message.channel.send(
                "⚠ Gra już trwa."
            )

            return

        RUNDA_AKTYWNA = True
        RUNDA_NUMER = 0
        PUNKTY = {}
        WYKORZYSTANE_KATEGORIE = []

        start_msg = await message.channel.send(
            "🟣 PM.SYSTEM ONLINE\n\n"
            "Rozgrywka rozpocznie się za 10 sekund..."
        )

        for i in range(10, 0, -1):

            if not RUNDA_AKTYWNA:
                return

            await start_msg.edit(
                content=
                f"🟣 PM.SYSTEM ONLINE\n\n"
                f"Start za: {i}"
            )

            await asyncio.sleep(1)

        for _ in range(MAX_RUND):

            if not RUNDA_AKTYWNA:
                return

            RUNDA_NUMER += 1
            ODPOWIEDZI = {}

            dostepne = [
                k for k in KATEGORIE.keys()
                if k not in WYKORZYSTANE_KATEGORIE
            ]

            if not dostepne:
                break

            AKTUALNA_KATEGORIA = random.choice(dostepne)
            WYKORZYSTANE_KATEGORIE.append(AKTUALNA_KATEGORIA)

            AKTUALNA_LITERA = random.choice(LITERY)

            runda_msg = await message.channel.send(
                f"╔════════════════╗\n"
                f"      DETHE-PM\n"
                f"╚════════════════╝\n\n"
                f"🟣 RUNDA {RUNDA_NUMER}/{MAX_RUND}\n\n"
                f"📂 Kategoria: {AKTUALNA_KATEGORIA}\n"
                f"🔤 Litera: {AKTUALNA_LITERA}\n\n"
                f"⏳ 15 sekund"
            )

            for i in range(15, 0, -1):

                if not RUNDA_AKTYWNA:
                    return

                await runda_msg.edit(
                    content=
                    f"╔════════════════╗\n"
                    f"      DETHE-PM\n"
                    f"╚════════════════╝\n\n"
                    f"🟣 RUNDA {RUNDA_NUMER}/{MAX_RUND}\n\n"
                    f"📂 Kategoria: {AKTUALNA_KATEGORIA}\n"
                    f"🔤 Litera: {AKTUALNA_LITERA}\n\n"
                    f"⏳ {i} sekund"
                )

                await asyncio.sleep(1)

            await message.channel.send(
                "⚠ Koniec rundy."
            )

            await asyncio.sleep(2)

        RUNDA_AKTYWNA = False

        ranking = sorted(
            PUNKTY.items(),
            key=lambda x: x[1],
            reverse=True
        )

        tekst = (
            "╔════════════════╗\n"
            "     PM.RESULTS\n"
            "╚════════════════╝\n\n"
        )

        for i, (gracz, pkt) in enumerate(ranking, start=1):
            tekst += f"{i}. {gracz} — {pkt} pkt\n"

        await message.channel.send(tekst)

        return

    # =====================================
    # ODPOWIEDZI PM
    # =====================================

    if RUNDA_AKTYWNA:

        if message.channel.id != KANAL_PM:
            return

        rola = discord.utils.get(
            message.guild.roles,
            name=ROLA_PM
        )

        if rola not in message.author.roles:
            return

        if not message.content.startswith("!"):
            return

        odpowiedz = message.content[1:].strip()

        if not odpowiedz:
            return

        if message.author.id in ODPOWIEDZI:
            return

        if not odpowiedz.lower().startswith(
            AKTUALNA_LITERA.lower()
        ):
            await message.add_reaction("❌")
            return

        plik = KATEGORIE[AKTUALNA_KATEGORIA]

        poprawne = []

        if os.path.exists(plik):

            with open(
                plik,
                "r",
                encoding="utf-8"
            ) as f:

                poprawne = [
                    x.strip().lower()
                    for x in f.readlines()
                ]

        if odpowiedz.lower() in poprawne:

            ODPOWIEDZI[message.author.id] = odpowiedz

            if len(ODPOWIEDZI) == 1:
                pkt = 15
            else:
                pkt = 10

            nick = message.author.display_name

            if nick not in PUNKTY:
                PUNKTY[nick] = 0

            PUNKTY[nick] += pkt

            await message.add_reaction("✅")

        else:

            await message.add_reaction("❌")

client.run(TOKEN)
