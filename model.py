import os
from tkinter import Tk
from view.main_view import Main_View


class Model:
    def __init__(self, controller):
        self.container = Tk()
        self.controller = controller
        self.view = Main_View(self.container, controller=self)

    # def uploadAction(self, audios):
    #     # global path
    #     # self.controller = Controller()
    #     for audio in audios:
    #         path = os.path.split(audio)
    #         audio = path[1]
    #         self.controller.add_audio(audio)
    #         self.path = f'{path[0]}/'