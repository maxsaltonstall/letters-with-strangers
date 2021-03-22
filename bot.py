import discord
from discord.ext import commands
import random
import string

# make this bot not client
client = discord.Client()
# make this an environment variable
token = 'token'

response = str('')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        response = 'Hi there, want some letters?'

    if message.content.startswith('.lws letter'):
        letter_rand = random.choice(string.ascii_uppercase)
        response = 'Your letter is: ' + letter_rand

    if message.content.startswith('.lws word'):
        response = 'you want to make a word, but I don''t know how yet'

    if response:
        await message.channel.send(response)

client.run(token)
