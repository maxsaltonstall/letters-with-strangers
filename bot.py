import os, logging
from player import Player
from letter import Letter
from dictionary import Dictionary

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv(override=True)
token = os.environ["TOKEN"]
lexicon = os.environ.get("LEXICON", "sowpods")  # specify a dictionary; default to SOWPODS

description = '''A bot to help strangers make words out of letters'''

# set the prefix bot will watch for
bot = commands.Bot(command_prefix='..', description=description)

all_letters = []  # list to store all letters deployed, for testing

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
    letter_rand = Letter.random_letter()
    await ctx.send(player.add_letter(letter_rand))
    all_letters.append(letter_rand)


@bot.command(brief='See what letters you have now', description='Find out current letters owned by player', aliases=['curr', 'cu'])
async def current(ctx):
    player = Player(ctx.author)
    logging.debug("Fetching letters for {}".format(player))
    try:
        letter_list = player.get_letters()
        logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    except Exception as e:
        logging.error(f"# Error 5 #: unable to fetch letters for {player.get_username()}")
        logging.exception(str(e))
    await ctx.send("{} your letters are {}".format(player, str(letter_list)))


@bot.command(brief='Use letters to score a word', description='Make a word out of letters you have in hand or party')
async def word(ctx, *args):
    player = Player(ctx.author)
    word = args[0].upper()
    dictionary = Dictionary(lexicon)
    await ctx.send(player.make_word(word, dictionary))


@bot.command(brief='Show me my progress', description='Get my score')
async def score(ctx):
    player = Player(ctx.author)
    await ctx.send(f"{player}, your score is {player.get_score()}, and you have {player.get_money()} glyphs to spend")


@bot.command(brief='All the letters bot has given', description='Find out what letters this bot has given out')
async def show_all(ctx):
    logging.debug("Full letter output requested")
    await ctx.send(str(all_letters))


@bot.command(brief='Greetings stranger', description='Hello and introductions')
async def hello(ctx):
    player = ctx.author
    await ctx.send("Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(player))


@bot.command(brief='Kick-start your LWS play', description='Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start!')
async def cheat(ctx):
    player = Player(ctx.author)
    await ctx.send(player.cheat())


@bot.command(breif="Shuffles your hand", description="Shuffles your hand!")
async def shuffle(ctx):
    player = Player(ctx.author)
    await ctx.send(player.shuffle_letters())


@bot.command(brief='[debug] Clear your hand', description='Remove all letters from your hand. For testing/debugging purposes.')
async def purge(ctx):
    player = Player(ctx.author)
    await ctx.send(player.purge())

bot.run(token)
