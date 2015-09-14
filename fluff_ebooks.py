#!env/bin/python

import tweetbots.ebook_bot as ebb
import config
import datetime

import logging
logging.basicConfig(filename='fluff_ebooks.log', level=logging.INFO)

stream = ebb.EbookBot(config, config.fluff_ebooks)

logging.debug("Loading training set...")
count = stream.train_csv('fluffy.csv')
logging.info("Learned %d tweets" % count)

if __name__ == "__main__":
    last_post_time = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        if now - last_post_time > datetime.timedelta(seconds=15*60):
            stream.post_randomly()
            last_post_time = now

        try:
            stream.user()
        except KeyboardInterrupt:
            break
        except:
            pass

