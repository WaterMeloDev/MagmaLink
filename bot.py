import discord
import os
import asyncio

from datetime import timedelta
from discord import app_commands, utils
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

client = commands.Bot(command_prefix = '>', intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    try: 
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except:
        print(f'already synced')
    change_status.start()
    print(f"Connected to {client.user}!")

async def load():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

activity = discord.Activity(type=discord.ActivityType.competing, name="SMPs")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=activity, status=discord.Status.online)


async def main():
    async with client:
        try:
            await load()
        except Exception as e:
            print(f"Error loading cogs: {e}")
        await client.start(token)

asyncio.run(main())