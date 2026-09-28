from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands
from style import success,danger,info

class Moderation(commands.Cog):
    def __init__(self,bot): self.bot=bot

    async def mod(self,i):
        if not i.user.guild_permissions.moderate_members:
            await i.response.send_message(embed=danger("ACCESS DENIED","You need **Moderate Members**."),ephemeral=True); return False
        return True

    @app_commands.command(name="warn",description="Warn a member.")
    async def warn(self,i,member:discord.Member,reason:str="No reason provided"):
        if not await self.mod(i): return
        if member.id==i.user.id:
            return await i.response.send_message(embed=danger("NOPE","You can't warn yourself."),ephemeral=True)
        n=await self.bot.db.add_warn(i.guild.id,member.id,i.user.id,reason,int(i.created_at.timestamp()))
        total=await self.bot.db.warn_count(i.guild.id,member.id)
        await i.response.send_message(embed=success("WARNING ADDED",f"{member.mention} • warning **#{n}**\n`{reason}`"))
        if total>=10 and member.bannable:
            await member.ban(reason=f"aftter auto-ban: {total} warnings")
        elif total>=7 and member.kickable:
            await member.kick(reason=f"aftter auto-kick: {total} warnings")
        elif total>=5 and member.moderatable:
            await member.timeout(timedelta(hours=24),reason=f"aftter: {total} warnings")
        elif total>=3 and member.moderatable:
            await member.timeout(timedelta(hours=1),reason=f"aftter: {total} warnings")

    @app_commands.command(name="warnings",description="View a member's warnings.")
    async def warnings(self,i,member:discord.Member):
        if not await self.mod(i): return
        rows=await self.bot.db.warns(i.guild.id,member.id)
        if not rows:
            return await i.response.send_message(embed=info("CLEAN RECORD",f"{member.mention} has no warnings."),ephemeral=True)
        text="\n".join(f"`#{r[0]}` <@{r[1]}> — {r[2]}" for r in rows)
        await i.response.send_message(embed=info(f"WARNINGS • {member}",text),ephemeral=True)

    @app_commands.command(name="clear",description="Delete 1–100 messages.")
    async def clear(self,i,amount:app_commands.Range[int,1,100]):
        if not await self.mod(i): return
        await i.response.defer(ephemeral=True)
        deleted=await i.channel.purge(limit=amount)
        await i.followup.send(embed=success("CHANNEL CLEANED",f"Deleted **{len(deleted)}** messages."),ephemeral=True)

    @app_commands.command(name="kick",description="Kick a member.")
    async def kick(self,i,member:discord.Member,reason:str="No reason provided"):
        if not await self.mod(i): return
        if not member.kickable: return await i.response.send_message(embed=danger("FAILED","My role is too low."),ephemeral=True)
        await member.kick(reason=reason)
        await i.response.send_message(embed=success("MEMBER KICKED",f"{member} • {reason}"))

    @app_commands.command(name="ban",description="Ban a member.")
    async def ban(self,i,member:discord.Member,reason:str="No reason provided"):
        if not await self.mod(i): return
        if not member.bannable: return await i.response.send_message(embed=danger("FAILED","My role is too low."),ephemeral=True)
        await member.ban(reason=reason)
        await i.response.send_message(embed=success("MEMBER BANNED",f"{member} • {reason}"))

    @app_commands.command(name="timeout",description="Timeout a member.")
    async def timeout(self,i,member:discord.Member,minutes:app_commands.Range[int,1,40320],reason:str="No reason provided"):
        if not await self.mod(i): return
        if not member.moderatable: return await i.response.send_message(embed=danger("FAILED","My role is too low."),ephemeral=True)
        await member.timeout(timedelta(minutes=minutes),reason=reason)
        await i.response.send_message(embed=success("TIMEOUT",f"{member.mention} • **{minutes} min**"))
