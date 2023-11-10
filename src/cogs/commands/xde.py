import asyncio

from discord.ext import commands
from discord.commands import slash_command
import discord
from run import bot
import src.load
from src.load import Colours
from sqlite3 import connect
import re
from discord.ext.commands.core import has_permissions


class AttendView(discord.ui.View):

    reacted_yes = []
    reacted_maybe = []
    reacted_no = []

    attend_embed_message: discord.Message
    attend_embed_round: str
    attend_embed_position: int

    @staticmethod
    async def reacted_same_twice(user: discord.Member, pressed_list: list):
        if user in pressed_list:
            pressed_list.remove(user)
            return True
        else:
            pressed_list.append(user)
            return False

    @staticmethod
    async def reacted_to_another(user:discord, list1: list, list2: list):
        if user in list1:
            list1.remove(user)
            return True
        elif user in list2:
            list2.remove(user)
            return True
        else:
            return False

    @staticmethod
    async def update_embed():

        formatted_yes_list = []
        formatted_maybe_list = []
        formatted_no_list = []

        for i in AttendView.reacted_yes:
            formatted_yes_list.append(i.name)
        for i in AttendView.reacted_maybe:
            formatted_maybe_list.append(i.name)
        for i in AttendView.reacted_no:
            formatted_no_list.append(i.name)

        yes_str = "\n".join(formatted_yes_list)
        maybe_str = "\n".join(formatted_maybe_list)
        no_str = "\n".join(formatted_no_list)

        embed = discord.Embed(title=f"XDE Porsche GT4 Challenge Round {AttendView.attend_embed_round}",
                              description="[Live Timings](http://ac.xde.nl:8772/live-timing?server=1) | [Server Link](https://acstuff.ru/s/q:race/online/join?httpPort=9604&ip=89.117.56.93) | [Website](https://xde.nl/)",
                              colour=Colours.standard)

        embed.set_image(
            url=XDE.gt4_track_maps[AttendView.attend_embed_position])

        embed.add_field(name="", value=f"""**```ml
        ‎
        PORSCHE GT4 CHALLENGE ROUND {AttendView.attend_embed_round[0]}
                        ```**""", inline=False)

        embed.add_field(name="", value=f"""```md
> Turning Up‎:
{yes_str}```""")
        embed.add_field(name="", value=f"""```prolog
Possibly:
{maybe_str}```""")
        embed.add_field(name="", value=f"""```ml
Not Turning Up:
{no_str}```""")

        embed.add_field(name="", value="Are you turning up?")

        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')

        await AttendView.attend_embed_message.edit(embed=embed)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
    async def yes_callback(self, button, ctx: discord.Interaction):
        if XDE.check_if_in_db(ctx.user) is True:
            if await AttendView.reacted_same_twice(ctx.user, AttendView.reacted_yes) is True:
                await ctx.response.send_message("Removed from turning up", ephemeral=True)
                # remove from yes list
            else:
                if await AttendView.reacted_to_another(ctx.user, AttendView.reacted_maybe, AttendView.reacted_no) is True:
                    await ctx.response.send_message("See you there!", ephemeral=True)
                    # add to yes list
                else:
                    await ctx.response.send_message("See you there!", ephemeral=True)
                    # add to yes list
            await AttendView.update_embed()
        else:
            await ctx.response.send_message("You are not signed up to the league, do so in <#1169965237932413021>", ephemeral=True)

    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.blurple, emoji="❔")
    async def maybe_callback(self, button, ctx: discord.Interaction):
        if XDE.check_if_in_db(ctx.user) is True:
            if await AttendView.reacted_same_twice(ctx.user, AttendView.reacted_maybe) is True:
                await ctx.response.send_message("Removed from possibly turning up", ephemeral=True)
                # remove from maybe list
            else:
                if await AttendView.reacted_to_another(ctx.user, AttendView.reacted_yes, AttendView.reacted_no) is True:
                    await ctx.response.send_message("You can react to this again (yes/no) if you know whether you will be here or not", ephemeral=True)
                    # add to maybe list
                else:
                    await ctx.response.send_message("You can react to this again (yes/no) if you know whether you will be here or not", ephemeral=True)
                    # add to maybe list
            await AttendView.update_embed()
        else:
            await ctx.response.send_message("You are not signed up to the league, do so in <#1169965237932413021>", ephemeral=True)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="✖")
    async def no_callback(self, button, ctx: discord.Interaction):
        if XDE.check_if_in_db(ctx.user) is True:
            if await AttendView.reacted_same_twice(ctx.user, AttendView.reacted_no) is True:
                await ctx.response.send_message("Removed from not turning up", ephemeral=True)
                # remove from no list
            else:
                if await AttendView.reacted_to_another(ctx.user, AttendView.reacted_yes, AttendView.reacted_maybe) is True:
                    await ctx.response.send_message(
                        "Hopefully we will see you next time", ephemeral=True)
                    # add to no list
                else:
                    await ctx.response.send_message(
                        "Hopefully we will see you next time", ephemeral=True)
                    # add to no list
            await AttendView.update_embed()
        else:
            await ctx.response.send_message("You are not signed up to the league, do so in <#1169965237932413021>", ephemeral=True)

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
    def check_if_in_db(user: discord.Member):
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
            if await self.check_first_message(ctx.author, ctx.channel) is None and self.check_if_in_db(ctx.author) is False:
                if await self.matches_regex(steam_id) is True:
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
                    await ctx.respond("Your steamid does not match the format, it should be 17 characters", ephemeral=True)
            else:
                await ctx.respond("You have already signed up", ephemeral=True)
        else:
            await ctx.respond("Wrong channel genius", ephemeral=True)

    @has_permissions(administrator=True)
    @slash_command(name="add_points_manual", description="Adds points to someone in the league")
    @discord.option("user", description="Which user do you want to add points too")
    @discord.option("points", description="How many points do you want to add to this users total")
    async def add_points_manual(self, ctx, user: discord.Member, points: int):
        try:
            con = connect(XDE.path)
            cur = con.cursor()

            cur.execute(f"update GT4_People set Points = Points + {points} where DiscordID='{user.id}'")
            con.commit()
            con.close()

            await ctx.respond(f"{points} points added to `{user.name}`", ephemeral=True)
        except:
            await ctx.respond("That user is not signed up to the league", ephemeral=True)

    @has_permissions(administrator=True)
    @slash_command(name="round_points_add", description="Goes through all the people who said they were attending and asks for how many points they scored")
    async def round_points_add(self, ctx):

        await ctx.respond("Command started...", ephemeral=True)
        for i in AttendView.reacted_yes:
            await ctx.send(f"How many points did `{i.name}` get?")
            try:
                points = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)

                con = connect(XDE.path)
                cur = con.cursor()

                cur.execute(f"update GT4_People set Points = Points + {int(points.content)} where DiscordID = '{points.author.id}'")
                con.commit()
                con.close()

            except asyncio.TimeoutError as e:
                await ctx.send("You ran out of time to respond")

    gt4_league_rounds = ["1: Barcelona", "2: Palmadera", "3: Brands Hatch", "4: Sebring", "5: Monza", "6: Deep Forest"]
    gt4_track_maps = ["https://cdn.discordapp.com/attachments/764190503867908097/1172589353822867587/outline.png?ex=6560ddef&is=654e68ef&hm=8667be27bb4e86fa6674ed66f64f63f6ab04bea7f83ce166e8c35bd34f5b46ec&",
                      "https://cdn.discordapp.com/attachments/764190503867908097/1172589566197243944/outline.png?ex=6560de22&is=654e6922&hm=bf8b89e8278775d784b46b60cb093a46e5c8590fbf31b20568fc56dab49452c6&",
                      "https://cdn.discordapp.com/attachments/764190503867908097/1172589692894593034/outline.png?ex=6560de40&is=654e6940&hm=2f78b7733243820e938c8e26af153da9dcdfc7a8af707701c882e2c8b4c1a59c&",
                      "https://cdn.discordapp.com/attachments/764190503867908097/1172590347621257216/outline.png?ex=6560dedc&is=654e69dc&hm=eec4cdd2acddf910f9d2dc20a847104a167dd1ddb3479e8b740769ef9de2c39e&",
                      "https://cdn.discordapp.com/attachments/764190503867908097/1172590664689655868/outline.png?ex=6560df28&is=654e6a28&hm=57402e0f0da9500ba9724ad7718ca46f7cefd123136bbf8737a63d347e891624&",
                      "https://cdn.discordapp.com/attachments/764190503867908097/1172590841450209290/outline.png?ex=6560df52&is=654e6a52&hm=9135fc048a7fd37dc88f7b5fdb48dc1728839e2182708c44711fcb699b994ed8&"]

    @has_permissions(administrator=True)
    @slash_command(name="attendance_embed", description="Sends the embed that people can acknowledge (or not) their attendance for the next round")
    @discord.option("league_round", description="What round is coming up?", choices=gt4_league_rounds)
    async def attendance_embed(self, ctx, league_round: str):
        await ctx.respond("Embed sent, you can hide this message.", ephemeral=True)

        position = int(league_round[0]) - 1

        AttendView.attend_embed_round = league_round
        AttendView.attend_embed_position = int(league_round[0]) - 1

        embed = discord.Embed(title=f"""
XDE Porsche GT4 Challenge Round {league_round}""",
                                  description="[Live Timings](http://ac.xde.nl:8772/live-timing?server=1) | [Server Link](https://acstuff.ru/s/q:race/online/join?httpPort=9604&ip=89.117.56.93) | [Website](https://xde.nl/)",
                                  colour=Colours.standard)

        embed.set_image(
            url=XDE.gt4_track_maps[position])

        embed.add_field(name="", value=f"""**```ml
        ‎
        PORSCHE GT4 CHALLENGE ROUND {league_round[0]}
                ```**""", inline=False)

        embed.add_field(name="", value="""```md
> Turning Up‎:```""")
        embed.add_field(name="", value="""```prolog
Possibly:```""")
        embed.add_field(name="", value="""```ml
Not Turning Up:```""")

        embed.add_field(name="", value="Are you turning up?")


        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                             icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')

        AttendView.attend_embed_message = await ctx.send(embed=embed, view=AttendView())

def setup(bot):
    bot.add_cog(XDE(bot))