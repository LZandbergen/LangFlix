
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import vlc
import sys
from Video import Video

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
        
        # create video window
        
        self.video = Video() # video screen + player button toolbar
        self.video.installEventFilter(self)

        # Styling Submit and Skip buttons
        submit_button = QtWidgets.QPushButton("Submit")

        submit_button.setStyleSheet("""background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 9px;
                                       border: 1px solid;""")
                                       
                                                              
        
        skip_button = QtWidgets.QPushButton("Skip")
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
        grid.addWidget(self.video, 8)
        #grid.addLayout(self.video_layout, 8)#addWidget(self.video)#, 0, 0)
        grid.addLayout(exercise_layout, 2)#, 0, 1)
        #grid.addWidget(subtitles, 1, 0, 1, 2)

        # Put grid in the window
        container = QtWidgets.QWidget()
        #container.setStyleSheet("background-color: #171717;")
        container.setLayout(grid)
        self.setCentralWidget(container)

    def showLayoutChildren(self, layout, show = True):
        for i in range(layout.count()):
            if layout.itemAt(i).widget() is None:
                    self.showLayoutChildren(layout.itemAt(i).layout(), show)
            else:
                if show:
                    layout.itemAt(i).widget().show()
                else:
                    layout.itemAt(i).widget().hide()
       
    def eventFilter(self, source, event):
        if source == self.video:
            if event.type() == QtCore.QEvent.Enter:
                if self.video.video_layout.count()==1:
                    self.video.video_layout.addItem(self.video.video_menuBar)
                    self.video.video_menuBar.setEnabled(True)
                    self.showLayoutChildren(layout = self.video.video_menuBar, show = True)
            elif event.type() == QtCore.QEvent.Leave:
                if self.video.video_layout.count()==2:
                    self.video.video_layout.removeItem(self.video.video_menuBar)
                    self.video.video_menuBar.setEnabled(False)
                    self.showLayoutChildren(layout = self.video.video_menuBar, show = False)
        
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
    
Instance = vlc.Instance()
player = Instance.media_player_new()
print(open("../Exercise4_demo.mp4"))
Media = Instance.media_new("../Exercise4_demo.mp4")
#Media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
player.set_media(Media) 
#player.video_set_spu(2)

vlcApp = QtWidgets.QApplication([])
vlcApp.setStyleSheet(global_style)

window = MainWindow()
window.show()

vlcApp.exec()