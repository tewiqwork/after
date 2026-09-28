import random
import discord
from discord import app_commands
from discord.ext import commands
from style import card

class Fun(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @app_commands.command(name="8ball",description="Ask the aftter 8-ball.")
    async def eightball(self,i,question:str):
        await i.response.send_message(embed=card("🎱・AFTTER 8-BALL",f"> {question}\n\n**{random.choice(['Absolutely.','Probably.','No shot.','Ask again later.','The void says yes.','The void says no.'])}**"))

    @app_commands.command(name="coin",description="Flip a coin.")
    async def coin(self,i):
        await i.response.send_message(embed=card("🪙・COIN",f"**{random.choice(['HEADS','TAILS'])}**"))

    @app_commands.command(name="dice",description="Roll a die.")
    async def dice(self,i):
        await i.response.send_message(embed=card("🎲・DICE",f"You rolled **{random.randint(1,6)}**."))

    @app_commands.command(name="ship",description="Check compatibility.")
    async def ship(self,i,member:discord.Member):
        await i.response.send_message(embed=card("💘・SHIP",f"{i.user.mention} × {member.mention}\n\n**{random.randint(0,100)}%**"))
