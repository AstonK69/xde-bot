from discord.ext import commands
import discord
from src.load import Colours
from src.run import bot

class on_message_edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        embed = discord.Embed(colour=Colours.standard, title="Message edited", description=f"{before.author.mention} edited the following:")
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        print(before.content)
        await after.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(on_message_edit(bot))