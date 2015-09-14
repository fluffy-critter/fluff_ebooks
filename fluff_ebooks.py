#!env/bin/python

import tweetbots.ebook_bot as ebb
import config

stream = ebb.EbookBot(config, config.fluff_ebooks)

print "Loading training set..."
count = stream.train_csv('fluffy.csv')

print "Learned %d tweets" % count
if __name__ == "__main__":
    while True:
        try:
            stream.user()
        except KeyboardInterrupt:
            break
        except:
            pass
        stream.post_randomly()
