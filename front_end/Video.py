import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import vlc
import time

class Video(QtWidgets.QWidget):
     def __init__(self):
        super().__init__()

        self.setStyleSheet("""background-color: black;""")
        self.isPaused = True
        self.isMuted = True

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
        Media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
        self.player.set_media(Media) 
        self.player.set_nsobject(self.video.winId())  

        # make volume slider                               
        self.volume_slider = QtWidgets.QSlider()
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.base_height = self.volume_slider.size().height()

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

        #video time slider
        self.time_slider = QtWidgets.QSlider()
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(self.player.get_length())
        self.time_slider.setSingleStep(1)
        self.time_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.time_slider.valueChanged.connect(lambda x: self.player.set_time(self.time_slider.value()))
        
        self.video_layout = QtWidgets.QVBoxLayout()
        self.video_layout.setSpacing(0)
        self.video_layout.setContentsMargins(0, 0, 0, 0)

        self.video_buttons.addWidget(self.play_button, 3)
        self.video_buttons.addWidget(self.volume_button, 3)
        self.video_buttons.addWidget(self.volume_slider, 4)
        self.video_menuBar.addWidget(self.time_slider)
        self.video_menuBar.addLayout(self.video_buttons)

        self.video_layout.addWidget(self.video, 8)
        self.video_layout.addLayout(self.video_menuBar)
        self.setLayout(self.video_layout)
        
        #self.installEventFilter(self)
     
     def showLayoutChildren(self, layout, show = True):
        for i in range(layout.count()):
            if show:
                layout.itemAt(i).widget().show()
            else:
                layout.itemAt(i).widget().hide()
     

     def update_time_slider(self):
         while self.time_slider.value() < self.time_slider.maximum() and not self.isPaused:
             time.sleep(1)
             self.time_slider.setValue(self.player.get_time())
                
     def show_volume_slider(self):
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
            
     def play_video(self):
        if self.player.is_playing():
            self.player.pause()
            self.isPaused = True
        else:
            self.player.play()
            self.isPaused = False
            self.update_time_slider()
            self.player.video_set_subtitle_file("/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt")

        self.play_button.setIcon(self.playButtonIcons[int(self.isPaused)])
                
     def change_volume(self):
        self.player.audio_set_volume(self.volume_slider.value())
        if self.volume_slider.value() == 0:
            self.isMuted = True
        else:
            self.isMuted = False
        self.volume_button.setIcon(self.volumeButtonIcons[int(self.isMuted)])
      
     def eventFilter(self, source, event):
        if source == self.play_button:
            if event.type() == QtCore.QEvent.Enter:
                if self.video_layout.count()==1:
                    self.video_layout.addItem(self.video_menuBar)
                    self.video_menuBar.setEnabled(True)
                    self.showLayoutChildren(layout = self.video_menuBar, show = True)
                    self.video.setStyleSheet("""background-color: black; 
                    border-bottom-color: white;
                    border-bottom-width: 15px;""")
            elif event.type() == QtCore.QEvent.Leave:
                if self.video_layout.count()==2:
                    self.video_layout.removeItem(self.video_menuBar)
                    self.video_menuBar.setEnabled(False)
                    self.showLayoutChildren(layout = self.video_menuBar, show = False)
                    self.video.setStyleSheet("""background-color: black; 
                    border-bottom-color: black;""")
        
        return super().eventFilter(source, event)
     