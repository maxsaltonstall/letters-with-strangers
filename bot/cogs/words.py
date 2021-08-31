import os
import logging

from discord.ext import commands
from dotenv import load_dotenv

from ..models.player import Player
from ..models.party import Party
from ..models.dictionary import Dictionary
from ..models.util.string_util import StringUtil

load_dotenv(override=True)
lexicon = os.environ.get("LEXICON", "sowpods")


class Words_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief="Buy a new letter", description="For getting new letters")
    async def get(self, ctx):
        player = Player(ctx.author)
        await ctx.send(player.add_letter())

    @commands.command(brief="Buy a new vowel, but for more money", description="For getting new vowels only")
    async def getvowel(self, ctx):
        cost = 5
        player = Player(ctx.author)
        if player.check_money(cost):
            player.deduct_money(cost)
            await ctx.send(player.add_letter(letter_type='vowel'))
        else:
            await ctx.send(f"Sorry, you can't affort a vowel. You need {cost} glyphs but you only have {player.get_money()}")

    @commands.command(brief='Get party\'s letters', description='Get all letters held by members of your party', aliases=['curr', 'cu'])
    async def letters(self, ctx):
        player = Player(ctx.author)
        if(player.get_party_id()):
            party = Party(player.get_party_id())
            party_letters = party.get_letters()
            if len(party_letters):
                msg = f"Your party has the letters {StringUtil.readable_list(party.get_letters(), 'bold')}"
            else:
                msg = "Your party has no letters! To get some letters, the members can use `..get`"
        else:
            letters = player.get_letters()
            if len(letters):
                msg = f"You have the letters {StringUtil.readable_list(player.get_letters(), 'bold')}"
            else:
                msg = "You have no letters. Get some with `..get`!"
        await ctx.send(msg)
    
    @commands.command(brief='Use letters to score a word', description='Make a word out of letters you have in hand or party')
    async def word(self, ctx, *args):
        if not len(args):
            await ctx.send("Please specify a word, like `..word orthography`")
        else:
            word = args[0].upper()
            message = await ctx.send(f"Checking dictionary for {word}…")
            try:
                if len(args):
                    dictionary = Dictionary(lexicon)
                    player = Player(ctx.author)
                    party_id = player.get_party_id()
                    if not party_id:
                        party = Party()
                        party.add_members([ctx.author])
                        party_id = party.get_id()
                    await message.edit(content=Party(party_id).make_word(word, dictionary))

            except Exception as e:
                logging.exception(str(e))
                await ctx.send("Server error! Unable to form word. 😞")

    @commands.command(brief="Shuffles your hand", description="Shuffles your hand!")
    async def shuffle(self, ctx):
        player = Player(ctx.author)
        await ctx.send(player.shuffle_letters())

    @commands.command(brief='[debug] Clear your hand', description='Remove all letters from your hand. For testing/debugging purposes.')
    async def purge(self, ctx):
        player = Player(ctx.author)
        await ctx.send(player.purge())


def setup(bot):
    bot.add_cog(Words_Cog(bot))
