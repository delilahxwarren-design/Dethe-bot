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

ROLA_PM = "GRACZPM"

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# BLOKADA DUPLIKATÓW
# =========================================

last_messages = set()

# =========================================
# PM SYSTEM
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
    "Jedzenie": "jedzenie.txt",
    "Miasto": "miasta.txt",
    "Państwo": "panstwa.txt",
    "Zwierzę": "zwierzeta.txt",
    "Film": "filmy.txt",
    "Gra": "gry.txt"
}

LITERY = list("ABCDEFGHIJKLMNOPRSTUWYZ")

SMIESZNE_TEKSTY = [
    "🧠 Dethe szuka inteligentnych graczy...",
    "🍕 Ładowanie chaosu i pizzy...",
    "☠ System wykrył brak snu administracji.",
    "👁 PM.SYSTEM obserwuje wasze odpowiedzi.",
    "🌑 Chomik losujący kategorię właśnie się obudził.",
    "💀 Dethe próbuje przypomnieć sobie alfabet.",
    "🎮 Ładowanie chaosu...",
    "⚠ Administracja nie odpowiada za utratę IQ."
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
    "https://open.spotify.com/track/2nLtzopw4rPReszdYBJU6h",

    # Arctic Monkeys
    "https://open.spotify.com/track/5XeFesFbtLpXzIVDNQP22n",
    "https://open.spotify.com/track/0NdTUS4UiNYCNn5FgVqKQY",

    # Billie Eilish
    "https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m",
    "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62",

    # Chase Atlantic
    "https://open.spotify.com/track/2NmsngXHeC1GQ9wWrzhOMf",
    "https://open.spotify.com/track/5yY9lUy8nbvjM1Uyo1Uqoc",

    # The Weeknd
    "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
    "https://open.spotify.com/track/7MXVkk9YMctZqd1Srtv4MB"
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

            await kanal.send(
                f"🎵 Dzisiejszy utwór od Dethe:\n"
                f"{random.choice(utwory)}"
            )

# =========================================
# PM GAME
# =========================================

async def start_pm_game(channel):

    global pm_aktywne
    global aktualna_kategoria
    global aktualna_litera
    global odpowiedzi
    global punkty
    global wykorzystane_kategorie
    global wiadomosci_graczy

    punkty = {}
    wykorzystane_kategorie = []

    start_msg = await channel.send(
        f"╔════════════════╗\n"
        f"      DETHE-PM\n"
        f"╚════════════════╝\n\n"
        f"{random.choice(SMIESZNE_TEKSTY)}\n\n"
        f"⏳ Start za 10 sekund"
    )

    for i in range(10, 0, -1):

        if not pm_aktywne:
            return

        await start_msg.edit(
            content=
            f"╔════════════════╗\n"
            f"      DETHE-PM\n"
            f"╚════════════════╝\n\n"
            f"{random.choice(SMIESZNE_TEKSTY)}\n\n"
            f"⏳ Start za: {i}"
        )

        await asyncio.sleep(1)

    for runda in range(1, MAX_RUND + 1):

        if not pm_aktywne:
            return

        odpowiedzi = {}
        wiadomosci_graczy = []

        dostepne = [
            k for k in KATEGORIE.keys()
            if k not in wykorzystane_kategorie
        ]

        if not dostepne:
            break

        aktualna_kategoria = random.choice(
            dostepne
        )

        wykorzystane_kategorie.append(
            aktualna_kategoria
        )

        aktualna_litera = random.choice(
            LITERY
        )

        runda_msg = await channel.send(
            f"╔════════════════╗\n"
            f"      DETHE-PM\n"
            f"╚════════════════╝\n\n"
            f"{random.choice(SMIESZNE_TEKSTY)}\n\n"
            f"🟣 RUNDA {runda}/{MAX_RUND}\n\n"
            f"📂 Kategoria: {aktualna_kategoria}\n"
            f"🔤 Litera: {aktualna_litera}\n\n"
            f"⏳ 15 sekund"
        )

        for i in range(15, 0, -1):

            if not pm_aktywne:
                return

            await runda_msg.edit(
                content=
                f"╔════════════════╗\n"
                f"      DETHE-PM\n"
                f"╚════════════════╝\n\n"
                f"{random.choice(SMIESZNE_TEKSTY)}\n\n"
                f"🟣 RUNDA {runda}/{MAX_RUND}\n\n"
                f"📂 Kategoria: {aktualna_kategoria}\n"
                f"🔤 Litera: {aktualna_litera}\n\n"
                f"⏳ {i} sekund"
            )

            await asyncio.sleep(1)

        for msg in wiadomosci_graczy:

            try:
                await msg.delete()
            except:
                pass

        await channel.send(
            "━━━━━━━━━━━━━━━━━━\n"
            "⏳ CZAS MINĄŁ\n"
            "━━━━━━━━━━━━━━━━━━"
        )

        await asyncio.sleep(3)

    pm_aktywne = False

    await channel.send(
        "🏁 Gra zakończona!\n"
        "📊 Trwa liczenie punktów..."
    )

    await asyncio.sleep(3)

    ranking = sorted(
        punkty.items(),
        key=lambda x: x[1],
        reverse=True
    )

    tekst = (
        "╔════════════════╗\n"
        "     PM.RESULTS\n"
        "╚════════════════╝\n\n"
    )

    if not ranking:

        tekst += "Nikt nie zdobył punktów."

    else:

        for i, (gracz, pkt) in enumerate(
            ranking,
            start=1
        ):

            tekst += f"{i}. {gracz} — {pkt} pkt\n"

    await channel.send(tekst)

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

    # BLOKADA DUPLIKATÓW

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
    # START PM
    # =====================================

    if message.content.lower() == "!start":

        if message.channel.id != KANAL_PM:
            return

        if pm_aktywne:
            return

        pm_aktywne = True

        asyncio.create_task(
            start_pm_game(message.channel)
        )

        return

    # =====================================
    # STOP PM
    # =====================================

    if message.content.lower() == "!stop":

        pm_aktywne = False

        await message.channel.send(
            "🛑 Dethe zatrzymał grę."
        )

        return

    # =====================================
    # ODPOWIEDZI PM
    # =====================================

    if pm_aktywne:

        if message.channel.id != KANAL_PM:
            return

        rola = discord.utils.get(
            message.guild.roles,
            name=ROLA_PM
        )

        if rola not in message.author.roles:
            return

        odpowiedz = message.content.strip()

        if not odpowiedz:
            return

        if message.author.id in odpowiedzi:
            return

        wiadomosci_graczy.append(
            message
        )

        odp_norm = normalize(odpowiedz)

        if not odp_norm.startswith(
            normalize(aktualna_litera)
        ):

            await message.add_reaction("❌")

            return

        plik = KATEGORIE[aktualna_kategoria]

        poprawne = []

        if os.path.exists(plik):

            with open(
                plik,
                "r",
                encoding="utf-8"
            ) as f:

                poprawne = [
                    normalize(x.strip())
                    for x in f.readlines()
                ]

        if odp_norm in poprawne:

            odpowiedzi[message.author.id] = odpowiedz

            if len(odpowiedzi) == 1:
                pkt = 15
            else:
                pkt = 10

            nick = message.author.display_name

            if nick not in punkty:
                punkty[nick] = 0

            punkty[nick] += pkt

            await message.add_reaction("✅")

        else:

            await message.add_reaction("❌")

client.run(TOKEN)
