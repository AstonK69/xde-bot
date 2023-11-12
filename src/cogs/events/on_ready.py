from discord.ext import commands


class on_ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("=======================")
        print("XDE Bot up and running!")
        print("=======================")

def setup(bot):
    bot.add_cog(on_ready(bot))
