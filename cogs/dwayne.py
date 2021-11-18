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
import sys
import requests
from discord.ext import commands


class DwayneBOT(commands.Cog):
    """
    Discord bot that queues and plays YouTube music! Awesome
    """

    def __init__(self, bot, **kwargs):
        self._bot = bot
        self._song_queue = []
        self._voice = None
        self._playing = False
        self._yt_api_key = None

        # Not sure if it's possible to pass arguments
        # to a Cog, such as an API key. For now just open
        # an text file that should presumably contain a key.
        try:
            yt_key = open("yt_api_key.txt", 'r').read()
            # API regex provided by https://github.com/l4yton/RegHex
            youtube_api_regex = "AIza[0-9A-Za-z\\-_]{35}"
            if re.match(youtube_api_regex, yt_key):
                self._yt_api_key = yt_key
            else:
                eprint("Invalid YouTube API key! Continuing without query functionality.")
        except FileNotFoundError:
            print("No YouTube Data API key found. Continuing without query functionality.")

    @commands.command()
    async def heydwayne(self, ctx):
        await ctx.send("Hey!")

    @commands.command()
    async def play(self, ctx, *args):
        """
        Queue a song and play songs from the song queue.
        Playback currently supported on YouTube via
        URL or query.
        """

        # Check if URL is a valid YouTube link
        url: str = args[0]
        if not self._validate_url(url):
            # If no YouTube API token was specified
            # when Dwayne was ran, then don't search
            # for videos.
            if not self._yt_api_key:
                await ctx.send(f"Invalid URL!")
                return
            # Otherwise, use !play parameters as
            # search query and find the URL of
            # the top search result.
            else:
                url = self._query_to_url(args)
                await ctx.send(f"{url}")
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f"You must be connected to a voice channel to play songs.")
            return

        # Always start by queueing the song in internal list
        self._song_queue.append(url)
        # Get YouTube video info with YT libs
        song_info = self._video_info(url)
        # If a song is already playing, then queue it and return
        if self._playing:
            await ctx.send(f"Got it! Just queued {song_info['title']}. Current song queue is:",
                           embed=self._queue_as_embed(ctx))
            return

        # Connect to author's voice channel
        self._voice = await channel.connect()
        await ctx.send(f"You got it boss. Preparing to stream {song_info['title']}")

        # Song playing loop for music queue
        while len(self._song_queue) != 0:
            self._playing = True
            current_song = self._song_queue.pop(0)
            song_info = self._video_info(current_song)

            # Download current song in queue to ./song.mp3
            self._yt_to_mp3("https://www.youtube.com/watch?v=adLGHcj_fmA")

            # Play song and notify it's playing
            await ctx.send(f"Now playing {song_info['title']}")
            self._voice.play(discord.FFmpegPCMAudio('song.mp3'))

            # Play until the song is over
            while self._voice.is_playing():
                await asyncio.sleep(1)
            self._voice.stop()

        # Disconnect after song queue is empty
        await self._voice.disconnect()
        self._playing = False

    @commands.command()
    async def skip(self, ctx):
        """
        Stop playing the current song and start playing
        the next song in the queue.
        """
        if not self._playing:
            await ctx.send(f"Can't skip a song if there's nothing playing.")
        await ctx.send(f"Got it! Skipping song.")
        self._voice.stop()

    @commands.command()
    async def stop(self, ctx):
        """
        Empty song queue and disconnect Dwayne from voice
        """
        if not self._playing:
            await ctx.send("Can't stop playing music if there is no music playing.")
            return
        self._song_queue = list()
        self._voice.stop()
        await self._voice.disconnect()
        await ctx.send("Got it. Stopping music and emptying song queue.")

    @staticmethod
    def _yt_to_mp3(url: str) -> None:
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

    def _query_to_url(self, args: tuple) -> str:
        """
        Return a valid YouTube URL based on the query
        provided in args (string tuple).
        """
        query = f"https://www.googleapis.com/youtube/v3/search?key={self._yt_api_key}&q={'+'.join(args)}&type=video&maxResults=1"
        result = requests.get(query).json()
        video_id = result["items"][0]["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        return url

    def _queue_as_str(self) -> str:
        """
        Return song queue as a multi-line string
        (no longer used, embed cards are used
        instead but this is kept just in case)
        """
        q_str = str()
        for i, song in enumerate(self._song_queue):
            q_str += str(i + 1) + ".\t" + self.url_to_title(song) + "\n"
        return q_str

    def _queue_as_embed(self, ctx) -> discord.Embed:
        """
        Generate a Discord embed card from this object's
        song queue
        """
        embed = discord.Embed(title='Dwayne\'s Song Queue')
        for song in self._song_queue:
            song_info = self._video_info(song)
            embed.add_field(name=song_info['title'], value=song_info['channel'], inline=False)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        return embed

    @staticmethod
    def _video_info(url: str):
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
    def _validate_url(url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        return re.match(youtube_regex, url)


def setup(bot):
    bot.add_cog(DwayneBOT(bot))


def eprint(*args, **kwargs):
    """
    Print to stderr
    """
    print(*args, file=sys.stderr, **kwargs)