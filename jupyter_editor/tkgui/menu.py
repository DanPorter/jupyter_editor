"""
Main crystal gui windows
"""

import sys, os

if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog as filedialog
else:
    import tkinter as tk
    from tkinter import filedialog

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
    """

    def __init__(self):
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

        self.notebook = NoteBook()

        # Create Widget elements from top down
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N)

        # Filename (variable)
        f_file = tk.Frame(frame)
        f_file.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        self.file = tk.StringVar(frame, self.notebook.filename)

        var = tk.Label(f_file, text='Notebook file:', font=SF, width=10)
        var.pack(side=tk.LEFT, expand=tk.NO)
        var = tk.Label(f_file, textvariable=self.file, width=40, font=TF)
        var.pack(side=tk.LEFT, expand=tk.YES)
        var = tk.Button(f_file, text='Load', font=BF, bg=btn, activebackground=btn_active, command=self.fun_load)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)
        var = tk.Button(f_file, text='Update', font=BF, bg=btn, activebackground=btn_active, command=self.fun_update)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)
        var = tk.Button(f_file, text='New', font=BF, bg=btn, activebackground=btn_active, command=self.fun_new)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=0)

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
        frm = tk.Frame(frame)
        frm.pack(side=tk.LEFT, anchor=tk.N)

        var = tk.Button(frm, text='Add cell as code', font=BF, bg=btn,
                        activebackground=btn_active, command=self.fun_add_code)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)
        var = tk.Button(frm, text='Add cell as markdown', font=BF, bg=btn,
                        activebackground=btn_active, command=self.fun_add_markdown)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)

        # start mainloop
        # In interactive mode, this freezes the terminal
        # To stop this, need a way of checking if interactive or not ('-i' in sys.argv)
        # However sys in this file is not the same as sys in the operating script
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    ###################################################################################
    ############################## FUNCTIONS ##########################################
    ###################################################################################

    def fun_update(self):
        """Update notebook from file"""
        filename = self.file.get()
        self.notebook.load(filename)

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

    def fun_add_code(self):
        """Add code as new code cell in notebook"""
        filename = self.file.get()
        source = self.text.get(1.0, tk.END)
        self.notebook.append_code(source)
        self.notebook.save(filename)

    def fun_add_markdown(self):
        """Add code as new markdown cell in notebook"""
        filename = self.file.get()
        source = self.text.get(1.0, tk.END)
        self.notebook.append_markdown(source)
        self.notebook.save(filename)

    def on_closing(self):
        """End mainloop on close window"""
        self.root.destroy()
