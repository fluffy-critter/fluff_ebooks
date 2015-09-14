import markov
import csv
from twython import TwythonStreamer, Twython

class EbookBot(TwythonStreamer):
    def __init__(self, site_config, bot_config, interval=16*50):
        super(EbookBot,self).__init__(
            site_config.app_key,
            site_config.app_secret,
            bot_config['oauth_token'],
            bot_config['oauth_token_secret'],
            timeout=interval)

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
            count = 0
            for row in reader:
                self.markov.learn_tweet(row[text_col])
                count += 1
        return count

    def on_success(self, tweet):
        if 'text' in tweet:
            screen_name = tweet['user']['screen_name']

            for user in self.learn_users:
                if tweet['user']['id'] == user['user_id']:
                    print "%s says: %s" % (screen_name, tweet['text'])
                    self.markov.learn_tweet(tweet['text'])

            for mention in tweet['entities']['user_mentions']:
                if mention['id'] == self.my_user_id:
                    response = '@%s ' % screen_name
                    print "%s says: %s" % (screen_name,tweet['text'])
                    response += self.markov.generate_tweet(letters_left=140 - len(response))
                    print "I will reply with: " + response
                    self.post_client.update_status(status=response, in_reply_to_status_id=tweet['id'])

    def post_randomly(self):
        tweet = self.markov.generate_tweet()
        print "Randomly posting: " + tweet
        self.post_client.update_status(status=tweet)
