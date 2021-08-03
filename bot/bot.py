import os, logging
import google.cloud.logging
from .models.player import Player
from .models.party import Party
from .models.dictionary import Dictionary
from .models.util.string_util import StringUtil

from discord.ext import commands

from dotenv import load_dotenv

description = '''A bot to help strangers make words out of letters'''

if os.environ.get("DEPLOYMENT_CONTEXT", "local") == "gce":
    # start up Google Cloud Logging
    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()
    logging.info("Starting Server...")

load_dotenv(override=True)
token = os.environ["TOKEN"]
lexicon = os.environ.get("LEXICON", "sowpods")  # specify a dictionary; default to SOWPODS

# set the prefix bot will watch for
bot = commands.Bot(command_prefix='..', description=description)

# ensure state storage directory exists
if not os.path.exists(".lws"):
    os.makedirs(".lws")

logging.basicConfig(level=logging.DEBUG)


@bot.event
async def on_ready():
    print('We have logged in as ')
    print(bot.user.display_name)
    print('\nLet''s make some words')


@bot.command(brief='Buy a new letter', description='For getting new letters')
# Players can request a new letter from the bot
# Currently up to 8 letters per player
async def get(ctx):
    player = Player(ctx.author)
    await ctx.send(player.add_letter())


@bot.command(brief='Form a party or list party members', description='Form a party with one or more other players; usage: `party @Friend1 @Friend2` (if no players specified, get a list of current members)')
async def party(ctx, *args):
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
        else:
            await ctx.send(str(Party(player.get_party_id())) if player.get_party_id() else "You're not in a party! Start one with `..party @User @User2`")
    except Exception as e:
        logging.exception(str(e))
        await ctx.send("Server error! Unable to complete `party` request. 😞")


@bot.command(brief='Leave your party', description='Leave your current party, if you\'re in one')
async def leave(ctx):
    player = Player(ctx.author)
    party = Party(player.get_party_id())
    msg = party.remove_member(player.get_id())
    player.unset_party_id()
    await ctx.send(msg)


@bot.command(brief='Get party\'s letters', description='Get all letters held by members of your party', aliases=['curr', 'cu'])
async def letters(ctx):
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


@bot.command(brief='Use letters to score a word', description='Make a word out of letters you have in hand or party')
async def word(ctx, *args):
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


@bot.command(brief='Show me my progress', description='Get my score')
async def score(ctx):
    player = Player(ctx.author)
    await ctx.send(f"{player}, your score is {player.get_score()}, you have {player.get_money()} glyphs to spend")


@bot.command(brief='Greetings stranger', description='Hello and introductions')
async def hello(ctx):
    player = ctx.author
    await ctx.send("Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(player))


@bot.command(brief='Kick-start your LWS play', description='Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start!')
async def cheat(ctx):
    if len(ctx.message.mentions):
        players = [Player(mentioned) for mentioned in ctx.message.mentions]
    else:
        players = [Player(ctx.author)]
    for player in players:
        player.cheat()
    await ctx.send("Okay cheaty! You cheated.")


@bot.command(breif="Shuffles your hand", description="Shuffles your hand!")
async def shuffle(ctx):
    player = Player(ctx.author)
    await ctx.send(player.shuffle_letters())


@bot.command(brief='[debug] Clear your hand', description='Remove all letters from your hand. For testing/debugging purposes.')
async def purge(ctx):
    player = Player(ctx.author)
    await ctx.send(player.purge())

def start():
    bot.run(token)