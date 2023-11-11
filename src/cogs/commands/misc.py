from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands.core import has_permissions

import src.cogs.commands.moderation
from src.load import Colours

activity_types = ["Playing", "Streaming", "Watching", "Listening"]
a_dict = {"Playing": 0,
          "Streaming": 1,
          "Watching": discord.ActivityType.watching,
          "Listening": discord.ActivityType.listening}


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="ping", description="Sends the bots latency in ms")
    async def ping(self, ctx):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            embed = discord.Embed(
                description=f"The bot responded in {round(self.bot.latency * 1000)}ms",
                colour=Colours.standard)
            await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="say", description="Repeats a message")
    @discord.option("text", description="Provide the text you want the bot to say")
    async def say(self, ctx, text: str):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            await ctx.respond('Message sent, you can now hide this message', ephemeral=True)
            await ctx.send(text)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Repeats a message in an embed")
    @discord.option("title", description="Provide a title")
    @discord.option("message", description="Provide a message")
    async def saye(self, ctx, title: str, message: str):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            embed = discord.Embed(title=title, description=message, colour=Colours.standard)
            embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                             icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
            await ctx.respond('Embed sent, you can now hide this message', ephemeral=True)
            await ctx.send(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @has_permissions(manage_nicknames=True)
    @slash_command(name="presence", description="Changes status and activity of bot")
    @discord.option("activity_type", description="Playing, Streaming, Listening, Watching [message]", required=False, choices=activity_types)
    @discord.option("activity_content", description="Changes the status message on the bots profile", required=False)
    async def presence(self, ctx, activity_type: str, activity_content: str):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            try:
                if a_dict[activity_type] == 0:
                    await self.bot.change_presence(activity=discord.Game(name=activity_content))
                elif a_dict[activity_type] == 1:
                    await self.bot.change_presence(activity=discord.Streaming(name=activity_content))
                else:
                    await self.bot.change_presence(activity=discord.Activity(type=a_dict[activity_type], name=activity_content))
                await ctx.respond(f"Changed presence to {activity_type} {activity_content}")
            except Exception as e:
                await ctx.respond(e)

    @cooldown(1, 3, BucketType.user)
    @has_permissions(manage_nicknames=True)
    @slash_command(name="nickname", description="Changes peoples nicknames")
    @discord.option("user", description="Select the user to change the name of", input_type=discord.Member)
    @discord.option("name", description="What nickname do you want to give them")
    async def nickname(self, ctx, user: discord.Member, name=""):
        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            try:
                await user.edit(nick=name)
                if name == "":
                    output = f"Changed {user.name}'s nickname back to normal"
                else:
                    output = f"Changed {user.name}'s nickname to {name}"

                await ctx.respond(output)
            except Exception as e:
                await ctx.respond(e)



def setup(bot):
    bot.add_cog(Misc(bot))
