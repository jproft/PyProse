# pyprosecommon.py
#
# constant-type definitions to increase readability
# many of these are determined by the (ancient!) encoding of the
# dictionary file PyProse inherits from earlier incarnations of Prose

import wx
import os, sys

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
TREEBLANK = " " * 6
TWIGMARK  = "->"

abouttxt = """\
A Python version of "Prose"
(for explanations see
        Virtual Muse: Experiments in Computer Poetry  
        Wesleyan University Press, 1996)

        Charles O. Hartman  
        charles.hartman@conncoll.edu

Version 1.0, March 2012
"""

helptxt = """\
PyProse generates sentences, It uses randomness
in two ways: First a sentence template (syntactical 
frame) is built by random choice among the rules 
in PROSE.GRA. Then the slots in the template are 
filled by random choice from the dictionary in 
PROSE.DIC.

Press the spacebar to generate a sentence, or use
the Sentence menu -- which also offers a "keep 
going until hit on the head" option.

When you click on an output sentence in the left-hand 
panel, PyProse will reconstruct and display its tree. 
Click on any part of the tree in the right-hand panel 
to highlight the corresponding output in the left panel.
"""

# the following functions are Not the Right Way to locate our grammar and
# dictionary data files, though they seem to work on Mac and Windows

def GetDefaultFilename(filename):
    wildcard = "All files (*.*) | *.*"
    # baroque way to get probable launched-from directory
    try:
        basedir = os.path.dirname(os.path.abspath(__file__))
    except:
        basedir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if sys.platform == 'darwin':	# Mac is weird!
        upto = basedir.find('/Contents/Resources')
        if upto != -1:
            basedir = basedir[:basedir[:upto].rfind('/')]
        return basedir + '/' + filename
    else:
        upto = basedir.find('.exe')
        if upto != -1:
            basedir = basedir[:basedir[:upto].rfind('\\')]
        return basedir + '\\' + filename

def LocateDataFile(filename):
    if os.path.exists(filename):
        return filename
    dlg = wx.FileDialog(self, message="Please locate the file " + filename,
                        defaultDir=os.getcwd(), defaultFile=filename,
                        wildcard=wildcard, style=wx.OPEN | wx.CHANGE_DIR)
    if dlg.ShowModal() == wx.ID_OK:
        filename = dlg.GetPath()
        dlg.Destroy()
        if os.path.exists(filename): return filename
        else: return None
    else:
        dlg.Destroy()
        return None
