"""
dwayne
A back-end Discord bot created as an alternative to Groovy and Rhythm
Copyright (C) 2021 Marcelo Cubillos
This project is available under the MIT license, see LICENSE.txt for more details

main.py
"""

import discord
import argparse
from discord.ext import commands

parser = argparse.ArgumentParser()
parser.add_argument("token", help="Discord access token")
args = parser.parse_args()
TOKEN = args.token
print(f"Running Dwayne using token: {TOKEN}")

if __name__ == '__main__':
    bot = commands.Bot(command_prefix="!", description='Dwayne')
    bot.load_extension("cogs.dwayne")

    @bot.event
    async def on_ready():
        print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


    bot.run(TOKEN, bot=True, reconnect=True)