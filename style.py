import discord

BLURPLE=0x5865F2
DARK=0x18191C
GREEN=0x57F287
RED=0xED4245
GOLD=0xFEE75C

def card(title, text="", color=BLURPLE):
    e=discord.Embed(title=title, description=text, color=color)
    e.set_footer(text="aftter • after dark")
    return e

def success(title,text=""): return card(f"✦ {title}",text,GREEN)
def danger(title,text=""): return card(f"× {title}",text,RED)
def info(title,text=""): return card(f"◆ {title}",text,BLURPLE)
