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
