#!env/bin/python

import tweetbots.clevergirl_bot as cgb
import config
import datetime
import ssl
import thread
import time
import logging
import sys
import random

logging.basicConfig(filename="clevergirlbot.log",level=logging.INFO)

bot = cgb.CleverGirlBot(config, config.clevergirlbot)

if __name__ == "__main__":
    while True:
        try:
            bot.user(track='clever girl')
        except ssl.SSLError:
            pass
        except KeyboardInterrupt:
            break
