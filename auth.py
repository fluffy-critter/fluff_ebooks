#!env/bin/python

from twython import Twython
import config
import string

twitter = Twython(config.app_key, config.app_secret)
auth = twitter.get_authentication_tokens(callback_url='oob')

print "Visit\n\n{url}\n\nand enter the PIN here: ".format(url=auth['auth_url'])
pin = raw_input('> ')

twitter = Twython(config.app_key, config.app_secret, auth['oauth_token'], auth['oauth_token_secret'])
tokens = twitter.get_authorized_tokens(pin)

formatter = string.Formatter()
print formatter.vformat('''{screen_name} = {
    'user_id': {user_id},
    'oauth_token': '{oauth_token}',
    'oauth_token_secret': '{oauth_token_secret}'
}''', [], tokens)
