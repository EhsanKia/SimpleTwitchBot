from twisted.internet import protocol, reactor
from collections import defaultdict

import bot
import time
import logging
import logging.config
logging.config.fileConfig('logging.conf')


class BotFactory(protocol.ClientFactory):
    protocol = bot.TwitchBot

    tags = defaultdict(dict)
    activity = dict()
    wait_time = 1

    def clientConnectionLost(self, connector, reason):
        logging.error("Lost connection, reconnecting")
        self.protocol = reload(bot).TwitchBot
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        msg = "Could not connect, retrying in {}s"
        logging.warning(msg.format(self.wait_time))
        time.sleep(self.wait_time)
        self.wait_time = min(512, self.wait_time * 2)
        connector.connect()


if __name__ == "__main__":
    reactor.connectTCP('irc.twitch.tv', 6667, BotFactory())
    reactor.run()
