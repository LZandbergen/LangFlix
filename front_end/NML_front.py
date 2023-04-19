
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import vlc
import sys

# Global style that is passed as an argument to the window somewhere below.
# I used it to set a style for ALL radiobuttons, rather than do it for each
# individual radiobutton
global_style = '''QtWidgets.QRadioButton {
                  color: red;
                  background-color: red;
               }
               QtWidgets.QRadioButton::indicator {
                  width: 11px;
                  height: 11px;
                  border-radius: 5px;
               }
               QtWidgets.QRadioButton::indicator::checked {
                  border: 3px solid;
                  border-radius: 6px;
                  border-color: red;
                  background-color: red;
                  width: 7px;
                  height: 7px;
               }
               QtWidgets.QRadioButton::indicator::unchecked {
                  border: 1px solid;
                  border-radius: 5px;
                  border-color: #00D1FF;
                  background-color: #00D1FF;
                  width: 11px;
                  height: 11px;
               }
               '''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LangFlix")
        self.setMinimumSize(QtCore.QSize(600, 300))
        self.setStyleSheet("""background-color: #4B4948;""")
        
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create and connect the combo box to switch between pages
        self.pageCombo = QtWidgets.QPushButton("Dictionary")
        self.pageCombo.addItems(["Page 1", "Page 2"])
        self.pageCombo.activated.connect(self.switchPage)
        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        # Create the first page
        self.page1 = QWidget()
        self.page1Layout = QFormLayout()
        self.page1Layout.addRow("Name:", QLineEdit())
        self.page1Layout.addRow("Address:", QLineEdit())
        self.page1.setLayout(self.page1Layout)
        self.stackedLayout.addWidget(self.page1)
        # Create the second page
        self.page2 = QWidget()
        self.page2Layout = QFormLayout()
        self.page2Layout.addRow("Job:", QLineEdit())
        self.page2Layout.addRow("Department:", QLineEdit())
        self.page2.setLayout(self.page2Layout)
        self.stackedLayout.addWidget(self.page2)
        # Add the combo box and the stacked layout to the top-level layout
        layout.addWidget(self.pageCombo)
        layout.addLayout(self.stackedLayout)
        
        # create video window
        #self.video_gui_window = QtGui.QWindow()

        
        self.video = QtWidgets.QWidget()
        self.video.setStyleSheet("""background-color: black;""")
        self.video_menuBar = QtWidgets.QHBoxLayout()
        
        # instantiate video player
        Instance = vlc.Instance()
        self.player = Instance.media_player_new()
        #Media = Instance.media_new("./Documents/NML/Exercise4_demo.mpg")
        Media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
        self.player.set_media(Media) 
        #player.video_set_spu(2)
        
        self.player.set_nsobject(self.video.winId())  
        #player.play()
        #player.video_set_subtitle_file('/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt')
        
        self.video_layout = QtWidgets.QVBoxLayout()
        self.video_layout.addWidget(self.video)
        play_button = QtWidgets.QPushButton('Play/Pause')
        play_button.setCheckable(True)
        play_button.clicked.connect(self.play_video)
        play_button.setStyleSheet("""background-color: #A143A8; 
                                       color: #00D1FF;
                                       border-radius: 9px;
                                       border: 1px solid;""")
        """                               
        pause_button = QtWidgets.QPushButton('Pause')
        pause_button.setCheckable(True)
        pause_button.clicked.connect(lambda x: self.player.pause())
        pause_button.setStyleSheet(#background-color: #A143A8; color: #00D1FF; border-radius: 9px; border: 1px solid;)
        """
                                       
        self.volume_slider = QtWidgets.QSlider()
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.valueChanged.connect(self.change_volume)
                                       
        volume_button = QtWidgets.QPushButton('Volume')
        volume_button.setCheckable(True)
        volume_button.clicked.connect(self.show_volume_slider)
        volume_button.setStyleSheet("""background-color: #A143A8; 
                                       color: #00D1FF;
                                       border-radius: 9px;
                                       border: 1px solid;""")

        
        self.video_menuBar.addWidget(play_button, 3)
        #self.video_menuBar.addWidget(pause_button, 2)
        self.video_menuBar.addWidget(volume_button, 3)
        self.video_menuBar.addWidget(self.volume_slider, 4)
        self.video_layout.addLayout(self.video_menuBar)
        
        #self.video_gui_window.setVisible(True)
        
        self.video.installEventFilter(self)



        # Styling Submit and Skip buttons
        submit_button = QtWidgets.QPushButton("Submit")
        #submit_button.setGeometry(200, 150, 100, 100)

        submit_button.setStyleSheet("""background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 9px;
                                       border: 1px solid;""")
                                       
                                                              
        
        skip_button = QtWidgets.QPushButton("Skip")
        #skip_button.setGeometry(200, 150, 100, 100)
        #skip_button.setStyleSheet("border-radius: 15 px; border: 2px solid black;")
        skip_button.setStyleSheet("""background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 9px;
                                       border: 1px solid;""")

         # Styling exercise text
        exercise_text = QtWidgets.QLabel("What do you think is going to be said next?")
        exercise_font = exercise_text.font()
        exercise_font.setPointSize(13)
        #exercise_font.setStyle("background-color: #D9D9D9;")
        exercise_text.setFont(exercise_font)
        exercise_text.setStyleSheet('QLabel {color: white;}')

        """
         # Styling subtitles text
        subtitles = QtWidgets.QLabel("Place for subtitles")
        subtitles_font = subtitles.font()
        subtitles_font.setPointSize(18)
        subtitles.setFont(subtitles_font) 
        subtitles.setAlignment(QtCore.Qt.AlignCenter) 
        """        

        # Create radiobuttons
        r_button1 = QtWidgets.QRadioButton("1")
        r_button1.setStyleSheet('QRadioButton {color: white;}')
        r_button2 = QtWidgets.QRadioButton("2")
        r_button2.setStyleSheet('QRadioButton {color: white;}')

         # Create an exercise layout
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(submit_button)
        buttons_layout.addWidget(skip_button)
        
        exercise_layout = QtWidgets.QVBoxLayout()
        exercise_layout.addWidget(exercise_text)
        exercise_layout.addWidget(r_button1)
        exercise_layout.addWidget(r_button2)
        exercise_layout.addLayout(buttons_layout)

        # Main grid with all stuff (exercise layout, video, subtitles)
        grid = QtWidgets.QHBoxLayout()#QGridLayout()
        grid.addLayout(self.video_layout, 8)#addWidget(self.video)#, 0, 0)
        grid.addLayout(exercise_layout, 2)#, 0, 1)
        #grid.addWidget(subtitles, 1, 0, 1, 2)

        # Put grid in the window
        container = QtWidgets.QWidget()
        #container.setStyleSheet("background-color: #171717;")
        container.setLayout(grid)
        self.setCentralWidget(container)
      
    def showLayoutChildren(self, layout, show = True):
        for i in range(layout.count()):
            if show:
                layout.itemAt(i).widget().show()
            else:
                layout.itemAt(i).widget().hide()
                
    def show_volume_slider(self):
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
            
    def play_video(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()
            self.player.video_set_subtitle_file("/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt")
                
    def change_volume(self):
        self.player.audio_set_volume(self.volume_slider.value())
        
       
    def eventFilter(self, source, event):
        if source == self.video:
            if event.type() == QtCore.QEvent.Enter:
                self.video_layout.addItem(self.video_menuBar)
                self.video_menuBar.setEnabled(True)
                self.showLayoutChildren(layout = self.video_menuBar, show = True)
            elif event.type() == QtCore.QEvent.Leave:
                self.video_layout.removeItem(self.video_menuBar)
                self.video_menuBar.setEnabled(False)
                self.showLayoutChildren(layout = self.video_menuBar, show = False)
        return super().eventFilter(source, event)
         
            
    """
        if qApp.activePopupWidget() is None:
            if event.type() == QtCore.QEvent.MouseMove:
                if self.video_menuBar.isHidden():
                    rect = self.gemetry()
                    rect.setHeight(60)
                    
                    if rect.contains(event.globalPos()):
                        self.video_menuBar.show()
                else:
                    rect = QtCore.QRect(
                        self.video_menuBar.mapToGlobal(QtWidgets.QPoint(0, 0)),
                        self.video_menuBar.size()
                    )
                    if not rect.contains(event.globalPos()):
                        self.video_menuBar.hide()
            elif event.type() == QtCore.QEvent.Leave:
                self.video_menuBar.hide()
    """
"""    
Instance = vlc.Instance()
player = Instance.media_player_new()
#Media = Instance.media_new("./Documents/NML/Exercise4_demo.mpg")
Media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
player.set_media(Media) 
#player.video_set_spu(2)
"""
vlcApp = QtWidgets.QApplication([])
vlcApp.setStyleSheet(global_style)

window = MainWindow()
window.show()

#player.set_nsobject(window.video.winId())  
#player.play()
#player.video_set_subtitle_file('/Users/mariiazamyrova/Downloads/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt')

vlcApp.exec()