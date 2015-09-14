#!env/bin/python

import tweetbots.ebook_bot as ebb
import config
import datetime
import ssl
import thread
import time
import logging
logging.basicConfig(filename='fluff_ebooks.log', level=logging.INFO)

bot = ebb.EbookBot(config, config.fluff_ebooks)

logging.debug("Loading training set...")
count = bot.train_csv('fluffy.csv')
logging.info("Learned %d tweets" % count)

if __name__ == "__main__":
    def scheduled_posts():
        while True:
            time.sleep(15*60)
            bot.post_randomly()
    bg_thread = thread.start_new_thread(scheduled_posts, ())

    while True:
        try:
            bot.user()
        except ssl.SSLError:
            pass
        except KeyboardInterrupt:
            break

    bg_thread.exit()
