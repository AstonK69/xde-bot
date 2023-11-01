from discord.ext import commands
import discord
from discord.ext.commands import CommandNotFound
from src.load import Colours


class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(intents=discord.Intents.all())

    @bot.event
    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description=f"That command is on cooldown please try again in a few seconds!",
                colour=Colours.standard)
        elif isinstance(error, CommandNotFound):
            command = str(ctx.message.content).split(" ")[0]
            embed = discord.Embed(
                description=f"Command `{command}` not found",
                colour=Colours.standard)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"Missing required argument for that command!",
                colour=Colours.standard)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"You are missing the permissions to do this!",
                colour=Colours.standard)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description=f"I do not have permission to do this!",
                colour=Colours.standard)
        else:
            error_ = str(error)[29:] if str(error).lower().startswith(
                "command") else str(error)
            embed = discord.Embed(
                description=f"{str(error_).capitalize()}",
                colour=Colours.standard)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(on_command_error(bot))
