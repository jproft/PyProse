# pyprose.py
#
# The main module of PyProse

from wx import App
from pygui import ProseFrame

title = "Prose - press Spacebar to generate sentence"

app = App(redirect=False)
ProseFrame(title).Show()
app.MainLoop()
