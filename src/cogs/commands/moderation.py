import datetime
from discord.ext import commands
import discord
from discord.ext.commands.core import has_permissions
from discord.commands import slash_command
import os
from src import load
from run import bot, loadCog
from src.load import Colours


def reloadCog(path, folder=True):
    if folder:
        for filename in os.listdir(f'{load.path}/cogs/{path}'):
            if filename.endswith('.py'):
                bot.reload_extension(f'cogs.{path}.{filename[:-3]}')
                print(f'{filename[:-3]} cog reloaded')
    else:
        bot.reload_extension(f'cogs.{path}')
        print(f"{path} reloaded")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @has_permissions(ban_members=True)
    @slash_command(name="ban", description="Bans people")
    @discord.option("member", description="Choose a member to ban")
    @discord.option("reason", description="What is the reason", default='Not specified')
    async def ban(self, ctx, member: discord.Member, reason: str):
        joined = member.joined_at
        joined = f"{joined.day}/{joined.month}/{joined.year}, {joined.hour:02d}:{joined.hour:02d}.{joined.second:02d}"
        embed = discord.Embed(title=f"{member.name} banned", description=f"Reason: {reason}", colour=Colours.standard)
        embed.add_field(name="Joined:", value=joined, inline=False)
        embed.add_field(name="Banned by:", value=ctx.author.name)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston")
        try:
            await member.ban(reason=reason)
        except:
            await ctx.respond('Something went wrong!')
        else:
            await ctx.respond(embed=embed)

    @slash_command(name="unban", description="Unbans people")
    @has_permissions(ban_members=True)
    @discord.option("id", description="Provide the id of the member")
    async def unban(self, ctx, *, id: str):
        user = await self.bot.fetch_user(int(id))
        try:
            await ctx.respond(f'<@{id}> has been unbanned by {ctx.author.mention}')
            await ctx.guild.unban(user)
        except:
            await ctx.respond('Something went wrong')

    @has_permissions(kick_members=True)
    @slash_command(name="kick", description="Kicks people")
    @discord.option("member", description="Choose a member to kick")
    @discord.option("reason", description="What is the reason", default="Not specified")
    async def kick(self, ctx, member: discord.Member, reason: str):
        joined = member.joined_at
        joined = f"{joined.day}/{joined.month}/{joined.year}, {joined.hour:02d}:{joined.hour:02d}.{joined.second:02d}"
        embed = discord.Embed(title=f"{member.name} kicked", description=f"Reason: {reason}", colour=Colours.standard)
        embed.add_field(name="Joined:", value=joined, inline=False)
        embed.add_field(name="Kicked by:", value=ctx.author.name)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston")
        try:
            await member.kick(reason=reason)
        except:
            await ctx.respond('Something went wrong!')
        else:
            await ctx.respond(embed=embed)

    @has_permissions(manage_messages=True)
    @slash_command(name="purge", description="Deletes messages")
    @discord.option("amount", description="Choose an amount", min_value=1, max_value=1001)
    async def purge(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.respond(f"Purged {amount} message(s)", ephemeral=True)
        except:
            await ctx.respond("`I do not have permission to do this!`", ephemeral=True)

    @has_permissions(kick_members=True)
    @slash_command(name="timeout", description="Times out a user")
    @discord.option("member", description="Choose a member to timeout")
    @discord.option("hours", description="How many hours for?", min_value=1, max_value=24, default=2)
    @discord.option("reason", description="What is the reason", default="Not specified")
    async def timeout(self, ctx, member: discord.Member, hours: int, reason: str):
        embed = discord.Embed(title=f"{member.name} Timed out", description=f"Reason: {reason}",
                              colour=Colours.standard)
        embed.add_field(name="Timed out for:", value=f"{hours} hours")
        embed.add_field(name="Timed out by:", value=ctx.author.name)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston")
        duration = datetime.timedelta(hours=hours)
        try:
            await member.timeout_for(duration=duration, reason=reason)
        except:
            await ctx.respond('Something went wrong!')
        else:
            await ctx.respond(embed=embed)

    @has_permissions(kick_members=True)
    @slash_command(name="remove_timeout", description="Removes the timeout on a user")
    @discord.option("member", description="Choose a member to timeout")
    @discord.option("reason", description="What is the reason", default="Not specified")
    async def remove_timeout(self, ctx, member: discord.Member, reason: str):
        try:
            await member.remove_timeout(reason=reason)
        except:
            await ctx.respond('Something went wrong!')
        else:
            await ctx.respond(f'I removed the timeout on {member.mention}')

    @has_permissions(ban_members=True)
    @slash_command(description="Reloads cog of bot")
    @discord.option("cog", description="Provide the name of the cog")
    async def refresh_cog(self, ctx, cog: str):
        try:
            try:
                loadCog(cog)
                await ctx.respond(f"{cog} successfully reloaded!")
            except:
                reloadCog(cog)
                await ctx.respond(f"{cog} successfully reloaded!")
        except Exception as error:
            await ctx.respond(f'Something went wrong {error}')


def setup(bot):
    bot.add_cog(Moderation(bot))
