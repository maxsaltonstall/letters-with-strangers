import logging

from discord.ext import commands

from ..models.player import Player
from ..models.party import Party
from ..models.dictionary import Dictionary
from ..models.util.string_util import StringUtil

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Show me my score', description='Get my score')
    async def score(self, ctx):
        player = Player(ctx.author)
        await ctx.send(f"{player}, your score is {player.get_score()}, you have {player.get_money()} glyphs to spend")

    @commands.command(brief='Show me my progress', description='Get my full profile and progress', aliases=['pr', 'profile', 'prog'])
    async def progress(self, ctx):
        player = Player(ctx.author)
        await player.show_progress(ctx)

def setup(bot):
    bot.add_cog(Player(bot))