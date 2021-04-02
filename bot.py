import os, random, logging, string

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.environ["TOKEN"]

HANDLIMIT = 8

description = '''A bot to help strangers make words out of letters'''

# set the prefix bot will watch for
bot = commands.Bot(command_prefix='..', description=description)

all_letters = []  # list to store all letters deployed, for testing
# TODO: replace with a real and complete word list, maybe scrabble? https://www.wordgamedictionary.com/sowpods/
valid_words = ['CAT', 'RAT', 'BAT', 'SAT', 'MAT', 'TALL', 'BALL', 'CALL', 'FALL', 'FAR', 'TAR',
               'BAR', 'CAR', 'CAB', 'TAB', 'LAB', 'GNAT', 'TAN', 'CAN', 'BAN', 'RAN', 'BASS',
               'MAN', 'APP', 'TART', 'FART', 'THAT', 'SEEN', 'LANE', 'TEEN', 'TALE', 'TEAL', 'FELL'
               'TELL', 'SET', 'NET', 'EAT', 'BEAT', 'NEAT', 'SEAT', 'TEAR', 'STAR', 'LANE', 'ARE',
               'SELL', 'SALE', 'SEAL', 'LEER', 'STELLAR', 'TREE', 'SEER', 'PEER', 'PEAR', 'APE',
               'TINE', 'SINE', 'SIN', 'NIT', 'RISE', 'LINT', 'TILL', 'SILL', 'TIN', 'TIRE', 'AND',
               'END', 'SAND', 'SEND', 'TEND', 'STAND', 'LET', 'TEN', 'RITE', 'BITE', 'SITE', 'LIT',
               'FIT', 'SIT', 'TIT', 'TAT', 'PAT', 'STALL']
words_i_know = frozenset(valid_words)  # used to speed up querying to see if word exists
letter_weight = {  # each integer = percent chance * 10 to appear, 100 = 10%

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


players = {}


class Player:

    def __init__(self, user):
        self.username = user.name
        self.letters = []
        self.score = 0

    def get_letters(self):
        return self.letters

    def add_letter(self, letter):
        self.letters.append(letter)

    def add_letters(self, letters):
        for letter in letters:
            self.letters.append(letter)

    def remove_letter(self, letter):
        self.letters.remove(letter)

    def remove_letters(self, letters):
        for letter in letters:
            self.letters.remove(letter)

    def num_letters(self):
        return len(self.letters)

    def get_username(self):
        return self.username

    def add_points(self, points):
        self.score += points

    def get_score(self):
        return self.score

    def __str__(self):
        return self.get_username()


def load_player(user):
    if not format_name(user) in players:
        players[format_name(user)] = Player(user)

    return players[format_name(user)]


def format_name(user):
    return f"{user.name}#{user.discriminator}"


@bot.command(description='For getting new letters')
# Players can request a new letter from the bot
# Currently up to 8 letters per player
async def get(ctx):
    player = load_player(ctx.author)
    username = player.get_username()
    if player.num_letters() >= HANDLIMIT:
        await ctx.send("{}, you already have a full hand of letters".format(username))
        return
    else:
        letter_rand = await random_letter()
        try:
            player.add_letter(letter_rand)
            logging.debug("gave {} to {}".format(letter_rand, username))
            await ctx.send("{}, you can have a {}".format(username, letter_rand))
        except:
            logging.debug("# Error 3 #: no letters found for {}".format(username))
        all_letters.append(letter_rand)
        return (letter_rand)


@bot.command(description='Find out current letters owned by player', aliases=['curr', 'cu'])
async def current(ctx):
    player = load_player(ctx.author)
    logging.debug("Fetching letters for {}".format(player))
    try:
        letter_list = player.get_letters()
        logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    except:
        letter_list = []
    await ctx.send("{} your letters are {}".format(player, str(letter_list)))


@bot.command(description='Make a word')
async def word(ctx, *args):
    player = load_player(ctx.author)
    word = args[0].upper()
    if word in words_i_know:  # is this a word I think is valid
        points = len(word)
        player.add_points(points)
        await ctx.send("{} formed the word ""{}"" and scored {} points".format(player, word, points))
        for ltr in word:  # try to remvoe letters in word from player's inventory
            ## TODO: need to check only unique letters, avoid duplicates
            try:
                player.remove_letter(ltr.upper())
            except:
                await ctx.send("# Error 1 #: Couldn't remove ''{}'' from {}'s letters".format(ltr, player))
    else:
        await ctx.send("# Error 2 #: I don't know the word ""{}"" yet, sorry".format(word))


@bot.command(description='Get my score')
async def score(ctx):
    player = load_player(ctx.author)
    await ctx.send(f"{player}, your score is {player.get_score()}")


@bot.command(description='Find out what letters this bot has given out')
async def show_all(ctx):
    logging.debug("Full letter output requested")
    await ctx.send(str(all_letters))


@bot.command(description='Hello and introductions')
async def hello(ctx):
    player = ctx.author
    await ctx.send("Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(player))


@bot.command(description='Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start!')
async def cheat(ctx):
    player = ctx.author
    game_player = load_player(player)
    try:
        game_player.add_letters(["E", "A", "S", "T", "L", "N", "R"])
    except:
        logging.debug("# Error 3 #: Error when cheating in letters")
    await ctx.send("You got the letters E, A, S, T, L, N, and R!")
# async def check_letters(letters, player):


# Give a semi-random letter, to help people make words
# TODO: Match proper frequencies for english words, see weight matrix above
async def random_letter():
    ltr = random.choice(string.ascii_uppercase)

bot.run(token)
