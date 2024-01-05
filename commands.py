import discord
from discord.ext import commands
import requests
from discord import Embed
console_log = 1192737481527926855
class general(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        # Check if the member has the "Mod" role
        mod_role = discord.utils.get(ctx.guild.roles, name="Mod")
        return mod_role in ctx.author.roles
    
    async def cog_command_error(self, ctx, error):
        console_log_ = self.bot.get_channel(console_log)
        # Check if the error is a CommandNotFound error
        if isinstance(error, commands.CheckFailure):
            channel = self.bot.get_channel(1192737481527926855)
            if channel:
                await ctx.send("คุณไม่มีสิทธ์")
                checkfailer_embed = discord.Embed()
                checkfailer_embed.add_field(name=' ', value=f'ปฎิเสธการใช้คำสั่ง\n ชื่อ discord: {ctx.author.name}\n id: {ctx.author.id}')
                console_ = self.bot.get_channel(console_log)
                await console_.send(embed=checkfailer_embed)
        else:
            # Handle other errors
            await console_log_.send(f"An error occurred: {error}")

        if isinstance(error, commands.CommandNotFound):
            # Send a log message to the specified channel
            channel = self.bot.get_channel(1192737481527926855)
            if channel:
                # Create a log message with user information and timestamp
                log_message = f"CommandNotFound: User: {ctx.author.id} - {ctx.author.name}, Time: {ctx.message.created_at}, Command: {ctx.message.content}"
                # Send the log message to the channel
                await channel.send(log_message)
            else:
                print("Channel not found")
                
    @commands.hybrid_command(name='เปลี่ยนรูปโปรไฟล์บอท', alises = ['pfp'])
    async def pfp(self,i:commands.Context,url:str):
        """เปลี่ยนรูปโปรบอท copy url แล้ววาง"""
        # Download the image from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Save the image to a file
            with open('avatar.png', 'wb') as f:
                f.write(response.content)
            # Set the bot's avatar using the file path
            with open('avatar.png', 'rb') as f:
                await self.bot.user.edit(avatar=f.read())
                await i.send('changes')
        else:
            await i.send(f"Failed to download image from {url}")

    @commands.hybrid_command(name='เปลี่ยนชื่อบอท',alieses=['name'])
    async def name(self,i:commands.Context,name:str):
        """เปลี่ยนชื่อบอท"""
        if name:
            await self.bot.user.edit(username=name)
            await i.send(f'เปลี่ยนเป็น `{self.bot.user.name}`')
        else:
            await i.send('failed')

    @commands.command(name='dm')
    async def dm(self, ctx: commands.Context, *, text: str):
        user = self.bot.get_user(240881837516259328)  # ผู้ใช้ที่เรียกคำสั่ง
        try:
            embed = Embed(title=f'{ctx.author.name}')
            embed.set_thumbnail(url=ctx.author.display_avatar)
            embed.add_field(name=' ',value=f'{text} ')
            await user.send(embed=embed)  # ส่งข้อความ DM ไปยังผู้ใช้
            await ctx.send(f"ส่ง DM ไปยัง {user.name} สำเร็จแล้วครับ!",delete_after=3)
        except Exception as e:
            await ctx.send(f"เกิดข้อผิดพลาดในการส่ง DM: {e}")

    
    @commands.hybrid_command(name='guild_pic', help='Display the profile picture of the guild')
    async def guild_pic(self, ctx:commands.Context):
        # Get the guild's icon URL
        guild_icon_url = ctx.guild.icon.url

        if guild_icon_url is not None:
            # Create an embed with the guild's icon
            embed = discord.Embed(title=f"Guild Icon - {ctx.guild.name}", color=discord.Color.blurple())
            embed.set_image(url=guild_icon_url)

            # Send the embed in the current channel
            await ctx.send(embed=embed)
        else:
            await ctx.send("This guild does not have an icon.")



async def setup(bot):
    await bot.add_cog(general(bot))