# pyprosecommon.py
#
# Constant-type definitions to increase readability

from sys import version as PY_VERSION
from wx import __version__ as WX_VERSION

PYPROSE_VERSION = "2.0"

# For tracking plurality.
SINGULAR   = 1
PLURAL     = 2

# For tracking person.
FIRST      = 1
SECOND     = 2
THIRD      = 3

# For tracking tense.
PRESENT    = 1
PAST       = 2

# For plurality, a stack implemented as a list, pushing the state
# means appending the current plurality (possibly UNSET), and popping
# means popping the last (-1) item; to test **current** plurality,
# check whether plurStack[-1] == None (plurStack[CURRENT] == UNSET)

UNSET      = None
CURRENT    = -1       # position in plurality stack

VOWELS	= 'aeiouAEIOU'    # handle 'y' separately

# For the dictionary.
FLAGS      = 3        # last field in each word entry
ISSING     = 0        # position within field
ISPLUR     = 1        #    "       "      " 
ISREG      = 2        #    "       "      "
SYLS       = 1        # field in word entry
STRESS     = 2        #   "    "   "    "

# For searches of IrregPart section of dictionary.
# (NOT arbitrary: offsets are in dictionary structure.)

INFINITIVE      = 0   # we never actually use this one
THIRDPRESENT    = 1
PASTTENSE       = 2
PASTPARTICIPLE  = 3

TAB = " " * 6    # amount of blank space per tree tab
TWG = "->"       # marker that indicates a tree twig

# Text for the 'About' dialog.
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

# Text for the 'Help' dialog.
HELP_TEXT = """\
PyProse generates sentences. It uses randomness
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
