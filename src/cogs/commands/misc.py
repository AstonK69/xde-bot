from discord.ext import commands
from discord import app_commands
import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands.core import has_permissions

MY_GUILD = discord.Object(id=1140717989780521020)


class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyBot(intents=intents)


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @client.tree.command(name="ping", description="Sends the bots latency in ms")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=f"The bot responded in {round(self.bot.latency * 1000)}ms",
            colour=0x6e00eb)
        await interaction.response.send_message(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @client.tree.command(name="say", description="Repeats a message")
    @app_commands.describe(text='The text you want me to repeat')
    async def say(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text)


def setup(bot):
    bot.add_cog(Misc(bot))
