# dwayne
### A less-than-perfect alternative to Groovy and Rhythm
Dwayne is a Discord music bot backend. He can be linked to a Discord Bot and stream YouTube music live inside a voice channel. He can
* Stream music off of YouTube in Discord
* Queue songs and automatically play them one after the other

## Requirements
* Git
* Python 3
* Pip 3
* macOS or Linux
  * Dwayne will run under Windows but since I don't know Powershell there's no setup script :(
* Discord Developer account

## Commands
* !play - Play a YouTube video in a voice channel
* !stop - Stop playing music
* !heydwayne - Ping Dwayne to see if he's online

## Setup
### Discord Access Token
First, follow this tutorial on the Discord Developer Portal to create a bot
```https://discordpy.readthedocs.io/en/stable/discord.html```

### Running on Linux or Mac
Then download the installation script from [here] and run ```chmod +x dwayne.sh```
then ```./dwayne.sh```

Upon running this script the first time, you will be asked to provide your bot's access token. 
You only need to provide this once; the script will automatically clone this database, perform the required setup, 
and can be called after the initial installation to run Dwayne whenever you want.

Whenever you want to run Dwayne, simply execute his script! ```./dwayne.sh```

### Installation + Running on Windows
To run Dwayne on Windows, make sure you have Python 3 installed. Then
create a virtual environment based off of Dwayne's requirements, and run
```main.py``` with your bot's access token as an argument.

### Potential Ideas for You
* You could run Dwayne off of a local Linux VM
* Or run Dwayne off of a VPS! (that's what I do)

### TODO
* Improve download speeds
* Create a GUI for Dwayne
* Implement skipping
* Implement simultaneous voice streaming

## License
This project is available under the MIT license. See LICENSE.txt for more information.
