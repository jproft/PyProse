# pygram.py
#
# the classes related to the grammar part of PyProse: loading it,
# using it to build a template for each sentence

import random
from pyprosecommon import *


# note on __init__: the 'mom' argument is a concession to the fact that
# PDict and Grammar must be owned by the Frame, if only because this
# module and the grammar one can't import the GUI one, for the sake
# of importing the random module at a controlled Last Point (for
# get/set state)

# the "weight" factor for rules (a number after the predicate) is treated
# here as controlling the number of repetitions of the rule in the
# grammar (only the old "Design a Sentence" function valued non-repetition
# in the grammar

class Grammar:

    def __init__(self, mom, filename):
        """Read the Grammar file into the internal data structure"""
        self.mom = mom
        self.Gr = {}
        gfile = open(filename, 'rU')
        for line in gfile.readlines():
            if len(line) < 3: continue	# "blank" (3 is arbitrary)
            slist = line.split()
            pred = slist[0]
            if slist[1].isdigit():
                weight = int(slist[1])
                start = 2
            else:
                weight = start = 1
            for i in range(weight): # repeat rule in Gr
                if pred not in self.Gr:
                    self.Gr[pred] = [slist[start:]]
                else:
                    self.Gr[pred].append(slist[start:])
        # mere curiosity: how many grammar rules?
        # self.gramLines = 0
        # for j in self.Gr:
        #   self.gramLines += len(self.Gr[j])
        gfile.close()

    def BuildTemplate(self):
        self.template = []
        self._buildTemplate('Sentence', 0)
        return self.template

    def _buildTemplate(self, predicate, level):
        """Recursively build a sentence template; 'level' arg tracks recursion for display"""
        self.mom.treeWin.AddText(TREEBLANK * level + predicate + '\n')
        for c in random.choice(self.Gr[predicate]):
            if c not in self.Gr:	# a twig
                self.mom.treeWin.AddText(TREEBLANK * (level+1) + '->' + c + '\n')
                self.template.append(c)
            else: self._buildTemplate(c, level + 1)



class Sentence:

    def __init__(self):
        self.randstate = random.getstate()		# will do again
        self.offset = 0			# will be set for each as added
        self.length = 0			# ditto
        self.plurStack = [None]  # stack of plurality states
        self.tense = PRESENT	# set at random per sentence
        self.person = None
        self.indefArtPending = False

    def __repr__(self):			# to print for debugging
        s = 'offset ' + `self.offset`
        if self.person == FIRST: s += ', person FIRST'
        elif self.person == SECOND: s += ', person SECOND'
        else: s += ', person THIRD'
        if self.tense == PRESENT: s += ', tense PRESENT'
        else: s += ', tense PAST'
        s += ', plur: ['
        for i in self.plurStack:
            if i == SINGULAR: s += "sing,"
            elif i == PLURAL: s += "plur,"
            else: s += 'unset,'
        s += ']'
        return s

    # streamline the interface for plurStack
    def pIsUnset(self):
        if self.plurStack[CURRENT] == UNSET: return True
        else: return False
    def pIsSing(self):
        if self.plurStack[CURRENT] == SINGULAR: return True
        else: return False
    def pIsPlur(self):
        if self.plurStack[CURRENT] == PLURAL: return True
        else: return False
    def pUnset(self):           # called only in pydict doPunct
        self.plurStack[CURRENT] = UNSET
    def pSetSing(self):
        self.plurStack[CURRENT] = SINGULAR
    def pSetPlur(self):
        self.plurStack[CURRENT] = PLURAL
