
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import vlc
import sys
from Lars_Video import Video

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
        self.setStyleSheet("""background-color: #171717;""")
        
        id1 = QtGui.QFontDatabase.addApplicationFont("front_end/fonts/Quicksand-SemiBold.ttf")
        id2 = QtGui.QFontDatabase.addApplicationFont("front_end/fonts/Quicksand-LightItalic.ttf")
        id3 = QtGui.QFontDatabase.addApplicationFont("front_end/fonts/Quicksand-Medium.ttf")
        if id1 < 0 or id2 < 0 or id3 < 0: 
            print("Error with adding font")
        families = []
        for id in [id1, id2, id3]: families.append(QtGui.QFontDatabase.applicationFontFamilies(id)) 

        # create video window
        
        self.video = Video() # video screen + player button toolbar
        self.video.installEventFilter(self)

        # Styling exercise text
        exercise_text = QtWidgets.QLabel("What do you think is going to be said next?")
        #exercise_text.setFont(QtGui.QFont(families[0]))
        exercise_text.setStyleSheet('QLabel {padding-left: 16px; color: #CACACA; font-size: 16px; font-weight: 780; background-color: #1E1E1E;}')

        # Styling exercise sentence
        exercise_sentence = QtWidgets.QLabel("some test sentence")
        #exercise_font = QtGui.QFont(families[0])
        #exercise_font.setItalic(True)
        #exercise_sentence.setFont(exercise_font) 
        exercise_sentence.setStyleSheet('QLabel {padding-left: 16px; color: #CACACA; font-size: 16px; font-weight: 750; background-color: #1E1E1E;}')


        # Create radiobuttons
        style =  '''QRadioButton 
                        {padding-left: 40px;  color: #D9D9D9; font-weight: 700; font-size: 15px; background-color: #1E1E1E;}
                    QRadioButton::indicator::unchecked
                        {border-radius: 7px; border: 1.5px solid; width: 10px; height: 10px; border-color: black;}
                    QRadioButton::indicator::checked
                        {image: url(front_end/RadioButton (1).png); width: 14px; height: 14px;}
                 '''
        r_button1 = QtWidgets.QRadioButton()
        r_button1.setStyleSheet(style)
        rb_text1 = QtWidgets.QLabel()
        rb_text1.setStyleSheet('QLabel {border: 0px; padding: 0px, 4px, 0px, 0px; color: #CACACA; font-size: 15px; font-weight: 700; background-color: #1E1E1E;}')
        #rb_text1.setFont(QtGui.QFont(families[0]))
        rb_layout1 = QtWidgets.QHBoxLayout()
        rb_layout1.setSpacing(0)
        rb_layout1.setAlignment(QtCore.Qt.AlignLeft)
        rb_layout1.addWidget(r_button1)
        rb_layout1.addWidget(rb_text1)
        r_button2 = QtWidgets.QRadioButton()
        r_button2.setStyleSheet(style)
        rb_text2 = QtWidgets.QLabel()
        rb_text2.setStyleSheet('QLabel {border: 0px; padding: 0px, 4px, 0px, 0px; color: #CACACA; font-size: 15px; font-weight: 700; background-color: #1E1E1E;}')
        #rb_text2.setFont(QtGui.QFont(families[0]))
        rb_layout2 = QtWidgets.QHBoxLayout()
        rb_layout2.setSpacing(0)
        rb_layout2.setAlignment(QtCore.Qt.AlignLeft)
        rb_layout2.addWidget(r_button2)
        rb_layout2.addWidget(rb_text2)
        r_button3 = QtWidgets.QRadioButton()
        r_button3.setStyleSheet(style)
        rb_text3 = QtWidgets.QLabel()
        rb_text3.setStyleSheet('QLabel {border: 0px; padding: 0px, 4px, 0px, 0px; color: #CACACA; font-size: 15px; font-weight: 700; background-color: #1E1E1E;}')
        #rb_text3.setFont(QtGui.QFont(families[0]))
        rb_layout3 = QtWidgets.QHBoxLayout()
        rb_layout3.setSpacing(0)
        rb_layout3.setAlignment(QtCore.Qt.AlignLeft)
        rb_layout3.addWidget(r_button3)
        rb_layout3.addWidget(rb_text3)
        rButtons_layout = QtWidgets.QVBoxLayout()
        rButtons_layout.addLayout(rb_layout1)
        rButtons_layout.addLayout(rb_layout2)
        rButtons_layout.addLayout(rb_layout3)
        rButtons_layout.setSpacing(0)

        # Styling Submit button
        submit_button = QtWidgets.QPushButton("Submit")
        #submit_button.setFont(QtGui.QFont(families[0]))
        submit_button.setStyleSheet("""QPushButton
                                      {background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 13px;
                                       border: 1px solid;
                                       border-color: #0043A8;
                                       height: 25px;
                                       width: 40px;
                                       font-weight: 750;}
                                       QPushButton::hover
                                       {background-color: #003585;
                                        border-color: #003585;
                                    }""")

        # Create correct/incorrect label
        cor_incor_text = QtWidgets.QLabel("")
        cor_incor_text.setStyleSheet('QLabel {color: #00D1FF; font-weight: 720; font-size: 15px; background-color: #1E1E1E;}')
        #cor_incor_text.setFont(QtGui.QFont(families[0]))
        cor_incor_icon = QtWidgets.QLabel()
        cor_incor_icon.setStyleSheet('QLabel {background-color: #1E1E1E;}')
        #QtGui.QIcon("./Documents/GitHub/LangFlix/front_end/tab_image.png")
        cor_incor_layout = QtWidgets.QHBoxLayout()
        cor_incor_layout.setAlignment(QtCore.Qt.AlignCenter)
        cor_incor_layout.addWidget(cor_incor_icon)
        cor_incor_layout.addWidget(cor_incor_text)
        
        self.correct_word = ''
        # Function to check if the answer is correct
        def checkAnswer():
            cur_checked = '_'
            for rb, word in [[r_button1,rb_text1], [r_button2,rb_text2], [r_button3,rb_text3]]:
                if rb.isChecked():
                    cur_checked = word.text()
                if cur_checked == self.correct_word:
                    cor_incor_text.setText("Great, correct!")
                    pixmap = QtGui.QPixmap("front_end/correct.png")
                    cor_incor_icon.setPixmap(pixmap)
                    buttons_stackedLayout.setCurrentIndex(1)
                    rb.setStyleSheet('''QRadioButton 
                                            {padding-left: 40px; color: #00D1FF; font-weight: 700; font-size: 15px; background-color: #1E1E1E;}
                                        QRadioButton::indicator::unchecked
                                            {border-radius: 7px; border: 1.5px solid; width: 10px; height: 10px; border-color: black;}
                                        QRadioButton::indicator::checked
                                            {image: url(front_end/RadioButton (1).png); width: 14px; height: 14px;}
                                    ''')
                    break
                else: 
                    cor_incor_text.setText("Incorrect, try again")
                    pixmap = QtGui.QPixmap("front_end/incorrect.png")
                    cor_incor_icon.setPixmap(pixmap)
        submit_button.clicked.connect(checkAnswer)                             


        self.num = 3 # Number of skips                                                      
        # Styling Skip button
        skip_button = QtWidgets.QPushButton("Skip (" + str(self.num) + ")")
        #skip_button.setFont(QtGui.QFont(families[0]))
        skip_button.setStyleSheet("""QPushButton
                                       {background-color: #1E1E1E; 
                                       color: #CACACA;
                                       border-radius: 4px;
                                       border: 1.5px solid;
                                       border-color: #CACACA;
                                       height: 25px;
                                       width: 40px;
                                       font-weight: 750;}
                                     QPushButton::hover
                                       {background-color: #121212;
                                    }""")
               
        # Function to skip exercise
        def skip():
            if self.num:
                self.num -= 1
                skip_button.setText("Skip (" + str(self.num) + ")")
                switchToDict()
                exercise_tab.setHidden(True)
        skip_button.clicked.connect(skip) 

        # Styling Continue button
        continue_button = QtWidgets.QPushButton("Continue")
        #continue_button.setFont(QtGui.QFont(families[0]))
        continue_button.setStyleSheet("""QPushButton
                                        {background-color: #0043A8; 
                                        color: #00D1FF;
                                        border-radius: 13px;
                                        border: 1px solid;
                                        border-color: #0043A8;
                                        height: 25px;
                                        width: 40px;
                                        font-weight: 750;}
                                        QPushButton::hover
                                       {background-color: #003585;
                                        border-color: #003585;
                                        }""")
        
        # Function to finish exercise and resume video  
        def Continue():
            switchToDict()
            exercise_tab.setHidden(True)
        continue_button.clicked.connect(Continue)

        # Create stacked layout for Submit/Skip and Continue buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(submit_button)
        buttons_layout.addWidget(skip_button)
        buttons_layout.setSpacing(80)
        buttons_layout.setContentsMargins(16,0,16,0)
        buttons_layout.setAlignment(QtCore.Qt.AlignTop)
        buttons_widget = QtWidgets.QWidget()
        buttons_widget.setStyleSheet("background-color: #1E1E1E;")
        buttons_widget.setLayout(buttons_layout)
        continueButton_layout = QtWidgets.QHBoxLayout()
        continueButton_layout.addWidget(continue_button)
        continueButton_layout.setContentsMargins(16,0,16,0)
        continueButton_layout.setAlignment(QtCore.Qt.AlignTop)
        continueButton_widget = QtWidgets.QWidget()
        continueButton_widget.setStyleSheet("background-color: #1E1E1E;")
        continueButton_widget.setLayout(continueButton_layout)
        buttons_stackedLayout = QtWidgets.QStackedLayout()
        buttons_stackedLayout.addWidget(buttons_widget)
        buttons_stackedLayout.addWidget(continueButton_widget)

        # Functions for switching between tabs
        def switchToDict():
            stackedLayout.setCurrentIndex(1)
            dictionary_tab.setStyleSheet('QPushButton {border: 0px; color: white; font-weight: 800; font-size: 16px; image: url("./Downloads/LangFlix/front_end/tab_image1.png"); text-align: center; background-position: center right;}')
            exercise_tab.setStyleSheet('QPushButton {border: 0px; color: #A7A7A7; font-weight: 800; font-size: 16px;} QPushButton::hover {color: #CACACA;}')
        def switchToExercise():
            stackedLayout.setCurrentIndex(0)
            exercise_tab.setVisible(True)
            exercise_tab.setStyleSheet('QPushButton {border: 0px; color: white; font-weight: 800; font-size: 16px; image: url("./Downloads/LangFlix/front_end/tab_image2.png"); text-align: center; background-position: center left;}')
            dictionary_tab.setStyleSheet('QPushButton {border: 0px; color: #A7A7A7; font-weight: 800; font-size: 16px;} QPushButton::hover {color: #CACACA;}')

        # Create and connect tabs to switch between pages
        dictionary_tab = QtWidgets.QPushButton("  Dictionary")
        #dictionary_tab.setFont(QtGui.QFont(families[0]))
        dictionary_tab.setStyleSheet('''QPushButton 
                                        {border: 0px; 
                                        color: white; 
                                        font-weight: 800; 
                                        font-size: 16px; 
                                        image: url("./Downloads/LangFlix/front_end/tab_image1.png"); 
                                        text-align: center; 
                                        background-position: center right;}
                                        QPushButton::hover
                                       {color: #CACACA;
                                    }''')
        size1 = (120, 50)
        dictionary_tab.setFixedSize(*size1)
        dictionary_tab.clicked.connect(switchToDict)     
        exercise_tab = QtWidgets.QPushButton("  Exercise")
        #exercise_tab.setFont(QtGui.QFont(families[0]))
        exercise_tab.setStyleSheet('''QPushButton 
                                        {border: 0px; 
                                        color: white; 
                                        font-weight: 800; 
                                        font-size: 16px; 
                                        image: url("front_end/tab_image2.png"); 
                                        text-align: center; 
                                        background-position: center left;}
                                        QPushButton::hover
                                       {color: #CACACA;
                                    }''')
        size2 = (110, 50)
        exercise_tab.setFixedSize(*size2)
        exercise_tab.clicked.connect(switchToExercise)
        tabs_layout = QtWidgets.QHBoxLayout()
        tabs_layout.addWidget(dictionary_tab)
        tabs_layout.addWidget(exercise_tab)
        tabs_layout.setAlignment(QtCore.Qt.AlignLeft)
        tabs_layout.setContentsMargins(0,0,0,0)
        tabs_layout.setSpacing(0)

        # Create a top-level layout
        side_layout = QtWidgets.QVBoxLayout()
        # Create the stacked layout
        stackedLayout = QtWidgets.QStackedLayout()
        
        def generateExercise(sentence, word1, word2, word3, cor_word):
            exercise_sentence.setText('"' + sentence + '"')
            rb_text1.setText(word1)
            rb_text2.setText(word2)
            rb_text3.setText(word3)
            self.correct_word = cor_word
            switchToExercise()

        # Create the exercise page       
        page1 = QtWidgets.QWidget()
        page1.setObjectName("page1")
        page1.setStyleSheet('#page1 {border: 2px solid; border-color: #121212; border-radius: 3px; background-color: #1E1E1E;}')   
        page1Layout = QtWidgets.QVBoxLayout()
        page1Layout.setAlignment(QtCore.Qt.AlignTop)
        page1Layout.addItem(QtWidgets.QSpacerItem(2, 24, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        page1Layout.addWidget(exercise_text)
        page1Layout.addItem(QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        page1Layout.addWidget(exercise_sentence)
        page1Layout.addItem(QtWidgets.QSpacerItem(2, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        page1Layout.addLayout(rButtons_layout)
        page1Layout.addItem(QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        page1Layout.addLayout(cor_incor_layout)
        page1Layout.addItem(QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        page1Layout.addLayout(buttons_stackedLayout)
        page1.setLayout(page1Layout)
        stackedLayout.addWidget(page1)
        # Generate text for the exercise
        generateExercise("Sentence with 'quotation' marks.", "word1", "word2", "word3", "word1")
        
        def addWordToDict(word, translation):
            row = QtWidgets.QHBoxLayout()
            row.setAlignment(QtCore.Qt.AlignLeft)
            new_word = QtWidgets.QLabel(word)
            new_word.setFont(QtGui.QFont(families[0]))
            new_word.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; padding-left: 16px; padding-right: 100px; width = 100; border-radius: 8px; height: 30; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
            equals = QtWidgets.QLabel("=")
            equals.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; height: 30; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
            word_translation = QtWidgets.QLabel(translation)
            word_translation.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; padding-left: 100px; border-radius: 8px; height: 30; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
            word_translation.setFont(QtGui.QFont(families[0])) 
            row.addWidget(new_word)
            row.addWidget(equals)
            row.addWidget(word_translation)
            row.setSpacing(0)
            page2Layout.addLayout(row)

        # Create the dictionary page
        page2 = QtWidgets.QWidget()
        page2.setObjectName("page2")
        page2.setStyleSheet('#page2 {border: 2px solid; border-color: #121212; border-radius: 3px; background-color: #1E1E1E;}')
        page2Layout = QtWidgets.QVBoxLayout()
        page2Layout.setAlignment(QtCore.Qt.AlignTop)
        spacer1 = QtWidgets.QSpacerItem(2, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        word_1 = QtWidgets.QLabel("word_1")
        #word_1.setFont(QtGui.QFont(families[0]))
        word_1.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; padding-left: 16px; border-radius: 8px; height: 30; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
        word_2 = QtWidgets.QLabel("word_2")
        #word_2.setFont(QtGui.QFont(families[0]))
        word_2.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; padding-left: 16px; border-radius: 8px; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
        page2Layout.addItem(spacer1)
        page2Layout.setSpacing(2)
        page2Layout.addWidget(word_1)
        page2Layout.addWidget(word_2)
        addWordToDict("word3","trans")
        addWordToDict("word4word4word4","tran")

        trigger_button = QtWidgets.QPushButton("Trigger exercise")            
        #trigger_button.clicked.connect(generateExercise("I'll buy you ## to come visit me.","un billete","un barco","un coche","un billete"))    
        page2Layout.addWidget(trigger_button)

        page2.setLayout(page2Layout)
        stackedLayout.addWidget(page2)

        # Add the tabs and the stacked layout to the top-level layout
        side_layout.addLayout(tabs_layout)
        side_layout.addLayout(stackedLayout)
        side_layout.setSpacing(0)
        
        # Main grid with all stuff (exercise layout, video, subtitles)
        grid = QtWidgets.QHBoxLayout()#QGridLayout()
        grid.addWidget(self.video, 8)#addWidget(self.video)#, 0, 0)
        grid.addLayout(side_layout, 2)#, 0, 1)
        #grid.addWidget(subtitles, 1, 0, 1, 2)

        # Put grid in the window
        container = QtWidgets.QWidget()
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
    


vlcApp = QtWidgets.QApplication([])
vlcApp.setStyleSheet(global_style)

window = MainWindow()
window.show()

vlcApp.exec()