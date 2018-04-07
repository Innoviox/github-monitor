import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

client = Bot(description="A bot by rassarian#4378", command_prefix="!", pm_help=True)

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
        len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Created by rassarian#4378')

@client.command()
async def ping(*args):
    await client.say(":ping_pong: Pong!")

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    await client.send_message(message.channel, message)


client.run("REDACTED")