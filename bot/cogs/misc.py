from discord.ext import commands

from ..models.player import Player


class Misc_Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Greetings stranger', description='Hello and introductions')
    async def hello(self, ctx):
        player = ctx.author
        await ctx.send("Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game.\nStart by using ..get to have the bot give you a letter, and you can use ..party to join with others players.\nOnce you have a group and some letters, use ..word to form a word and score points!".format(player))

    @commands.command(brief='Kick-start your LWS play', description='Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start!')
    async def cheat(self, ctx):
        if len(ctx.message.mentions):
            players = [Player(mentioned) for mentioned in ctx.message.mentions]
        else:
            players = [Player(ctx.author)]
        for player in players:
            player.cheat()
        await ctx.send("Okay cheaty! You cheated.")


def setup(bot):
    bot.add_cog(Misc_Cogs(bot))
