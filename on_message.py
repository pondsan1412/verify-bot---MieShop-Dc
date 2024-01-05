import discord
from discord.ext import commands

class onmessage(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user: return
        
        if isinstance(message.channel, discord.DMChannel):
            # ตรวจสอบว่าข้อความมาจาก DM
            general_channel = discord.utils.get(self.bot.get_all_channels(), name='console-bot')
            if general_channel:
                try:
                    if message.attachments:
                        for attachment in message.attachments:
                            image_url = attachment.url
                            embed = discord.Embed(
                                    title="New Direct Message with Image",
                                    description=f"From: {message.author.name}\n id: {message.author.id}\nContent: {message.content}",
                                    color=0x00ff00
                                )
                            embed.set_image(url=image_url)
                            await general_channel.send(embed=embed)
                            break  # เพื่อหยุดการ loop หากพบรูปภาพ
                    else:
                        embed = discord.Embed(
                            title="New Direct Message",
                            description=f"From: {message.author.name}\n id: {message.author.id}\nContent: {message.content}",
                            color=0x00ff00
                        )
                        await general_channel.send(embed=embed)
                except discord.HTTPException as e:
                    print(f"Failed to send message to general channel: {e}")
            else:
                print("The 'general' channel does not exist in this guild.")

async def setup(bot):
    await bot.add_cog(onmessage(bot))