# fluff_ebooks

First there was horse_ebooks. Then there came a proliferation of other _ebooks Tweetbots.

Here's yet another one.

## Setup

1. Clone this repo
2. Run `./setup.sh`
3. Create a new [Twitter application](http://apps.twitter.com)
4. Copy `config.py.dist` to `config.py` and fill out the `app_key` and `app_secret` fields with your app's OAuth credentials

## Configuring bots

Log in to Twitter as the account you want to impersonate, and run `./auth.py` and follow its instructions. Then paste the resulting code block into `config.py`

Log in to Twitter as the bot you want to post as, and run `./auth.py` and follow its instructions, then paste its code block into `config.py`.

If you want to get your full tweet archive for a training set, you can do that from the [account settings page](https://twitter.com/settings/account) and requesting an archive. The archive will be a .zip file which contains `username.csv` among other stuff.

Now you can create a bot; just copy `fluff_ebooks.py` to a new script and modify it as needed.

## TODO

* Save the Markov chain training data out persistently
* Do catch-up training at startup maybe?
* More bot styles (e.g. @CleverGirlBot needs to finally exist)
* More generic event-driven bot API
