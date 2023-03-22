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
import asyncio
from cogs.dwayne import DwayneBOT

parser = argparse.ArgumentParser()
parser.add_argument("token", help="Discord access token")
args = parser.parse_args()
TOKEN = args.token
print(f"Running Dwayne using token: {TOKEN}")


async def main():
    intents = discord.Intents.all()
    intents.members = True
    bot = commands.Bot(command_prefix="!", description='Dwayne', intents=intents)
    async with bot:
        await bot.add_cog(DwayneBOT(bot))
        await bot.start(TOKEN)

        @bot.event
        async def on_ready():
            print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


if __name__ == '__main__':
    asyncio.run(main())
