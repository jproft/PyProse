# pyprose.py 1.0
#
# The main module of PyProse

# A DEAD-SIMPLE DIAGNOSTIC MESSAGING SYSTEM, CROSS-PLATFORM
# myMsg = "current sentence index is " + `self.currSent`
# aDiagDlg = wx.MessageDialog(None, myMsg).ShowModal()


from pyprosecommon import * # imports wx
from pygui import *
from pygram import *
from pydict import *


#saveout = sys.stdout
#fsock = open('PYPROSE.OUT', 'w')
#sys.stdout = fsock
app = wx.App(redirect=False)
## setup up IPython embedded interpreter
#try:
    #__IPYTHON__
#except NameError:
    #from IPython.Shell import IPShellEmbed
    #ipargs = ['-wthread','-pi1','In <\\#>:','-pi2','   .\\D.:','-po','Out<\\#>:']
    #banner = 'Dropping into IPython interpreter'
    #exit_msg = '*** Back to main program'
    #app.ipshell = IPShellEmbed(ipargs,banner=banner,exit_msg=exit_msg)
#else:
    #def ipshell(): pass
# # #
windowTitle = "Prose - press Spacebar to generate sentence"
pf = ProseFrame(windowTitle)
pf.Show()
app.MainLoop()
#sys.stdout = saveout
#fsock.close()


