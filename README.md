# Jupyter Editor
Create, open and edit jupyter notebook files.

By Dan Porter, Diamond Light Source Ltd. 2020

### What is this?
jupyter_editor load Jupyter notebook **.ipynb* files (json) and can edit the contents:
 - Add new python cells
 - Add new markdown cells
 - Edit source of current cells
 - append to current file or create new *.ipynb files
 - give cells a hidden reference so the correct cell will always be changed.

**Remember:**
 - Only the .ipynb file is changed, it does not update the jupyter server.
 - Save the Jupyter notebook before loading the current file
 - Refresh the Jupyter notebook page after updating the file

### Usage:
```commandline
ipython -i -m jupyter_editor notebook.ipynb
```
Or use the GUI:
```commandline
ipython -m jupyer_editor gui
```
 
 
### Example:
```python
import jupyter_editor as je

# Create new notebook/ open notebook
notebook = je.NoteBook(r"~/autoNotebook.ipynb")

# Add code cell
notebook.append_code("#This is some new code\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n", name='imports')
notebook.save() # this will overwrite the current notebook file, any unsaved changes on the jupyter server will be lost.
# Now refresh jupyter notebook on the web to see changes


# Edit notebook using 'name' tag
notebook.edit_by_name('imports', 'import sys, os\n')
notebook.save()
```


