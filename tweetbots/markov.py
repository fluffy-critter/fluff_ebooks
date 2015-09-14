from twython import TwythonStreamer
import random
import config

class MarkovChain:
    ''' dead-simple markov chain that learns from tweets '''
    def __init__(self):
        self.tokens = {}

    def learn_word(self, cur, word, weight=1):
        ''' Learn a word for the markov chain '''
        if not cur in self.tokens:
            self.tokens[cur] = { "total": 0, "next": {}}
        node = self.tokens[cur]
        node["total"] += weight
        if not word in node["next"]:
            node["next"][word] = 0
        node["next"][word] += weight

    def learn_tweet(self, tweet_text):
        ''' Learn a sentence from a tweet. Strips out all @mentions. '''
        cur = None
        for word in tweet_text.split():
            if word[0] != '@':
                self.learn_word(cur, word)
                cur = word
        self.learn_word(cur, None)

    def choose_next_word(self, cur):
        ''' Choose the next word from this markov chain given a seed word '''
        node = self.tokens[cur]
        candidate = None
        remain = random.randint(0, node["total"])
        for (word,weight) in node["next"].items():
            candidate = word
            remain -= weight
            if remain <= 0:
                break
        return candidate

    def generate_tweet(self, start_word=None, letters_left=140):
        ''' Generate a random tweet from this markov chain '''
        words = []
        last_word = start_word
        while letters_left > 0:
            next_word = self.choose_next_word(last_word)
            if next_word == None or len(next_word) > letters_left:
                break
            words.append(next_word)
            letters_left -= 1 + len(next_word)
            last_word = next_word
        return " ".join(words)

