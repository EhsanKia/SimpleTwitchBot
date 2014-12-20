from twisted.words.protocols import irc
from twisted.internet import reactor
from collections import defaultdict
from commands import Permission
import markov_chain
import traceback
import commands
import logging
import signal
import json
import time

with open('bot_config.json') as fp:
    CONFIG = json.load(fp)

class TwitchBot(irc.IRCClient):
    last_warning = defaultdict(int)
    owner_list = CONFIG['owner_list']
    ignore_list = CONFIG['ignore_list']
    nickname = str(CONFIG['username'])
    password = str(CONFIG['oauth_key'])
    channel = "#" + str(CONFIG['channel'])

    hosting = False
    pause = False
    commands = []

    def signedOn(self):
        self.factory.wait_time = 1
        logging.warning("Signed on as {}".format(self.nickname))

        signal.signal(signal.SIGINT, self.manual_action)

        # Get data structures stored in factory
        self.mods = self.factory.mods
        self.subs = self.factory.subs
        self.activity = self.factory.activity
        self.markov = self.factory.markov

        # Load commands
        self.reload_commands()

        # Join channel
        self.sendLine("TWITCHCLIENT 3")
        self.join(self.channel)

    def joined(self, channel):
        logging.warning("Joined %s" % channel)

    def privmsg(self, user, channel, msg):
        # Extract twitch name
        name = user.split('!', 1)[0].lower()

        # Catch twitch specific commands
        if name in ["jtv", "twitchnotify"]:
            self.jtv_command(msg)
            return

        # Log the message
        logging.info("{}: {}".format(name, msg))

        # Ignore messages by ignored user
        if name in self.ignore_list:
            return

        print channel
        print self.channel

        # Ignore message sent to wrong channel
        if channel != self.channel:
            return

        # Check if bot is paused
        if not self.pause or name in self.owner_list:
            self.process_command(name, msg)
        else:
            self.process_command("__USER__", "__UPDATE__")

        # Log user activity
        self.activity[name] = time.time()

    def modeChanged(self, user, channel, added, modes, args):
        if channel != self.channel: return

        # Keep mod list up to date
        func = 'add' if added else 'discard'
        for name in args:
            getattr(self.mods, func)(name)

        change = 'added' if added else 'removed'
        info_msg = "Mod {}: {}".format(change, ', '.join(args))
        logging.warning(info_msg)

    def write(self, msg, debug=False):
        if not debug:
            self.msg(self.channel, msg)
        logging.info("{}: {}".format(self.nickname, msg))

    def get_permission(self, user):
        '''Returns the users permission level'''
        if user in self.owner_list:
            return Permission.Admin
        elif user in self.mods:
            return Permission.Moderator
        elif user in self.subs:
            return Permission.Subscriber
        return Permission.User

    def process_command(self, user, msg):
        perm_levels = ['User', 'Subscriber', 'Moderator', 'Owner']
        msg = msg.strip()
        perm = self.get_permission(user)
        first = True

        # Flip through commands and execute the first one that matches
        # Check if user has permission to execute command
        # Also reduce warning message spam by limiting it to one per minute
        for cmd in self.commands:
            try:
                match = cmd.match(self, user, msg)
                if not match or not first: continue
                cname = cmd.__class__.__name__
                if perm < cmd.perm:
                    if time.time() - self.last_warning[cname] < 60:
                        continue
                    self.last_warning[cname] = time.time()
                    reply = "{}: You don't have access to that command. Minimum level is {}."
                    self.write(reply.format(user, perm_levels[cmd.perm]))
                else:
                    cmd.run(self, user, msg)
                    first = False
            except:
                logging.error(traceback.format_exc())


    def manual_action(self, *args):
        cmd = raw_input("Command: ").strip()
        if cmd == "q": # Stop bot
            self.terminate()
        elif cmd == 'r': # Reload bot
            self.reload()
        elif cmd == 'rm': # Reload markov module
            self.reload_markov()
        elif cmd == 'rc': # Reload commands
            self.reload_commands()
        elif cmd == 'p': # Pause bot
            self.pause = not self.pause
        elif cmd.startswith("t"):
            # Test an command in debug mode
            # Doesn't send the bots reply to channel
            msg = cmd[2:]
            self.process_command('ehsankia', msg, debug=True)
        elif cmd.startswith("s"):
            # Say something as the bot
            self.write(cmd[2:])

    def jtv_command(self, msg):
        # Log commands that aren't in those
        IGNORED = ["USERCOLOR", "EMOTESET", "SPECIALUSER", "HISTORYEND"]
        if not any(map(msg.startswith, IGNORED)):
            logging.debug(msg)

        if msg.startswith('SPECIALUSER'):
            # Track subscibers in chat
            cmd, name, arg = msg.split()
            if arg == "subscriber":
                self.subs.add(name)
        elif "subscribed" in msg:
            # Someone subscribed
            name = msg[:-17]
            reply = "Thanks for subbing {}!"
            self.write(reply.format(name))
        elif "Now hosting" in msg:
            # Entered host mode
            self.hostTarget = msg[12:-1]
            self.hosting = True
        elif "Exited host" in msg:
            # Exited host mode
            self.hostTarget = None
            self.hosting = False

    def get_active_users(self, t=60*10):
        ''' Returns list of users active in chat in
        the past t seconds (default: 10m)'''

        now = time.time()
        active_users = []
        for user, last in self.activity.items():
            if now - last < t:
                active_users.append(user)

        return active_users

    def close_commands(self):
        # Gracefully end commands
        for cmd in self.commands:
            try:
                cmd.close(self)
            except:
                logging.error(traceback.format_exc())

    def reload_commands(self):
        logging.warning("Reloading commands")

        # Reload commands
        self.close_commands()
        cmds = reload(commands)
        self.commands = [
            cmds.General(self),
            cmds.OwnerCommands(self),
            cmds.SimpleReply(self),
            cmds.Calculator(self),
            cmds.Timer(self),
            cmds.Sex(self),
            cmds.MarkovLog(self),
        ]

    def reload(self):
        logging.warning("Reloading bot!")
        self.close_commands()
        self.quit()

    def reload_markov(self):
        logging.warning("Reloading markov bot!")
        NewMarkov = reload(markov_chain).MarkovChat
        self.factory.markov = NewMarkov()
        self.markov = self.factory.markov

    def terminate(self):
        self.close_commands()
        reactor.stop()