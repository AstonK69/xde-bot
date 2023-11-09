from discord.ext import commands
from discord.commands import slash_command
import discord
from run import bot
import src.load
from src.load import Colours, signed_up_users
from sqlite3 import connect
import re
from discord.ext.commands.core import has_permissions

class XDE(commands.Cog):

    path = f"{__file__}".replace("\\", "/")
    path = path.replace("cogs/commands/xde.py", "data/xde.db")

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

    @staticmethod
    async def check_if_in_db(user: discord.Member):
        con = connect(XDE.path)
        cur = con.cursor()

        result = cur.execute(f"select PlayerID from GT4_People where DiscordID = '{user.id}'")
        if len(result.fetchall()) == 0:
            con.close()
            return False
        else:
            con.close()
            return True

    @staticmethod
    async def matches_regex(id: str):
        if re.search("[0-9]{17}", id):
            return True
        else:
            return False


    @slash_command(name="sign_up", description="Changes peoples nicknames")
    @discord.option("ac_name", description="What is your name on Assetto Corsa")
    @discord.option("steam_id", description="What is your Steam ID (http://vacbanned.com/)")
    @discord.option("custom_livery", description="Are you going to provide your own custom livery",
                    choices=[True, False])
    @discord.option("team_name", description="What is your team name (optional)", required=False)
    async def sign_up(self, ctx, ac_name: str, steam_id: str, custom_livery: bool, team_name="Not provided"):

        if ctx.channel_id == 1171189350797680700: # xde = 762734160330227732, test = 1171189350797680700
            if await self.check_first_message(ctx.author, ctx.channel) is None and await self.check_if_in_db(ctx.author) is False and await self.matches_regex(steam_id) is True:
                if custom_livery is True:
                    await ctx.respond(
                        "Please make sure to send your livery in <#1169965404383354910> as soon as possible",
                        ephemeral=True)
                else:
                    await ctx.respond(
                        "Please tell us which of the premade liveries on the car you would like in <#1169965404383354910>",
                        ephemeral=True)

                con = connect(XDE.path)
                cur = con.cursor()

                cur.execute(f"insert into GT4_People(DiscordID, DiscordName, SteamID, HasLivery, TeamName, Points) values ('{ctx.author.id}', '{ctx.author.name}', '{steam_id}', {custom_livery}, '{team_name}', 0)")
                con.commit()

                con.close()

                src.load.signed_up_users.append(bot.get_user(ctx.author.id))

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

    @has_permissions(administrator=True)
    @slash_command(name="add_points", description="Changes peoples nicknames")
    @discord.option("user", description="Which user do you want to add points too")
    @discord.option("points", description="How many points do you want to add to this users total")
    async def add_points(self, ctx, user: discord.Member, points: int):
        try:
            con = connect(XDE.path)
            cur = con.cursor()

            cur.execute(f"update GT4_People set Points = Points + {points} where DiscordID='{user.id}'")
            con.commit()
            con.close()

            await ctx.respond(f"{points} points added to `{user.name}`", ephemeral=True)
        except:
            await ctx.respond("That user is not signed up to the league", ephemeral=True)



def setup(bot):
    bot.add_cog(XDE(bot))