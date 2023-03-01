from tkinter import *
from tkinter import filedialog


class Audio_View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_audio_frame()

    def setup_audio_frame(self):
        self.create_audio_frame()
        self.pack_audio_frame()

    def create_audio_frame(self):
        self.upload_button = Button(self.root, text='Upload Audio File', command=lambda: self.controller.uploadActionFile())
        self.remove_button = Button(self.root, text='Remove Audio File', command=lambda: self.controller.removeAudio())
        self.audio_box = Listbox(self.root, bg='white', fg='black', width=60)

    def pack_audio_frame(self):
        self.upload_button.pack(pady=10)
        self.remove_button.pack(pady=10)
        self.audio_box.pack()

