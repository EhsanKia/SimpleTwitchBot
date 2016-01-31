**SimpleTwitchBot**
===============

This is a basic implementation of a Twitch IRC Bot coded in Python.
It contains most of the gory specifics needed to interact with Twitch chat.
I've included a couple basic commands as examples, but this is intended to just be a skeleton and not a fully featured bot.

If you want something even more barebone than this, checkout [BareboneTwitchBot](https://github.com/EhsanKia/BareboneTwitchBot).

# Installation and usage
All you should need is Pyhton 2.7+ with [Twisted](https://twistedmatrix.com/trac/) installed.
You then copy this project in a folder, configure the bot and run `twitch_irc.py`.

#### Configuration:
Make sure to modify the following values in `bot_config.json`:
- `channel`: Twitch channel which the bot will run on
- `username`: The bot's Twitch user
- `oauth_key`: IRC oauth_key for the bot user (from [here](http://twitchapps.com/tmi/))
- `owner_list`: List of Twitch users which have admin powers on bot
- `ignore_list`: List of Twitch users which will be ignored by the bot

**Warning**: Make sure all channel and user names above are in lowercase.

#### Usage:
The main command-line window will show chat log and other extra messsages.

You can enter commands by pressing CTRL+C on the command line:
- `q`: Closes the bot
- `r`: Reloads the code in `bot.py` and reconnects
- `rm`: reloads the code in `markov_chain.py`
- `ra`: reloads the code in `commands.py` and reloads commands
- `p`: Pauses bot, ignoring commands from non-admins
- `t <msg>`: Runs a test command with the bot's reply not being sent to the channel
- `s <msg>`: Say something as the bot in the channel

As you can see, the bot was made to be easy to modify live.
You can simply modify most of the code and quickly reload it.
The bot will also auto-reconnect if the connection is lost.

# Code Overview

#####`twitch_irc.py`
This is the file that you run. It just starts up a Twisted IRC connection with the bot protocol.
The bot is currently built to only run in one channel, but you can still open all the files over
to another folder with a different config and run it in parallel.

#####`bot.py`
Contains the bot IRC protocol. The main guts of the bot are here.

#####`commands.py`
This is where the commands are stored. The code is built to be modular.
Each "Command" class has:
- `perm` variable from the Permission Enum to set access level
- `__init__` function that initializes the command
- `match` function that checks if this command needs to run
- `run` function which actually runs the command
- `close` function which is used to cleanup and save things

All commands are passed the bot instance where they can get list of mods, subs and active users.
`match` and `run` are also passed the name of the user issuing the command and the message.

#####`markov_chain.py`
A simple Markov Chain chat bot which learns from chat messages and tries to generate coherent replies.
By default, it's only invoked with "!chat" or "!chat about <context>" commands, but you can change the
`chattiness` parameter in the file to a small fraction like 0.01 to have it randomly reply to people.
It usually needs a couple hundred lines of chat to really start becoming effective.

# Contact
If you have any extra questions about the code, you can send me a PM on twitch: @ehsankia
