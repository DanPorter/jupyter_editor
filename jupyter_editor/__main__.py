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

By Dan Porter, PhD
Diamond
2020
"""
if __name__ == '__main__':

    import sys
    import jupyter_editor as je

    print('\nJupyter Editor version %s, %s\n By Dan Porter, Diamond Light Source Ltd.' % (je.__version__, je.__date__))
    print('See help(je) for info, or type: je.EditorMenu() to get started!')

    notebook = None
    for arg in sys.argv:
        if 'ipynb' in arg.lower():
            print('notebook = je.NoteBook("%s")' % arg)
            notebook = je.NoteBook(arg)
            print(notebook)
        elif 'gui' in arg.lower():
            je.EditorMenu(notebook)
