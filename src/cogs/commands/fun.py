from discord.ext import commands
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
import discord
import pyfiglet
from random import randint
from src.load import Colours


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends ascii text")
    @discord.option("message", description="Choose your message")
    @discord.option("font", description="Choose your font, go to the pyfiglet github to find the fonts", default="big")
    async def ascii(self, ctx, *, message: str, font: str):
        result = pyfiglet.figlet_format(message, font=font)
        await ctx.respond(content=f"```{result}```")

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Gets avatar of a user")
    @discord.option("user", description="Choose a member")
    async def avatar(self, ctx, user: discord.Member):
        pfp = user.display_avatar

        embed = discord.Embed(title=f"{user.name}'s Avatar", description=f"[Download]({pfp.url})",
                              color=Colours.standard)
        embed.set_image(url=pfp.url)
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston")

        await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Sends someones iq!")
    @discord.option("user", description="Choose a user")
    async def iq(self, ctx, user: discord.Member):
        coolpeople = [760602301790158868]
        badpeople = [940014203937366016]

        if user.id in coolpeople:
            embed = discord.Embed(
                description=f"{user.name}'s iq is ∞",
                colour=Colours.standard)
        elif user.id in badpeople:
            embed = discord.Embed(
                description=f"{user.name}'s iq is 0",
                colour=Colours.standard)
        else:
            embed = discord.Embed(
                description=f"{user.name}'s iq is {randint(0, 200)}",
                colour=Colours.standard)

        await ctx.respond(embed=embed)

    @slash_command(description="Sends info about a user")
    @discord.option("user", description="Choose a member")
    async def whois(self, ctx, *, user: discord.Member):
        roles = "None"
        if len(user.roles) > 1:
            roles = "".join(f"{i.mention} " for i in user.roles[1:])

        time = user.created_at
        date = f"{time.day}/{time.month}/{time.year} {time.hour:02d}:{time.minute:02d}.{time.second:02d} UTC"

        jointime = user.joined_at
        datejoin = f"{jointime.day}/{jointime.month}/{jointime.year} {jointime.hour:02d}:{jointime.minute:02d}.{jointime.second:02d} UTC"

        embed = discord.Embed(title=f"{user.name}",
                              description=f"""
User: {user.mention}
ID: `{user.id}`
Created At: `{date}`
Bot: `{user.bot}`
Joined At: `{datejoin}`
Nickname: `{user.nick}`
Roles:
{roles}
""", color=Colours.standard)
        embed.set_thumbnail(url=str(user.display_avatar))
        embed.set_footer(text=f"Xtreme Dutch Elite ・ 2023 | Created by Aston",
                         icon_url='https://cdn.discordapp.com/attachments/940889123437309972/1168232344256258058/smaller_xde_logo.png?ex=65510427&is=653e8f27&hm=5f07726900ba157438dc6da3be2bcd10db6e5e3daa9825e4814dd75ff0fa677d&')
        await ctx.respond(embed=embed)

    @cooldown(1, 3, BucketType.user)
    @slash_command(description="Evaluates text provided")
    @discord.option("expression", description="Enter your expression to evaluate")
    async def evaluate(self, ctx, expression: str):
        try:
            out = str(eval(expression))
            embed = discord.Embed(colour=Colours.standard)
            embed.add_field(name="Input", value=expression, inline=False)
            embed.add_field(name="Output", value=out, inline=False)
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"{e}, try adding multiplication (*) signs before any brackets")

    @slash_command(description="Game of tic tac toe!")
    async def tictactoe(self, ctx):
        await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

def setup(bot):
    bot.add_cog(Fun(bot))
