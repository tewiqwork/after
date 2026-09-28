import discord
from discord import app_commands
from discord.ext import commands
from style import success,danger,info

class Setup(commands.Cog):
    def __init__(self,bot): self.bot=bot

    async def owner(self,i):
        ok=i.guild and (i.user.id==i.guild.owner_id or i.user.guild_permissions.administrator)
        if not ok:
            await i.response.send_message(embed=danger("ACCESS DENIED","Only the server owner or an administrator can do this."),ephemeral=True)
        return ok

    @app_commands.command(name="nuke",description="Reset the server to aftter's clean 5-channel layout.")
    async def nuke(self,i):
        if not await self.owner(i): return
        await i.response.send_message(
            embed=danger("NUKE CONFIRMATION",
                         "This will **delete every channel and category** in this server.\n\n"
                         "Type `/nuke-confirm` immediately after this message to continue."),
            ephemeral=True
        )

    @app_commands.command(name="nuke-confirm",description="Confirm a full server channel reset.")
    async def nuke_confirm(self,i):
        if not await self.owner(i): return
        await i.response.defer(ephemeral=True)
        guild=i.guild

        # Delete channels first; Discord handles categories independently.
        for ch in list(guild.channels):
            try:
                await ch.delete(reason=f"aftter reset by {i.user}")
            except (discord.Forbidden,discord.HTTPException):
                pass

        cats={}
        for name in ("information","community","support","voice"):
            cats[name]=await guild.create_category(f"— {name} —",reason="aftter layout")

        channels=[
            ("📢・announcements",cats["information"],"text"),
            ("📄・readme",cats["information"],"text"),
            ("💬・chat",cats["community"],"text"),
            ("🆘・support",cats["support"],"text"),
            ("🔎・create [+]",cats["voice"],"voice")
        ]
        created=[]
        for name,cat,kind in channels:
            if kind=="voice":
                ch=await guild.create_voice_channel(name,category=cat,reason="aftter layout")
                await self.bot.db.set_voice(guild.id,ch.id)
            else:
                ch=await guild.create_text_channel(name,category=cat,reason="aftter layout")
            created.append(ch)

        # Make a compact branded readme.
        readme=created[1]
        await readme.send(embed=info(
            "aftter",
            "**after dark. clean community.**\n\n"
            "Use `/help` to see commands.\n"
            "Join **🔎・create [+]** to get your own temporary voice room.\n\n"
            "• moderation\n• clans\n• anti-link\n• temporary voice\n• fun"
        ))
        await i.followup.send(embed=success("SERVER RESET","aftter rebuilt the server with **exactly 5 channels**."),ephemeral=True)
