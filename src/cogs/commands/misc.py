from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands.core import has_permissions
from src.load import Colours


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="ping", description="Sends the bots latency in ms", guild_ids=[1140717989780521020])
    async def ping(self, ctx):
        embed = discord.Embed(
            description=f"The bot responded in {round(self.bot.latency * 1000)}ms",
            colour=Colours.standard)
        await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="say", description="Repeats a message", guild_ids=[1140717989780521020])
    async def say(self, ctx, text: str):
        await ctx.respond(text)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Repeats a message in an embed")
    @discord.option("title", description="Provide a title")
    @discord.option("message", description="Provide a message")
    async def saye(self, ctx, title: str, message: str):
        embed = discord.Embed(title=title, description=message, colour=Colours.standard)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
