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
# BLOKADY
# =========================================

last_messages = set()

cooldown_ping = set()
cooldown_utwor = set()
cooldown_butelka = set()

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
    "👻 System sprawdza czy gracze żyją."
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
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP"
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

# =========================================
# MESSAGE
# =========================================

@client.event
async def on_message(message):

    global pm_aktywne

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

        if message.author.id in cooldown_ping:
            return

        cooldown_ping.add(
            message.author.id
        )

        await message.channel.send(
            "🏓 Pong!"
        )

        await asyncio.sleep(2)

        cooldown_ping.remove(
            message.author.id
        )

        return

    # =====================================
    # UTWÓR
    # =====================================

    if message.content.lower() in [
        "!utwór",
        "!utwor"
    ]:

        if message.author.id in cooldown_utwor:
            return

        cooldown_utwor.add(
            message.author.id
        )

        embed = discord.Embed(
            title="🎵 Dethe poleca",
            description=random.choice(utwory),
            color=0x6a0dad
        )

        await message.channel.send(
            embed=embed
        )

        await asyncio.sleep(2)

        cooldown_utwor.remove(
            message.author.id
        )

        return

    # =====================================
    # BUTELKA
    # =====================================

    if message.content.lower() == "!butelka":

        if message.author.id in cooldown_butelka:
            return

        cooldown_butelka.add(
            message.author.id
        )

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

            cooldown_butelka.remove(
                message.author.id
            )

            return

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

            cooldown_butelka.remove(
                message.author.id
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

        await asyncio.sleep(3)

        cooldown_butelka.remove(
            message.author.id
        )

        return

    # =====================================
    # KOLOR HEX
    # =====================================

    if message.content.lower().startswith("!kolor"):

        args = message.content.split()

        if len(args) < 2:

            await message.channel.send(
                "🎨 Użycie:\n"
                "!kolor #ff00ff"
            )

            return

        hex_kolor = args[1]

        if not hex_kolor.startswith("#"):

            await message.channel.send(
                "❌ Podaj kolor HEX."
            )

            return

        if len(hex_kolor) != 7:

            await message.channel.send(
                "❌ Zły format HEX."
            )

            return

        try:

            kolor_int = int(
                hex_kolor[1:],
                16
            )

        except:

            await message.channel.send(
                "❌ Niepoprawny HEX."
            )

            return

        guild = message.guild

        nazwa_roli = f"KOLOR-{message.author.id}"

        rola = discord.utils.get(
            guild.roles,
            name=nazwa_roli
        )

        if not rola:

            rola = await guild.create_role(
                name=nazwa_roli,
                colour=discord.Colour(
                    kolor_int
                )
            )

        else:

            await rola.edit(
                colour=discord.Colour(
                    kolor_int
                )
            )

        # usuń stare role kolorów

        for r in message.author.roles:

            if r.name.startswith("KOLOR-"):

                try:
                    await message.author.remove_roles(r)
                except:
                    pass

        # dodaj rolę

        await message.author.add_roles(
            rola
        )

        # przesuń rolę najwyżej jak się da

        try:

            bot_member = guild.me

            await rola.edit(
                position=bot_member.top_role.position - 1
            )

        except:

            await message.channel.send(
                "⚠ Nie mogę przesunąć roli wyżej.\n"
                "Ustaw rolę bota wyżej w Discordzie."
            )

        await message.channel.send(
            f"🎨 {message.author.mention} ustawił własny kolor."
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

client.run(TOKEN)
