# pygui.py
#
# The interface classes for PyProse

import wx
import wx.stc as stc
import pygram, pydict
from pyprosecommon import *
from os import getcwd

# Note: It is essential to import random AFTER the two other modules.
# Each of them needs to import it; but each time it's imported, the
# the generator is reseeded. The import here must be the last, if 
# we're to use setstate/getstate to reproduce conditions for 
# rebuilding a sentence tree
import random


class ProseFrame(wx.Frame):

    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(900,700))
        
        self.s = []         # list of instances of class Sentence
        self.currSent = -1  # increment as index
        
        random.seed()	    # just once per app run, for reconstruction

        self.dict = pydict.PDict(self)
        self.grammar = pygram.Grammar(self)
        
        self.outSTC = OutputSTC(self, -1)
        self.treeWin = TreeSTC(self, -1)
        
        # SIZERS AND LAYOUT #

        ls = wx.BoxSizer(wx.HORIZONTAL)
        rs = wx.BoxSizer(wx.HORIZONTAL)
        ms = wx.BoxSizer(wx.HORIZONTAL)
        
        ls.Add(self.outSTC, 1, wx.EXPAND)
        rs.Add(self.treeWin, 1, wx.EXPAND)
        
        ms.Add(ls, 2, wx.EXPAND)
        ms.Add(rs, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(ms)
        self.Layout()
        
        # MENU STUFF #
        
        menuBar = wx.MenuBar()

        titles = ["File", "Sentences", "&Help"]  # Keep 'Help' last!
        menus = [wx.Menu() for t in titles]

        items = [
            ("&Save output\tCtrl+S", 101, self.SaveOutput),
            ("&Generate one sentence\tCtrl+G", 201, self.GenSentence),
            ("&Until mouse-click\tCtrl+U", 202, self.StartTimer),
            ("PyProse help", 301, self.ShowHelp),
            ("About PyProse", wx.ID_ABOUT, self.ShowAbout)
        ]

        for t in items:
            if t[1] == wx.ID_ABOUT:
                menus[len(menus)-1].Append(t[1], t[0])
            else:
                menus[t[1]//100-1].Append(t[1], t[0])
            self.Bind(wx.EVT_MENU, t[2], id=t[1])

        for i, m in enumerate(menus):
            menuBar.Append(m, titles[i])

        wx.GetApp().SetMacHelpMenuTitleName("&Help")
        self.SetMenuBar(menuBar)

        # SETUP FOR CONTINUOUS GENERATION #
        
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.GenSentence)
        self.outSTC.Bind(wx.EVT_LEFT_DOWN, self.StopTimer)

        self.ShowAbout() # Show 'About' on start.

    def SaveOutput(self, evt=None):
        """Write all text output so far to a file"""
        self.StopTimer()
        dlg = wx.FileDialog(
            self, message="Save As", defaultDir=getcwd(), 
            defaultFile="output.txt", wildcard="*.txt", 
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
        )
        if dlg.ShowModal() == wx.ID_OK:
            with open(dlg.GetPath(), 'w') as f:
                f.write(self.outSTC.GetText())
        dlg.Destroy()

    def ShowAbout(self, evt=None):
        dlg = wx.MessageDialog(
            self, message=ABOUT_TEXT, 
            caption="PyProse", style=wx.OK
        )
        dlg.ShowModal()
        dlg.Destroy()

    def ShowHelp(self, evt=None):
        dlg = wx.MessageDialog(
            self, message=HELP_TEXT, 
            caption="PyProse Help", style=wx.OK
        )
        dlg.ShowModal()
        dlg.Destroy()

    def StartTimer(self, evt=None):
        self.Timer.Start(100)

    def StopTimer(self, evt=None):
        if self.Timer.IsRunning():
            self.Timer.Stop()

    def GenSentence(self, evt=None):
        """Calls grammar to make template, dictionary to fill it in"""
        # establish data for the sentence
        sData = pygram.Sentence()
        if random.randint(0,1):
            sData.tense = PRESENT
        else:
            sData.tense = PAST
        sData.randstate = random.getstate()
        # next three lines, the whole center of the business
        self.treeWin.ClearAll()         # prepare to draw new tree
        sentenceTemplate = self.grammar.BuildTemplate()
        sent = self.dict.BuildSentence(sentenceTemplate, sData)
        # display; sentences added at end, go to end before figuring offset!
        self.outSTC.GotoLine(self.outSTC.GetLineCount()+1)
        sData.offset = self.outSTC.GetCurrentPos()
        sData.length = len(sent)
        self.s.append(sData)
        self.outSTC.AddText(sent)
        self.outSTC.GotoLine(self.outSTC.GetLineCount()+1)
        self.currSent = len(self.s) - 1

# end of class ProseFrame
# # # # # # # # # # # # #


class TreeSTC(stc.StyledTextCtrl):
    
    def __init__(self, parent, ID):
        """Initialize a StyledTextControl for display of sentence trees"""
        stc.StyledTextCtrl.__init__(self, parent, ID)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)

    def OnMouseDown(self, event):
        """Select portion of tree embedded with clicked line, and what corresponds in output"""
        mom = self.GetParent()	# to examine and mark output text
        cLine = self.LineFromPosition(
            self.PositionFromPoint(event.GetPosition())
        )
        if not cLine:
            lStrt = 0
        else:
            lStrt = self.GetLineEndPosition(cLine - 1) + 1
        self.SetSelection(lStrt, self.GetLineEndPosition(cLine))
        twigsBefore = 0
        for ln in range(cLine):
            if IsTwigLine(self.GetLine(ln)):
                twigsBefore += 1
        line = self.GetLine(cLine)
        sentInx = mom.currSent
        if line.find(TWIGMARK) != -1:	# a twig
            if line.find('#') == -1:	# other than a flag
                twigs = MarkTwigLimits(mom, sentInx)
                mom.outSTC.SetSelection(
                    twigs[twigsBefore][0], 
                    twigs[twigsBefore][1]
                )
            else:      # flag, no repr in output; erase any selection
                mom.outSTC.SetSelection(
                    mom.outSTC.GetSelectionStart(), 
                    mom.outSTC.GetSelectionStart()
                )
        else:		# a predicate
            level = line.count(TREEBLANK);
            twigCount = 0
            for ln in range(cLine+1, self.GetLineCount()):
                s = self.GetLine(ln)
                if s.count(TREEBLANK) <= level:
                    break
                if IsTwigLine(s):
                    twigCount += 1
            endSel = self.PositionFromLine(ln-1) + self.LineLength(ln-1)
            self.SetSelection(self.GetSelectionStart(), endSel)
            twigs = MarkTwigLimits(mom, sentInx)
            if len(twigs):
                mom.outSTC.SetSelection(
                    twigs[twigsBefore][0], 
                    twigs[twigsBefore+twigCount-1][1]
                )
#
# # # # # # end of TreeStC itself

# non-class functions to do bits of TreeSTC's OnMouseDown's work

def MarkTwigLimits(theFrame, sent):
    """Nonclass helper for TreeSTC: [what does this do??]"""
    sStart = theFrame.s[sent].offset
    sEnd = sStart + theFrame.s[sent].length
    s = theFrame.outSTC.GetTextRange(sStart, sEnd)
    twiglist = [[sStart,sStart]]
    c = 0
    while c < len(s):
        if s[c] in " ,)(;:.?":
            twiglist[len(twiglist)-1][1] = c + sStart
            if s[c] == ' ':
                c += 1
            if c >= len(s):
                break
            twiglist.append([c+sStart,c+sStart+1])
            if s[c] == '(':
                c += 1
                twiglist.append([c+sStart,c+sStart+1])
        c += 1
    return twiglist

def IsTwigLine(s):
    """Non-class helper for TreeSTC: Identify a 'twig' line"""
    return (s.find(TWIGMARK) != -1 and s.find('#') == -1)


# end of class TreeSTC (and adjunct functions)
# # # # # # # # # # # # # # # # # # # # # # #


class OutputSTC(stc.StyledTextCtrl):
    """This StyledTextControl is for sentences output by the program"""

    def __init__(self, parent, ID):
        """Initialize an STC formatted for output, bind mouse and key commands"""
        stc.StyledTextCtrl.__init__(self, parent, ID)
        self.SetUseHorizontalScrollBar(0)
        self.SetMargins(20,10)
        self.SetWrapMode(stc.STC_WRAP_WORD)
        self.SetEndAtLastLine(0)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMousePrelimDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)

# This messy dance is Josiah Carlson's suggestion for how to handle both
# mouseclick and doubleclick: the former selects the whole sentence, the
# latter selects the single word (excluding non-internal punctuation)
    def OnMousePrelimDown(self, event):
        self.handled = 0
        wx.CallAfter(self.OnMouseDown, event.GetPosition())

    def OnMouseDown(self, mouseclickpos):
        mom = self.GetParent()
        if self.handled or not len(mom.s): return
        clickpos = self.PositionFromPoint(mouseclickpos)
        for inx in range(len(mom.s)):
                if mom.s[inx].offset > clickpos: break
        if mom.s[inx].offset > clickpos: inx -= 1
        sentend = mom.s[inx].offset + mom.s[inx].length - 1
        mom.currSent = inx
        self.SetSelection(mom.s[inx].offset, sentend)
        mom.treeWin.ClearAll()
        # recreate state of rand gen for BuildTemplate
        temprand = random.getstate()
        random.setstate(mom.s[inx].randstate)
        sentenceTemplate = mom.grammar.BuildTemplate()
        random.setstate(temprand)

    def OnDoubleClick(self, event):
        self.handled = 0                # coordination with single-click
        # select a single word (including internal punct, excluding terminal)
        startword = endword = self.PositionFromPoint(event.GetPosition())
        while startword > 0 and not chr(self.GetCharAt(startword)).isspace():
            startword -= 1
        startword += 1
        if not chr(self.GetCharAt(startword)).isalnum():
            startword += 1
        while endword < self.GetTextLength() and not chr(self.GetCharAt(endword)).isspace():
            endword += 1
        # flaw: excludes terminal apostrophe from plural possessives
        if not chr(self.GetCharAt(endword - 1)).isalnum():
            endword -= 1
        self.SetSelection(startword, endword)

# <this is where further code is called that will replace the word>
# and how does that work? from the text I need to work back to position in the template (not easy!);
# then go through something like PDict.BuildSentence() to get a new candidate for that slot; and
# I may have to rerun the whole template up to that point to find out what the state of plurality, 
# tense, and person is at that point. What a mess. Would keeping word-level data about each
# sentence make more sense? (and then reconstructing the members of PDict to take arguments
# for person, tense, plurality, rather than a single, simple Sentence data package)
# What this begins to amount to is keeping all the output as some kind of internal data structure,
# rather than using the STC, the display itself, as the data-home of all the sentences.

    def OnKeyDown(self, event):
        """ Keystrokes: space for generate; escape to quit. """
        if event.KeyCode == wx.WXK_SPACE:
            self.GetParent().GenSentence()
        elif event.KeyCode == wx.WXK_ESCAPE:
            self.GetParent().Close()


# end of class OutputSTC
# # # # # # # # # # # # #
