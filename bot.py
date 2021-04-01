import os, random, string, logging, collections, asyncio, # jsonpickle
from collections import defaultdict
from os import path

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

description = '''A bot to help strangers make words out of letters'''

# set the prefix bot will watch for
bot = commands.Bot(command_prefix='..', description=description)

# make this an environment variable
token = ''

pl_letters = defaultdict(list) # dictionary of lists for letters owned by each player
all_letters = [] # list to store all letters deployed, for testing
valid_words = ['CAT', 'RAT', 'BAT', 'SAT', 'MAT', 'TALL', 'BALL', 'CALL', 'FALL', 'FAR', 'TAR',
               'BAR', 'CAR', 'CAB', 'TAB', 'LAB', 'GNAT', 'TAN', 'CAN', 'BAN', 'RAN', 'BASS',
               'MAN', 'APP', 'TART', 'FART', 'THAT', 'SEEN', 'LANE', 'TEEN', 'TALE', 'TEAL', 'FELL'
               'TELL', 'SET', 'NET', 'EAT', 'BEAT', 'NEAT', 'SEAT', 'TEAR', 'STAR', 'LANE', 'ARE',
               'SELL', 'SALE', 'SEAL', 'LEER', 'STELLAR', 'TREE', 'SEER', 'PEER', 'PEAR', 'APE',
               'TINE', 'SINE', 'SIN', 'NIT', 'RISE', 'LINT', 'TILL', 'SILL', 'TIN', 'TIRE', 'AND',
               'END', 'SAND', 'SEND', 'TEND', 'STAND', 'LET', 'TEN']
words_i_know = frozenset(valid_words) # used to speed up querying
letter_weight = { # each integer = percent chance * 10 to appear, 100 = 10%

    "A": 85, "B": 20, "C": 45, "D": 34, "E": 112, "F": 18, "G": 25, "H": 30, "I": 75, "J": 2,
    "K": 11, "L": 55, "M": 30, "N": 67, "O": 72, "P": 32, "Q": 2, "R": 76, "S": 57, "T": 69, 
    "U": 36, "V": 10, "W": 13, "X": 2, "Y": 18, "Z": 2
}

logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    print('We have logged in as ')
    print(bot.user.display_name)
    print('\nLet''s make some words')

@bot.command(description='For getting new letters')
# give player a random letter, adding to their collection
async def get(ctx):
    player = ctx.author
    letter_rand = await random_letter(player)
    try:
        pl_letters[player].append(letter_rand)
        logging.debug("gave {} to {}".format(letter_rand, player))
        await ctx.send("{}, you can have a {}".format(player, letter_rand))
    except:
        pl_letters[player] = ''
        logging.debug("# Error 3 #: no letters found for {}".format(player))
    all_letters.append(letter_rand)
    return (letter_rand)

@bot.command(description='Find out current letters owned by player', aliases=['curr', 'cu'])
async def current(ctx):
    player = ctx.author
    logging.debug("Fetching letters for {}".format(player))
    try:
        letter_list = pl_letters[player]
        logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    except:
        letter_list = []
    await ctx.send("{} your letters are {}".format(player, str(pl_letters[player])))

@bot.command(description='Make a word')
async def word(ctx, *args):
    player = ctx.author
    word = args[0]
    if word in words_i_know: # is this a word I think is valid
        points = len(word)
        await ctx.send("{} formed the word ""{}"" and scored {} points".format(player, word, points))
        for l in word: # try to remvoe letters in word from player's inventory
            ## TODO: need to check only unique letters, avoid duplicates
            try:
                pl_letters[player].remove(l.upper())
            except:
                await ctx.send("# Error 1 #: Couldn't remove ''{}'' from {}'s letters".format(l, player))
    else:
        await ctx.send("# Error 2 #: I don't know the word ""{}"" yet, sorry".format(word))

@bot.command(description='Find out what letters this bot has given out')
async def show_all(ctx):
    logging.debug("Full letter output requested")
    await ctx.send(str(all_letters))

@bot.command(description='Hello and introductions')
async def hello(ctx):
    player = ctx.author
    await ctx.send("Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(player))

#async def check_letters(letters, player):

# Give a semi-random letter, to help people make words
# TODO: Match proper frequencies for english words, see weight matrix above


async def random_letter(author):
    curr = pl_letters[author]
    l = ''
    r = random.randint(1,12)
    if r == 1 or r == 2:
        l = 'E'
    elif r == 3:
        l = 'A'
    elif r == 4:
        l = 'R'
    elif r == 5:
        l = 'T'
    elif r == 6:
        l = 'N'
    elif r == 7:
        l = 'S'
    elif r == 8:
        l = 'L'
    elif r == 9:
        l = 'I'
    else:
        l = random.choice(string.ascii_uppercase)
    return l

bot.run(token) 