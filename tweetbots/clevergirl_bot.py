from twython import TwythonStreamer, Twython, TwythonError
import logging
import random
import datetime
import Queue
import time
import thread
from collections import namedtuple

QueueItem = namedtuple("QueueItem", "when text reply_id")

class CleverGirlBot(TwythonStreamer):

    def __init__(self, site_config, bot_config, timeout=30):
        super(CleverGirlBot,self).__init__(
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

        self.my_user_id = bot_config['user_id']
        self.respond_to = bot_config.get('respond_to', [])
        self.post_queue = Queue.Queue()

        self.thread_id = thread.start_new_thread(self.worker_task, ())
        logging.info("Worker thread: %d", self.thread_id)

    def on_success(self, tweet):
        logging.debug(repr(tweet))
        if 'text' in tweet and not 'retweeted_status' in tweet:
            screen_name = tweet['user']['screen_name']

            respond = False

            for mention in tweet['entities']['user_mentions']:
                if mention['id'] == self.my_user_id:
                    logging.info("Mentioned")
                    respond = True

            for term in self.respond_to:
                if term.lower() in tweet['text'].lower():
                    logging.info("Matched phrase %s", term)
                    respond = True

            if respond:
                response = '@%s ' % screen_name
                logging.info("Replying: <%s> %s", screen_name,tweet['text'])
                response += self.generate_tweet()
                logging.info("Response: %s", response)
                self.post(response, tweet['id'])

    def post(self, response, reply_id):
        self.post_queue.put(QueueItem(datetime.datetime.now() + datetime.timedelta(seconds=10), response, reply_id))

    def worker_task(self):
        while True:
            tweet = self.post_queue.get()
            wait_time = (tweet.when - datetime.datetime.now()).seconds
            if wait_time > 0:
                time.sleep(wait_time)

            logging.info("Worker posting tweet [%s](in reply to %s)", tweet.text, tweet.reply_id)
            try:
                self.post_client.update_status(status=tweet.text, in_reply_to_status_id=tweet.reply_id)
            except TwythonError, e:
                logging.info("Post failed: %s", e)
                # self.post_queue.put(tweet)

    def generate_tweet(self):
        rawr = 'R' + 'a'*random.randint(0,5) + 'w'*random.randint(0,4) + 'r'*random.randint(1,3)

        rawr += random.choice(['', '...', '.', '...?', '!'])
        rawr = random.choice([
            (lambda x:x.upper()),
            (lambda x:x.lower()),
            (lambda x:x),
            (lambda x:x.upper() + '!')
            ])(rawr)

        rawr += random.choice(['', '', '', '', ' :>', ' *nuzzles*', ' *playfully nips*'])

        return rawr

    def run(self):
        self.user(track=','.join(self.respond_to))
