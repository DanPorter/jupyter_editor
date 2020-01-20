# Jupyter Editor
Create, open and edit jupyter notebook files.

Example:
``` Python
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