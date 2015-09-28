import markov
import csv
from twython import TwythonStreamer, Twython
import logging
import HTMLParser
import os

class EbookBot(TwythonStreamer):
    html = HTMLParser.HTMLParser()

    def __init__(self, site_config, bot_config, timeout=30):
        super(EbookBot,self).__init__(
            site_config.app_key,
            site_config.app_secret,
            bot_config['oauth_token'],
            bot_config['oauth_token_secret'],
            timeout=timeout)

        self.post_client = Twython(
            site_config.app_key,
            site_config.app_secret,
            bot_config['oauth_token'],
            bot_config['oauth_token_secret'])

        self.markov = markov.MarkovChain()

        self.my_user_id = bot_config['user_id']
        if 'learn_users' in bot_config:
            self.learn_users = bot_config['learn_users']
        else:
            self.learn_users = []

        self.corpus_file = bot_config.get('corpus_file', None)
        if self.corpus_file and os.path.isfile(self.corpus_file):
            logging.info("Reading corpus file %s", self.corpus_file)
            with open(self.corpus_file, 'r') as file:
                self.markov.load_corpus(file.read())
            logging.info("Done")

    def flush(self):
        if self.corpus_file:
            with open(self.corpus_file, 'w') as file:
                file.write(self.markov.get_corpus())

    def post(self, text, reply_id=None):
        status = self.html.unescape(text)
        self.post_client.update_status(status=text, in_reply_to_status_id=reply_id)

    def train_csv(self, filename):
        ''' Train from a Twitter archive CSV file. Returns the number of tweets learned. '''
        with open(filename, 'r') as tweetfile:
            reader = csv.reader(tweetfile)

            col_ids = {}
            cur_id = 0
            for col in reader.next():
                col_ids[col] = cur_id
                cur_id += 1

            text_col = col_ids["text"]
            rt_col = col_ids["retweeted_status_id"]
            count = 0
            for row in reader:
                if row[text_col] and not row[rt_col]:
                    self.markov.learn_tweet(row[text_col])
                    count += 1
        return count

    def on_success(self, tweet):
        logging.debug(repr(tweet))
        if 'text' in tweet and not 'retweeted_status' in tweet:
            screen_name = tweet['user']['screen_name']

            for user in self.learn_users:
                if tweet['user']['id'] == user['user_id']:
                    logging.info("Learning: <%s> %s", screen_name, tweet['text'])
                    self.markov.learn_tweet(tweet['text'])
                    self.flush()

            for mention in tweet['entities']['user_mentions']:
                logging.info("Checking user_id %d %d", mention['id'], self.my_user_id)
                if mention['id'] == self.my_user_id:
                    response = '@%s ' % screen_name
                    logging.info("Replying: <%s> %s", screen_name,tweet['text'])
                    response += self.markov.generate_tweet(letters_left=140 - len(response))
                    logging.info("Response: %s", response)
                    self.post(response, reply_id=tweet['id'])

    def post_randomly(self):
        tweet = self.markov.generate_tweet()
        logging.info("Randomly posting: " + tweet)
        self.post(tweet)
