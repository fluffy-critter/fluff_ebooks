from twython import TwythonStreamer, Twython
import logging
import random

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

    def on_success(self, tweet):
        logging.debug(repr(tweet))
        if 'text' in tweet and not 'retweeted_status' in tweet:
            screen_name = tweet['user']['screen_name']

            respond = False

            for mention in tweet['entities']['user_mentions']:
                logging.info("Checking user_id %d %d", mention['id'], self.my_user_id)
                if mention['id'] == self.my_user_id:
                    respond = True

            for term in self.respond_to:
                if term.lower() in tweet['text'].lower():
                    respond = True

            if respond:
                response = '@%s ' % screen_name
                logging.info("Replying: <%s> %s", screen_name,tweet['text'])
                response += self.generate_tweet()
                logging.info("Response: %s", response)
                self.post_client.update_status(status=response, reply_id=tweet['id'])

    def generate_tweet(self):
        rawr = 'R' + 'a'*random.randint(0,5) + 'w'*random.randint(0,3) + 'r'*random.randint(1,3)

        rawr += random.choice(['', '...', '.', '...?', '!'])
        rawr = random.choice([
            (lambda x:x.upper()),
            (lambda x:x.lower()),
            (lambda x:x),
            (lambda x:x.upper() + '!')
            ])(rawr)

        rawr += random.choice(['', '', '', '', ' :>', ' *nuzzles*', ' *playfully nips*'])

        return rawr