#!/usr/bin/env python3
from functools import *

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

class MarkovNodeList():
    START = "START_OF_SENTENCE"
    END = "END_OF_SENTENCE"

    def __init__(self):
        # dict of { "word": MarkovNode }
        self.words = {}
        self.words[MarkovNodeList.START] = MarkovNode(MarkovNodeList.START)

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

# test MarkovNode
m = MarkovNode("test")
m.increase_link("anna")
m.increase_link("anna")
m.increase_link("anna")
m.increase_link("jared")
m.increase_link("jared")
assert m.word == "test"
assert len(m.next_words) == 2
assert m.next_words["anna"] == 3
assert m.next_words["jared"] == 2
assert m.link_total() == 5

# test MarkovNodeList
mnl = MarkovNodeList()
mnl.increase_link(MarkovNodeList.START, "poke")
mnl.increase_link("poke", "anna")
mnl.increase_link("anna", "and")
mnl.increase_link("and", "then")
mnl.increase_link("then", "poke")
mnl.increase_link("poke", "jared")
mnl.increase_link("jared", MarkovNodeList.END)

assert mnl.words["poke"].next_words == {"anna": 1, "jared": 1}
