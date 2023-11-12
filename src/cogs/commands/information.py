from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType

import src
from src.load import Colours
from src.data.league_embeds import f1_05_embed, gt4_embed

leagues = ["Formula 1 2005", "Porsche GT4 Challenge"]
league_embeds = {"Formula 1 2005": f1_05_embed, "Porsche GT4 Challenge": gt4_embed}

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends information about the current league")
    @discord.option("league", description="Which leage would you like information on?", required=False, choices=leagues)
    async def league(self, ctx, league="Formula 1 2005"):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            embed = league_embeds[league]
            await ctx.channel.send(embed=embed)
            await ctx.respond('League embed sent!', ephemeral=True)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends all the XDE Social media pages")
    async def socials(self, ctx):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
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