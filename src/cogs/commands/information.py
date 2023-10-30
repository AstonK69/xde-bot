from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands.core import has_permissions
from src.load import Colours


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends information about the current league")
    async def league(self, ctx):
        embed = discord.Embed(title="XDE Formula 1 2005 League", description="[Live Timings](http://ac.xde.nl:8772/live-timing?server=1) | [Server Link](https://acstuff.ru/s/q:race/online/join?httpPort=9604&ip=89.117.56.93) | [Website](https://xde.nl/)", colour=Colours.standard)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1140717990350966879/1168250192722661547/Screenshot_xde_vrc_2005_mclaren_mp420_acu_hungaroring_16-9-123-18-3-48.png?ex=655114c6&is=653e9fc6&hm=e4a97957555232f853243a914f2d2d0c2c1ed16b616092502ddfe53b588b4c00&")
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
        await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends all the XDE Social media pages")
    async def socials(self, ctx):
        embed = discord.Embed(title="XDE Social Media Pages",
                              description="""
[Website](https://xde.nl/)

[Youtube](https://www.youtube.com/@xderacingcommunity)

[Instagram](https://www.instagram.com/xde_racing_community/)

[Reddit](https://www.reddit.com/user/XDE_Racing_Community)

[Twitter](https://twitter.com/XDE_Racing)

[Facebook](https://www.facebook.com/profile.php?id=100085710858576)
                              """,
                              colour=Colours.standard)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Information(bot))