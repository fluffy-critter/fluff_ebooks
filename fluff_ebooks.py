#!env/bin/python

import tweetbots.ebook_bot as ebb
import config
import datetime
import ssl

import logging
logging.basicConfig(filename='fluff_ebooks.log', level=logging.INFO)

bot = ebb.EbookBot(config, config.fluff_ebooks)

logging.debug("Loading training set...")
count = bot.train_csv('fluffy.csv')
logging.info("Learned %d tweets" % count)

if __name__ == "__main__":
    last_post_time = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        logging.info("Time since last post: %s", now - last_post_time)
        if now - last_post_time > datetime.timedelta(minutes=15):
            logging.info("Timeout exceeded; posting now")
            bot.post_randomly()
            last_post_time = now

        try:
            bot.user()
        except ssl.SSLError:
            pass
        except KeyboardInterrupt:
            break
