import os, random, string, logging, jsonpickle

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
               'FIT', 'SIT', 'TIT', 'TAT', 'PAT', 'STALL', 'TEST', 'SEE', 'SEA', 'TEE', 'TEA', 'LEE',
               'TEAT', 'SEAR']
words_i_know = frozenset(valid_words)  # used to speed up querying to see if word exists
letter_weight = {  # each integer = percent chance * 10 to appear, 100 = 10%

    "A": 85, "B": 20, "C": 45, "D": 34, "E": 112, "F": 18, "G": 25, "H": 30, "I": 75, "J": 2,
    "K": 11, "L": 55, "M": 30, "N": 67, "O": 72, "P": 32, "Q": 2, "R": 76, "S": 57, "T": 69,
    "U": 36, "V": 10, "W": 13, "X": 2, "Y": 18, "Z": 2
}

# ensure state storage directory exists
if not os.path.exists(".lws"):
    os.makedirs(".lws")

logging.basicConfig(level=logging.DEBUG)


@bot.event
async def on_ready():
    print('We have logged in as ')
    print(bot.user.display_name)
    print('\nLet''s make some words')


players = {}

class Player:

    def __init__(self, user):
        
        self.name = format_name(user)
        self.statefile = f".lws/{self.name}.json"
        
        try:
            with open(self.statefile,'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        except FileNotFoundError as e:
            logging.debug(f"statefile not found; initializing statefile for {self.name}")
            self.state = {}
            self.state["username"] = user.name
            self.state["letters"] = []
            self.state["score"] = 0
            self.save_state()

    def get_letters(self):
        return self.state["letters"]

    def add_letter(self, letter):
        self.state["letters"].append(letter)
        self.save_state()

    def cheat(self):
        try:
            self.remove_all_letters()
            for ltr in ["E", "A", "S", "T", "L", "N", "R"]:
                self.add_letter(ltr)
            return("Your hand is now: E, A, S, T, L, N, and R!")
        except:
            logging.error("# Error 4 #: Error when cheating in letters")
            return("Unable to help you cheat, cheaty!")

    def remove_letter(self, letter):
        self.state["letters"].remove(letter.upper())
        self.save_state()

    def remove_letters(self, letters):
        for letter in letters:
            self.remove_letter(letter)

    def remove_all_letters(self):
        self.state["letters"] = []
        self.save_state()

    def num_letters(self):
        return len(self.state["letters"])

    def get_username(self):
        return self.state["username"]

    def add_points(self, points):
        self.state["score"] += points
        self.save_state()

    def get_score(self):
        return self.state["score"]

    def save_state(self):
        pickled = jsonpickle.encode(self.state)
        with open(self.statefile,'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def __str__(self):
        return self.get_username()


def format_name(user):
    return f"{user.name}#{user.discriminator}"


@bot.command(description='For getting new letters')
# Players can request a new letter from the bot
# Currently up to 8 letters per player
async def get(ctx):
    player = Player(ctx.author)
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
        except Exception as e:
            logging.error("# Error 3 #: no letters found for {}".format(username))
            logging.exception(str(e))
        all_letters.append(letter_rand)
        return (letter_rand)


@bot.command(description='Find out current letters owned by player', aliases=['curr', 'cu'])
async def current(ctx):
    player = Player(ctx.author)
    logging.debug("Fetching letters for {}".format(player))
    try:
        letter_list = player.get_letters()
        logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    except:
        letter_list = []
    await ctx.send("{} your letters are {}".format(player, str(letter_list)))


@bot.command(description='Make a word')
async def word(ctx, *args):
    player = Player(ctx.author)
    word = args[0].upper()
    if word in words_i_know:  # is this a word I think is valid
        points = len(word)
        player.add_points(points)
        await ctx.send("{} formed the word ""{}"" and scored {} points".format(player, word, points))
        for ltr in word:  # try to remvoe letters in word from player's inventory
            ## TODO: need to check only unique letters, avoid duplicates
            try:
                player.remove_letter(ltr)
            except:
                msg = f"# Error 1 #: Couldn't remove '{ltr}' from {player}'s letters"
                logging.error(msg)
                await ctx.send(msg)
    else:
        await ctx.send("# Error 2 #: I don't know the word ""{}"" yet, sorry".format(word))


@bot.command(description='Get my score')
async def score(ctx):
    player = Player(ctx.author)
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
    player = Player(ctx.author)
    await ctx.send(player.cheat())


# Give a semi-random letter, to help people make words
# TODO: Match proper frequencies for english words, see weight matrix above
async def random_letter():
    ltr = ''
    r = random.randint(1, 12)
    if r == 1 or r == 2:
        ltr = 'E'
    elif r == 3:
        ltr = 'A'
    elif r == 4:
        ltr = 'R'
    elif r == 5:
        ltr = 'T'
    elif r == 6:
        ltr = 'N'
    elif r == 7:
        ltr = 'S'
    elif r == 8:
        ltr = 'L'
    elif r == 9:
        ltr = 'I'
    else:
        ltr = random.choice(string.ascii_uppercase)
    return ltr

bot.run(token)
