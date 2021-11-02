# dwayne
### A music-playing Discord bot created as an alternative to Groovy and Rhythm 
Dwayne is a Discord bot backend designed to control music-streaming via YouTube on Discord. He can be linked to a Discord Bot API token and stream YouTube music live inside a voice channel. He can also queue songs and play them sequentially.

## Requirements
* Git
* Python 3
* Pip 3
* macOS or Linux
  * Dwayne will run under Windows but since I don't know Powershell there's no setup script :(
* ffmpeg 
* Discord Developer account

## Commands
* !play - Play a YouTube video in a voice channel
  * Works either with a URL or a query (e.g. !play here comes the sun)
* !stop - Stop playing music
* !heydwayne - Ping Dwayne to see if he's online

## Setup
### Discord Access Token
First, follow this tutorial on the Discord Developer Portal to create a bot
```https://discordpy.readthedocs.io/en/stable/discord.html```

### Linux or Mac
Then download and run the installation script
```
wget https://github.com/marceloclubhouse/dwayne/releases/download/v0.1.0/dwayne.sh
chmod +x dwayne.sh
./dwayne.sh
```

Upon running this script the first time, you will be asked to provide your bot's access token, and optionally a
YouTube Data API key if you want to enable queries. 
You only need to provide this once; the script will automatically clone this database, perform the required setup, 
and can be called after the initial installation to run Dwayne whenever you want.

Whenever you want to run Dwayne, simply execute his script! ```./dwayne.sh```

### Windows
To run Dwayne on Windows, make sure you have Python 3 installed. Then
create a virtual environment based off of Dwayne's requirements, and run
```main.py``` with your bot's access token as an argument.

You can do this method on Linux too but I figured it would be nice to automate it with a script :)

## Potential Ideas for Running Dwayne
* You could run Dwayne off of a local Linux VM if you can't setup Dwayne on Windows
* Or run Dwayne off of a VPS! (that's what I do)

## TODO
* Improve download speeds
* Create a GUI for Dwayne
* Implement skipping
* Implement simultaneous voice streaming

## License
This project is available under the MIT license. See LICENSE.txt for more information.
