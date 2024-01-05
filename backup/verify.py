import discord
from discord.ext import commands
import asyncio

guild_mie = 982351785844961300
user_mie = 240881837516259328
user_pond = 324207503816654859
console_log = 1192737481527926855

import locale
locale.setlocale(locale.LC_ALL, 'th_TH.UTF-8')

months_thai = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10: "ตุลาคม",
    11: "พฤศจิกายน",
    12: "ธันวาคม"
}

class Select(discord.ui.Select):
    def __init__(self,bot:commands.Bot,user_id):
        options=[
            discord.SelectOption(label='ข้อมูลในรูปภาพไม่ตรงกับที่คุณให้ข้อมูลมา', description=' '),
            discord.SelectOption(label='รูปภาพที่ส่งมาไม่ถูกต้อง (ไม่ใช่ข้อมูล ARK ID)',description=' '),
            discord.SelectOption(label='อื่นๆ')
        ]
        super().__init__(placeholder='เลือกเหตผลที่ปฏิเสธ',max_values=1,min_values=1,options=options)
        self.bot = bot
        self.user_id = user_id

    async def callback(self, interaction:discord.Interaction):
        await interaction.response.defer()
        dm_user = self.bot.get_user(self.user_id)
        if self.values[0] == 'ข้อมูลในรูปภาพไม่ตรงกับที่คุณให้ข้อมูลมา':
            await dm_user.send('เหตผล: ข้อมูลในรูปภาพไม่ตรงกับที่คุณให้ข้อมูลมา')
        if self.values[0] == 'รูปภาพที่ส่งมาไม่ถูกต้อง (ไม่ใช่ข้อมูล ARK ID)':
            await dm_user.send('เหตผล: รูปภาพที่ส่งมาไม่ถูกต้อง (ไม่ใช่ข้อมูล ARK ID)')
        if self.values[0] == 'อื่นๆ':
            await dm_user.send('เหตผล: None')
        await interaction.response.send_message('ส่งเหตผลที่ปฏิเสธสำเร็จ')
        
        
    

class MyView(discord.ui.View):
    def __init__(
            self,
            bot: commands.Bot,
            name,
            user_id, #user id ของทาง discord
            #แถบต่อไปนี้คือรับค่ามาจาก class อื่น
            nick_name,#ชื่อเล่นที่กรอกตอนตอบคำถาม
            player_id_name, #ชื่อในเกม
            player_id, #เป็น id ในเกมของ user
            ship, #ship คือ server name ของเกม pso2
            basic_data_photo, #รูปภาพที่ยืนยันตัวตนแล้ว
            user_pfp # รับค่ารูปโปรไฟล์
    ):
        super().__init__(timeout=None)
        self.bot = bot  
        self.name = name 
        self.user_id = user_id 
        self.nick_name = nick_name
        self.player_id_name = player_id_name
        self.player_id = player_id
        self.ship = ship
        self.basic_data_photo = basic_data_photo
        self.user_pfp = user_pfp
        self.add_item(Select(bot=self.bot,user_id=self.user_id))

    @discord.ui.button(label='ยืนยัน', style=discord.ButtonStyle.green,emoji='<:emoji_1:983414292458119178>')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """สร้างปุ่ม yes เพื่อยืนยัน user เข้า"""
        self.clear_items()
        user = interaction.user
        guild_id = guild_mie  # ID ของเซิร์ฟเวอร์ที่ต้องการ
        guild = self.bot.get_guild(guild_id)  # ใช้ self.bot.get_guild() เพื่อรับอ็อบเจกต์เซิร์ฟเวอร์จาก ID
        if guild:
            member = guild.get_member(self.user_id)  # ใช้ guild.get_member() เพื่อรับอ็อบเจกต์สมาชิกจาก ID ของผู้ใช้
            if member:
                role = discord.utils.get(guild.roles, name="Member")
                if role:
                    await member.add_roles(role)
                    
                    await interaction.response.send_message(f'เราได้เพิ่ม {self.name} เข้าสู่ server ของคุณแล้ว')
                else:
                    await interaction.response.send_message('Role "Member" not found in the specified guild.')
            else:
                await interaction.response.send_message('User not found in the specified guild.')
        else:
            await interaction.response.send_message('Guild with the specified ID not found.')

        #ส่ง บัตรประชาชนเข้า channel ที่ลงทะเบียนแล้ว
        embed = discord.Embed(title='ผู้ที่ผ่านการยืนยันตัวตนแล้ว ✅ ',color=discord.Color.green())
        
        
        guild = self.bot.get_guild(guild_mie)
        joined_at = guild.get_member(self.user_id)
        user_dm = self.bot.get_user(self.user_id)
        month_thai = months_thai[user_dm.created_at.month]
        create_at = user_dm.created_at.strftime(f'%d {month_thai} %Y เวลา %H:%M:%S น.')
        embed.add_field(
            name=f'บัตรประชาชน', value=f"""
            ชื่อเล่น: {self.nick_name} <@{self.user_id}>
            Player ID Name: {self.player_id_name}
            Player ID: {self.player_id}
            Ship: {self.ship}
            ==========================================
            discord_id: {self.user_id}
            discord_user: {self.name}
            วันที่เข้าร่วม discord: {user_dm} เข้าร่วมวันที่ {create_at}
            วันที่เข้าร่วม server นี้: {joined_at.joined_at.strftime("%Y-%m-%d")}
            
        """)
        
        embed.set_image(url=self.basic_data_photo)
        embed.set_thumbnail(url=self.user_pfp)
        embed.set_footer(text=f'ยืนยันแล้ว โดย {interaction.user.name}',icon_url='https://i.pinimg.com/originals/70/a5/52/70a552e8e955049c8587b2d7606cd6a6.gif')
        channel_verified = self.bot.get_channel(1192734726344167474)
        await channel_verified.send(embed=embed)
        you_has_been_verified = self.bot.get_user(self.user_id)
        if you_has_been_verified.dm_channel is None:
            await you_has_been_verified.create_dm()
        
        await you_has_been_verified.dm_channel.send('คุณได้รับการยืนยันตัวตนเรียบร้อยแล้ว จาก server \'Mie PSO 2 NGS Global รับเติม AC\'')
        console_log_ = self.bot.get_channel(console_log)
        await console_log_.send(content=f'กดยืนยันสมาชิก `{self.name}` เข้า server เรียบร้อยแล้ว ')
        self.stop()

    @discord.ui.button(label='Cancel',style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        """เป็นฟังชั่นที่สร้างปุ่ม No เพื่อปฏิเสธการรับ role member"""
        self.clear_items()
        await interaction.response.send_message(f'ปฏิเสธ {self.name} เรียบร้อย')
        user_dm = self.bot.get_user(self.user_id)
        await user_dm.send('คุณถูกปฏิเสธการเข้า server นี้ โปรดแก้ไขการยืนยันตัวตนของคุณใหม่')
        cancel = self.bot.get_channel(console_log)
        embed = discord.Embed(title='ไม่ผ่านการยืนยันตัวตน ❌ ',color=discord.Color.red())
        month_thai = months_thai[user_dm.created_at.month]
        create_at = user_dm.created_at.strftime(f'%d {month_thai} %Y เวลา %H:%M:%S น.')
        guild = self.bot.get_guild(guild_mie)
        joined_at = guild.get_member(self.user_id)
        
        embed.add_field(
            name=f'บัตรประชาชน', value=f"""
            ชื่อเล่น: {self.nick_name} <@{self.user_id}>
            Player ID Name: {self.player_id_name}
            Player ID: {self.player_id}
            Ship: {self.ship}
            ==========================================
            discord_id: {self.user_id}
            discord_user: {self.name}
            วันที่เข้าร่วม discord: {user_dm} เข้าร่วมวันที่ {create_at}
            วันที่เข้าร่วม server นี้: {user_dm} เข้าร่วมเซิร์ฟเวอร์เราเมื่อ {joined_at}
            
        """)
        embed.set_image(url=self.basic_data_photo)
        embed.set_thumbnail(url=self.user_pfp)
        embed.set_footer(text=f'ปฎิเสธโดย {interaction.user.name} ')
        await cancel.send(embed=embed)
        console_log_ = self.bot.get_channel(console_log)
        await console_log_.send(f'{self.name} ถูกปฏิเสธ')
        Select(bot=self.bot,user_id=self.user_id)

class event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if message.channel.id == 982351786205675584:
            if message.guild.me.guild_permissions.manage_messages:
                if any(role.name == 'Member' for role in message.author.roles):
                    if message.mentions:
                        await message.author.send(f"{message.author.mention} คุณได้ทำการเรียกแอดมินแล้ว โปรดรอการตอบกลับ")
                        user = self.bot.get_user(user_mie)
                        console_log_ = self.bot.get_channel(console_log)
                        if user:
                            embed = discord.Embed(title='ลูกค้า mention',color=discord.Color.blurple())
                            embed_console  = discord.Embed()
                            inbox_url = f'https://discord.com/channels/@me/{message.author.id}'
                            embed.add_field(name=f'ลูกค้า: {message.author.name}', value=f'กดinbox: {message.author.mention}\njump to channel: {message.channel.jump_url}')
                            embed_console.add_field(name=' ', value=f'{message.author.mention} ได้ทำการเรียกแอดมินปาร์ม!!! ใน {message.channel.mention}')
                            await user.send(content=f'{user.mention}',embed=embed)
                            await console_log_.send(embed=embed_console)
                        await message.delete()




    @commands.hybrid_command(name='register',alieses=['reg'])
    async def register(self, ctx: commands.Context):
        print(f'{ctx.author.name} ใช้คำสั่ง register')
        console_log_ = self.bot.get_channel(console_log)
        embed = discord.Embed()
        embed.add_field(name=' ', value=f'{ctx.author.name} ใช้สำสั่ง register')
        await console_log_.send(embed=embed)
        # Check if the author has the "member" role
        member_role = discord.utils.get(ctx.guild.roles, name="Member")
        if member_role in ctx.author.roles:
            await ctx.send("คุณได้ยืนยันตัวตนไปแล้วครับ/ค่ะ",ephemeral=True)
            embed_already = discord.Embed(title='ใช้คำสั่งซ้ำ register')
            embed_already.add_field(name=' ', value=f'{ctx.author.name} ใช้คำสั่งซ้ำ เพราะได้ลงทะเบียนไปแล้ว')
            await console_log_.send(embed=embed_already)
            return

        # If the author doesn't have the "member" role, continue with the registration process
        # Ask the user for their nickname
        await ctx.send("โปรดกรอกชื่อเล่นครับ/ค่ะ",ephemeral=True)
        nickname_response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        # Ask the user for their player ID name
        await ctx.send("โปรดกรอก player id name  ของคุณครับ/ค่ะ",ephemeral=True)
        player_id_name_response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        # Ask the user for their player ID (integer only)
        while True:
            await ctx.send("โปรดระบุ Player Id ของคุณด้วยครับ/ค่ะ",ephemeral=True)
            player_id_response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            try:
                player_id = int(player_id_response.content)
                break
            except ValueError:
                await ctx.send("นี่ไม่ใช่ Player Id ที่ถูกต้องครับ/ค่ะ",ephemeral=True)

        # Ask the user for their ship (Feoh, Ur, Thorn, Ansur only)
        while True:
            await ctx.send("คุณอยู่ Ship อะไรครับ/ค่ะ?",ephemeral=True)
            ship_response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if ship_response.content.lower() in ["1", "2", "3", "4"]:
                break
            else:
                await ctx.send("ship ไม่ถูกต้อง โปรดกรอกให้ถูกต้องด้วยครับ/ค่ะ",ephemeral=True)

        # Ask the user to attach an image
        await ctx.send("โปรดแนบรูปภาพในหน้า ARKS ID (ในเกม) ของคุณมาด้วยครับ/ค่ะ",ephemeral=True)
        while True:
            attachment_response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.attachments)
            if attachment_response.attachments:
                # The user has attached an image, continue with the registration process
                break
            else:
                await ctx.send("ผิดพลาด: โปรดแนบรูปหน้า ARKS ID (ในเกม) ให้ถูกต้องด้วยครับ",ephemeral=True)

        # If the user has provided all required information, continue with the registration process
        # ...
        await ctx.send('คุณได้ตอบคำถามครบแล้ว โปรดรอขั้นตอนการตรวจสอบเพื่อรับรองการเข้า server นี้อย่างสมบูรณ์',ephemeral=True)

        # Delete all the user's messages in the registration process, excluding the final message from the bot
        await ctx.channel.purge(check=lambda m: m.author == ctx.author and m.content != 'คุณได้ตอบคำถามครบแล้ว โปรดรอขั้นตอนการตรวจสอบเพื่อรับรองการเข้า server นี้อย่างสมบูรณ์')


        # Create the embed with the user's information
        embed = discord.Embed(title=f'คำขอเข้า server', colour=discord.Color.red())
        embed.add_field(name=f'ชื่อใน Discord: {ctx.author.name}', value=f"""
            ชื่อเล่น: {nickname_response.content}
            Player ID Name: {player_id_name_response.content}
            Player ID: {player_id}
            Ship: {ship_response.content}
        """)
        
        # Set the image of the embed to the attached image
        embed.set_image(url=attachment_response.attachments[0].url)
        embed.set_footer(text=f'<@{ctx.author.id}> ')
        view = MyView(bot=self.bot,name=ctx.author.name,user_id=ctx.author.id,nick_name=nickname_response.content,player_id_name=player_id_name_response.content,player_id=player_id_response.content,ship=ship_response.content,basic_data_photo=attachment_response.attachments[0].url,user_pfp=ctx.author.display_avatar)
        # Send the embed to th e user's DM
        
        user = self.bot.get_user(user_mie)
        if user.dm_channel is None:
            await user.create_dm()

        await user.dm_channel.send(embed=embed,view=view)



async def setup(bot):
    await bot.add_cog(event(bot))
