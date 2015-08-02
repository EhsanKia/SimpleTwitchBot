from math_parser import NumericStringParser
from threading import Thread
import time
import re


# Set of permissions for the commands
class Permission:
    User, Subscriber, Moderator, Admin = range(4)


# Base class for a command
class Command(object):
    perm = Permission.Admin

    def __init__(self, bot):
        pass

    def match(self, bot, user, msg):
        return False

    def run(self, bot, user, msg):
        pass

    def close(self, bot):
        pass


class MarkovLog(Command):
    '''Markov Chat bot that learns from chat
    and generates semi-sensible sentences

    You can use "!chat" to generate a completely
    random sentence, or "!chat about <context>" to
    generate a sentence containing specific words'''

    perm = Permission.User

    def match(self, bot, user, msg):
        self.reply = bot.markov.log(msg)
        cmd = msg.lower()
        case1 = cmd.startswith("!chat about")
        case2 = cmd == "!chat"
        return case1 or case2 or self.reply

    def run(self, bot, user, msg):
        cmd = msg.lower()
        if cmd == "!chat":
            reply = bot.markov.random_chat()
            bot.write(reply)
        elif cmd.startswith("!chat about"):
            reply = bot.markov.chat(msg[12:])
            bot.write(reply)
        else:
            bot.write(self.reply)


class SimpleReply(Command):
    '''Simple meta-command to output a reply given
    a specific command. Basic key to value mapping.'''

    perm = Permission.User

    replies = {
        "!ping": "pong",
        "!headset": "Logitech G930 Headset",
        "!rts": "/me REAL TRAP SHIT",
        "!nfz": "/me NO FLEX ZONE!",
    }

    def match(self, bot, user, msg):
        cmd = msg.lower().strip()
        for key in self.replies:
            if cmd == key:
                return True
        return False

    def run(self, bot, user, msg):
        cmd = msg.lower().strip()

        for key, reply in self.replies.items():
            if cmd == key:
                bot.write(reply)
                break


class Calculator(Command):
    ''' A chat calculator that can do some pretty
    advanced stuff like sqrt and trigonometry

    Example: !calc log(5^2) + sin(pi/4)'''

    nsp = NumericStringParser()
    perm = Permission.User

    def match(self, bot, user, msg):
        return msg.lower().startswith("!calc ")

    def run(self, bot, user, msg):
        expr = msg.split(' ', 1)[1]
        try:
            result = self.nsp.eval(expr)
            if result.is_integer():
                result = int(result)
            reply = "{} = {}".format(expr, result)
            bot.write(reply)
        except:
            bot.write("{} = ???".format(expr))


class General(Command):
    '''Some miscellaneous commands in here'''
    perm = Permission.User

    def match(self, bot, user, msg):
        cmd = msg.lower()
        if cmd.startswith("!active"):
            return True
        return False

    def run(self, bot, user, msg):
        reply = None
        cmd = msg.lower()

        if cmd.startswith("!active"):
            active = len(bot.get_active_users())
            if active == 1:
                reply = "{}: There is {} active user in chat"
            else:
                reply = "{}: There are {} active users in chat"
            reply = reply.format(user, active)

        if reply:
            bot.write(reply)


class Timer(Command):
    '''Sets a timer that will alert you when it runs out'''
    perm = Permission.Moderator

    def match(self, bot, user, msg):
        return msg.lower().startswith("!timer")

    def run(self, bot, user, msg):
        cmd = msg.lower()
        if cmd == "!timer":
            bot.write("Usage: !timer 30s or !timer 5m")
            return

        arg = cmd[7:].replace(' ', '')
        match = re.match("([\d\.]+)([sm]).*", arg)
        if match:
            d, u = match.groups()
            t = float(d) * (60 if u == 'm' else 1)
            thread = TimerThread(bot, user, t)
            thread.start()
        elif arg.isdigit():
            thread = TimerThread(bot, user, int(arg) * 60)
            thread.start()
        else:
            bot.write("{}: Invalid argument".format(user))


class TimerThread(Thread):
    def __init__(self, b, u, t):
        Thread.__init__(self)
        self.bot = b
        self.user = u
        self.time = int(t)

    def run(self):
        secs = self.time % 60
        mins = self.time / 60

        msg = "{}: Timer started for".format(self.user)
        if mins > 0:
            msg += " {}m".format(mins)
        if secs > 0:
            msg += " {}s".format(secs)

        self.bot.write(msg)
        time.sleep(self.time)
        self.bot.write("{}: Time is up!".format(self.user))


class OwnerCommands(Command):
    '''Some miscellaneous commands for bot owners'''

    perm = Permission.Admin

    def match(self, bot, user, msg):
        cmd = msg.lower().replace(' ', '')
        if cmd.startswith("!sleep"):
            return True
        elif cmd.startswith("!wakeup"):
            return True

        return False

    def run(self, bot, user, msg):
        cmd = msg.lower().replace(' ', '')
        if cmd.startswith("!sleep"):
            bot.write("Going to sleep... bye!")
            bot.pause = True
        elif cmd.startswith("!wakeup"):
            bot.write("Good morning everyone!")
            bot.pause = False
