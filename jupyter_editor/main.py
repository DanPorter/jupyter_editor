"""
Jupyter file editor

By Dan Porter
"""

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
    Search notebook for cell with metadata['name']=name, return cell index
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
    """
    def __init__(self, filename=None):
        if filename is None:
            self.notebook = create_notebook()
            filename = 'test.ipynb'
        else:
            self.load(filename)
        self.filename = filename

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        self.notebook = load_nb(filename)

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        save_nb(filename, self.notebook)

    def append_code(self, code_str, name=None):
        cell = create_code_cell(code_str, name)
        self.notebook['cells'] += [cell]

    def append_markdown(self, code_str, name=None):
        cell = create_markdown_cell(code_str, name)
        self.notebook['cells'] += [cell]

    def cell_source(self, cell_index):
        """Return string source for cell"""
        return ''.join(self.notebook['cells'][cell_index]['source'])

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

    def search(self, name):
        """Search notebook for cell called name, return index"""
        return search_notebook(self.notebook, name)

    def edit_by_name(self, name, source='', append=True):
        """Edit cell with metaname=name"""
        idx = self.search(name)
        if idx:
            self.edit_cell(idx, source, append)


