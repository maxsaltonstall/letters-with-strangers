import os, random, string, logging, collections, asyncio, jsonpickle
from collections import defaultdict
from os import path

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

description = """A bot to help strangers make words out of letters"""

# set the prefix bot will watch for

bot = commands.Bot(command_prefix="..", description=description)

# make this an environment variable
token = os.environ["TOKEN"]

pl_letters = defaultdict(list)  # dictionary of lists for letters owned by each player
all_letters = []  # list to store all letters deployed, for testing


class Game:
    # game state is stored in a JSON file in folder `.lws` (which is .gitignore'd)
    # TODO: create alternative cloud-backed storage mechanism
    statefile = ".lws/gamestate.json"

    def save(self):
        pickled = jsonpickle.encode(self.state)
        with open(self.statefile,'w') as statefile:
            statefile.write(pickled)
            statefile.close()
        
    def load(self):
        if path.exists(self.statefile):
            logging.debug("FILE EXISTS")
            with open(self.statefile,'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
            logging.debug(self.state)
        else:
            self.state = {}
            self.state["pl_letters"] = defaultdict(list) # dictionary of lists for letters owned by each player
            self.state["all_letters"] = [] # list to store all letters deployed, for testing

    def get_player_letters(self, player):
        return self.state["pl_letters"][format_player_id(player)]

    def add_player_letter(self, player, letter):
        self.state["pl_letters"][format_player_id(player)].append(letter)
        self.state["all_letters"].append(letter)

    def get_all_letters(self):
        if len(self.state["all_letters"]) == 0:
            return("You have no letters!")
        elif len(self.state["all_letters"]) == 1:
            return("You have 1 letter, which is " + self.state["all_letters"][0] + ".")
        else:
            return("You have the letters " + str(" and ".join([", ".join(self.state["all_letters"][:-1]),self.state["all_letters"][-1]] if len(self.state["all_letters"]) > 2 else self.state["all_letters"])) + ".")


logging.basicConfig(level=logging.DEBUG)

def format_player_id(player):
    return f"{player.name}#{player.discriminator}"

@bot.event
async def on_ready():
    print("We have logged in as ")
    print(bot.user.display_name)
    print("\nLet" "s make some words")


"""
@bot.event
async def on_message(message):
    response = str('')
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        response = 'Hi there, want some letters?'

    if message.content.startswith('letter'):
        new_letter = await give_letter(message.author)
        response = 'Your letter is: ' + new_letter

    if message.content.startswith('my letter'):
        logging.debug("Calling current_letters")
        response = await current_letters(message.author)

    if message.content.startswith('all letter'):
        response = await show_all_letter():

    if message.content.startswith('use letter'):
        response = 'I''m still learning how to make words'

    if message.content.startswith('word'):
        response = 'you want to make a word, but I don''t know how yet'

    if response:
        await message.channel.send(response)
"""


@bot.command(description="For getting new letters")
# give player a random letter, adding to their collection
async def get(ctx):
    game = Game()
    game.load()
    player = ctx.author
    letter_rand = random.choice(string.ascii_uppercase) # TODO: break into function, fix probability
    game.add_player_letter(player, letter_rand)
    logging.debug("gave {} to {}".format(letter_rand, player))
    await ctx.send("Hi {}, you can have a {}".format(player, letter_rand))
    game.save()
    return letter_rand


@bot.command(description="Find out current letters owned by player")
async def current(ctx):
    game = Game()
    game.load()
    player = ctx.author
    logging.debug("Fetching letters for {}".format(player))
    letter_list = game.get_player_letters(player)
    logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    await ctx.send("{} your letters are {}".format(player, str(letter_list)))


@bot.command(description="Find out what letters this bot has given out")
async def show_all(ctx):
    game = Game()
    game.load()
    logging.debug("Full letter output requested")
    await ctx.send(game.get_all_letters())

@bot.command(description='Hello and introductions')
async def hello(ctx):
    player = ctx.author
    await ctx.send(
        "Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(
            player
        )
    )


# async def check_letters(letters, player):

bot.run(token)
