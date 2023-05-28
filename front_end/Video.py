import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtMultimediaWidgets as QtMultimediaWidgets
import vlc
import pysrt
import re
import sys
#import time
from datetime import timedelta
from os import path
import numpy as np
import itertools

slider_style = """
QSlider::groove:horizontal {
border: 1px solid #bbb;
background: pale gray;
height: 7px;
border-radius: 6px;
}

QSlider::sub-page:horizontal {
background: white;
border: 1px solid #777;
height: 7px;
border-radius: 6px;
}

QSlider::add-page:horizontal {
background: pale gray;
border: 1px solid #777;
height: 7px;
border-radius: 6px;
}

QSlider::handle:horizontal {
background: white;
width: 3px;
margin-top: 0px;
margin-bottom: 0px;
border-radius: 6px;
}

QSlider::handle:horizontal:hover {
background: white;
border-radius: 6px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border: 1px solid #aaa;
border-radius: 6px;
}
"""

slider_style_hover = """
QSlider::groove:horizontal {
border: 1px solid #bbb;
background: pale gray;
height: 7px;
border-radius: 6px;
}

QSlider::sub-page:horizontal {
background: white;
border: 1px solid #777;
height: 7px;
border-radius: 6px;
}

QSlider::add-page:horizontal {
background: pale gray;
border: 1px solid #777;
height: 7px;
border-radius: 6px;
}

QSlider::handle:horizontal {
background: white;
width: 5px;
margin-top: -4px;
margin-bottom: -4px;
border-radius: 6px;
}

QSlider::handle:horizontal:hover {
background: white;
border-radius: 6px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border: 1px solid #aaa;
border-radius: 6px;
}
"""

class Video(QtWidgets.QWidget):
     
     cue_ex_sig = QtCore.Signal()
     cue_app_off = QtCore.Signal()
     cue_app_on = QtCore.Signal()

     def __init__(self, episode):
        super().__init__()

        self.episode = episode # key string for series_dict

        series_dict = {'fr_ep1': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/French/S01E01 Are We Shtty.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/FRENCH_Détox_Off.the.Hook.English.S01E01.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_FRENCH_Détox_Off.the.Hook.French.S01E01.srt"},
                       'fr_ep2': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/French/FRENCH_Détox.Off_The_Hook.S01E02.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/FRENCH_Détox_Off.the.Hook.English.S01E02.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_FRENCH_Détox_Off.the.Hook.French.S01E02.srt"},
                       'sp_ep1': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/Spanish/Machos alfa S01E01 In decostruzione DLMux 1080p E-AC3+AC3 ITA SPA SUBS.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_SPANISH_Machos.Alfa.English.S01E01.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_SPANISH_Machos.Alfa.Spanish.S01E01.srt"},
                       'sp_ep2': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/Spanish/SPANISH_Machos.Alfa_S01E02.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_SPANISH_Machos.Alfa.English.S01E02.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_SPANISH_Machos.Alfa.Spanish.S01E02.srt"},
                       'de_ep1': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/German/How.To.Sell.Drugs.Online.Fast.S01E01.720p.NF.WEBRip.x264-GalaxyTV.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E01.English.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_GERMAN_How.to.Sell.Drugs.Online.Fast.S01E01.German.srt"},
                       'de_ep2': {'vid': "C:/Users/chant/Documents/GitHub/LangFlix/shows/German/GERMAN_How.To.Sell.Drugs.Online.Fast_S01E02.mkv", 'sub_l1': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E02.English.srt", 'sub_l2': "C:/Users/chant/Documents/GitHub/LangFlix/subtitles/MODIFIED_GERMAN_How.to.Sell.Drugs.Online.Fast.S01E02.German.srt"}}

        self.zipf_start = -1 # user's CEFR level (as Zipf frequency) at the start of app use
        self.zipf_cur = self.zipf_start # user's current language level

        self.subs_are_dual = False # indicator of subtitles being in dual mode or not
        self.num_correct_ex = [] # array that store exercise results as a sequence of 0 (incorrect) and 1 (correct)

        self.num_exercises = 10 # number of exercises per video

        self.sub_ind_for_ex = [] # array to store the indices of candidate subs per exercise

        self.ind_to_stop_at_stack = [] # stack to store next subtitle to pause at
        
        self.cur_ex_ind = 0 # current exercise index

        self.old_volume = 0 # volume prior to mute button being pressed

        self.isPaused = True # boolean indicating if video is paused
        self.isMuted = True # boolean indicating if video is muted

        self.subs_orig = pysrt.open(series_dict[episode]['sub_l1']) #the modified subs with ###
        self.subs_cur = pysrt.open(series_dict[episode]['sub_l1']) #subs currently used for the exercises with no ###

        self.subs_l1 = pysrt.open(series_dict[episode]['sub_l1']) # plain l1 subs with no ### and no highlighted words
        self.subs_l2 = pysrt.open(series_dict[episode]['sub_l2']) # l2 subs
        
        self.prep_subs() # preprocess the subtitle file to make exercises with
        #self.make_dual_subs() # generate dual subtitles for the Dual subtitles settings

        # create video window
        self.video = QtWidgets.QFrame() # video screen
        self.video.setStyleSheet("""background-color: black; border-bottom-color: white;""")
        
        # instantiate video player
        Instance = vlc.Instance()
        self.player = Instance.media_player_new()
        self.media = Instance.media_new(series_dict[episode]['vid'])
        self.player.set_media(self.media) 
        
        # Connect video player to window: https://github.com/devos50/vlc-pyqt5-example
        if sys.platform == "win32": # for Windows
            self.player.set_hwnd(self.video.winId())
        else:
            self.player.set_nsobject(self.video.winId())  
               
        self.videoEventManager = self.player.event_manager()

        #volume slider                               
        self.volume_slider = QtWidgets.QSlider()
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.valueChanged.connect(self.change_volume)

        #volume button 
        self.volumeButtonIcons = [QtGui.QIcon("icons8-speaker-50.png"),
                                QtGui.QIcon("icons8-no-speaker-50.png")]
                                
        self.volume_button = QtWidgets.QPushButton()
        self.base_width = self.volume_button.size().width()
        self.volume_button.setCheckable(True)
        self.volume_button.clicked.connect(self.volume_mute)
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])
        self.volume_button.setStyleSheet("""border-style: solid;""")

        #play/pause button
        self.playButtonIcons = [QtGui.QIcon("icons8-pause-50.png"),
                                QtGui.QIcon("icons8-play-50.png")]
        
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setCheckable(True)
        self.play_button.clicked.connect(self.play_video)
        self.play_button.setIcon(self.playButtonIcons[int(self.isPaused)])
        self.play_button.setStyleSheet("""border-style: solid;""")
        self.videoEventManager.event_attach(vlc.EventType.MediaPlayerPaused, lambda x: self.set_play_button_style()) 
        self.videoEventManager.event_attach(vlc.EventType.MediaPlayerPlaying, lambda x: self.set_play_button_style()) 

        
        #LangFlix on/off toggle to the video window
        self.appOnToggle = QtWidgets.QPushButton("LangFlix")
        self.appOnToggle.setCheckable(True)
        self.appOnToggle.setChecked(True)
        self.appOnToggle.setStyleSheet("""QPushButton
                                      {background-color: lightblue; 
                                       color: white;
                                       border-radius: 6px;
                                       border: 1px solid;
                                       border-style: solid;
                                       font-weight: 750;}""")
        self.appOnToggle.clicked.connect(self.set_subtitles)
        
        #time value display
        self.time_text = QtWidgets.QLineEdit()
        self.time_text.setReadOnly(True)
        self.time_text.setStyleSheet("""color: white;
                                       border-radius: 0px;
                                       font-weight: 750;""")
        self.time_text.setText("00:00:00/--:--:--")
        
        #video time slider
        self.time_slider = QtWidgets.QSlider()
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(1000)
        self.time_slider.setSingleStep(1)
        self.time_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.time_slider.sliderPressed.connect(self.on_time_slider_pressed)
        self.time_slider.sliderMoved.connect(self.change_video_pos)
        self.time_slider.sliderReleased.connect(self.on_time_slider_released)
        self.time_slider.setStyleSheet(slider_style)
        self.time_slider.installEventFilter(self)

        # group all of the video buttons together in the HBox layout
        self.video_buttons = QtWidgets.QHBoxLayout()
        self.video_buttons.addWidget(self.play_button, 1)
        self.video_buttons.addWidget(self.appOnToggle, 2)
        self.video_buttons.addWidget(self.volume_button, 1)
        self.video_buttons.addWidget(self.volume_slider, 3)
        self.video_buttons.addWidget(self.time_text, 3)

        # put together the buttons and the time progress bar to make up the menu bar
        self.video_menuBar = QtWidgets.QVBoxLayout()
        self.video_menuBar.addWidget(self.time_slider)
        self.video_menuBar.addLayout(self.video_buttons)

        # main video layout
        self.video_layout = QtWidgets.QVBoxLayout()
        self.video_layout.setSpacing(0)
        self.video_layout.setContentsMargins(0, 0, 0, 0)

        # put all of the sub layouts together in the main layout
        self.video_layout.addWidget(self.video)
        self.video_layout.addLayout(self.video_menuBar)
        self.setLayout(self.video_layout)
        
     # function that gets the current Zipf frequency
     def get_current_zipf(self):
         return self.zipf_cur
     
     # function that sets the Zipf frequency
     def set_zipf(self, new_zipf):
         self.zipf_start = new_zipf
         self.zipf_cur = new_zipf

     # function that mutes the video
     def volume_mute(self):
        if self.volume_slider.value() != 0:
            self.old_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
            self.isMuted = True
        else:
            self.volume_slider.setValue(self.old_volume)
            self.isMuted = False
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])

     # function that changes the play button icon and sets the correct subtitle file
     def set_play_button_style(self):
         self.isPaused = not self.player.is_playing()
         if self.player.is_playing():
             if self.subs_are_dual:
                 self.make_dual_subs()
                 self.player.video_set_subtitle_file("subs_cleaned_dual.srt")
             else:
                 if self.appOnToggle.isChecked():
                    self.player.video_set_subtitle_file("subs_cleaned.srt")
                 else: 
                    self.player.video_set_subtitle_file("subs_cleaned_no_ex.srt")
         self.play_button.setIcon(self.playButtonIcons[int(self.isPaused)])

     # function that maps the play button to the video play/pause functions. Also sets the video audio track
     def play_video(self):
        if "fr" in self.episode or "sp_ep2" in self.episode:
            self.player.audio_set_track(3)
        if "sp_ep1" in self.episode:
            self.player.audio_set_track(2)
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

     # function for changing video volume with volume slider
     def change_volume(self):
        self.player.audio_set_volume(self.volume_slider.value())
        if self.volume_slider.value() == 0:
            self.isMuted = True
        else:
            self.isMuted = False
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])

     # function that allows the user to scroll through the video with a time slider
     def change_video_pos(self):
         self.player.set_position(self.time_slider.value()/1000)
         total_time = str(timedelta(microseconds = self.player.get_length()*1000)).split('.')[0]
         cur_time = str(timedelta(microseconds = self.player.get_time()*1000)).split('.')[0]
         self.time_text.setText(f'{cur_time}/{total_time}')

     # function that controls slider appearance when it is dragged
     def on_time_slider_pressed(self):
         self.time_slider.setStyleSheet(slider_style_hover)
         self.player.pause()

     # function that controls slider appearance when it is released
     def on_time_slider_released(self):
         self.time_slider.setStyleSheet(slider_style)
         self.player.play()

     '''
     #function that upates the time slider slider position and the time display text
     def update_time_slider(self):
         self.time_slider.setValue(self.player.get_position()*1000)
         total_time = str(timedelta(microseconds = self.player.get_length()*1000)).split('.')[0]
         cur_time = str(timedelta(microseconds = self.player.get_time()*1000)).split('.')[0]
         self.time_text.setText(f'{cur_time}/{total_time}')
     '''

     def set_subtitles(self):
         if self.subs_are_dual:
             self.make_dual_subs()
             self.player.video_set_subtitle_file("subs_cleaned_dual.srt")
         else:
             if self.appOnToggle.isChecked():
                self.player.video_set_subtitle_file("subs_cleaned.srt")
             else: 
                self.player.video_set_subtitle_file("subs_cleaned_no_ex.srt")

     # function that selects candidate subs for every exercise timestamp and cleans the subtitles from the ### markup
     def prep_subs(self):
         break_time = timedelta(minutes = 3)
         ex_counter = 1
         low_time_bound = break_time * ex_counter - timedelta(microseconds= 30*10**6) # lower search frame bound by 30 seconds
         up_time_bound = break_time * ex_counter + timedelta(microseconds=60 * 10**6) # upper search frame bound by 60 seconds
         sub_ind_list = []
         for ind in range(len(self.subs_orig)):
             sub_time = self.sub_time_to_timedelta(self.subs_orig[ind].start)
             word= self.get_word_data_from_sub(ind)
             if word: # if subtitle contains a word of interest
                 self.subs_cur[ind].text = re.sub(r'###[\W\w]+:[\W\w]+:[\W\w]+:[\W\w]+###', '', self.subs_cur[ind].text) # clean subtitle for later displaying
                 self.subs_l1[ind].text = self.subs_cur[ind].text
                 if sub_time >= low_time_bound and sub_time <= up_time_bound: # if subtitle falls within the time interval
                     sub_ind_list.append(ind)
             elif sub_time > up_time_bound and ex_counter < self.num_exercises:
                 self.sub_ind_for_ex.append(sub_ind_list.copy())
                 sub_ind_list = []
                 ex_counter+=1
                 low_time_bound = break_time * ex_counter - timedelta(microseconds= 30*10**6)
                 up_time_bound = break_time * ex_counter + timedelta(microseconds=60 * 10**6)
         self.subs_cur.save("subs_cleaned.srt", encoding='utf-8')
         self.subs_l1.save("subs_cleaned_no_ex.srt", encoding='utf-8')
         print(self.sub_ind_for_ex)
         self.num_exercises = len(self.sub_ind_for_ex) # update number of exercises to the number of possible exercises
         self.choose_ex_ind(self.sub_ind_for_ex[0])
             
     # function that chooses the subtitle for the next exercise
     def choose_ex_ind(self, ind_list):
         try:
            ind = min(ind_list, key = lambda x: abs(self.zipf_cur - float(self.get_word_data_from_sub(x)[0][2])))
            self.ind_to_stop_at_stack.append(ind)
            if self.cur_ex_ind % 3 == 0: # do exercise type 1 every 3 exercises
                word_data = self.get_word_data_from_sub(ind)[0]
                self.subs_cur[ind].text = re.sub(word_data[0], '<font color=#00D1FF weight=750><b>'+word_data[0]+'</b></font>', self.subs_cur[ind].text)
                self.subs_cur.save("subs_cleaned.srt", encoding='utf-8')
         except: return

     # function that extracts the data between ### in the 'modified' subtitle file
     def get_word_data_from_sub(self, ind):
         return re.findall(r'###([\W\w]+):([\W\w]+):([\W\w]+):([\W\w]+)###', self.subs_orig[ind].text)
         
     # function that convert the subtitle time property to a datetime.timedelta value
     def sub_time_to_timedelta(self, time):
         return timedelta(hours=time.hours, minutes=time.minutes, 
                             seconds=time.seconds, microseconds=time.milliseconds * 1000) 
     
     # function that generates dual subtitles
     def make_dual_subs(self):
         for ind in range(len(self.subs_l2)):
             self.subs_l2[ind].text = '<font color=#F3E73C>'+self.subs_l2[ind].text+'</font>'
         rsubs = self.subs_l1 + self.subs_l2
         if self.appOnToggle.isChecked(): rsubs = self.subs_cur + self.subs_l2
         rsubs.sort()
         rsubs.clean_indexes()
         rsubs.save ("subs_cleaned_dual.srt", encoding='utf-8')

     # function that adjusts the user's language level (Zipf frequency) based on the sequence of their (in)correct exercise answers
     def adjust_difficulty(self):
         print('old list', self.num_correct_ex)
         print('old zipf', self.zipf_cur)
         if self.num_correct_ex[-1] == 1:
             self.zipf_cur += -0.1 * 2 ** (len(list(itertools.takewhile(lambda x: x == 1, self.num_correct_ex[::-1]))) - 1)
         else:
             self.zipf_cur += 0.1 * 2 ** (len(list(itertools.takewhile(lambda x: x == 0, self.num_correct_ex[::-1]))) - 1)
         
         if (np.asarray(self.num_correct_ex).all() or not np.asarray(self.num_correct_ex).any()) and len(self.num_correct_ex) == 3: 
             self.num_correct_ex = []
         elif len(self.num_correct_ex) == 2 and self.num_correct_ex[0] != self.num_correct_ex[1]:
             self.num_correct_ex.pop(0)
         elif len(self.num_correct_ex) == 3:
             if self.num_correct_ex[0] != self.num_correct_ex[1]:
                 self.num_correct_ex.pop(0)
             elif self.num_correct_ex[1] != self.num_correct_ex[2]:
                 self.num_correct_ex.pop(0)
                 self.num_correct_ex.pop(0)

         print('new list', self.num_correct_ex)
         print('new list', self.zipf_cur)
     
     