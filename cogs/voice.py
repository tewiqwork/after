import discord
from discord.ext import commands

class TempVoice(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.rooms=set()

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if after.channel and after.channel.id==await self.bot.db.voice(member.guild.id):
            cat=after.channel.category
            overwrites={
                member.guild.default_role: discord.PermissionOverwrite(connect=True),
                member: discord.PermissionOverwrite(connect=True,manage_channels=True,move_members=True)
            }
            room=await member.guild.create_voice_channel(
                f"🔊・{member.display_name[:25]}'s room",
                category=cat,overwrites=overwrites,reason="aftter temp voice"
            )
            self.rooms.add(room.id)
            try: await member.move_to(room)
            except discord.HTTPException: pass

        if before.channel and before.channel.id in self.rooms and not before.channel.members:
            try: await before.channel.delete(reason="aftter empty temp voice")
            except discord.HTTPException: pass
            self.rooms.discard(before.channel.id)
