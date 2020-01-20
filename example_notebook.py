"""
Test logbook code
"""

import jupyter_editor as je

notebook = je.NoteBook(r"C:\Users\grp66007\autoNotebook.ipynb")

notebook.append_code("#This is some new code\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n",'imports')
notebook.save()

idx = notebook.search('imports')
print('Cell no: %s'%idx)

notebook.edit_by_name('imports', 'import sys, os\n')
notebook.save()