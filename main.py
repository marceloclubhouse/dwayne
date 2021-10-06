import discord
import argparse
from discord.ext import commands

parser = argparse.ArgumentParser()
parser.add_argument("token", help="Discord access token")
args = parser.parse_args()
TOKEN = args.token

if __name__ == '__main__':
    bot = commands.Bot(command_prefix="!", description='Dwayne')
    bot.load_extension("dwayne")

    @bot.event
    async def on_ready():
        print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


    bot.run(TOKEN, bot=True, reconnect=True)