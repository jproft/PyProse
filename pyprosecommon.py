# pyprosecommon.py
#
# constant-type definitions to increase readability
# many of these are determined by the (ancient!) encoding of the
# dictionary file PyProse inherits from earlier incarnations of Prose

from sys import version as PY_VERSION
from wx import __version__ as WX_VERSION

PYPROSE_VERSION = "2.0"

PLURAL     = 2
SINGULAR   = 1
UNSET      = None
FIRST      = 1
SECOND     = 2
THIRD      = 3
PRESENT    = 1
PAST       = 2
CURRENT    = -1      # position in plurality stack

# these values (except UNSET), entirely arbitrary, allow us to track
# plurality, person and tense states for each sentence.

# for plurality, a stack implemented as a list, pushing the state
# means appending the current plurality (possibly UNSET), and popping
# means popping the last (-1) item; to test **current** plurality,
# check whether plurStack[-1] == None (plurStack[CURRENT] == UNSET)

VOWELS	= 'aeiouAEIOU'    # handle 'y' separately

# for the dictionary
FLAGS      = 3       # last field in each word entry
ISSING     = 0       # position w/i field
ISPLUR     = 1       #        "
ISREG      = 2       #        "
SYLS       = 1       # field in word entry
STRESS     = 2       #        "

# for searches of IrregPart section of dictionary --
# NOT arbitrary, offsets specified in dictionary structure

INFINITIVE      = 0  # we never actually use this one
THIRDPRESENT    = 1
PASTTENSE       = 2
PASTPARTICIPLE  = 3

# used in display of trees, and calculations on them
TAB = " " * 6
TWG = "->"

ABOUT_TEXT = """\
A Python version of "Prose"
(for explanations see
        Virtual Muse: Experiments in Computer Poetry  
        Wesleyan University Press, 1996)

        By Charles O. Hartman  
        charles.hartman@conncoll.edu

        Programming contributions by Julia Proft
        
Version %s  |  Python %s  |  wxPython %s
""" % (PYPROSE_VERSION, PY_VERSION.split()[0], WX_VERSION)

HELP_TEXT = """\
PyProse generates sentences, It uses randomness
in two ways: First a sentence template (syntactical 
frame) is built by random choice among the rules 
in grammar.py. Then the slots in the template are 
filled by random choice from the dictionary in 
dictionary.py.

Press the spacebar to generate a sentence, or use
the Sentence menu -- which also offers a "keep 
going until hit on the head" option.

When you click on an output sentence in the left-hand 
panel, PyProse will reconstruct and display its tree. 
Click on any part of the tree in the right-hand panel 
to highlight the corresponding output in the left panel.
"""
