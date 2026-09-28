import re
import discord
from discord.ext import commands
from style import danger

URL=re.compile(r"(https?://|www\.)",re.I)
INVITE=re.compile(r"(discord\.gg/|discord\.com/invite/)",re.I)
ALLOW=("youtube.com","youtu.be","minecraft.net","github.com")

class AutoMod(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,m):
        if not m.guild or m.author.bot or m.author.guild_permissions.manage_messages: return
        if not URL.search(m.content): return
        s=m.content.lower()
        if any(x in s for x in ALLOW): return
        try:
            await m.delete()
            await m.channel.send(embed=danger("LINK BLOCKED",f"{m.author.mention}, links aren't allowed here."),delete_after=4)
        except discord.HTTPException: pass
