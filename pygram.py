# pygram.py
#
# the classes related to the grammar part of PyProse: loading it,
# using it to build a template for each sentence

import random
from pyprosecommon import *
from grammar import GRAMMAR


class Grammar:

    def __init__(self, mom):
        """Read the GRAMMAR dictionary into the internal data structure"""
        self.mom = mom
        self.Gr = {}
        for pred, rules in GRAMMAR.items():
            self.Gr[pred] = []
            for rule in rules:
                slist = rule.split()
                if slist[0].isdigit():
                    weight = int(slist[0])
                    start = 1
                else:
                    weight = 1
                    start = 0
                for i in range(weight): # repeat rule in Gr
                    self.Gr[pred].append(slist[start:])

    def BuildTemplate(self, predicate="Sentence", level=0):
        if not level:
            self.template = []
        self.mom.treeWin.AddText(TAB * level + predicate + '\n')
        for c in random.choice(self.Gr[predicate]):
            if c not in self.Gr: # a twig
                self.mom.treeWin.AddText(TAB * (level+1) + TWG + c + '\n')
                self.template.append(c)
            else:
                self.BuildTemplate(c, level + 1)
        return self.template


class Sentence:

    def __init__(self):
        self.offset = 0
        self.length = 0
        self.person = None
        self.tense = PRESENT
        self.plurStack = [None]
        self.indefArtPending = False
        self.randstate = random.getstate()

    def __repr__(self):
        s = 'offset ' + `self.offset`
        # Add person to string.
        if self.person == FIRST:
            s += ', person FIRST'
        elif self.person == SECOND:
            s += ', person SECOND'
        else:
            s += ', person THIRD'
        # Add tense to string.
        if self.tense == PRESENT:
            s += ', tense PRESENT'
        else:
            s += ', tense PAST'
        s += ', plur: ['
        # Add plurality to string.
        for i in self.plurStack:
            if i == SINGULAR:
                s += "sing,"
            elif i == PLURAL:
                s += "plur,"
            else:
                s += 'unset,'
        s += ']'
        return s

    def pIsUnset(self):
        return self.plurStack[CURRENT] == UNSET

    def pIsSing(self):
        return self.plurStack[CURRENT] == SINGULAR

    def pIsPlur(self):
        return self.plurStack[CURRENT] == PLURAL

    def pUnset(self):
        self.plurStack[CURRENT] = UNSET

    def pSetSing(self):
        self.plurStack[CURRENT] = SINGULAR

    def pSetPlur(self):
        self.plurStack[CURRENT] = PLURAL
