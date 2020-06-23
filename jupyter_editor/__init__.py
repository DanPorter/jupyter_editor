r"""
Jupyter Editor

Load Jupyter *.ipynb files (json) and edit the contents.
 - Add new python cells
 - Add new markdown cells
 - Edit source of current cells
 - append to current file or create new *.ipynb files

*** Remember ***
 - Save the Jupyter notebook before loading the current file
 - Refresh the Jupyter notebook page after updating the file

Usage:
    >> import jupyter_editor as je
    >> notebook = je.NoteBook(r"C:\Users\dgpor\autoNotebook.ipynb")
    >> notebook.append_code("#This is some new code\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n",'imports')
    >> notebook.save()

For GUI use:
    ipython -m jupyter_editor gui

To Parse a notebook file:
    ipython -m jupyter_editor 'somefile.ipynb'

GitHub Repo: https://github.com/DanPorter/jupyter_editor

By Dan Porter, PhD
Diamond
2020

Version 1.1.0
Last updated: 23/06/20

Version History:
23/06/20    1.1.0   Version History started
"""

from .main import NoteBook
from .tkgui.menu import EditorMenu

__version__ = "1.1.0"
__date__ = "23/06/2020"

def start_gui():
    EditorMenu()