from tkinter import *
from view.audio_view import *
from view.transcript_view import *
from view.annotation_view import *


class Main_View:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.setup()

    def setup(self):
        self.create_menu()
        self.create_panedwindow()

    def create_menu(self):
        self.frame = Frame(self.container)
        self.menuBar = Menu(self.frame)
        self.home = Menu(self.menuBar, tearoff=0, activebackground='green', activeforeground='white')
        self.menuBar.add_cascade(label='IE Tool', menu=self.home)
        self.home.add_command(label='Industry')
        self.home.add_command(label='Research')
        self.home.add_separator()
        self.home.add_command(label='Exit', command=self.container.quit)
        self.container.config(menu=self.menuBar)
        self.frame.pack()

    def create_panedwindow(self):
        self.pw = PanedWindow(self.container, orient=HORIZONTAL)
        self.leftFrame = Frame(self.pw)
        self.rightFrame = Frame(self.pw)
        self.annotationFrame = Frame(self.pw)
        self.leftpanel = Audio_View(self.leftFrame, self.controller)
        self.centerpanel = Transcript_View(self.rightFrame, self.controller)
        self.annotationPanel = Annotation_View(self.annotationFrame, self.controller)
        self.pw.pack(fill=BOTH, expand=True)
        self.pw.configure(sashrelief=RAISED)
        self.pw.add(self.leftFrame, width=150)
        self.pw.add(self.rightFrame, width=500)
        self.pw.add(self.annotationFrame)

