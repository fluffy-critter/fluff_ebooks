#!env/bin/python

import tweetbots.ebook_bot as ebb
import config
import datetime
import ssl
import thread
import time
import logging
import sys

logging.basicConfig(filename="fluff_ebooks.log",level=logging.INFO)

bot = ebb.EbookBot(config, config.fluff_ebooks)

for csv in sys.argv[1:]:
    logging.info("Training from %s", csv)
    count = bot.train_csv(csv)
    logging.info("Learned %d tweets" % count)
bot.flush()

if __name__ == "__main__":
    def scheduled_posts():
        while True:
            try:
                time.sleep(3600)
                bot.post_randomly()
            except:
                pass
    bg_thread = thread.start_new_thread(scheduled_posts, ())

    while True:
        try:
            bot.user()
        except ssl.SSLError:
            pass
        except KeyboardInterrupt:
            break

