import logging

from discord.ext import commands

from ..models.player import Player
from ..models.party import Party


class Party_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Form a party or list party members', description='Form a party with one or more other players; usage: `party @Friend1 @Friend2` (if no players specified, get a list of current members)')
    async def party(self, ctx):
        try:
            player = Player(ctx.author)
            mentions = [mention for mention in ctx.message.mentions]
            if len(mentions):
                if player.get_party_id():
                    party = Party(player.get_party_id())
                else:
                    party = Party()
                    party.add_members([ctx.author])
                await ctx.send(party.add_members(mentions))
                logging.debug(f"🥳 New party created!\nMembers: {party.get_members}\nID: {party.get_id}")
            else:
                await ctx.send(str(Party(player.get_party_id())) if player.get_party_id() else "You're not in a party! Start one with `..party @User @User2`")
        except Exception as e:
            logging.exception(str(e))
            await ctx.send("Server error! Unable to complete `party` request. 😞")
    
    @commands.command(brief='Leave your party', description='Leave your current party, if you\'re in one')
    async def leave(self, ctx):
        player = Player(ctx.author)
        party = Party(player.get_party_id())
        msg = party.remove_member(player.get_id())
        player.unset_party_id()
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Party_Cog(bot))
