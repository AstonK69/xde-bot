import datetime
from discord.ext import commands
import discord
from discord.ext.commands.core import has_permissions
from discord.commands import slash_command
import os
from src import load
from run import bot, loadCog
from src.load import Colours
from discord import ChannelType


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

    @has_permissions(manage_channels=True)
    @slash_command(name="create_league_category", description="Creates new section of channels for a new league")
    @discord.option("category name", description="Provide the name of the league")
    @discord.option("channel prefix", description="Provide the shortened version of the league name that should be on the front of channel names (ie. f1_05)")
    async def create_league_category(self, ctx: discord.ApplicationContext, cat_name: str, pre_name: str):

        await ctx.respond("Creating the channels for `" + cat_name + "` league")

        if " " in pre_name:
            pre_name = pre_name.replace(" ", "-")

        admin_overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
        }

        category = await ctx.guild.create_category(cat_name)
        ann_channel = await ctx.guild.create_text_channel(f"{pre_name}-announcements", category=category, overwrites=admin_overwrites)
        await ann_channel.edit(type=ChannelType.news)

        pts_channel = await ctx.guild.create_text_channel(f"{pre_name}-points", category=category, overwrites=admin_overwrites)
        await pts_channel.edit(type=ChannelType.news)

        info_channel = await ctx.guild.create_text_channel(f"{pre_name}-rules-and-info", category=category, overwrites=admin_overwrites)
        await info_channel.edit(type=ChannelType.news)

        await ctx.guild.create_text_channel(f"{pre_name}-sign-up", category=category)

        await ctx.guild.create_text_channel(f"{pre_name}-chat", category=category)

        await ctx.guild.create_text_channel(f"{pre_name}-livery-submissions", category=category)



    @has_permissions(administrator=True)
    @slash_command(name="delete_category", description="Deletes a category and all the channels it has")
    @discord.option("category name", description="Select the category you want to delete", input_type=discord.CategoryChannel)
    @discord.option("are you sure", description="Are you sure you want to delete this category", choices=[True, False])
    async def delete_category(self, ctx: discord.ApplicationContext, category: discord.CategoryChannel, confirm: bool):

        if confirm:
            await ctx.respond("Deleting category...", ephemeral=True)

            for i in category.channels:
                await i.delete(reason=f"Bulk delete command performed by: {ctx.author.name}")
            await category.delete(reason=f"Bulk delete command performed by: {ctx.author.name}")
            await ctx.send("Successfully deleted category")
        else:
            await ctx.respond("Cancelled", ephemeral=True)


    @has_permissions(manage_channels=True)
    @slash_command(name="hide_category", description="Hides league that is completed and moves it to the bottom")
    @discord.option("category name", description="Select the category you want to hide", input_type=discord.CategoryChannel)
    async def hide_category(self, ctx: discord.ApplicationContext, category: discord.CategoryChannel):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.get_role(777534984445231124): discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.get_role(777523593738977301): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        await category.edit(overwrites=overwrites)
        await ctx.respond(f"`{category.name}` hidden successfully")


def setup(bot):
    bot.add_cog(Moderation(bot))
