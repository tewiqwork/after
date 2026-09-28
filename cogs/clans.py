import discord
from discord import app_commands
from discord.ext import commands
from style import success,danger,info

class Clans(commands.Cog):
    def __init__(self,bot): self.bot=bot

    async def nick(self,m,tag):
        base=m.display_name
        if base.startswith("[") and "] " in base: base=base.split("] ",1)[1]
        try: await m.edit(nick=(f"[{tag}] {base}" if tag else base)[:32],reason="aftter clan tag")
        except discord.HTTPException: pass

    group=app_commands.Group(name="clan",description="Clan system")

    @group.command(name="create",description="Create a clan.")
    async def create(self,i,tag:app_commands.Range[str,2,5],name:app_commands.Range[str,2,24]):
        if await self.bot.db.clan(i.guild.id,i.user.id):
            return await i.response.send_message(embed=danger("ALREADY IN CLAN","Leave your current clan first."),ephemeral=True)
        role=await i.guild.create_role(name=f"[{tag.upper()}] {name}",reason="aftter clan")
        await self.bot.db.create_clan(i.guild.id,name,tag.upper(),i.user.id,role.id)
        await i.user.add_roles(role)
        await self.nick(i.user,tag.upper())
        await i.response.send_message(embed=success("CLAN CREATED",f"**[{tag.upper()}] {name}**\nYour role and nickname were updated."))

    @group.command(name="add",description="Add a member.")
    async def add(self,i,member:discord.Member):
        c=await self.bot.db.clan(i.guild.id,i.user.id)
        if not c or c[3]!=i.user.id:
            return await i.response.send_message(embed=danger("OWNER ONLY","Only the clan owner can add members."),ephemeral=True)
        if await self.bot.db.clan(i.guild.id,member.id):
            return await i.response.send_message(embed=danger("ALREADY IN CLAN","That member already has a clan."),ephemeral=True)
        await self.bot.db.add_member(c[0],member.id)
        role=i.guild.get_role(c[4])
        if role: await member.add_roles(role)
        await self.nick(member,c[2])
        await i.response.send_message(embed=success("MEMBER ADDED",f"{member.mention} joined **[{c[2]}] {c[1]}**."))

    @group.command(name="info",description="Show your clan.")
    async def info_cmd(self,i):
        c=await self.bot.db.clan(i.guild.id,i.user.id)
        if not c: return await i.response.send_message(embed=info("NO CLAN","You're not in a clan."),ephemeral=True)
        await i.response.send_message(embed=info(f"[{c[2]}] {c[1]}",f"Owner: <@{c[3]}>\nRole: <@&{c[4]}>"))

    @group.command(name="leave",description="Leave your clan.")
    async def leave(self,i):
        c=await self.bot.db.clan(i.guild.id,i.user.id)
        if not c: return await i.response.send_message(embed=danger("NO CLAN","You're not in a clan."),ephemeral=True)
        if c[3]==i.user.id: return await i.response.send_message(embed=danger("OWNER","Delete the clan first."),ephemeral=True)
        await self.bot.db.remove_member(c[0],i.user.id)
        role=i.guild.get_role(c[4])
        if role:
            try: await i.user.remove_roles(role)
            except discord.HTTPException: pass
        await self.nick(i.user,"")
        await i.response.send_message(embed=success("LEFT CLAN","Your clan tag was removed."))

    @group.command(name="delete",description="Delete your clan.")
    async def delete(self,i):
        c=await self.bot.db.clan(i.guild.id,i.user.id)
        if not c or c[3]!=i.user.id: return await i.response.send_message(embed=danger("OWNER ONLY","Only the owner can delete the clan."),ephemeral=True)
        role=i.guild.get_role(c[4])
        if role:
            try: await role.delete(reason="aftter clan deleted")
            except discord.HTTPException: pass
        await self.bot.db.delete_clan(c[0])
        await self.nick(i.user,"")
        await i.response.send_message(embed=success("CLAN DELETED","The clan and its role are gone."))
