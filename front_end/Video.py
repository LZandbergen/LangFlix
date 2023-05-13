import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtMultimediaWidgets as QtMultimediaWidgets
import vlc
import pysrt
import re
#import time
from datetime import timedelta

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
     def __init__(self):
        super().__init__()

        #self.setStyleSheet("""background-color: black;""")
        self.isPaused = True
        self.isMuted = True
        self.subs_orig = pysrt.open("/Users/mariiazamyrova/Downloads/LangFlix/back_end/MANUAL_Money.Heist.S01E01.XviD-AFG-eng copy.srt")
        self.subs_cur = pysrt.open("/Users/mariiazamyrova/Downloads/LangFlix/back_end/MANUAL_Money.Heist.S01E01.XviD-AFG-eng copy.srt")
        
        #self.subs = pysrt.open("/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt")
        self.sub_to_pause_at = [1, 12]
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.timerEvent)
        self.prep_subs()
        #self.buttonSizeHeight = self.size().height()/10 * 3

        self.volumeButtonIcons = [QtGui.QIcon("/Users/mariiazamyrova/Downloads/icons8-speaker-50.png"),
                                QtGui.QIcon("/Users/mariiazamyrova/Downloads/icons8-no-speaker-50.png")]

        self.playButtonIcons = [QtGui.QIcon("/Users/mariiazamyrova/Downloads/icons8-pause-50.png"),
                                QtGui.QIcon("/Users/mariiazamyrova/Downloads/icons8-play-50.png")]
        # create video window
        self.video = QtWidgets.QFrame()#QWidget() # video screen
        self.video.setStyleSheet("""background-color: black; border-bottom-color: white;""")
        self.video_menuBar = QtWidgets.QVBoxLayout()
        self.video_buttons = QtWidgets.QHBoxLayout()
        
        # instantiate video player
        Instance = vlc.Instance()
        self.player = Instance.media_player_new()
        self.media = Instance.media_new("/Users/mariiazamyrova/Downloads/Exercise1_demo.mp4")
        #self.media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
        self.player.set_media(self.media) 
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
        self.volume_button.clicked.connect(self.show_volume_slider)
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
        
        #video time slider
        self.time_slider = QtWidgets.QSlider()
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(1000)
        self.time_slider.setSingleStep(1)
        self.time_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.time_slider.sliderPressed.connect(self.on_time_slider_pressed)
        self.time_slider.sliderMoved.connect(self.change_video_pos)
        self.time_slider.sliderReleased.connect(self.on_time_slider_released)
        self.videoEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, lambda x: self.react_to_time_change(self.sub_to_pause_at)) 
        self.time_slider.setStyleSheet(slider_style)
        self.time_slider.installEventFilter(self)
        
        self.video_layout = QtWidgets.QVBoxLayout()
        self.video_layout.setSpacing(0)
        self.video_layout.setContentsMargins(0, 0, 0, 0)

        self.video_buttons.addWidget(self.play_button, 3)
        self.video_buttons.addWidget(self.volume_button, 3)
        self.video_buttons.addWidget(self.volume_slider, 4)
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
                
     def show_volume_slider(self):
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()

     def set_play_button_style(self):
         self.isPaused = not self.player.is_playing()
         if self.player.is_playing():
             self.player.video_set_subtitle_file("/Users/mariiazamyrova/Downloads/LangFlix/front_end/MANUAL_Money.Heist.S01E01.XviD-AFG-eng.wordsreplaced.srt")
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

     def on_time_slider_pressed(self):
         self.time_slider.setStyleSheet(slider_style_hover)
         self.player.pause()

     def on_time_slider_released(self):
         self.time_slider.setStyleSheet(slider_style)
         self.player.play()

     #how do we want to cue pausing? Should we use a dictionary with subtitle index to pause at, exercise type and the text to use for execise?
     #how do i schedule video pause at given time?
     
     # function that cues events related to video timing
     def react_to_time_change(self, indices):
         #update slider position
         self.time_slider.setValue(self.player.get_position()*1000)
         try:
             ind = indices[0]
         except:
             return 
         timestamp = self.subs_cur[ind].start
         sub_time = timedelta(hours=timestamp.hours, minutes=timestamp.minutes, 
                             seconds=timestamp.seconds, microseconds=timestamp.milliseconds * 1000)   
         low_time_bound = timedelta(microseconds=self.player.get_time()*1000)
         up_time_bound = sub_time + timedelta(microseconds=1000*1000)
         if low_time_bound >= sub_time and low_time_bound < up_time_bound:
             self.player.pause()
             self.sub_to_pause_at.remove(ind)

     def prep_subs(self):
         for ind in self.sub_to_pause_at:
             word= re.findall(r'##([\W\w]+):([\W\w]+):([\W\w]+)##', self.subs_orig[ind].text)
             if word:
                 self.subs_cur[ind].text = re.sub(word[0][0], '<font color=#00D1FF weight=750><b>'+word[0][1]+'</b></font>', self.subs_orig[ind].text)
                 self.subs_cur[ind].text = re.sub(r'##[\W\w]+:[\W\w]+:[\W\w]+##', '', self.subs_cur[ind].text)
         self.subs_cur.save('/Users/mariiazamyrova/Downloads/LangFlix/front_end/MANUAL_Money.Heist.S01E01.XviD-AFG-eng.wordsreplaced.srt', encoding='utf-8')