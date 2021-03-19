"""
Main crystal gui windows
"""

import sys, os

if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
else:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox

from ..main import NoteBook

# Fonts
TF = ["Times", 12]
BF = ["Times", 14]
SF = ["Times New Roman", 14]
LF = ["Times", 14]
HF = ['Courier',12]
TTF = ("Helvetica", 10, "bold italic")
# Colours - background
bkg = 'snow'
ety = 'white'
btn = 'azure' #'light slate blue'
opt = 'azure' #'light slate blue'
btn2 = 'gold'
TTBG = 'light grey'
# Colours - active
btn_active = 'grey'
opt_active = 'grey'
# Colours - Fonts
txtcol = 'black'
btn_txt = 'black'
ety_txt = 'black'
opt_txt = 'black'
TTFG = 'red'


class EditorMenu:
    """
    GUI menu of edit options
      EditorMenu('jupyter_notebook.ipynb')
    """

    def __init__(self, filename=None):
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('Jupyter Notebook Editor  by D G Porter [dan.porter@diamond.ac.uk]')
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)

        box_height = 6
        box_width = 40

        self.notebook = NoteBook(filename)

        # Create Widget elements from top down
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N, expand=tk.YES, fill=tk.BOTH)

        # Filename (variable)
        f_file = tk.Frame(frame)
        f_file.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        self.file = tk.StringVar(frame, self.notebook.filename)

        var = tk.Label(f_file, text='Notebook file:', font=SF, width=10)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)
        var = tk.Label(f_file, textvariable=self.file, width=40, font=TF)
        var.pack(side=tk.LEFT, expand=tk.YES)
        var = tk.Button(f_file, text='Load', font=BF, bg=btn, activebackground=btn_active, command=self.fun_load)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)
        var = tk.Button(f_file, text='Update', font=BF, bg=btn, activebackground=btn_active, command=self.fun_update)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)
        var = tk.Button(f_file, text='New', font=BF, bg=btn, activebackground=btn_active, command=self.fun_new)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)

        ########################################################
        # List box with scroll bar
        frm_list = tk.Frame(frame)
        frm_list.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        scl_texty = tk.Scrollbar(frm_list)
        scl_texty.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.list = tk.Listbox(frm_list,
                            font=HF,
                            width=box_width,
                            height=box_height,
                            selectmode=tk.SINGLE,
                            background='white',
                            yscrollcommand=scl_texty.set)
        self.list.configure(exportselection=False)
        self.list.bind("<<ListboxSelect>>", self.fun_cell_select)

        # Populate text box
        self.fun_listcells()

        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        scl_texty.config(command=self.list.yview)

        ########################################################
        # Cell type and name
        frm = tk.Frame(frame, bd=1, relief=tk.GROOVE)
        frm.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.current_cell = tk.IntVar(frame, 0)
        self.cell_type = tk.StringVar(frame, 'code')
        self.cell_name = tk.StringVar(frame, '')

        var = tk.Entry(frm, textvariable=self.current_cell, font=TF, width=4, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, padx=5)

        var = tk.Label(frm, text='Type:', font=SF)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)
        var = tk.OptionMenu(frm, self.cell_type, *['code', 'markdown'])
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT, padx=5)

        var = tk.Label(frm, text='Name:', font=SF)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)
        var = tk.Entry(frm, textvariable=self.cell_name, font=TF, width=20, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)

        ########################################################
        # Eval box with scroll bar
        frm_text = tk.Frame(frame)
        frm_text.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        scl_textx = tk.Scrollbar(frm_text, orient=tk.HORIZONTAL)
        scl_textx.pack(side=tk.BOTTOM, fill=tk.BOTH)

        scl_texty = tk.Scrollbar(frm_text)
        scl_texty.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.text = tk.Text(frm_text,
                            font=HF,
                            width=box_width,
                            height=box_height,
                            wrap=tk.NONE,
                            background='white',
                            xscrollcommand=scl_textx.set,
                            yscrollcommand=scl_texty.set)
        self.text.configure(exportselection=True)

        # Populate text box
        self.text.insert(tk.END, 'Type code here')

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        scl_textx.config(command=self.text.xview)
        scl_texty.config(command=self.text.yview)

        # self.txt_text.config(xscrollcommand=scl_textx.set,yscrollcommand=scl_texty.set)

        ########################################################
        # Cell Buttons
        frm = tk.Frame(frame, bd=1, relief=tk.GROOVE)
        frm.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)

        var = tk.Button(frm, text='Edit cell', font=BF, bg=btn,
                        activebackground=btn_active, command=self.fun_edit_source)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5, pady=5)

        box = tk.Frame(frm, bd=1, relief=tk.SUNKEN)
        box.pack(side=tk.LEFT)

        var = tk.Button(box, text='Add cell', font=BF, bg=btn,
                        activebackground=btn_active, command=self.fun_add_source)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5, pady=5)

        self.cell_option = tk.IntVar(frame, 0)
        for n, mode in enumerate(['end', 'above', 'below']):
            var = tk.Radiobutton(box, text=mode, variable=self.cell_option, value=n, font=BF)
            var.pack(side=tk.LEFT)

        # start mainloop
        # In interactive mode, this freezes the terminal
        # To stop this, need a way of checking if interactive or not ('-i' in sys.argv)
        # However sys in this file is not the same as sys in the operating script
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    ###################################################################################
    ############################## FUNCTIONS ##########################################
    ###################################################################################

    def fun_listcells(self):
        """Update listbox with cells"""
        self.list.delete(0, tk.END)
        for n, cell in enumerate(self.notebook.notebook['cells']):
            name = (cell['metadata']['name'] if 'name' in cell['metadata'].keys() else '')
            example = (cell['source'][0].strip() if len(cell['source']) > 0 else 'Empty')
            cell_type = cell['cell_type']
            cell_len = len(cell['source'])
            desc = '%3d: %10s : name=%10s : %2d lines : %s' % (n, cell_type, name, cell_len, example)
            self.list.insert(tk.END, desc)

    def fun_update(self):
        """Update notebook from file"""
        filename = self.file.get()
        self.notebook.load(filename)
        self.fun_listcells()

    def fun_load(self):
        """Select a notebook file and load new notebook"""
        # root = Tk().withdraw() # from Tkinter
        default_directory = os.path.expanduser('~')
        filename = filedialog.askopenfilename(parent=self.root,
                                              title='Select a notebook file',
                                              initialdir=default_directory,
                                              defaultextension='.ipynb',
                                              filetypes=[('Jupyter Notebook', '.ipynb'),
                                                         ('All files', '.*')])
        if filename:
            self.file.set(filename)
            self.fun_update()

    def fun_new(self):
        """Select a filename and create a new file"""
        default_directory = os.path.expanduser('~')
        filename = filedialog.asksaveasfilename(parent=self.root,
                                                title='Choose new filename',
                                                initialdir=default_directory,
                                                defaultextension='.ipynb',
                                                filetypes=[('Jupyter Notebook', '.ipynb'),
                                                           ('All files', '.*')])

        if filename:
            self.file.set(filename)
            self.notebook.filename = filename
            self.notebook.save(filename)

    def fun_cell_select(self, event):
        """Select cell in listbox"""
        current = self.list.curselection()
        if len(current) == 0:
            return
        else:
            current = current[0]
        self.current_cell.set(current)
        cell = self.notebook.notebook['cells'][current]
        name = (cell['metadata']['name'] if 'name' in cell['metadata'].keys() else '')
        self.cell_type.set(cell['cell_type'])
        self.cell_name.set(name)
        txt = self.notebook.cell_source(current)
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, txt)

    def fun_edit_source(self):
        """Replace currently selected cell with source"""
        current = self.current_cell.get()
        if current < 0 or current > len(self.notebook.notebook['cells']):
            messagebox.showinfo('jupyter editor', 'Please select a cell to edit')
            return
        # cell_type = self.cell_type.get()
        cell_name = self.cell_name.get()
        if cell_name == '':
            cell_name = None
        source = self.text.get(1.0, tk.END)
        self.notebook.edit_cell(current, source, append=False, name=cell_name)
        self.fun_listcells()

    def fun_add_source(self):
        """Add text as new ncell in notebook"""
        filename = self.file.get()
        cell_type = self.cell_type.get()
        cell_name = self.cell_name.get()
        if cell_name == '':
            cell_name = None
        source = self.text.get(1.0, tk.END)

        if cell_type == 'code':
            self.notebook.append_code(source, name=cell_name)
        else:
            self.notebook.append_markdown(source, name=cell_name)
        self.notebook.save(filename)
        self.fun_listcells()

    def on_closing(self):
        """End mainloop on close window"""
        self.root.destroy()
