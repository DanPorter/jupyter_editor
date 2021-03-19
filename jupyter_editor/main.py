"""
Jupyter file editor

By Dan Porter
"""

import os
import json


def load_nb(filename):
    """
    Load jupyter notebook file, return dict object
    :param filename: filename.ipynb
    :return: dict
    """
    with open(filename) as fobj:
        data = json.load(fobj)
    return data


def save_nb(filename, notebook):
    """
    Save jupyter notebook file
    :param filename: filename to save to (.ipynb)
    :param notebook: dict notebook to save
    :return: None
    """
    with open(filename, 'wt') as fobj:
        json.dump(notebook, fobj)
    print('Notebook saved')


def string2list(source):
    """Convert string to list of stings"""
    return source.splitlines(True)


def search_notebook(notebook, name):
    """
    Search notebook for cell with metadata['name']=name, return first cell index
    :param notebook: dict: jupyter notebook
    :param name: str: name identifyer to search for, first instance returned
    :return: int: index
    """

    for idx, cell in enumerate(notebook['cells']):
        if 'name' in cell['metadata'].keys():
            if cell['metadata']['name'] == name:
                return idx
    print('%s not found' % name)
    return None


def create_code_cell(source='', name=None):
    """
    Create code cell block
    :param source: str python code
    :param name: str : name to identify this cell, should be unique
    :return: dict cell block
    """

    cell = {
        'cell_type': "code",
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': string2list(source)
    }
    if name:
        cell['metadata']['name'] = name
    return cell


def create_markdown_cell(source='', name=None):
    """
    Create markdown cell block
    :param source: str python code
    :param name: name to identify this cell, should be unique
    :return: dict cell block
    """

    cell = {
        'cell_type': "markdown",
        'metadata': {},
        'source': string2list(source)
    }
    if name:
        cell['metadata']['name'] = name
    return cell


def create_notebook(cells=[]):
    """
    Create notebook dict
    :param cells: list of cell dicts
    :return: dict
    """
    # See https://ipython.org/ipython-doc/3/notebook/nbformat.html
    notebook = {
        'metadata': {},
        'nbformat': 4,
        'nbformat_minor': 0,
        'cells': cells,
    }
    return notebook


class NoteBook:
    """
    Jupyter notebook class
    Usage:
        nb = Notebook('/path/notebook.ipynb')  # opens notebook if it exists, or creates a new one
        nb = NoteBook()  # creates new notebook called 'test.ipynb'
        nb.notebook  # underlying dict object containing jupyter cells
        print(nb)    # displays notebook cells
        print(nb.all_cells())  # prints source for every cell in notebook
    Methods:
        nb.load('file.ipynb')       Load file
        nb.save()                   Save .ipynb file (previous filename used)
        nb.save('newfile.ipynb')    Save as
        nb.append_code('code str')  Add code cell
        nb.append_markdown('str')   Add markdown cell
        nb.edit_cell(idx, 'str')    Edit/ append previous cell
    Methods using named cells:
        nb.search(name)             returns first index of named cell
        nb.edit_by_name(name,'str') Edit/ append previous cell using name
    """
    def __init__(self, filename=None):
        if filename is None:
            self.notebook = create_notebook()
            filename = 'test.ipynb'
        elif os.path.isfile(filename):
            self.load(filename)
        else:
            self.notebook = create_notebook()
        self.filename = filename

    def __repr__(self):
        return "JupyterNotebook Object with %d cells: NoteBook('%s')" % (len(self.notebook['cells']), self.filename)

    def __str__(self):
        out = 'Notebook(\'%s\')\n' % self.filename
        for n, cell in enumerate(self.notebook['cells']):
            name = (cell['metadata']['name'] if 'name' in cell['metadata'].keys() else '')
            example = (cell['source'][0].strip() if len(cell['source']) > 0 else 'Empty')
            cell_type = cell['cell_type']
            cell_len = len(cell['source'])
            out += '%3d: %10s : name=%10s : %2d lines : %s\n' % (n, cell_type, name, cell_len, example)
        return out

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        self.notebook = load_nb(filename)

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        save_nb(filename, self.notebook)

    def addcell(self, cell):
        """Add cell to end of cells, add empty cell after"""
        if len(self.notebook['cells']) > 0:
            lastcell = self.notebook['cells'][-1]
            if len(lastcell['source']) == 0:
                # replace last empty cell with new cell
                self.notebook['cells'][-1] = cell
            else:
                # append new cell to end
                self.notebook['cells'] += [cell]
        else:
            # append new cell to end
            self.notebook['cells'] += [cell]

        # append empty cell to end
        empty_cell = create_code_cell('')
        self.notebook['cells'] += [empty_cell]

    def insert(self, index, cell):
        """Inserts cell after cells[index]"""
        ncells = len(self.notebook['cells'])
        if index >= ncells:
            index = -1
        self.notebook['cells'].insert(index, cell)

    def search(self, name):
        """Search notebook for cell called name, return index"""
        return search_notebook(self.notebook, name)

    def insert_by_name(self, name, cell):
        """Insert cell after named cell"""
        idx = self.search(name)
        if idx:
            self.insert(idx+1, cell)
        else:
            print('cell appended to end')
            self.addcell(cell)

    def append_code(self, code_str, name=None):
        cell = create_code_cell(code_str, name)
        self.addcell(cell)

    def append_markdown(self, code_str, name=None):
        cell = create_markdown_cell(code_str, name)
        self.addcell(cell)

    def cell_source(self, cell_index=0, name=None):
        """Return string source for cell"""
        if name is not None:
            cell_index = self.search(name)
        return ''.join(self.notebook['cells'][cell_index]['source'])

    def all_cells(self):
        """return str of all cells in notebook"""
        out = 'Notebook(\'%s\')\n' % self.filename
        for n, cell in enumerate(self.notebook['cells']):
            name = (cell['metadata']['name'] if 'name' in cell['metadata'].keys() else '')
            cell_type = cell['cell_type']
            cell_len = len(cell['source'])
            source = ''.join(cell['source'])
            out += '%3d: %10s : name=%10s : %2d lines \n%s\n' % (n, cell_type, name, cell_len, source)
        return out

    def edit_cell(self, cell_index, source='', append=True, name=None):
        """Replace or append string source in cell"""
        cell = self.notebook['cells'][cell_index]
        current_source = self.cell_source(cell_index)
        if append:
            source = current_source + '\n' + source
        cell['source'] = string2list(source)
        if name:
            cell['metadata']['name'] = name
        self.notebook['cells'][cell_index] = cell

    def edit_by_name(self, name, source='', append=True):
        """Edit cell with metaname=name"""
        idx = self.search(name)
        if idx is not None:
            self.edit_cell(idx, source, append)
        else:
            print('Code cell appended to end')
            self.append_code(source, name)

