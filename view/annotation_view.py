from tkinter import *
from tkinter import ttk


class Annotation_View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_annotation_frame()

    def setup_annotation_frame(self):
        self.create_annotation_frame()
        self.pack_annotation_frame()

    def create_annotation_frame(self):
        self.tool_bar = Frame(self.root)
        self.highlight_button = Button(self.tool_bar, text='Highlight', command=lambda: self.controller.highlight())
        self.clear_highlight_button = Button(self.tool_bar, text='Clear Highlight',
                                             command=lambda: self.controller.clear_highlight())
        self.extract_button = Button(self.tool_bar, text='Extract', command=lambda: self.controller.gettext())
        self.delete_annotation_button = Button(self.tool_bar, text='Remove Annotation',
                                               command=lambda: self.controller.delete_annotation())
        self.annotation_file = Button(self.tool_bar, text='File', command=lambda: self.create_annotation_file_option())
        self.annotation_search = Button(self.tool_bar, text='Search', command=lambda: self.create_searchRecords())
        self.s = ttk.Style()
        self.annotation_box = ttk.Treeview(self.root, column=("c1", "c2", "c3"), show='headings', height=5)
        self.annotation_box.column("# 1", anchor=CENTER)
        self.annotation_box.heading("# 1", text="Sentence")
        self.annotation_box.column("# 2", anchor=CENTER)
        self.annotation_box.heading("# 2", text="Annotation Tag")
        self.annotation_box.column("# 3", anchor=CENTER)
        self.annotation_box.heading("# 3", text="Description")
        self.addannotate_Tag = Button(self.root, text='Add Tag', command=lambda: self.add_Tag())

    def pack_annotation_frame(self):
        self.tool_bar.pack()
        self.highlight_button.grid(row=0, column=0, sticky=W, padx=5)
        self.clear_highlight_button.grid(row=0, column=1, sticky=W, padx=5)
        self.extract_button.grid(row=0, column=2, sticky=W, padx=5)
        self.delete_annotation_button.grid(row=0, column=3, sticky=W, padx=5)
        self.annotation_file.grid(row=0, column=4, sticky=W, padx=5)
        self.annotation_search.grid(row=0, column=5, sticky=W, padx=5)
        self.s.theme_use('clam')
        self.annotation_box.pack(pady=20)
        self.addannotate_Tag.pack(pady=20)

    def create_annotation_file_option(self):
        self.listtop = Toplevel(self.root)
        self.listtop.title("File Menu")
        self.listtop.geometry("150x150")
        self.open_list_btn = Button(self.listtop, text="Open", command=lambda: self.controller.open_excel_file())
        self.open_list_btn.pack(pady=5)
        self.save_list_btn = Button(self.listtop, text="Save", command=lambda: self.controller.save_excel_file())
        self.save_list_btn.pack(pady=5)
        self.clear_list_btn = Button(self.listtop, text="Clear", command=lambda: self.controller.clear_table())
        self.clear_list_btn.pack(pady=5)

    def create_searchRecords(self):
        # global search_entry, search
        self.search = Toplevel(self.root)
        self.search.title('Lookup Records')
        self.search.geometry('400x200')

        self.search_frame = LabelFrame(self.search, text='Annotation Name')
        self.search_entry = Entry(self.search_frame)
        self.search_button = Button(self.search_frame, text='Search Annotation', command=self.controller.lookup)
        self.search_frame.pack(padx=10, pady=10)
        self.search_entry.pack(padx=20, pady=20)
        self.search_button.pack(padx=20, pady=20)

    def add_Tag(self):
        self.tag_window = Toplevel(self.root)
        self.tag_window.geometry("750x400")
        self.tag_label = Label(self.tag_window, text='Select the Tag')
        self.tag_label.pack(pady=10)
        self.tags = ['Requirement', 'Follow up', 'Mistake', 'Custom']
        self.list_frame = Frame(self.tag_window)
        self.list_frame.pack()

        self.list_scroll = Scrollbar(self.list_frame)
        self.list_scroll.pack(side=RIGHT, fill=Y)

        self.dropdown_label = Text(self.list_frame, width=20, height=1)
        self.dropdown_label.pack()

        self.dropdown = Listbox(self.list_frame, selectmode="multiple", yscrollcommand=self.list_scroll.set)
        self.dropdown.bind('<<ListboxSelect>>', self.controller.selectedValue)
        self.dropdown.pack(pady=5)

        for self.each_item in range(len(self.tags)):
            self.dropdown.insert(END, self.tags[self.each_item])
            self.dropdown.itemconfig(self.each_item)

        self.description_label = Label(self.tag_window, text='Description')
        self.description_label.pack(pady=5)

        self.description_frame = Frame(self.tag_window)
        self.description_frame.pack()

        self.description_scroll = Scrollbar(self.description_frame)
        self.description_scroll.pack(side=RIGHT, fill=Y)

        self.description_text = Text(self.description_frame, width=60, height=3, font=('times new roman', 16),
                                     selectbackground='yellow', selectforeground='black',
                                     yscrollcommand=self.description_scroll.set)
        self.description_text.pack(pady=10)

        self.button = Button(self.tag_window, text="Ok", command=lambda: [self.controller.gettag_values(), self.tag_window.destroy()])
        self.button.pack(pady=10)

