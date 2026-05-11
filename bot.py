import discord
import random
import os
import asyncio
from discord.ext import tasks
from datetime import datetime
from flask import Flask
from threading import Thread

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
# KEEP ALIVE 💜
# =========================================

app = Flask('')

@app.route('/')
def home():
    return "Dethe żyje 💜"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# HASŁA DETHE
# =========================================

HASLA_START = [
    "PRÓBA ROZPOCZĘTA",
    "SYSTEM AKTYWNY",
    "ARENA OTWARTA",
    "CZAS START",
    "WEJDŹ DO GRY",
    "ROZPOCZĘCIE RUNDY",
    "TRYB GRY AKTYWNY"
]

HASLA_KONIEC = [
    "RUNDA ZAMKNIĘTA",
    "CZAS MINĄŁ",
    "ANALIZA ODPOWIEDZI",
    "KONIEC PRÓBY",
    "RUNDA DOBIEGŁA KOŃCA"
]

HASLA_WIN = [
    "MISTRZ PRÓBY",
    "OSTATNI OCALAŁY",
    "ZWYCIĘZCA ARENY",
    "KRÓL DETHE",
    "DOMINATOR RUND"
]

HASLA_TIMER = [
    "POSPIESZ SIĘ",
    "MYŚL SZYBCIEJ",
    "CZAS UCIEKA",
    "OSTATNIE SEKUNDY",
    "NAPIĘCIE ROŚNIE"
]

# =========================================
# MUZYKA
# =========================================

utwory = [

    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
    "https://open.spotify.com/track/3LlAyCYU26dvFZBDUIMb7a",
    "https://open.spotify.com/track/1NtIMM4N0cFa1dNzN15chl",
    "https://open.spotify.com/track/62yJjFtgkhUrXktIoSjgP2",

    "https://open.spotify.com/track/6rLqjzGV5VMLDWEnuUqi8q",
    "https://open.spotify.com/track/5R8dQOPq8haW94K7mgERlO",
    "https://open.spotify.com/track/0SiywuOBRcynK0uKGWdCnn",

    "https://open.spotify.com/track/2qSkIjg1o9h3YT9RAgYN75",
    "https://open.spotify.com/track/5N3hjp1WNayUPZrA8kJmJP",

    "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P",
    "https://open.spotify.com/track/58ge6dfP91o9oXMzq3XkIS",
    "https://open.spotify.com/track/2nLtzopw4rPReszdYBJU6h"
]

# =========================================
# PAŃSTWA MIASTA
# =========================================

KATEGORIE = [
    "Państwo",
    "Miasto",
    "Zwierzę",
    "Imię",
    "Rzecz",
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

LITERY = list("ABCDEFGHIJKLMNOPRSTUWZ")

gra_pm = False
odpowiedzi_pm = {}
punkty_pm = {}
aktualna_litera = ""

# =========================================
# READY
# =========================================

@client.event
async def on_ready():
    print(f"{client.user} online!")
    codzienny_utwor.start()

# =========================================
# CODZIENNY UTWÓR
# =========================================

@tasks.loop(minutes=1)
async def codzienny_utwor():

    teraz = datetime.now()

    if teraz.hour == 21 and 30 <= teraz.minute <= 32:

        kanal = client.get_channel(KANAL_ID)

        if kanal:
            await kanal.send(
                f"🎶 Dzisiejszy utwór od Dethe:\n{random.choice(utwory)}"
            )

            await asyncio.sleep(180)

# =========================================
# MESSAGE EVENT
# =========================================

@client.event
async def on_message(message):

    global gra_pm
    global odpowiedzi_pm
    global punkty_pm
    global aktualna_litera

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
                f"❌ {message.author.mention} już bierze udział w grze."
            )

            return

        await message.author.add_roles(role)

        await message.channel.send(
            f"✅ {message.author.mention} dołączył do Państw Miast!"
        )

    # =========================================
    # STOP GRY
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
    # ODPOWIEDZI PM
    # =========================================

    if (
        gra_pm
        and message.channel.id == KANAL_PM
        and any(role.name == ROLA_PM for role in message.author.roles)
    ):

        if message.author.id not in odpowiedzi_pm:

            odpowiedz = message.content.strip()

            if odpowiedz.lower().startswith(aktualna_litera.lower()):

                odpowiedzi_pm[message.author.id] = {
                    "nick": message.author.name,
                    "odpowiedz": odpowiedz
                }

    # =========================================
    # PING
    # =========================================

    if message.content == "!ping":
        await message.channel.send("🏓 Pong!")

    # =========================================
    # LOSOWY UTWÓR
    # =========================================

    if message.content == "!utwór":

        await message.channel.send(
            f"🎵 Dethe poleca:\n{random.choice(utwory)}"
        )

    # =========================================
    # BUTELKA
    # =========================================

    if message.content == "!butelka":

        members = [
            member for member in message.channel.members
            if not member.bot and any(role.name == ROLA_BUTELKA for role in member.roles)
        ]

        if len(members) < 2:

            await message.channel.send(
                "❌ Za mało osób z rolą BUTELKA!"
            )

            return

        osoba = random.choice(members)

        await message.channel.send("🍾 Dethe kręci butelką...")
        await asyncio.sleep(1)

        await message.channel.send("3️⃣")
        await asyncio.sleep(1)

        await message.channel.send("2️⃣")
        await asyncio.sleep(1)

        await message.channel.send("1️⃣")
        await asyncio.sleep(1)

        wybor = random.choice([
            "❓ PYTANIE",
            "🔥 WYZWANIE"
        ])

        await message.channel.send(
            f"🍾 Butelka wskazuje: {osoba.mention}\n\n{wybor}"
        )

    # =========================================
    # START GRY PM
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

            kategoria = losowe_kategorie[runda - 1]
            aktualna_litera = random.choice(LITERY)

            msg = await message.channel.send(
                f"🎯 [ RUNDA {runda}/{ILOSC_RUND} ]\n\n"
                f"📚 Kategoria: **{kategoria}**\n"
                f"🔤 Litera: **{aktualna_litera}**\n\n"
                f"⏳ Pozostały czas: {CZAS_RUNDY}s"
            )

            for czas in range(CZAS_RUNDY, 0, -1):

                if not gra_pm:
                    break

                tekst = random.choice(HASLA_TIMER)

                await msg.edit(
                    content=
                    f"🔥 [ {tekst} ]\n\n"
                    f"📚 Kategoria: **{kategoria}**\n"
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
                    f"✅ **{data['nick']}** — "
                    f"{data['odpowiedz']} (+{pkt} pkt)"
                )

            if not wyniki:

                wyniki.append(
                    "❌ Nikt nie udzielił poprawnej odpowiedzi."
                )

            ranking = sorted(
                punkty_pm.values(),
                key=lambda x: x["punkty"],
                reverse=True
            )

            tabela = ""

            for i, gracz in enumerate(ranking, start=1):

                tabela += (
                    f"{i}. {gracz['nick']} — "
                    f"{gracz['punkty']} pkt\n"
                )

            await message.channel.send(
                f"🏁 [ {random.choice(HASLA_KONIEC)} ]\n\n"
                + "\n".join(wyniki)
                + "\n\n🏆 Ranking:\n"
                + tabela
            )

            await asyncio.sleep(PRZERWA_MIEDZY_RUNDAMI)

        # =========================================
        # KONIEC GRY
        # =========================================

        if punkty_pm:

            zwyciezca = max(
                punkty_pm.values(),
                key=lambda x: x["punkty"]
            )

            await message.channel.send(
                f"👑 [ {random.choice(HASLA_WIN)} ]\n\n"
                f"🏆 {zwyciezca['nick']} zdobywa "
                f"{zwyciezca['punkty']} pkt!"
            )

        gra_pm = False

# =========================================
# RUN
# =========================================

client.run(TOKEN)
