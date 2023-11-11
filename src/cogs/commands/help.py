from discord.ext import commands
from discord.commands import slash_command
import discord

import src
from src.load import Colours

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Sends a list of commands")
    async def help(self, ctx):

        async def check(self, ctx, **perms: bool):
            ch = ctx.channel
            permissions = ch.permissions_for(ctx.author)

            missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]

            if not missing:
                return True

        if await src.cogs.commands.moderation.check_enabled(ctx) is True:
            embed = discord.Embed(title="XDE Slash Commands", description="[Website](https://xde.nl/) | [Discord](https://discord.gg/ZrAwZbBJpg)", color=Colours.standard)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&")
            embed.add_field(name="Ascii", value="Converts text into an image of the text", inline=True)
            embed.add_field(name="Avatar", value="Sends the avatar of a user", inline=True)
            embed.add_field(name="Evaluate", value="Evaluates the text, whether it be code or arithmetic", inline=True)
            embed.add_field(name="Iq", value="Sends the iq of a user", inline=True)
            embed.add_field(name="Help", value="This command", inline=True)
            embed.add_field(name="League", value="Sends the latest information about our current racing league", inline=True)
            embed.add_field(name="Ping", value="Sends the bots latency", inline=True)
            embed.add_field(name="Presence", value="Changes the status on the bots profile", inline=True)
            embed.add_field(name="Say", value="Repeats a message", inline=True)
            embed.add_field(name="Saye", value="Sends messages in an embed", inline=True)
            embed.add_field(name="Tictactoe", value="Sends a message with buttons that allows you to play tictactoe", inline=True)
            embed.add_field(name="Socials", value="Sends all the links to our social media pages", inline=True)
            embed.add_field(name="Whois", value="Sends info on a discord user", inline=True)
            embed.set_footer(text="Xtreme Dutch Elite ・ 2023 | Created by Aston", icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
            await ctx.respond(embed=embed, ephemeral=True)

            if await check(self, ctx, manage_roles=True):
                embed = discord.Embed(title="XDE Admin Commands",
                                      description="[Website](https://xde.nl/) | [Discord](https://discord.gg/ZrAwZbBJpg)",
                                      color=Colours.standard)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&")
                embed.add_field(name="Add_points_manual", value="Command for manually adding points to someone in the league", inline=True)
                embed.add_field(name="Attendance_embed", value="Sends the embed for the next round coming up that people can react to", inline=True)
                embed.add_field(name="Bans", value="Bans people", inline=True)
                embed.add_field(name="Create_league_category", value="Allows you to create a new category with all the necessary channels for a new league", inline=True)
                embed.add_field(name="Delete_category", value="Deletes a category of your choice, use with caution make sure you delete the right one")
                embed.add_field(name="Hide_category", value="Changes a categories permissions so it cannot be seen, all you have to do is move it to the bottom", inline=True)
                embed.add_field(name="Kick", value="Kicks people", inline=True)
                embed.add_field(name="Purge", value="Deletes messages", inline=True)
                embed.add_field(name="Round_points_add", value="Prompt to set the points for everyone who turned up to the league round", inline=True)
                embed.add_field(name="Timeout", value="Times out a user", inline=True)
                embed.add_field(name="Refresh_Cog", value="Refreshes the commands if code is updated", inline=True)
                embed.add_field(name="Remove_timeout", value="Removes the timeout on a user", inline=True)
                embed.add_field(name="Unban", value="Unbans people with their id", inline=True)
                embed.set_footer(text="Xtreme Dutch Elite ・ 2023 | Created by Aston", icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
                await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))