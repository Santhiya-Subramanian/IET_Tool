import os
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk


class Transcript_View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_transcript_frame()

    def setup_transcript_frame(self):
        self.create_transcript_frame()
        self.pack_transcript_frame()

    def create_transcript_frame(self):
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path_play = "images\play_pause.png"
        rel_path_stop = "images\stop.png"
        rel_path_forward = "images/forward.png"
        rel_path_rewind = "images/rewind.png"
        abs_file_path_play = os.path.join(script_dir, rel_path_play)
        abs_file_path_stop = os.path.join(script_dir, rel_path_stop)
        abs_file_path_forward = os.path.join(script_dir, rel_path_forward)
        abs_file_path_rewind = os.path.join(script_dir, rel_path_rewind)
        print(abs_file_path_play)
        print(abs_file_path_stop)
        print(abs_file_path_forward)
        print(abs_file_path_rewind)
        play_pause_btn_img = Image.open(abs_file_path_play)
        stop_btn_img = Image.open(abs_file_path_stop)
        forward_btn_img = Image.open(abs_file_path_forward)
        rewind_btn_img = Image.open(abs_file_path_rewind)

        # Resize the Image
        resized_play_pause_img = play_pause_btn_img.resize((50, 50), Image.LANCZOS)
        self.resized_play_pausebtn_img = ImageTk.PhotoImage(resized_play_pause_img)

        resized_stop_img = stop_btn_img.resize((50, 50), Image.LANCZOS)
        self.resized_stopbtn_img = ImageTk.PhotoImage(resized_stop_img)

        resized_forward_img = forward_btn_img.resize((50, 50), Image.LANCZOS)
        self.resized_forwardbtn_img = ImageTk.PhotoImage(resized_forward_img)

        resized_rewind_img = rewind_btn_img.resize((50, 50), Image.LANCZOS)
        self.resized_rewindbtn_img = ImageTk.PhotoImage(resized_rewind_img)

        # label
        self.audio_Label = Label(self.root, text='')

        # Create Status Bar
        self.status_bar = Label(self.root, text='', bd=1, relief=GROOVE, anchor=E)

        # Create Player Control Frame
        self.control_frame = Frame(self.root)

        self.play_pause_btn = Button(self.control_frame, image=self.resized_play_pausebtn_img, borderwidth=0,
                                     command=lambda: self.controller.play_pause())
        self.stop_btn = Button(self.control_frame, image=self.resized_stopbtn_img, borderwidth=0,
                               command=lambda: self.controller.stop_audio())
        self.forward_btn = Button(self.control_frame, image=self.resized_forwardbtn_img, borderwidth=0)
        self.rewind_btn = Button(self.control_frame, image=self.resized_rewindbtn_img, borderwidth=0)

        print("Need to add the slide command. removed for testing purpose")
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=self.controller.slide)

        self.transcribe_button = Button(self.root, text='Transcribe',
                                        command=lambda: (self.controller.transcribe_action(), self.controller.get_str_val()))

        self.transcribe_file = Button(self.root, text='File', command=lambda: self.create_file_option())

        self.text_frame = Frame(self.root)

        self.text_scroll = Scrollbar(self.text_frame)

        self.text_box = Text(self.text_frame, width=40, height=15, font=('times new roman', 16),
                             selectbackground='yellow',
                             selectforeground='black', yscrollcommand=self.text_scroll.set)

    def pack_transcript_frame(self):
        self.audio_Label.pack()
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=1)
        self.control_frame.pack(pady=10)
        self.play_pause_btn.grid(row=0, column=0, padx=10)
        self.stop_btn.grid(row=0, column=2, padx=10)
        self.forward_btn.grid(row=0, column=3, padx=10)
        self.rewind_btn.grid(row=0, column=4, padx=10)
        self.slider.pack(pady=10)
        self.transcribe_button.pack(pady=10)
        self.transcribe_file.pack()
        self.text_frame.pack(pady=10)
        self.text_scroll.pack(side=RIGHT, fill=Y)
        self.text_box.pack(pady=10)

    def create_file_option(self):
        self.top = Toplevel(self.root)
        self.top.title("File Menu")
        self.top.geometry("150x150")
        self.open_btn = Button(self.top, text="Open", command=lambda: self.controller.open_file())
        self.open_btn.pack(pady=5)
        self.save_btn = Button(self.top, text="Save", command=lambda: self.controller.save_file())
        self.save_btn.pack(pady=5)
        self.saveAs_btn = Button(self.top, text="SaveAs", command=lambda: self.controller.saveAs_file())
        self.saveAs_btn.pack(pady=5)