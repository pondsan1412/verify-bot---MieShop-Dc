import discord
from discord.ext import commands

def intents():
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    return intents

class bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!",intents=intents())

    async def setup_hook(self):
        await self.load_extension('testcog')



import keep_tk
bot_ = bot()
bot_.run(keep_tk.miebot_tk)