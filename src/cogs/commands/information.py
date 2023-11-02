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

        embed.add_field(name="", value="""**```ml
     
     XTREME DUTCH ELITE FORMULA ONE 2005 LEAGUE
        ```**""", inline=False)

        embed.add_field(name="", value="The current league we are running in XDE is the F1 2005 cars, there is 8 rounds of different style tracks which makes for some amazing racing. They run on sunday evenings for europe and below we have made timestamps to put all session times into your own timezone. All the necessary information about the league and signing up is below:", inline=False)

        embed.add_field(name="Calendar", value="here are all the different tracks on the calendar for the league:", inline=False)
        embed.add_field(name="", value=""">>> **Round 1**
Interlagos
Laps: 20""")
        embed.add_field(name="", value=""">>> **Round 2**
Red Bull Ring
Laps: 22""")
        embed.add_field(name="", value=""">>> **Round 3**
Maggiore
Laps: 16""")
        embed.add_field(name="", value=""">>> **Round 4**
Silverstone
Laps: 18""")
        embed.add_field(name="", value=""">>> **Round 5**
Hungaroring
Laps: 17""")
        embed.add_field(name="", value=""">>> **Round 6**
Istanbul Park
Laps: 16""")
        embed.add_field(name="", value=""">>> **Round 7**
Hockenheimring
Laps: 19""")
        embed.add_field(name="", value=""">>> **Round 8**
Spa-Francorchamps
Laps: 13""")

        embed.add_field(name="Session Times", value="""The layout of the evening consists of a practice session which we dont require you to be there for, our briefing which we expect everyone to be in voice chat for, qualifying and the 2 races. The second race starting grid is the reverse of the finishing results of race one. Below is the times and length for all the sessions on the day:
(Times are subject to change and may vary from weekend to weekend)""",
                        inline=False)
        embed.add_field(name="", value=""">>> **Practice**
<t:1698950700:t> - <t:1698952500:t> (30 Minutes)""", inline=False)
        embed.add_field(name="", value=""">>> **Briefing**
<t:1698952500:t> - <t:1698953400:t> (15 Minutes)""", inline=False)
        embed.add_field(name="", value=""">>> **Qualifying**
<t:1698953400:t> - <t:1698954600:t> (20 Minutes)""", inline=False)
        embed.add_field(name="", value=""">>> **Race 1 - Standard**
<t:1698954600:t> - <t:1698956400:t> (30 Minutes)""", inline=False)
        embed.add_field(name="", value=""">>> **Race 2 - Reverse Grid**
<t:1698956400:t> - <t:1698958200:t> (30 Minutes)""", inline=False)

        embed.add_field(name="Discord channels", value="Here are all the channel links for all the channels dedicated to the league:", inline=False)
        embed.add_field(name="", value="""> Updates => <#1142909987014852809>
> Points => <#1142910050722127923>
> Rules => <#1142910537961853061>
> Sign-up => <#1142910131198234816>
> General chat => <#1142910189801046076>
> Liveries => <#1142910230439673978>""", inline=False)

        embed.add_field(name="Useful links", value="Below are all the useful links that you will need if you're taking part in the formula 1 league:", inline=False)
        embed.add_field(name="", value=""">>> **Rulebook** (We do encourage you to look briefly at it all)
https://docs.google.com/document/d/1p1DRlkKzuKrGw3CeRMiDGooGnSOgxnrB8AGG6T5AGmg/edit?usp=sharing

**Download links** (Cars, Tracks, Safety car and Liveries)
https://docs.google.com/document/d/1p1DRlkKzuKrGw3CeRMiDGooGnSOgxnrB8AGG6T5AGmg/edit?usp=sharing

**Live Timing Page**
http://xde.nl:8772/live-timing?server=1

**Server Link**
https://acstuff.ru/s/q:race/online/join?httpPort=9604&ip=89.117.56.93""")

        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
        await ctx.channel.send(embed=embed)
        await ctx.respond('League embed sent!', ephemeral=True)

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