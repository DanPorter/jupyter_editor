"""
Jupyter Editor

Load Jupyter *.ipynb files (json) and edit the contents.
 - Add new python cells
 - Add new markdown cells
 - Edit source of current cells
 - append to current file or create new *.ipynb files

*** Remember ***
 - Save the Jupyter notebook before loading the current file
 - Refresh the Jupyter notebook page after updating the file
"""

from .main import NoteBook
from .tkgui.menu import EditorMenu

