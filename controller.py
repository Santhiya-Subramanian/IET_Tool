import csv
import os
import time
import tkinter
from tkinter import *
from tkinter import filedialog, colorchooser
import tkinter.messagebox as mb
import pandas as pd
import pygame
from mutagen.mp3 import MP3
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from google.cloud import speech_v1p1beta1 as speech
from view.main_view import Main_View


class Controller:
    def __init__(self):
        self.container = Tk()
        self.view = Main_View(self.container, controller=self)
        pygame.mixer.init()
        self.str_val = None
        # self.model = Model(controller=self)

    def run(self):
        self.container.geometry('1200x800')
        self.container.title("Interview Elicitation")
        self.container.mainloop()

    def uploadAction(self, audios):
        # global path
        for audio in audios:
            path = os.path.split(audio)
            audio = path[1]
            self.add_audio(audio)
            self.path = f'{path[0]}/'

    def uploadActionFile(self):
        # global path
        audios = filedialog.askopenfilenames()
        self.uploadAction(audios)

    def add_audio(self, audio):
        self.view.leftpanel.audio_box.insert(END, audio)

    def removeAudio(self):
        self.view.leftpanel.audio_box.delete(ANCHOR)
        pygame.mixer.init()
        pygame.mixer.music.stop()

    def play_audio(self):
        # self.stopped
        self.stopped = False

        self.audio = self.view.leftpanel.audio_box.get(ACTIVE)
        self.audio_name = self.audio
        self.audio = f'{self.path}{self.audio}'
        # print(self.audio)

        pygame.mixer.music.load(self.audio)
        # print(slider.get())
        pygame.mixer.music.play(loops=0, start=int(self.view.centerpanel.slider.get()))
        self.view.centerpanel.audio_Label.config(text=self.audio_name)
        # call audio length function
        self.audio_Time()

        # create Global Pause Variable

    global paused
    paused = False

    global play
    play = False

    def play_pause(self):
        global play
        play = not play
        if play:
            self.play_audio()
        else:
            self.pause_audio(paused)

    def slide(self, x):
        # slider_label.config(text=f'{int(slider.get())} of {int(audio_total_length)}')
        self.audio = self.view.leftpanel.audio_box.get(ACTIVE)
        self.audio = f'{self.path}{self.audio}'

        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play(loops=0, start=int(self.view.centerpanel.slider.get()))

    def audio_Time(self):
        self.current_time = pygame.mixer.music.get_pos() / 1000
        # slider_label.config(text=f'Slider: {int(slider.get())} and Song Pos: {int(current_time)}')
        self.formatted_time = time.strftime('%M:%S', time.gmtime(self.current_time))

        self.audio = self.view.leftpanel.audio_box.get(ACTIVE)
        self.audio = f'{self.path}{self.audio}'
        # loading the song to Mutagen
        self.load_audio_to_mutagen = MP3(self.audio)
        global audio_total_length
        self.audio_total_length = self.load_audio_to_mutagen.info.length
        # print("audio total length type ")
        # print(type(audio_total_length))
        self.formatted_audio_length = time.strftime('%M:%S', time.gmtime(self.audio_total_length))

        self.current_time += 1

        if int(self.view.centerpanel.slider.get()) == int(self.audio_total_length):
            self.view.centerpanel.status_bar.config(text=f'Time Elapsed: {self.formatted_audio_length}')

        elif paused:
            pass

        elif int(self.view.centerpanel.slider.get()) == int(self.current_time):
            self.slider_position = int(self.audio_total_length)
            self.view.centerpanel.slider.config(to=self.slider_position, value=int(self.current_time))

        else:
            self.slider_position = int(self.audio_total_length)
            self.view.centerpanel.slider.config(to=self.slider_position, value=int(self.view.centerpanel.slider.get()))
            self.formatted_time = time.strftime('%M:%S', time.gmtime(int(self.view.centerpanel.slider.get())))
            self.view.centerpanel.status_bar.config(
                text=f'Time Elapsed: {self.formatted_time} / {self.formatted_audio_length}')

            self.slider_time = int(self.view.centerpanel.slider.get()) + 1
            self.view.centerpanel.slider.config(value=self.slider_time)

        self.view.centerpanel.status_bar.after(1000, self.audio_Time)

    global audio_total_length

    # # create Global Pause Variable
    # global paused
    # paused = False

    def pause_audio(self, is_paused):
        self.is_paused = is_paused
        global paused
        self.paused = is_paused

        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True

    def stop_audio(self):
        self.view.centerpanel.status_bar.config(text='')
        self.view.centerpanel.slider.config(value=0)
        pygame.mixer.music.stop()
        self.view.leftpanel.audio_box.selection_clear(ACTIVE)

        self.view.centerpanel.status_bar.config(text='')
        self.view.centerpanel.audio_Label.config(text='')

        self.stopped = True

    def transcribe_action(self):
        audio_file = self.view.leftpanel.audio_box.curselection()
        input_file_name = self.view.leftpanel.audio_box.get(audio_file)
        self.clear_textbox()
        # upload your json key
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/santh/PycharmProjects/pythonProject/IET-Tool/json_key.json'
        client = speech.SpeechClient()

        media_uri_path = 'gs://speech_to_text_audio_file/'
        audio_path = f'{media_uri_path}{input_file_name}'
        print(self.path[1])

        audio_file = speech.RecognitionAudio(uri=audio_path)

        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=10,
        )

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=48000,
            language_code="en-US",
            diarization_config=diarization_config,
            # model='audio'
        )

        operation = client.long_running_recognize(
            config=config,
            audio=audio_file
        )

        response = operation.result(timeout=90)
        result = response.results[-1]
        words_info = result.alternatives[0].words
        words_list = []
        for word_info in words_info:
            words_list.append({
                'word': word_info.word,
                'speaker_tag': word_info.speaker_tag,
                'start_time': word_info.start_time.seconds,
                'end_time': word_info.end_time,
            })
        current_speaker = words_list[0]['speaker_tag']
        speaker_start_time = words_list[0]['start_time']
        speaker_end_time = words_list[0]['end_time']
        current_line = []
        script = []

        for item in words_list:
            if item['speaker_tag'] != current_speaker:
                script.append({
                    'speaker': current_speaker,
                    'line': current_line,
                    'start_time': speaker_start_time,
                    'end_time': speaker_end_time
                })
                current_line = []
                current_speaker = item['speaker_tag']
                speaker_start_time = item['start_time']
                speaker_end_time = item['end_time']
            else:
                current_line.append(item['word'])

        script.append({
            'speaker': current_speaker,
            'line': current_line,
            'start_time': speaker_start_time,
            'end_time': speaker_end_time
        })
        timer_list = []
        self.timevalues = []
        for line in script:
            startTime = line['start_time']
            self.str_val = str(startTime)
            print(self.str_val)
            script = f"{self.str_val}  Speaker{line['speaker']}: " + " ".join(line['line'])

            self.add_script(script)
            findtext = f"{self.str_val}  {'speaker'}"
            # print('list', self.timevalues)

            if findtext:
                idx = '1.0'
                while 1:
                    # searches for desired string from index 1
                    idx = self.view.centerpanel.text_box.search(findtext, idx, nocase=1, stopindex=END)

                    if not idx: break

                    # last index sum of current index and
                    # length of text
                    lastidx = '%s+%dc' % (idx, len(findtext))

                    self.view.centerpanel.text_box.insert(idx, '\n\n')

                    # overwrite 'Found' at idx
                    self.view.centerpanel.text_box.tag_add('found', idx, lastidx)
                    idx = lastidx

                self.view.centerpanel.text_box.tag_config('found')

            self.r = Button(self.view.centerpanel.text_box, text=self.str_val, background='Green',
                            command=lambda m=self.str_val: self.timelink(m))

            self.timevalue = self.r.cget('text')
            self.timevalues.append(self.timevalue)
            timer_list.append(self.timevalue)
            if (findtext and self.r):
                idx = '1.0'
                while 1:
                    # searches for desired string from index 1
                    idx = self.view.centerpanel.text_box.search(findtext, idx, nocase=1, stopindex=END)
                    if not idx: break
                    # last index sum of current index and
                    # length of text
                    lastidx = '% s+% dc' % (idx, len(findtext))
                    self.view.centerpanel.text_box.insert(idx, '\n\n Speak')
                    self.view.centerpanel.text_box.delete(idx, lastidx)
                    self.view.centerpanel.text_box.window_create(self.view.centerpanel.text_box.index(idx),
                                                                 window=self.r)

                    num = 3
                    lastidx = '% s+% dc' % (idx, num)

                    # overwrite 'Found' at idx
                    self.view.centerpanel.text_box.tag_add('found', idx, lastidx)
                    idx = lastidx

                self.view.centerpanel.text_box.tag_config('found')

    def timelink(self, button_press):
        # print('button pressed', button_press)
        # print('inside', self.timevalues)
        self.view.centerpanel.slider.config(value=int(button_press))
        self.play_audio()

    global opened_file_name
    opened_file_name = False

    def open_file_logic(self):
        if self.transcribe_text_file:
            global opened_file_name
            opened_file_name = self.transcribe_text_file[0]

        transcribed_file_path = os.path.split(self.transcribe_text_file[0])
        print(transcribed_file_path[1])
        self.text_file = transcribed_file_path[1]
        self.transcribe_text_file = open((self.transcribe_text_file[0]), 'r')
        transcribed_text = self.transcribe_text_file.read()
        self.add_text(transcribed_text)
        self.transcribe_text_file.close()
        self.view.centerpanel.top.destroy()

    def save_file_logic(self):
        global opened_file_name
        if opened_file_name:
            transcribe_file_save = open(opened_file_name, 'w')
            transcribe_file_save.write(self.view.centerpanel.text_box.get("1.0", END))
            transcribe_file_save.close()
        else:
            self.saveAs_file()
        self.view.centerpanel.top.destroy()

    def saveAs_file_logic(self):
        if self.transcribe_file_save:
            self.file_name = self.transcribe_file_save
            filepath = os.path.split(self.transcribe_file_save)
            self.file_name = self.file_name.replace(filepath[0], "")

            transcribe_file_save = open(self.transcribe_file_save, 'w')
            transcribe_file_save.write(self.view.centerpanel.text_box.get("1.0", END))
            transcribe_file_save.close()
        self.view.centerpanel.top.destroy()

    def get_transcribe_action(self):
        self.transcribe_action()

    def add_script(self, script):
        self.view.centerpanel.text_box.insert(END, script)

    def clear_textbox(self):
        self.view.centerpanel.text_box.delete("1.0", "end")

    def get_str_val(self):
        self.str_val.get()

    def open_file(self):
        self.view.centerpanel.text_box.delete("1.0", END)
        self.transcribe_text_file = filedialog.askopenfilenames()
        self.open_file_logic()

    def add_text(self, transcribed_text):
        self.view.centerpanel.text_box.insert(END, transcribed_text)

    def save_file(self):
        self.save_file_logic()

    def saveAs_file(self):
        self.transcribe_file_save = filedialog.asksaveasfilename(defaultextension=".*",
                                                                 filetypes=(
                                                                 ("Text File", "*.txt"), ("Word File", "*.docx")))
        self.saveAs_file_logic()

    def highlight(self):
        self.highlightCount = 0
        my_color = colorchooser.askcolor()[1]
        self.highlightCount += 1
        try:
            self.view.centerpanel.text_box.tag_add(self.highlightCount, "sel.first", "sel.last")
            self.view.centerpanel.text_box.tag_configure(self.highlightCount, foreground="Black", background=my_color)
        except tkinter.TclError:
            pass

    def clear_highlight(self):
        self.view.centerpanel.text_box.tag_remove(self.highlightCount, "sel.first", "sel.last")

    global extracted_text

    def gettext(self):
        global extracted_text
        extracted_text = self.view.centerpanel.text_box.get("sel.first", "sel.last")
        print(extracted_text)
        self.view.annotationPanel.annotation_box.insert('', 'end', values=(extracted_text, '', ''))

    def delete_annotation(self):
        selected_item = self.view.annotationPanel.annotation_box.selection()[0]
        self.view.annotationPanel.annotation_box.delete(selected_item)

    # def close_win(self, top):
    #     top.destroy()

    def open_excel_file(self):
        self.excel_file_name = filedialog.askopenfilenames()
        self.open_list()

    def save_excel_file(self):
        self.save_annotation_list = filedialog.asksaveasfilename(defaultextension=".*",
                                                            filetypes=(
                                                                ("CSV File", "*.csv"), ("Word File", "*.docx")))
        self.save_list()

    def clear_table(self):
        self.clear_list()

    def open_list(self):
        if self.view.excel_file_name:
            try:
                self.view.excel_file_name = r"{}".format(self.view.excel_file_name[0])
                self.df = pd.read_excel(self.view.excel_file_name)
            except ValueError:
                print("file couldn't be open")

        self.clear_list()

        self.view.annotationPanel.annotation_box['column'] = list(self.df.columns)
        self.view.annotationPanel.annotation_box['show'] = "headings"

        for column in self.view.annotationPanel.annotation_box["column"]:
            self.view.annotationPanel.annotation_box.heading(column, text=column)

        self.df_rows = self.df.to_numpy().tolist()
        for row in self.df_rows:
            self.view.annotationPanel.annotation_box.insert("", "end", values=row)

        self.view.annotationPanel.listtop.destroy()

    def save_list(self):
        if len(self.view.annotationPanel.annotation_box.get_children()) < 1:
            mb.showinfo("No data", "No data to export")
            return False

        with open(self.save_annotation_list, mode='a', newline='') as my_excel_file:
            write = csv.writer(my_excel_file, dialect='excel')
            for i in self.view.annotationPanel.annotation_box.get_children():
                row = self.view.annotationPanel.annotation_box.item(i)['values']
                write.writerow(row)
        mb.showinfo("Message", "Export successfully")
        self.view.annotationPanel.listtop.destroy()

    def clear_list(self):
        self.view.annotationPanel.annotation_box.delete(*self.view.annotationPanel.annotation_box.get_children())

    def lookup(self):
        lookup_record = self.view.annotationPanel.search_entry.get()
        selections = []
        # print(lookup_record)
        self.view.annotationPanel.annotation_box['column'] = list(self.df.columns)
        self.view.annotationPanel.annotation_box['show'] = "headings"

        for record in self.view.annotationPanel.annotation_box.get_children():
            if lookup_record in self.view.annotationPanel.annotation_box.item(record)['values']:
                print(self.view.annotationPanel.annotation_box.item(record)['values'])
                selections.append(record)
        self.view.annotationPanel.annotation_box.selection_set(selections)
        self.view.annotationPanel.search.destroy()

    def gettag_values(self):
        self.current_item = self.view.annotationPanel.annotation_box.focus()
        self.current_value = self.view.annotationPanel.annotation_box.item(self.current_item, 'values')
        print(self.current_value[0])
        self.view.annotationPanel.annotation_box.item(self.current_item,
                            values=(
                            self.current_value[0], self.view.annotationPanel.dropdown_label.get("1.0", END), self.view.annotationPanel.description_text.get("1.0", END)))

    def selectedValue(self, evt):
        for self.dropvalue in self.view.annotationPanel.dropdown.curselection():
            print(self.dropvalue)
        self.view.annotationPanel.dropdown_label.delete("1.0", "end")
        for self.dropvalue in self.view.annotationPanel.dropdown.curselection():
            self.selected_tag_value = self.view.annotationPanel.dropdown.get(self.dropvalue)
            self.view.annotationPanel.dropdown_label.insert(END, f'{self.selected_tag_value}, ')

