"""
dwayne
A back-end Discord bot created as an alternative to Groovy and Rhythm
Copyright (C) 2021 Marcelo Cubillos
This project is available under the MIT license, see LICENSE.txt for more details

dwayne.py
"""

import asyncio
import discord
import yt_dlp
import youtube_dl
import os
import re
from discord.ext import commands


class DwayneBOT(commands.Cog):
    """
    Discord bot that queues and plays YouTube music! Awesome
    """

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
        self.voice = None
        self.playing = False

    @commands.command()
    async def heydwayne(self, ctx):
        await ctx.send("Hey!")

    @commands.command()
    async def play(self, ctx, url):
        """
        Queue a song and play songs from the song queue
        """

        # Check if URL is valid via regex
        if not self.validate_url(url):
            await ctx.send(f"Invalid URL!")
            return
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f"You must be connected to a voice channel to play songs.")
            return

        # Always start by queueing the song in internal list
        self.song_queue.append(url)
        # Get YouTube video info with YT libs
        song_info = self.video_info(url)
        # If a song is already playing, then queue it and return
        if self.playing:
            await ctx.send(f"Got it! Just queued {song_info['title']}. Current song queue is:",
                           embed=self.queue_as_embed(ctx))
            return

        # Connect to author's voice channel
        self.voice = await channel.connect()
        await ctx.send(f"You got it boss. Preparing to stream {song_info['title']}")

        # Song playing loop for music queue
        while len(self.song_queue) != 0:
            self.playing = True
            current_song = self.song_queue.pop(0)
            song_info = self.video_info(current_song)

            # Download current song in queue to ./song.mp3
            self.yt_to_mp3(current_song)

            # Play song and notify it's playing
            await ctx.send(f"Now playing {song_info['title']}")
            self.voice.play(discord.FFmpegPCMAudio('song.mp3'))

            # Play until the song is over
            while self.voice.is_playing():
                await asyncio.sleep(1)
            self.voice.stop()

        # Disconnect after song queue is empty
        await self.voice.disconnect()
        self.playing = False

    @commands.command()
    async def stop(self, ctx):
        """
        Empty song queue and disconnect Dwayne from voice
        """
        if not self.playing:
            await ctx.send("Can't stop playing music if there is no music playing.")
            return
        self.song_queue = list()
        self.voice.stop()
        await self.voice.disconnect()
        await ctx.send("Got it. Stopping music and emptying song queue.")

    @staticmethod
    def yt_to_mp3(url: str) -> None:
        """
        Download YouTube video as 'song.mp3' in current
        directory using yt-dlp
        """

        # Delete previous song
        print("Deleting previous song...")
        try:
            os.remove("song.mp3")
        except FileNotFoundError:
            pass

        # Download current song
        print("Downloading YouTube video...")
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'keepvideo': False,
            'outtmpl': "song.mp3",
            'throttled-rate': '100K'
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print(f"Finished downloading {url}")

    def queue_as_str(self) -> str:
        """
        Return song queue as a multi-line string
        (no longer used, embed cards are used
        instead but this is kept just in case)
        """
        q_str = str()
        for i, song in enumerate(self.song_queue):
            q_str += str(i + 1) + ".\t" + self.url_to_title(song) + "\n"
        return q_str

    def queue_as_embed(self, ctx) -> discord.Embed:
        """
        Generate a Discord embed card from this object's
        song queue
        """
        embed = discord.Embed(title='Dwayne\'s Song Queue')
        for song in self.song_queue:
            song_info = self.video_info(song)
            embed.add_field(name=song_info['title'], value=song_info['channel'], inline=False)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        return embed

    @staticmethod
    def video_info(url: str):
        """
        Download YouTube video's meta-data and return
        it as a dictionary.

        This function uses youtube_dl rather than yt-dlp
        because yt-dlp re-downloads the android player
        API JSON, and is actually slower than youtube_dl
        in this context.
        """
        info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
        return info

    @staticmethod
    def validate_url(url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        return re.match(youtube_regex, url)


def setup(bot):
    bot.add_cog(DwayneBOT(bot))
