from twython import TwythonStreamer
import random
import config
import ast
from collections import namedtuple

class MarkovChain:
    ''' dead-simple markov chain '''
    def __init__(self):
        self.tokens = {}

    def load_corpus(self, corpus_data):
        ''' this is stupidly insecure/unsafe '''
        self.tokens = eval(corpus_data)

    def get_corpus(self):
        return repr(self.tokens)

    def learn_word(self, cur, word, weight=1):
        ''' Learn a word for the markov chain '''
        cur_node = self.tokens.setdefault(cur, { "total": 0, "next": {} })
        cur_node["total"] += weight

        cur_word = cur[0] or ''

        next_node = (word,
            max(cur[1] + cur_word.count('(') - cur_word.count(')'), 0),
            max(cur[2] + (cur_word[:1] == "'" and 1) - cur_word[1:].count("'"), 0),
            max(cur[3] + (cur_word[:1] == '"' and 1) - cur_word[1:].count('"'), 0)
            )

        cur_node["next"][next_node] = cur_node["next"].get(next_node, 0) + weight
        return next_node

    def learn_tweet(self, tweet_text):
        ''' Learn a sentence from a tweet. Strips out all @mentions. '''
        cur = (None,0,0,0)
        for word in tweet_text.split():
            if word[0] != '@':
                cur = self.learn_word(cur, word)
        self.learn_word(cur, None)

    def choose_next_word(self, cur):
        ''' Choose the next word from this markov chain given a seed word '''
        node = self.tokens[cur]
        candidate = (None,0,0,0)
        remain = random.randint(0, node["total"])
        for (word,weight) in node["next"].items():
            candidate = word
            remain -= weight
            if remain <= 0:
                break
        return candidate

    def generate_tweet(self, start_word=None, size=140):
        ''' Generate a random tweet from this markov chain '''
        words = []
        last_word = (start_word,0,0,0)
        letters_left = size
        while True:
            next_word = self.choose_next_word(last_word)

            if next_word[0] == None:
                break

            if len(next_word[0]) > letters_left:
                # we ran out of space; rather than trying to backtrack, let's just start over
                words = []
                last_word = (start_word,0,0,0)
                letters_left = size
                continue

            words.append(next_word)
            letters_left -= 1 + len(next_word)
            last_word = next_word
        return " ".join(map((lambda node:node[0]), words))
