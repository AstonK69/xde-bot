from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands.core import has_permissions
from src.load import Colours

activity_types = ["Playing", "Streaming", "Watching", "Listening"]
a_dict = {"Playing": 0,
          "Streaming": 1,
          "Watching": discord.ActivityType.watching,
          "Listening": discord.ActivityType.listening}


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def check_first_message(user: discord.Member, channel: discord.TextChannel):

        counter = 0

        async for i in channel.history(limit=100):
            for j in i.embeds:
                if user.name in j.title:
                    counter += 1

        if counter != 0:
            return 1
        else:
            return None

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="ping", description="Sends the bots latency in ms")
    async def ping(self, ctx):
        embed = discord.Embed(
            description=f"The bot responded in {round(self.bot.latency * 1000)}ms",
            colour=Colours.standard)
        await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="say", description="Repeats a message")
    async def say(self, ctx, text: str):
        await ctx.respond('Message sent, you can now hide this message', ephemeral=True)
        await ctx.send(text)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Repeats a message in an embed")
    @discord.option("title", description="Provide a title")
    @discord.option("message", description="Provide a message")
    async def saye(self, ctx, title: str, message: str):
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
        try:
            await user.edit(nick=name)
            if name == "":
                output = f"Changed {user.name}'s nickname back to normal"
            else:
                output = f"Changed {user.name}'s nickname to {name}"

            await ctx.respond(output)
        except Exception as e:
            await ctx.respond(e)


    @slash_command(name="sign_up", description="Changes peoples nicknames")
    @discord.option("ac_name", description="What is your name on Assetto Corsa")
    @discord.option("steam_id", description="What is your Steam ID (http://vacbanned.com/)")
    @discord.option("custom_livery", description="Are you going to provide your own custom livery", choices=["Yes", "No"])
    @discord.option("team_name", description="What is your team name (optional)", required=False)
    async def sign_up(self, ctx, ac_name: str, steam_id: str, custom_livery: str, team_name = "Not provided"):

        if ctx.channel_id == 762734160330227732:
            if await self.check_first_message(ctx.author, ctx.channel) is None:
                if custom_livery == "Yes":
                    await ctx.respond("Please make sure to send your livery in <#1169965404383354910> as soon as possible", ephemeral=True)
                else:
                    await ctx.respond("Please tell us which of the premade liveries on the car you would like in <#1169965404383354910>", ephemeral=True)

                embed = discord.Embed(title=f"New sign up: {ctx.author.name}", colour=Colours.standard, description=f"""
Discord User: {ctx.author.mention}
AC Name: `{ac_name}`
Steam ID: `{steam_id}`
Team: `{team_name}`
Livery: `{custom_livery}`
            """)
                embed.set_thumbnail(url=str(ctx.author.display_avatar))
                embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                                 icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
                await ctx.send(embed=embed)
            else:
                await ctx.respond("You have already signed up", ephemeral=True)
        else:
            await ctx.respond("Wrong channel genius", ephemeral=True)



def setup(bot):
    bot.add_cog(Misc(bot))
