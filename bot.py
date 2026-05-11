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

KANAL_ID = 1501855557584162818
ROLA_BUTELKA = "BUTELKA"

KANAL_PM = 1503427984273703002
ROLA_PM = "GRACZPM"

CZAS_RUNDY = 10
ILOSC_RUND = 10
PRZERWA_MIEDZY_RUNDAMI = 8

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# HASŁA
# =========================================

HASLA_START = [
    "PRÓBA ROZPOCZĘTA",
    "SYSTEM AKTYWNY",
    "ARENA OTWARTA",
    "CZAS START",
    "WEJDŹ DO GRY"
]

HASLA_KONIEC = [
    "RUNDA ZAMKNIĘTA",
    "CZAS MINĄŁ",
    "ANALIZA ODPOWIEDZI"
]

HASLA_TIMER = [
    "POSPIESZ SIĘ",
    "MYŚL SZYBCIEJ",
    "CZAS UCIEKA",
    "OSTATNIE SEKUNDY"
]

HASLA_WIN = [
    "MISTRZ PRÓBY",
    "OSTATNI OCALAŁY",
    "ZWYCIĘZCA ARENY"
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
    "Marka",
    "Samochód",
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

LITERY = list("ABCDEFGHIJKLMNOPRSTUWZŁŻŚĆŃÓĘĄŹ")

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
# BAZY KATEGORII
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
    "Marka": load_words("marki.txt"),
    "Samochód": load_words("samochody.txt"),
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

    if message.author == client.user:
        return

    # =========================================
    # DOŁĄCZ
    # =========================================

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

    # =========================================
    # PING
    # =========================================

    if message.content == "!ping":

        await message.channel.send("🏓 Pong!")

    # =========================================
    # STOP
    # =========================================

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
            f"🏁 [ {random.choice(HASLA_KONIEC)} ]\n\n"
            "⛔ Gra została zatrzymana."
        )

        return

    # =========================================
    # ODPOWIEDZI
    # =========================================

    if (
        gra_pm
        and message.channel.id == KANAL_PM
        and any(role.name == ROLA_PM for role in message.author.roles)
    ):

        if message.author.id not in odpowiedzi_pm:

            odpowiedz = message.content.strip()

            odpowiedz_clean = usun_polskie_znaki(
                odpowiedz.lower()
            )

            litera_clean = usun_polskie_znaki(
                aktualna_litera.lower()
            )

            baza = BAZY.get(
                aktualna_kategoria,
                []
            )

            baza_clean = [
                usun_polskie_znaki(x)
                for x in baza
            ]

            # =========================================
            # POPRAWNA ODPOWIEDŹ
            # =========================================

            if (
                odpowiedz_clean.startswith(litera_clean)
                and odpowiedz_clean in baza_clean
            ):

                odpowiedzi_pm[message.author.id] = {
                    "nick": message.author.name,
                    "odpowiedz": odpowiedz
                }

                await message.add_reaction("✅")

            # =========================================
            # GŁOSOWANIE
            # =========================================

            elif odpowiedz_clean.startswith(litera_clean):

                vote_msg = await message.channel.send(
                    f"⚠️ Nieznana odpowiedź:\n"
                    f"**{odpowiedz}**\n\n"
                    f"Czy uznać?"
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

                    odpowiedzi_pm[message.author.id] = {
                        "nick": message.author.name,
                        "odpowiedz": odpowiedz
                    }

                    await message.add_reaction("✅")

                else:

                    await message.add_reaction("❌")

    # =========================================
    # START
    # =========================================

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

        start_msg = await message.channel.send(
            f"⚔️ [ {random.choice(HASLA_START)} ]\n\n"
            "Gra rozpoczyna się za 10 sekund..."
        )

        for i in range(10, 0, -1):

            await start_msg.edit(
                content=
                f"⚔️ [ {random.choice(HASLA_START)} ]\n\n"
                f"Start za {i}..."
            )

            await asyncio.sleep(1)

        # =========================================
        # RUNDY
        # =========================================

        for runda in range(1, ILOSC_RUND + 1):

            if not gra_pm:
                break

            odpowiedzi_pm = {}

            aktualna_kategoria = losowe_kategorie[
                runda - 1
            ]

            aktualna_litera = random.choice(LITERY)

            msg = await message.channel.send(
                f"🎯 [ RUNDA {runda}/{ILOSC_RUND} ]\n\n"
                f"📚 Kategoria: **{aktualna_kategoria}**\n"
                f"🔤 Litera: **{aktualna_litera}**\n\n"
                f"⏳ Pozostały czas: {CZAS_RUNDY}s"
            )

            for czas in range(CZAS_RUNDY, 0, -1):

                if not gra_pm:
                    break

                await msg.edit(
                    content=
                    f"🔥 [ {random.choice(HASLA_TIMER)} ]\n\n"
                    f"📚 Kategoria: **{aktualna_kategoria}**\n"
                    f"🔤 Litera: **{aktualna_litera}**\n\n"
                    f"⏳ Pozostały czas: {czas}s"
                )

                await asyncio.sleep(1)

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
                f"🏁 [ {random.choice(HASLA_KONIEC)} ]\n\n"
                + "\n".join(wyniki)
                + "\n\n🏆 Ranking:\n"
                + tabela
            )

            await asyncio.sleep(
                PRZERWA_MIEDZY_RUNDAMI
            )

        # =========================================
        # ZWYCIĘZCA
        # =========================================

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

# =========================================
# RUN
# =========================================

client.run(TOKEN)
