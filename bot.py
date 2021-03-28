import os, random, string, logging, collections, asyncio, pickle
from collections import defaultdict

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

description = """A bot to help strangers make words out of letters"""

# set the prefix bot will watch for
bot = commands.Bot(
    command_prefix="..", description=description)

# make this an environment variable
token = os.environ["TOKEN"]

pl_letters = defaultdict(list)  # dictionary of lists for letters owned by each player
all_letters = []  # list to store all letters deployed, for testing

# TODO: factor out into a separate file
class Game:
    state = {}
    state["pl_letters"] = defaultdict(   list
    )  # dictionary of lists for letters owned by each player
    state["all_letters"] = []  # list to store all letters deployed, for testing

    def save(self):
        print("TODO: save to file")

    def load(self):
        print("TODO: load from file")


logging.basicConfig(level=logging.DEBUG)


@bot.event
async def on_ready():
    print("We have logged in as ")
    print(
        bot.user.display_name
    )
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
    letter_rand = random.choice(
        string.ascii_uppercase
    )  # TODO: break into function, fix probability
    player = ctx.author
    try:
        game.state["pl_letters"][player].append(letter_rand)
        logging.debug("gave {} to {}".format(
            letter_rand, player))
        await ctx.send("Hi {}, you can have a {}".format(player, letter_rand))
    except:
        game.state["pl_letters"][player] = ""
        logging.debug("no letters found for {}".format(player))
    game.state["all_letters"].append(letter_rand)
    game.save()
    return letter_rand


@bot.command(description="Find out current letters owned by player")
async def current(ctx):
    game = Game()
    player = ctx.author
    logging.debug("Fetching letters for {}".format(player))
    try:
        letter_list = game.state["pl_letters"][player]
        logging.debug("got letters for {}: {}".format(player, str(letter_list)))
    except:
        letter_list = []
    await ctx.send(
        "{} your letters are {}".format(player, str(game.state["pl_letters"][player]))
    )


@bot.command(description="Find out what letters this bot has given out")
async def show_all(ctx):
    game = Game()
    logging.debug("Full letter output requested")
    if len(game.state["all_letters"]) == 0:
        await ctx.send("You have no letters!")
    elif len(game.state["all_letters"]) == 1:
        await ctx.send("You have 1 letter, which is " + game.state["all_letters"][0] + "."
        )
    else:
        await ctx.send(
            "You have the letters "
            + str(
                " and ".join(
                    [
                        ", ".join(game.state["all_letters"][:-1]),
                        game.state["all_letters"][-1],
                    ]
                    if len(game.state["all_letters"]) > 2
                    else game.state["all_letters"]
                )
            )
            + "."
        )


@bot.command(description="Hello and introductions")
async def hello(ctx):
    player = ctx.author
    await ctx.send(
        "Hello {}, and welcome to Letters With Strangers. I'm here to help you play the game".format(
            player
        )
    )


# async def check_letters(letters, player):

bot.run(token)
