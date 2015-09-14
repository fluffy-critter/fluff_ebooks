#!env/bin/python

import tweetbots.ebook_bot as ebb
import config

import logging
logging.basicConfig(filename='fluff_ebooks.log', level=logging.INFO)

stream = ebb.EbookBot(config, config.fluff_ebooks)

logging.debug("Loading training set...")
count = stream.train_csv('fluffy.csv')
logging.info("Learned %d tweets" % count)

if __name__ == "__main__":
    while True:
        try:
            stream.user()
        except KeyboardInterrupt:
            break
        except:
            pass
        stream.post_randomly()
