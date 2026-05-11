import discord
import random
import asyncio
import os

from discord.ext import tasks
from datetime import datetime

# =========================================
# TOKEN
# =========================================

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
CZAS_GLOSOWANIA = 15

# =========================================
# DISCORD
# =========================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# =========================================
# NORMALIZACJA
# =========================================

def normalize(txt):

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

    txt = txt.lower().strip()

    for pl, normal in zamiany.items():
        txt = txt.replace(pl, normal)

    return txt

# =========================================
# ŁADOWANIE PLIKÓW
# =========================================

def load_words(filename):

    try:

        with open(
            f"data/{filename}",
            "r",
            encoding="utf-8"
        ) as file:

            return [
                line.strip()
                for line in file.readlines()
                if line.strip()
            ]

    except:
        return []

# =========================================
# KATEGORIE
# =========================================

KATEGORIE = {

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

LITERY = list("ABCDEFGHIJKLMNOPRSTUWYZ")

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

UTWORY = [

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
# BUTELKA
# =========================================

PYTANIA_BUTELKA = [

    "Kogo najbardziej lubisz?",
    "Największy sekret?",
    "Najbardziej cringowy moment?",
    "Do kogo napiszesz po grze?",
    "Kto jest hottest na serwerze?",
    "Największy red flag?"
]

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

    if teraz.hour == 21 and teraz.minute == 30:

        kanal = client.get_channel(
            KANAL_SPOTIFY
        )

        if kanal:

            await kanal.send(
                f"🎶 Dzisiejszy utwór:\n"
                f"{random.choice(UTWORY)}"
            )

            await asyncio.sleep(60)

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
            f"🎵 Polecany utwór:\n"
            f"{random.choice(UTWORY)}"
        )

        return

    # =====================================
    # BUTELKA
    # =====================================

    if message.content == "!butelka":

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

        pytanie = random.choice(
            PYTANIA_BUTELKA
        )

        await message.channel.send(
            f"🍾 BUTELKA\n\n"
            f"{osoba1.mention} ➜ "
            f"{osoba2.mention}\n\n"
            f"❓ {pytanie}"
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
                "❌ Masz już rolę."
            )

            return

        await message.author.add_roles(
            role
        )

        await message.channel.send(
            f"✅ {message.author.mention} "
            f"dołączył do gry!"
        )

        return

    # =====================================
    # START
    # =====================================

    if message.content == "!start":

        if message.channel.id != KANAL_PM:
            return

        if gra_pm:

            await message.channel.send(
                "❌ Gra już trwa."
            )

            return

        gra_pm = True
        punkty_pm = {}

        losowe_kategorie = random.sample(
            list(KATEGORIE.keys()),
            ILOSC_RUND
        )

        await message.channel.send(
            f"⚔️ [ {random.choice(HASLA_START)} ]"
        )

        await asyncio.sleep(3)

        for runda in range(1, ILOSC_RUND + 1):

            odpowiedzi_pm = {}

            aktualna_kategoria = (
                losowe_kategorie[runda - 1]
            )

            aktualna_litera = random.choice(
                LITERY
            )

            timer_msg = await message.channel.send(
                f"🔥 RUNDA {runda}/{ILOSC_RUND}\n\n"
                f"📚 Kategoria: "
                f"**{aktualna_kategoria}**\n"
                f"🔤 Litera: "
                f"**{aktualna_litera}**\n\n"
                f"⏳ {CZAS_RUNDY}s"
            )

            for czas in range(
                CZAS_RUNDY - 1,
                -1,
                -1
            ):

                await asyncio.sleep(1)

                await timer_msg.edit(
                    content=
                    f"🔥 [ {random.choice(HASLA_TIMER)} ]\n\n"
                    f"📚 Kategoria: "
                    f"**{aktualna_kategoria}**\n"
                    f"🔤 Litera: "
                    f"**{aktualna_litera}**\n\n"
                    f"⏳ {czas}s"
                )

            wyniki = []

            for user_id, data in odpowiedzi_pm.items():

                if user_id not in punkty_pm:

                    punkty_pm[user_id] = {
                        "nick": data["nick"],
                        "punkty": 0
                    }

                punkty_pm[user_id]["punkty"] += 10

                wyniki.append(
                    f"✅ {data['nick']} — "
                    f"{data['odpowiedz']}"
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

    if message.content == "!stop":

        gra_pm = False

        await message.channel.send(
            "⛔ Gra zatrzymana."
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

        odpowiedz_clean = normalize(
            odpowiedz
        )

        litera_clean = normalize(
            aktualna_litera
        )

        baza = KATEGORIE.get(
            aktualna_kategoria,
            []
        )

        baza_clean = [
            normalize(x)
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
                f"👎 = NIE\n\n"
                f"⏳ {CZAS_GLOSOWANIA} sekund"
            )

            await vote_msg.add_reaction("👍")
            await vote_msg.add_reaction("👎")

            await asyncio.sleep(
                CZAS_GLOSOWANIA
            )

            vote_msg = await message.channel.fetch_message(
                vote_msg.id
            )

            up = 0
            down = 0

            for reaction in vote_msg.reactions:

                if str(reaction.emoji) == "👍":
                    up = reaction.count - 1

                elif str(reaction.emoji) == "👎":
                    down = reaction.count - 1

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

# =========================================
# START BOTA
# =========================================

client.run(TOKEN)
