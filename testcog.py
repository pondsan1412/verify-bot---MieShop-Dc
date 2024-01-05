import discord
from discord.ext import commands

class cogtest(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author == self.bot.user: return

    @commands.command(name='test')
    async def test(self,i:commands.Context):
        await i.send(view=SelectView())

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label='รูปไม่ตรงกับที่กรอก', description=' ')
        ]
        super().__init__(placeholder='เลือกเหตผลที่ปฏิเสธ',max_values=1,min_values=1,options=options)
    
    async def callback(self, interaction:discord.Interaction):
        if self.values[0] == 'รูปไม่ตรงกับที่กรอก':
            await interaction.response.send_message('คุณถูกปฏิเสธ ข้อหา รูปไม่ตรงกับข้อมูลที่กรอก')

class SelectView(discord.ui.View):
    def __init__(self, *, timeout= None):
        super().__init__(timeout=timeout)
        self.add_item(Select())

async def setup(bot):
    await bot.add_cog(cogtest(bot))