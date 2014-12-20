from collections import defaultdict, deque
import cPickle as pickle
import random
import os

class MarkovChat(object):
    chain_length = 2
    chattiness = 0
    max_words = 25
    messages_to_generate = 5
    separator = '\x01'
    stop_word = '\x02'
    ltable = defaultdict(list)
    rtable = defaultdict(list)
    train_data = 'logs/markov_train.txt'

    def __init__(self):
        self.load_file(self.train_data)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename) as fp:
                self.ltable, self.rtable = pickle.load(fp)

    def save_data(self):
        with open(self.filename, 'w') as fp:
            obj = [self.ltable, self.rtable]
            pickle.dump(obj, fp)

    def split_message(self, message):
        # split the incoming message into words, i.e. ['what', 'up', 'bro']
        words = message.split()

        # if the message is any shorter, it won't lead anywhere
        if len(words) > self.chain_length:

            # add some stop words onto the message
            # ['what', 'up', 'bro', '\x02']
            words.append(self.stop_word)
            words = [self.stop_word, self.stop_word] + words

            # len(words) == 4, so range(4-2) == range(2) == 0, 1, meaning
            # we return the following slices: [0:3], [1:4]
            # or ['what', 'up', 'bro'], ['up', 'bro', '\x02']
            for i in range(len(words) - self.chain_length):
                yield words[i:i + self.chain_length + 1]

    def generate_message(self, seed):
        gen_words = deque(seed)

        for i in range(self.max_words/2):
            lwords = gen_words[0], gen_words[1]
            rwords = gen_words[-2], gen_words[-1]
            lkey = self.separator.join(lwords).lower()
            rkey = self.separator.join(rwords).lower()
            oldlen = len(gen_words)

            if gen_words[0] != self.stop_word and lkey in self.ltable:
                next_word = random.choice(self.ltable[lkey])
                gen_words.appendleft(next_word)

            if gen_words[-1] != self.stop_word and rkey in self.rtable:
                next_word = random.choice(self.rtable[rkey])
                gen_words.append(next_word)

            if oldlen == len(gen_words):
                break

        return ' '.join(gen_words).strip('\x02 ')

    def log(self, msg):
        # speak only when spoken to, or when the spirit moves me
        if msg.startswith('!') or 'http://' in msg or not msg.count(' '):
            return

        with open(self.train_data, 'a') as fp:
            fp.write(msg + "\n")

        messages = []
        if random.random() < self.chattiness:
            for words in self.split_message(msg):
                # if we should say something, generate some messages based on what
                # was just said and select the longest, then add it to the list
                best_message = ''
                for i in range(self.messages_to_generate):
                    generated = self.generate_message(words)
                    if len(generated) > len(best_message):
                        best_message = generated

                if len(best_message.split()) > 3:
                    messages.append(best_message)

        self.train(msg)

        if messages:
            return random.choice(messages)

    def train(self, msg):
        for words in self.split_message(msg):
            # grab everything but the last word
            lkey = self.separator.join(words[1:]).lower()
            rkey = self.separator.join(words[:-1]).lower()

            # add the last word to the set
            self.ltable[lkey].append(words[0])
            self.rtable[rkey].append(words[-1])

    def random_chat(self):
        key = random.choice(self.rtable.keys())
        words = key.split(self.separator)
        return self.generate_message(words)

    def chat(self, context):
        words = context.split()
        if len(words) == 1:
            keys = []
            word = words[0].lower()
            for k, v in self.rtable.items():
                if k.endswith(word):
                    keys.extend(v)
            if keys:
                k = random.choice(keys)
                words.append(k)
        if len(words) == 1:
            keys = []
            word = words[0].lower()
            for k, v in self.ltable.items():
                if k.startswith(word):
                    keys.extend(v)
            if keys:
                k = random.choice(keys)
                words = [k] + words
        if len(words) < 2:
            return "Have nothing to say~"

        all_msgs = []
        for ctx in zip(words, words[1:]):
            messages = [self.generate_message(ctx) for i in range(3)]
            all_msgs.extend(messages)

        ctx = context.lower()
        all_msgs = [m for m in all_msgs if m.lower() not in ctx]
        if not all_msgs:
            return "Have nothing to say~"
        return random.choice(all_msgs)

    def load_file(self, filename):
        try:
            with open(filename) as fp:
                lines = fp.readlines()
        except:
            lines = []

        lines = list(set(lines))
        for line in lines:
            self.train(line)
