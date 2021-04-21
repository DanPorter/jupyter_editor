"""
Run jupyter notebook as script, output html document
https://nbconvert.readthedocs.io/en/latest/nbconvert_library.html
This script requires packages nbformat and nbconvert
"""

import jupyter_editor as je
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

notebook_file = 'test_nb_script.ipynb'
html_file = 'test_html.html'

# jupyter notebook
print('Use jupyter_editor to generate notebook')
notebook = je.NoteBook()
notebook.append_code("import numpy as np\nimport matplotlib.pyplot as plt")
notebook.append_code("x = np.arange(-10, 10, 0.01)\ny = x**2")
notebook.append_code("plt.figure()\nplt.plot(x, y)\nplt.xlabel('x')\nplt.ylabel('y')")
print(notebook)
notebook.save(notebook_file)

print('Open notebook using nbformat')
nb = nbformat.read(notebook_file, as_version=4)

print('Executing notebook using nbconvert.preprocessors.ExecutePreprocessor')
ep = ExecutePreprocessor()  # timeout=600, kernel_name='python3'
ep.preprocess(nb)

print('Exporting html using nbconvert.HTMLExporter')
exporter = HTMLExporter()
(body, resources) = exporter.from_notebook_node(nb)

with open(html_file, 'wt') as f:
    f.write(body)
print('Executed notebook %s written to %s' % (notebook_file, html_file))

print('finished!')
