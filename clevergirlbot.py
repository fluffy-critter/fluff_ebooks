#!env/bin/python

import tweetbots.ebook_bot as ebb
import config
import datetime
import ssl
import thread
import time
import logging
import sys
import random

def rawr_wordfilter(word):
    if not word:
        return word
    rawr = ''

    split_wr = random.randint((len(word) - 1)*5/8, len(word) - 1)

    for in_letter in word:
        if rawr and in_letter.lower() in 'aeiou':
            letter = 'a'
        elif not 'r' in rawr.lower() or len(rawr) >= split_wr:
            letter = 'r'
        else:
            letter = 'w'
        if in_letter.isupper():
            letter = letter.upper()
        rawr += letter
    return rawr

def rawr_linefilter(line):
    output = ''
    cur_word = ''
    for letter in line:
        if letter.isalnum():
            cur_word += letter
        else:
            output += rawr_wordfilter(cur_word) + letter
            cur_word = ''
    output += rawr_wordfilter(cur_word)
    return output

logging.basicConfig(level=logging.INFO)

bot = ebb.EbookBot(config, config.clevergirlbot)
for csv in sys.argv[1:]:
    logging.info("Training from %s", csv)
    count = bot.train_csv(csv, rawr_linefilter)
    logging.info("Learned %d tweets" % count)
bot.flush()

if __name__ == "__main__":
    def scheduled_posts():
        while True:
            try:
                time.sleep(3456)
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

