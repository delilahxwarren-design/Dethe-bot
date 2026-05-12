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
    "🐸 Żaba od kodu daje wam ostatnią szansę.",
    "💜 Fioletowy system aktywowany.",
    "🚨 Alarm: gracze zaczynają myśleć.",
    "📦 Ładowanie losowych liter...",
    "🧿 PM.SYSTEM patrzy.",
    "🪦 Dethe zakopał poprzednią kategorię.",
    "🍪 Serwer został opłacony ciastkami.",
    "🫠 IQ serwera spadło poniżej normy.",
    "📡 Skanowanie odpowiedzi...",
    "🌪 Nadciąga chaos państw i miast."
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
    "https://open.spotify.com/track/1OcSfkeCg9hRC2sFKB4IMJ"
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
                description=random.choice(
                    utwory
                ),
                color=0x6a0dad
            )

            await kanal.send(
                embed=embed
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

        embed = discord.Embed(
            title="🎵 Dethe poleca",
            description=random.choice(
                utwory
            ),
            color=0x6a0dad
        )

        await message.channel.send(
            embed=embed
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
                "❌ Brak roli BUTELKA."
            )

            return

        if (
            message.channel.id
            == KANAL_BUTELKA_DOM
        ):

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

        osoba = random.choice(
            members
        )

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
    # KOLOR HEX
    # =====================================

    if message.content.lower().startswith(
        "!kolor"
    ):

        args = message.content.split()

        if len(args) < 2:

            await message.channel.send(
                "🎨 Użycie:\n"
                "!kolor #ff00ff"
            )

            return

        hex_kolor = args[1].lower()

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

        nazwa_roli = (
            message.author.display_name
        )

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

        if rola not in message.author.roles:

            await message.author.add_roles(
                rola
            )

        try:

            await rola.edit(
                position=
                guild.me.top_role.position - 1
            )

        except:
            pass

        await message.channel.send(
            f"🎨 {message.author.mention} ustawił kolor {hex_kolor}"
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

        odp_norm = normalize(
            odpowiedz
        )

        if not odp_norm.startswith(
            normalize(
                aktualna_litera
            )
        ):

            await message.add_reaction(
                "❌"
            )

            return

        plik = KATEGORIE[
            aktualna_kategoria
        ]

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

            odpowiedzi[
                message.author.id
            ] = odpowiedz

            if len(odpowiedzi) == 1:
                pkt = 15
            else:
                pkt = 10

            nick = (
                message.author.display_name
            )

            if nick not in punkty:
                punkty[nick] = 0

            punkty[nick] += pkt

            await message.add_reaction(
                "✅"
            )

        else:

            await message.add_reaction(
                "❌"
            )

# =========================================
# START
# =========================================

client.run(TOKEN)
