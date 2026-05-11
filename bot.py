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

KANAL_PM = 1503427984273703002
KANAL_SPOTIFY = 1501855557584162818

ROLA_PM = "GRACZPM"
ROLA_BUTELKA = "BUTELKA"

CZAS_RUNDY = 10
ILOSC_RUND = 10
PRZERWA_MIEDZY_RUNDAMI = 5

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# HASŁA
# =========================================

HASLA_START = [
    "SYSTEM AKTYWNY",
    "ARENA OTWARTA",
    "PRÓBA ROZPOCZĘTA"
]

HASLA_TIMER = [
    "MYŚL SZYBCIEJ",
    "CZAS UCIEKA",
    "OSTATNIE SEKUNDY"
]

HASLA_STOP = [
    "RUNDA ZAKOŃCZONA",
    "ANALIZA ODPOWIEDZI"
]

HASLA_WIN = [
    "ZWYCIĘZCA",
    "MISTRZ ARENY"
]

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
# KATEGORIE
# =========================================

KATEGORIE = [
    "Państwo",
    "Miasto",
    "Zwierzę",
    "Imię",
    "Jedzenie",
    "Kolor",
    "Zawód",
    "Roślina",
    "Gra",
    "Film",
    "Serial",
    "Sport",
    "Instrument",
    "Napój",
    "Słodycz",
    "Fast food",
    "Owoc",
    "Warzywo",
    "Kwiat",
    "Mebel"
]

LITERY = list("ABCDEFGHIJKLMNOPRSTUWYZ")

# =========================================
# POLSKIE ZNAKI
# =========================================

def usun_polskie_znaki(txt):

    zamiany = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ż": "z",
        "ź": "z"
    }

    txt = txt.lower()

    for pl, normal in zamiany.items():
        txt = txt.replace(pl, normal)

    return txt

# =========================================
# WCZYTYWANIE PLIKÓW
# =========================================

def load_words(filename):

    try:

        with open(
            f"data/{filename}",
            "r",
            encoding="utf-8"
        ) as file:

            return [
                line.strip().lower()
                for line in file.readlines()
                if line.strip()
            ]

    except:
        return []

# =========================================
# BAZY
# =========================================

BAZY = {

    "Państwo": load_words("panstwa.txt"),
    "Miasto": load_words("miasta.txt"),
    "Zwierzę": load_words("zwierzeta.txt"),
    "Imię": load_words("imiona.txt"),
    "Jedzenie": load_words("jedzenie.txt"),
    "Kolor": load_words("kolory.txt"),
    "Zawód": load_words("zawody.txt"),
    "Roślina": load_words("rosliny.txt"),
    "Gra": load_words("gry.txt"),
    "Film": load_words("filmy.txt"),
    "Serial": load_words("seriale.txt"),
    "Sport": load_words("sporty.txt"),
    "Instrument": load_words("instrumenty.txt"),
    "Napój": load_words("napoje.txt"),
    "Słodycz": load_words("slodycze.txt"),
    "Fast food": load_words("fastfood.txt"),
    "Owoc": load_words("owoce.txt"),
    "Warzywo": load_words("warzywa.txt"),
    "Kwiat": load_words("kwiaty.txt"),
    "Mebel": load_words("meble.txt")
}

# =========================================
# STAN GRY
# =========================================

gra_pm = False
odpowiedzi_pm = {}
punkty_pm = {}

aktualna_litera = ""
aktualna_kategoria = ""

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

            await asyncio.sleep(180)

# =========================================
# MESSAGE
# =========================================

@client.event
async def on_message(message):

    global gra_pm
    global odpowiedzi_pm
    global punkty_pm
    global aktualna_litera
    global aktualna_kategoria

    if message.author.bot:
        return

    # =====================================
    # PING
    # =====================================

    if message.content == "!ping":

        await message.channel.send(
            "🏓 Pong!"
        )

        return

    # =====================================
    # UTWÓR
    # =====================================

    if message.content == "!utwor":

        await message.channel.send(
            f"🎵 Dethe poleca:\n"
            f"{random.choice(utwory)}"
        )

        return

    # =====================================
    # DOŁĄCZ
    # =====================================

    if message.content == "!dolacz":

        role = discord.utils.get(
            message.guild.roles,
            name=ROLA_PM
        )

        if role in message.author.roles:

            await message.channel.send(
                "❌ Masz już rolę GRACZPM."
            )

            return

        await message.author.add_roles(role)

        await message.channel.send(
            f"✅ {message.author.mention} dołączył do gry!"
        )

        return

    # =====================================
    # START
    # =====================================

    if message.content == "!gra-start":

        if message.channel.id != KANAL_PM:
            return

        if gra_pm:

            await message.channel.send(
                "❌ Gra już trwa!"
            )

            return

        gra_pm = True
        punkty_pm = {}

        losowe_kategorie = random.sample(
            KATEGORIE,
            ILOSC_RUND
        )

        # =================================
        # COUNTDOWN
        # =================================

        start_msg = await message.channel.send(
            f"⚔️ [ {random.choice(HASLA_START)} ]\n\n"
            f"Start za 10..."
        )

        for i in range(9, -1, -1):

            if not gra_pm:
                return

            await start_msg.edit(
                content=
                f"⚔️ [ {random.choice(HASLA_START)} ]\n\n"
                f"Start za {i}..."
            )

            await asyncio.sleep(15)

        # =================================
        # RUNDY
        # =================================

        for runda in range(1, ILOSC_RUND + 1):

            if not gra_pm:
                break

            odpowiedzi_pm = {}

            aktualna_kategoria = losowe_kategorie[
                runda - 1
            ]

            aktualna_litera = random.choice(
                LITERY
            )

            timer_msg = await message.channel.send(
                f"🎯 RUNDA {runda}/{ILOSC_RUND}\n\n"
                f"📚 Kategoria: **{aktualna_kategoria}**\n"
                f"🔤 Litera: **{aktualna_litera}**\n\n"
                f"⏳ {CZAS_RUNDY}s"
            )

            for czas in range(
                CZAS_RUNDY - 1,
                -1,
                -1
            ):

                if not gra_pm:
                    break

                await asyncio.sleep(1)

                await timer_msg.edit(
                    content=
                    f"🔥 [ {random.choice(HASLA_TIMER)} ]\n\n"
                    f"📚 Kategoria: **{aktualna_kategoria}**\n"
                    f"🔤 Litera: **{aktualna_litera}**\n\n"
                    f"⏳ {czas}s"
                )

            if not gra_pm:
                break

            wyniki = []

            pierwsza = True

            for user_id, data in odpowiedzi_pm.items():

                pkt = 10

                if pierwsza:
                    pkt += 5
                    pierwsza = False

                if user_id not in punkty_pm:

                    punkty_pm[user_id] = {
                        "nick": data["nick"],
                        "punkty": 0
                    }

                punkty_pm[user_id]["punkty"] += pkt

                wyniki.append(
                    f"✅ {data['nick']} — "
                    f"{data['odpowiedz']} (+{pkt} pkt)"
                )

            if not wyniki:

                wyniki.append(
                    "❌ Brak poprawnych odpowiedzi."
                )

            ranking = sorted(
                punkty_pm.values(),
                key=lambda x: x["punkty"],
                reverse=True
            )

            tabela = ""

            for i, gracz in enumerate(
                ranking,
                start=1
            ):

                tabela += (
                    f"{i}. "
                    f"{gracz['nick']} — "
                    f"{gracz['punkty']} pkt\n"
                )

            await message.channel.send(
                f"🏁 [ {random.choice(HASLA_STOP)} ]\n\n"
                + "\n".join(wyniki)
                + "\n\n🏆 Ranking:\n"
                + tabela
            )

            await asyncio.sleep(
                PRZERWA_MIEDZY_RUNDAMI
            )

        # =================================
        # ZWYCIĘZCA
        # =================================

        if punkty_pm:

            zwyciezca = max(
                punkty_pm.values(),
                key=lambda x: x["punkty"]
            )

            await message.channel.send(
                f"👑 [ {random.choice(HASLA_WIN)} ]\n\n"
                f"🏆 {zwyciezca['nick']} "
                f"wygrywa z wynikiem "
                f"{zwyciezca['punkty']} pkt!"
            )

        gra_pm = False

        return

    # =====================================
    # STOP
    # =====================================

    if message.content == "!gra-stop":

        if message.channel.id != KANAL_PM:
            return

        if not gra_pm:

            await message.channel.send(
                "❌ Gra nie trwa."
            )

            return

        gra_pm = False

        await message.channel.send(
            "⛔ Gra została zatrzymana."
        )

        return

    # =====================================
    # ODPOWIEDZI
    # =====================================

    if (
        gra_pm
        and message.channel.id == KANAL_PM
        and any(
            role.name == ROLA_PM
            for role in message.author.roles
        )
    ):

        if message.author.id in odpowiedzi_pm:
            return

        odpowiedz = message.content.strip()

        odpowiedz_clean = (
            usun_polskie_znaki(
                odpowiedz.lower()
            )
        )

        litera_clean = (
            usun_polskie_znaki(
                aktualna_litera.lower()
            )
        )

        baza = BAZY.get(
            aktualna_kategoria,
            []
        )

        baza_clean = [
            usun_polskie_znaki(x)
            for x in baza
        ]

        # =================================
        # POPRAWNA
        # =================================

        if (
            odpowiedz_clean.startswith(
                litera_clean
            )
            and odpowiedz_clean in baza_clean
        ):

            odpowiedzi_pm[
                message.author.id
            ] = {
                "nick": message.author.name,
                "odpowiedz": odpowiedz
            }

            await message.add_reaction("✅")

            return

        # =================================
        # GŁOSOWANIE
        # =================================

        elif odpowiedz_clean.startswith(
            litera_clean
        ):

            vote_msg = await message.channel.send(
                f"⚠️ Nieznana odpowiedź:\n"
                f"**{odpowiedz}**\n\n"
                f"👍 = TAK\n"
                f"👎 = NIE"
            )

            await vote_msg.add_reaction("👍")
            await vote_msg.add_reaction("👎")

            await asyncio.sleep(5)

            vote_msg = await message.channel.fetch_message(
                vote_msg.id
            )

            up = 0
            down = 0

            for reaction in vote_msg.reactions:

                if str(reaction.emoji) == "👍":
                    up = reaction.count

                elif str(reaction.emoji) == "👎":
                    down = reaction.count

            if up > down:

                odpowiedzi_pm[
                    message.author.id
                ] = {
                    "nick": message.author.name,
                    "odpowiedz": odpowiedz
                }

                await message.add_reaction("✅")

            else:

                await message.add_reaction("❌")

            return

    # =====================================
    # BUTELKA
    # =====================================

    if message.content == "!butelka":

        members = [

            member for member in message.channel.members

            if (
                not member.bot
                and any(
                    role.name == ROLA_BUTELKA
                    for role in member.roles
                )
            )
        ]

        if len(members) < 2:

            await message.channel.send(
                "❌ Za mało osób z rolą BUTELKA!"
            )

            return

        osoba = random.choice(members)

        await message.channel.send(
            "🍾 Dethe kręci butelką..."
        )

        await asyncio.sleep(1)

        wybor = random.choice([
            "❓ PYTANIE",
            "🔥 WYZWANIE"
        ])

        await message.channel.send(
            f"🍾 Butelka wskazuje:\n"
            f"{osoba.mention}\n\n"
            f"{wybor}"
        )

        return

client.run(TOKEN)
