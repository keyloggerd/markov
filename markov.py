#!/usr/bin/env python3
import pickle
import random
import re
import os

random.seed()

MARKOV_NODE_LIST_FILE = 'markov_node_list.pkl'


class MarkovNode(object):
    def __init__(self, word):
        self.word = word
        # next_words should be a dict of { "word": occurances of that word after this one }
        self.next_words = {}
        self.length = len(word)

    def __str__(self):
        return self.word + ": " + str(self.next_words)

    def increase_link(self, next_word):
        n = self.next_words.get(next_word)
        if n is not None:
            self.next_words[next_word] += 1
        else:
            self.next_words[next_word] = 1

    def link_total(self):
        return sum(self.next_words.values(), 0)

    def choose_next(self):
        select = []
        for word in self.next_words:
            for _ in range(self.next_words[word]):
                select.append(word)
        return select[random.randint(0, len(select)-1)]


class MarkovNodeList():
    BARRIER = "<break>"

    def __init__(self):
        # dict of { "word": MarkovNode }
        self.words = {}
        self.words[MarkovNodeList.BARRIER] = MarkovNode(MarkovNodeList.BARRIER)

    def __str__(self):
        out = ""
        for i in self.words:
            out += str(self.words[i]) + "\n"
        return out

    def increase_link(self, cur_word, next_word):
        n = self.words.get(next_word)
        if n is None:
            # make a node for the new word
            self.words[next_word] = MarkovNode(next_word)
        # increase the link from this word to that one
        self.words[cur_word].increase_link(next_word)

    def get_words_of_length(self, length):
        return [a for a in self.words.keys() if len(a) == length]

    def ingest_file(self, file_name):
        with open(file_name) as f:
            content = f.read()

        content = content.lower()
        content = re.sub(r'([^a-z0-9\'\. ])', r' ', content)
        content = re.sub(r'(\b\' | \'\b)', r' ', content)
        content = re.sub(r'\.', r' . ', content)

        words = content.split()
        prev_word = MarkovNodeList.BARRIER
        for cur_word in words:
            if cur_word == '.':
                self.increase_link(prev_word, MarkovNodeList.BARRIER)
                prev_word = MarkovNodeList.BARRIER
            else:
                self.increase_link(prev_word, cur_word)
                prev_word = cur_word

    def generate(self, length):
        cur_word = MarkovNodeList.BARRIER
        out = ""
        for _ in range(length):
            next_word = self.words[cur_word].choose_next()
            out += next_word + " "
            cur_word = next_word
        return out

    @staticmethod
    def load(file_name):
        with open(file_name, 'rb') as input:
            return pickle.load(input)

    def save(self):
        with open('markov_node_list.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)


def main():
    mnl1 = MarkovNodeList.load(MARKOV_NODE_LIST_FILE)
    print(mnl1)


# rudimentary tests --------------------------
# test MarkovNode
m=MarkovNode("test")
m.increase_link("anna")
m.increase_link("anna")
m.increase_link("anna")
m.increase_link("jared")
m.increase_link("jared")
m.choose_next()
assert m.word == "test"
assert len(m.next_words) == 2
assert m.next_words["anna"] == 3
assert m.next_words["jared"] == 2
assert m.link_total() == 5

# test MarkovNodeList
mnl=MarkovNodeList()
mnl.increase_link(MarkovNodeList.BARRIER, "poke")
mnl.increase_link("poke", "anna")
mnl.increase_link("anna", "and")
mnl.increase_link("and", "then")
mnl.increase_link("then", "poke")
mnl.increase_link("poke", "jared")
mnl.increase_link("jared", MarkovNodeList.BARRIER)

assert mnl.words["poke"].next_words == {"anna": 1, "jared": 1}


main()
