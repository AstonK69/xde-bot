from datetime import datetime, timedelta
from discord.ext import commands
import discord
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from discord.ext import tasks
from sqlite3 import connect
import re
import pytz
import asyncio

def check_existing_entry(date: str, time: str):
    path = f"{__file__}".replace("\\", "/")
    path = path.replace("cogs/commands/update.py", "data/sauce_market.db")

    con = connect(path)
    cur = con.cursor()
    rows = cur.execute(f"select Date, Time from Sauces").fetchall()
    for i in rows:
        if i[0] == date and i[1] == time:
            return True
    return False


class Saucer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reminder.start()
        self.path = f"{__file__}".replace("\\", "/")
        self.path = self.path.replace("cogs/commands/saucer.py", "data/sauce_market.db")
        self.graph_path = self.path.replace("sauce_market.db", "graph.png")

    sauces = ["Salsa", "Hot Sauce", "Guacamole", "Pico de Gallo", "Chipotle Mayo"]

    @tasks.loop(minutes=1)
    async def reminder(self):
        now = datetime.now()
        if now.minute == 0:
            channel = self.bot.get_channel(1124630222302617710)
            await channel.send("<@760602301790158868> <@940014203937366016> The Sauce Market has updated!")

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="graph", description="Updates the sauce market prices")
    @discord.option("sauce", description="Do you want to see an individual sauce?", required=False, choices=sauces)
    @discord.option("time", description="How much of the sauces history do you want to see? (x days, default 7)", required=False)
    async def graph(self, ctx: discord.ApplicationContext, sauce="All", time=7):
        con = connect(self.path)
        cur = con.cursor()

        hours = int(time) * 24

        x = []
        salsa = []
        hotsauce = []
        guacamole = []
        pico_de_gallo = []
        chipotle_mayo = []

        rows = cur.execute("select * from Sauces").fetchall()
        for point in rows:
            temp = f"{point[1]} {point[2][:-3]}"
            temp = datetime.strptime(temp, '%Y-%m-%d %H:%M')
            x.append(temp)
            salsa.append(int(point[3]) if point[3] != '' or None else np.nan)
            hotsauce.append(int(point[4]) if point[4] != '' or None else np.nan)
            guacamole.append(int(point[5]) if point[5] != '' or None else np.nan)
            pico_de_gallo.append(int(point[6]) if point[6] != '' or None else np.nan)
            chipotle_mayo.append(int(point[7]) if point[7] != '' or None else np.nan)

        con.close()

        x = x[-hours:]
        salsa = salsa[-hours:]
        hotsauce = hotsauce[-hours:]
        guacamole = guacamole[-hours:]
        pico_de_gallo = pico_de_gallo[-hours:]
        chipotle_mayo = chipotle_mayo[-hours:]

        sauce_lists = {"All": True, "Salsa": salsa, "Hot Sauce": hotsauce, "Guacamole": guacamole,
                       "Pico de Gallo": pico_de_gallo, "Chipotle Mayo": chipotle_mayo}
        sauce_colours = {"Salsa": "#ff0000", "Hot Sauce": "#5e0000", "Guacamole": "#11ff00", "Pico de Gallo": "#bf00ff",
                         "Chipotle Mayo": "#ffbe73"}
        

        plt.title(f'Sauce Market Trends (Past {time} Days)')
        plt.xlabel('Time (Days)')
        plt.ylabel('Price ($)')
        plt.tight_layout()
        plt.autoscale()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:00'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())

        if sauce_lists[sauce] is True:
            plt.plot(x, salsa, color='#ff0000', label='Salsa')
            plt.plot(x, hotsauce, color='#5e0000', label='Hot Sauce')
            plt.plot(x, guacamole, color='#11ff00', label='Guacamole')
            plt.plot(x, pico_de_gallo, color='#bf00ff', label='Pico de Gallo')
            plt.plot(x, chipotle_mayo, color='#ffbe73', label='Chipotle Mayo')
        else:
            plt.plot(x, sauce_lists[sauce], color=sauce_colours[sauce], label=sauce)

        plt.gcf().autofmt_xdate()
        plt.legend(fontsize='xx-small')
        plt.savefig(self.graph_path, bbox_inches='tight')
        plt.clf()

        with open(self.graph_path, 'rb') as f:
            image = discord.File(f)
            await ctx.respond(file=image)

    @cooldown(1, 3, BucketType.user)
    @slash_command(name="update_prices", description="Updates the sauce market prices")
    async def update_prices(self, ctx: discord.ApplicationContext):
        embed_message = self.bot.get_message(ctx.channel.last_message_id)

        prices = re.findall(r'\$(\d+)\s*\|', embed_message.embeds[0].description)
        cur_time = datetime.now(pytz.timezone("UTC"))
        date = cur_time.strftime('%Y-%m-%d')
        time = cur_time.strftime('%H:00')

        if len(prices) != 5:
            await ctx.respond('The regex is still not right there is more than 5 prices in the list')
        elif check_existing_entry(date, time) is False:
            con = connect(self.path)
            con.cursor().execute(
                f"insert into Sauces(Date, Time, Salsa, Hotsauce, Guacamole, Pico_de_gallo, Chipotle_mayo) values ('{date}', '{time}', '{prices[0]}', '{prices[1]}', '{prices[2]}', '{prices[3]}', '{prices[4]}')")
            con.commit()
            con.close()

            await ctx.respond("Updated the sauces")
        else:
            await ctx.respond("The current hours sauce prices have already been updated in my database!")


def setup(bot):
    bot.add_cog(Saucer(bot))
