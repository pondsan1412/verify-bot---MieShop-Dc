import discord
from discord.ext import commands
import random

#class intents
def intents():
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    return intents

#class selfbot self.bot = bot
class selfbot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('mie!'),
            intents = intents()
        )

    async def selfready_notification(self,channels,user_id):
            label = ['บอทพร้อมแล้ว','bot ready','พร้อมทำงาน','พร้อมรับใช้ท่าน Mie','ข้าได้ลืมตาตื่น']
            print(random.choice(label))
            for channel_name in channels:
                channel = discord.utils.get(
                    self.get_all_channels(),
                    name = channel_name
                )
                if channel:
                    await channel.send(random.choice(label))
            
            user = self.get_user(user_id)
            if user:
                await user.send(random.choice(label))

    async def on_ready(self):
        channels = 'general'
        await self.selfready_notification(channels,user_id=None)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="สิ่งผิดปกติ"))
        await self.tree.sync()
    
    
    async def setup_hook(self):
        await self.load_extension('commands')
        await self.load_extension('on_message')
        await self.load_extension('verify')




