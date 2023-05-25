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

     def __init__(self, video_file, sub_file_l1, sub_file_l2):
        super().__init__()

        #self.cefr_start = 'A2' #cefr
        #self.cefr_cur = 5.0 #zipf

        self.zipf_start = -1
        self.zipf_cur = self.zipf_start

        self.subs_are_dual = False
        self.num_correct_ex = []

        self.zero_counter = 0
        self.one_counter = 0
        self.def_dec = -0.1
        self.def_inc = 0.1

        #self.time_between_ex = 60 * 10**6 #time intervals between exercises
        #self.ex_counter = 1 #counter for number of exercises so far

        self.num_exercises = 10 # number of exercises per video

        self.sub_ind_for_ex = [] # array to store the indices of candidate subs per exercise

        self.ind_to_stop_at_stack = [] # stack to store next subtitle to pause at
        
        self.cur_ex_ind = 0 # current exercise index

        self.old_volume = 0 # volume prior to mute button being pressed

        #self.setStyleSheet("""background-color: black;""")
        self.isPaused = True
        self.isMuted = True
        self.subs_orig = pysrt.open(sub_file_l1)
        self.subs_cur = pysrt.open(sub_file_l1)

        self.subs_l2 = pysrt.open(sub_file_l2)
        
        #self.subs = pysrt.open("/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt")
        #self.sub_to_pause_at = [1, 12]
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.timerEvent)
        self.prep_subs()
        self.make_dual_subs()
        #self.buttonSizeHeight = self.size().height()/10 * 3

        self.volumeButtonIcons = [QtGui.QIcon("icons8-speaker-50.png"),
                                QtGui.QIcon("icons8-no-speaker-50.png")]

        self.playButtonIcons = [QtGui.QIcon("icons8-pause-50.png"),
                                QtGui.QIcon("icons8-play-50.png")]
        # create video window
        self.video = QtWidgets.QFrame()#QWidget() # video screen
        self.video.setStyleSheet("""background-color: black; border-bottom-color: white;""")
        self.video_menuBar = QtWidgets.QVBoxLayout()
        self.video_buttons = QtWidgets.QHBoxLayout()
        
        # instantiate video player
        Instance = vlc.Instance()
        self.player = Instance.media_player_new()
        self.media = Instance.media_new(video_file)
        #self.media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
        self.player.set_media(self.media) 
        self.player.audio_set_volume(0)
        
        # Connect video player to window: https://github.com/devos50/vlc-pyqt5-example
        if sys.platform == "win32": # for Windows
            self.player.set_hwnd(self.video.winId())
        else:
            self.player.set_nsobject(self.video.winId())  
               
        self.videoEventManager = self.player.event_manager()

        # make volume slider                               
        self.volume_slider = QtWidgets.QSlider()
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.valueChanged.connect(self.change_volume)

        #self.base_height = self.volume_slider.size().height()

        # make volume button                         
        self.volume_button = QtWidgets.QPushButton()
        self.base_width = self.volume_button.size().width()
        self.volume_button.setCheckable(True)
        self.volume_button.clicked.connect(self.volume_mute)
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])
        #self.volume_button.size().setHeight(self.buttonSizeHeight)
        #self.volume_button.setMinimumHeight(self.buttonSizeHeight)
        #self.volume_button.setMinimumWidth(self.base_width)
        self.volume_button.setStyleSheet("""border-style: solid;""")

        # make play/pause button
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setCheckable(True)
        self.play_button.clicked.connect(self.play_video)
        self.play_button.setIcon(self.playButtonIcons[int(self.isPaused)])
        #self.play_button.size().setHeight(self.buttonSizeHeight)
        #self.play_button.setMinimumHeight(self.buttonSizeHeight)
        #self.volume_button.setMinimumWidth(self.base_width)
        self.play_button.setStyleSheet("""border-style: solid;""")
        self.videoEventManager.event_attach(vlc.EventType.MediaPlayerPaused, lambda x: self.set_play_button_style()) 
        self.videoEventManager.event_attach(vlc.EventType.MediaPlayerPlaying, lambda x: self.set_play_button_style()) 

        '''
        # add turn LangFlix on/off toggle to the video window
        self.appOnToggle = QtWidgets.QPushButton("LangFlix")
        self.appOnToggle.setCheckable(True)
        self.appOnToggle.setStyleSheet("""QPushButton
                                      {background-color: grey; 
                                       color: white;
                                       border-radius: 6px;
                                       border: 1px solid;
                                       border-style: solid;
                                       font-weight: 750;}""")
        '''

        #time value
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
        
        self.video_layout = QtWidgets.QVBoxLayout()
        self.video_layout.setSpacing(0)
        self.video_layout.setContentsMargins(0, 0, 0, 0)

        self.video_buttons.addWidget(self.play_button, 1)
        #self.video_buttons.addWidget(self.appOnToggle, 2)
        self.video_buttons.addWidget(self.volume_button, 1)
        self.video_buttons.addWidget(self.volume_slider, 3)
        self.video_buttons.addWidget(self.time_text, 3)

        self.video_menuBar.addWidget(self.time_slider)
        self.video_menuBar.addLayout(self.video_buttons)

        self.video_layout.addWidget(self.video)
        self.video_layout.addLayout(self.video_menuBar)
        self.setLayout(self.video_layout)
        
        #self.installEventFilter(self)
     """
     def showLayoutChildren(self, layout, show = True):
        for i in range(layout.count()):
            if show:
                layout.itemAt(i).widget().show()
            else:
                layout.itemAt(i).widget().hide()
     """
    #  def get_cefr(self):
    #      return self.cefr_cur
     
    #  def set_cefr(self, new_cefr):
    #      self.cefr_cur = new_cefr

     def get_current_zipf(self):
         return self.zipf_cur
     
     def set_zipf(self, new_zipf):
         self.zipf_start = new_zipf
         self.zipf_cur = new_zipf

     def volume_mute(self):#show_volume_slider(self):
        if self.volume_slider.value() != 0:
            self.old_volume = self.volume_slider.value()
            #self.player.audio_set_volume(0)
            self.volume_slider.setValue(0)
            self.isMuted = True
        else:
            self.volume_slider.setValue(self.old_volume)
            self.isMuted = False
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])
        '''
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
        '''

     def set_play_button_style(self):
         self.isPaused = not self.player.is_playing()
         if self.player.is_playing():
             if self.subs_are_dual:
                 self.player.video_set_subtitle_file("subs_cleaned_dual.srt")
             else:
                 self.player.video_set_subtitle_file("subs_cleaned.srt")
             #self.player.video_set_subtitle_file("/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt")
         self.play_button.setIcon(self.playButtonIcons[int(self.isPaused)])
          
     def play_video(self):
        if self.player.is_playing():
            self.player.pause()
            #self.isPaused = True
            #self.timer.stop()
        else:
            self.player.play()
            #self.isPaused = False
            #self.timer.start(1000)
            #self.player.video_set_subtitle_file("/Users/mariiazamyrova/Downloads/LangFlix/front_end/La.casa.de.papel.S01E01.WEBRip.NetflixCopy.srt")
                
     def change_volume(self):
        self.player.audio_set_volume(self.volume_slider.value())
        if self.volume_slider.value() == 0:
            self.isMuted = True
        else:
            self.isMuted = False
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])
        
     def change_video_pos(self):
         self.player.set_position(self.time_slider.value()/1000)
         total_time = str(timedelta(microseconds = self.player.get_length()*1000)).split('.')[0]
         cur_time = str(timedelta(microseconds = self.player.get_time()*1000)).split('.')[0]
         self.time_text.setText(f'{cur_time}/{total_time}')

     def on_time_slider_pressed(self):
         self.time_slider.setStyleSheet(slider_style_hover)
         self.player.pause()

     def on_time_slider_released(self):
         self.time_slider.setStyleSheet(slider_style)
         self.player.play()

     def update_time_slider(self):
         self.time_slider.setValue(self.player.get_position()*1000)
         total_time = str(timedelta(microseconds = self.player.get_length()*1000)).split('.')[0]
         cur_time = str(timedelta(microseconds = self.player.get_time()*1000)).split('.')[0]
         self.time_text.setText(f'{cur_time}/{total_time}')

     #how do we want to cue pausing? Should we use a dictionary with subtitle index to pause at, exercise type and the text to use for execise?
     #how do i schedule video pause at given time?
     '''
     # function that cues events related to video timing
     def react_to_time_change(self, indices):
         #update slider position
         self.time_slider.setValue(self.player.get_position()*1000)
         try:
             ind = indices[0]
         except:
             return 
         #compute one exercise in advance
         #timestamp = timedelta(microseconds=self.ex_counter * self.time_between_ex)#
         sub_start = self.subs_cur[ind].start
         sub_time = timedelta(hours=sub_start.hours, minutes=sub_start.minutes, 
                             seconds=sub_start.seconds, microseconds=sub_start.milliseconds * 1000)   
         #low_time_bound = sub_time - timedelta(microseconds= 10**6)
         player_time = timedelta(microseconds=self.player.get_time()*1000)
         up_time_bound = sub_time + timedelta(microseconds= 10**6)
         if player_time >= sub_time and player_time <= up_time_bound:
             self.player.pause()
             self.cur_ex_ind+=1
             self.choose_ex_ind(self.sub_ind_for_ex[self.cur_ex_ind])
             self.ind_to_stop_at_stack.pop(0)
     '''

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
                 if sub_time >= low_time_bound and sub_time <= up_time_bound: # if subtitle falls within the time interval
                     sub_ind_list.append(ind)
             elif sub_time > up_time_bound and ex_counter < self.num_exercises:
                 self.sub_ind_for_ex.append(sub_ind_list.copy())
                 sub_ind_list = []
                 ex_counter+=1
                 low_time_bound = break_time * ex_counter - timedelta(microseconds= 30*10**6)
                 up_time_bound = break_time * ex_counter + timedelta(microseconds=60 * 10**6)
         self.subs_cur.save("subs_cleaned.srt", encoding='utf-8')
         print(self.sub_ind_for_ex)
         self.num_exercises = len(self.sub_ind_for_ex) # update number of exercises to the number of possible exercises
         self.choose_ex_ind(self.sub_ind_for_ex[0])
             
             
         '''
         for ind in self.sub_to_pause_at:
             word= re.findall(r'###([\W\w]+):([\W\w]+):([\W\w]+)###', self.subs_orig[ind].text)
             if word:
                 self.subs_cur[ind].text = re.sub(word[0][0], '<font color=#00D1FF weight=750><b>'+word[0][1]+'</b></font>', self.subs_orig[ind].text)
                 self.subs_cur[ind].text = re.sub(r'###[\W\w]+:[\W\w]+:[\W\w]+###', '', self.subs_cur[ind].text)
         self.subs_cur.save(\"MANUAL_Money.Heist.S01E01.XviD-AFG-eng.wordsreplaced.srt", encoding='utf-8')
         '''
     def choose_ex_ind(self, ind_list):
         try:
            ind = min(ind_list, key = lambda x: abs(self.zipf_cur - float(self.get_word_data_from_sub(x)[0][2])))
            self.ind_to_stop_at_stack.append(ind)
            if self.cur_ex_ind % 3 == 0: # do exercise type 1 every 3 exercises
                word_data = self.get_word_data_from_sub(ind)[0]
                self.subs_cur[ind].text = re.sub(word_data[0], '<font color=#00D1FF weight=750><b>'+word_data[0]+'</b></font>', self.subs_cur[ind].text)
                self.subs_cur.save("subs_cleaned.srt", encoding='utf-8')
         except: return

     def get_word_data_from_sub(self, ind):
         return re.findall(r'###([\W\w]+):([\W\w]+):([\W\w]+):([\W\w]+)###', self.subs_orig[ind].text)
         
     def sub_time_to_timedelta(self, time):
         return timedelta(hours=time.hours, minutes=time.minutes, 
                             seconds=time.seconds, microseconds=time.milliseconds * 1000) 
     
     def make_dual_subs(self):
         for ind in range(len(self.subs_l2)):
             self.subs_l2[ind].text = '<font color=#F3E73C>'+self.subs_l2[ind].text+'</font>'
         rsubs = self.subs_cur + self.subs_l2
         rsubs.sort()
         rsubs.clean_indexes()
         rsubs.save ("subs_cleaned_dual.srt", encoding='utf-8')

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


         '''
         if len(self.num_correct_ex) == 3: # reevaluate the langauge level every 3 exercises
             if sum(self.num_correct_ex) == 3: #if got 3 correct in a row increase difficulty (decrease zipf)
                 self.zipf_cur =  max(1, self.zipf_cur - 0.5)
             elif sum(self.num_correct_ex) == 1: #if got only 1 out of 3 correct in a row decrease difficulty (increase zipf)
                 self.zipf_cur = min(self.zipf_cur + 0.5, 7)
             while True: # remove the sequence of correct exercises preceding the wrong one
                 try:
                    ex = self.num_correct_ex.pop(0)
                 except: break
                 if ex == 0:
                     break
         '''
         print('new list', self.num_correct_ex)
         print('new list', self.zipf_cur)
     
     