
import PySide6.QtCore as QtCore
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
        
        self.video = QtWidgets.QWidget()
        
        #main_layout = QHBoxLayout()
        #exercise_layout = QVBoxLayout()

        # Styling Submit and Skip buttons
        submit_button = QtWidgets.QPushButton("Submit")
        #submit_button.setGeometry(200, 150, 100, 100)

        submit_button.setStyleSheet("""background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 5px;
                                       border: 1px solid;""")
                                       
                                                              
        
        skip_button = QtWidgets.QPushButton("Skip")
        #skip_button.setGeometry(200, 150, 100, 100)
        #skip_button.setStyleSheet("border-radius: 15 px; border: 2px solid black;")
        skip_button.setStyleSheet("""background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 5px;
                                       border: 1px solid;""")

         # Styling exercise text
        exercise_text = QtWidgets.QLabel("What do you think is going to be said next?")
        exercise_font = exercise_text.font()
        exercise_font.setPointSize(13)
        #exercise_font.setStyle("background-color: #D9D9D9;")
        exercise_text.setFont(exercise_font)

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
        r_button2 = QtWidgets.QRadioButton("2")

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
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.video, 0, 0)
        grid.addLayout(exercise_layout, 0, 1)
        #grid.addWidget(subtitles, 1, 0, 1, 2)

        # Put grid in the window
        container = QtWidgets.QWidget()
        #container.setStyleSheet("background-color: #171717;")
        container.setLayout(grid)
        self.setCentralWidget(container)

Instance = vlc.Instance()
player = Instance.media_player_new()
#Media = Instance.media_new("./Documents/NML/Exercise4_demo.mpg")
Media = Instance.media_new("/Users/mariiazamyrova/Desktop/NML_front_end/Exercise4_demo.mp4")
player.set_media(Media) 

vlcApp = QtWidgets.QApplication([])
vlcApp.setStyleSheet(global_style)

window = MainWindow()
window.show()

player.set_nsobject(window.video.winId())  
player.play()

vlcApp.exec()