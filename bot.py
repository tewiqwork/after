import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import DB
from cogs.moderation import Moderation
from cogs.automod import AutoMod
from cogs.voice import TempVoice
from cogs.clans import Clans
from cogs.setup import Setup
from cogs.fun import Fun

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

class Aftter(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            chunk_guilds_at_startup=False,
            max_messages=0,
        )
        self.db = DB("aftter.db")

    async def setup_hook(self):
        await self.db.init()
        for cog in (Moderation, AutoMod, TempVoice, Clans, Setup, Fun):
            await self.add_cog(cog(self))
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="after dark • /help",
            )
        )
        print(f"aftter online • {self.user}")

bot = Aftter()
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing in .env")
bot.run(TOKEN)
