
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import vlc
import sys
from datetime import timedelta
from os import path
from Video import Video
import re
import random
from cefr_to_zipf import cefr_to_zipf_func
import json
from deep_translator import GoogleTranslator

#### START
from py_toggle import PyToggle

def hex2QColor(c):
    """Convert Hex color to QColor"""
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)

class HintMessageBox(QtWidgets.QMessageBox):
    def __init__(self):
        super().__init__()
        
        def mouseClickEvent(self, event):
            self.close()

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)

        self.activateWindow()
        self.setGeometry(960, 78, 200, 100)
        self.setStyleSheet("QDialog {background-color: #1E1E1E; border: 2px solid; border-radius: 5px; border-color: #121212;}")

        self.backgroundColor = hex2QColor("1E1E1E")
        self.foregroundColor = hex2QColor("1E1E1E")
        self.borderRadius = 5
        def paintEvent(self, event):
            # get current window size
            s = self.size()
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
            qp.setPen(self.foregroundColor)
            qp.setBrush(self.backgroundColor)
            qp.drawRoundedRect(0, 0, s.width(), s.height(),
                            self.borderRadius, self.borderRadius)
            qp.end()
#### END

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LangFlix")
        self.setWindowIcon(QtGui.QIcon('Icons/logo.png'))
        self.setMinimumSize(QtCore.QSize(600, 300))
        self.setStyleSheet("""background-color: #171717;""")
        
        id1 = QtGui.QFontDatabase.addApplicationFont(path.join("front_end", "Fonts", "Quicksand-SemiBold.ttf"))
        id2 = QtGui.QFontDatabase.addApplicationFont(path.join("front_end", "Fonts", "Quicksand-LightItalic.ttf"))
        id3 = QtGui.QFontDatabase.addApplicationFont(path.join("front_end", "Fonts", "Quicksand-Medium.ttf"))
        if id1 < 0 or id2 < 0 or id3 < 0: 
            print("Error with adding font")
        families = []
        for id in [id1, id2, id3]: families.append(QtGui.QFontDatabase.applicationFontFamilies(id)) 

        # create video window  
        episode = 'fr_ep1'
        self.video = Video(episode = episode) # video screen + player button toolbar
        self.video.videoEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, lambda x: react_to_time_change(self.video.ind_to_stop_at_stack)) 
        
        translator = GoogleTranslator(source=episode[:2], target='en')
        self.appIsOn = True

        def switchAppOff():
            if self.video.appOnToggle.isChecked():
                self.appIsOn = True
                self.video.appOnToggle.setStyleSheet("""QPushButton
                                      {background-color: lightblue; 
                                       color: white;
                                       border-radius: 6px;
                                       border: 1px solid;
                                       border-style: solid;
                                       font-weight: 750;}""")
                self.video.videoEventManager.event_detach(vlc.EventType.MediaPlayerPositionChanged)
                self.video.videoEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, lambda x: react_to_time_change(self.video.ind_to_stop_at_stack)) 
                self.video.cue_app_on.emit()
            else:
                self.appIsOn = False
                self.video.appOnToggle.setStyleSheet("""QPushButton
                                      {background-color: grey; 
                                       color: white;
                                       border-radius: 6px;
                                       border: 1px solid;
                                       border-style: solid;
                                       font-weight: 750;}""")
                self.video.videoEventManager.event_detach(vlc.EventType.MediaPlayerPositionChanged)
                self.video.videoEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, lambda x: react_to_time_change_LangFlix_Off(self.video.ind_to_stop_at_stack)) 
                self.video.cue_app_off.emit()
        self.video.appOnToggle.clicked.connect(switchAppOff)
        

        # Styling exercise text
        exercise_text = QtWidgets.QLabel("What do you think is going to be said \nnext?")
        exercise_text.setWordWrap(True)
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
                        {image: url(Icons/RadioButton.png); width: 14px; height: 14px;}
                 '''
        style2 =  '''QRadioButton 
                        {padding-left: 12px; color: #D9D9D9; font-weight: 700; font-size: 12px; background-color: #1E1E1E;}
                    QRadioButton::indicator::unchecked
                        {border-radius: 6px; border: 1.5px solid; width: 9px; height: 9px; border-color: black;}
                    QRadioButton::indicator::checked
                        {image: url(Icons/RadioButton.png); width: 13px; height: 13px;}
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
        #### START
        cor_incor_icon.setFixedSize(16,16)
        cor_incor_icon.setScaledContents(True)
        #### END
        #QtGui.QIcon(path.join("front_end", "tab_image.png"))
        cor_incor_layout = QtWidgets.QHBoxLayout()
        cor_incor_layout.setAlignment(QtCore.Qt.AlignCenter)
        cor_incor_layout.addWidget(cor_incor_icon)
        cor_incor_layout.addWidget(cor_incor_text)
        
        self.correct_word = ''
        self.answer_opt_transl = {}
        # Function to check if the answer is correct
        def checkAnswer():
            cur_checked = '_'
            is_correct = 0
            for rb, word in [[r_button1,rb_text1], [r_button2,rb_text2], [r_button3,rb_text3]]:
                if rb.isChecked():
                    cur_checked = word.text()
                if cur_checked == self.correct_word:
                    is_correct = 1
                    cor_incor_text.setText("Great, correct!")
                    pixmap = QtGui.QPixmap(path.join("front_end", "correct.png"))
                    cor_incor_icon.setPixmap(pixmap)
                    cor_incor_icon.setHidden(False)
                    buttons_stackedLayout.setCurrentIndex(1)
                    addWordToDict(self.correct_word, self.answer_opt_transl[self.correct_word])
                    rb.setStyleSheet('''QRadioButton 
                                            {padding-left: 40px; color: #00D1FF; font-weight: 700; font-size: 15px; background-color: #1E1E1E;}
                                        QRadioButton::indicator::unchecked
                                            {border-radius: 7px; border: 1.5px solid; width: 10px; height: 10px; border-color: black;}
                                        QRadioButton::indicator::checked
                                            {image: url(Icons/RadioButton.png); width: 14px; height: 14px;}
                                    ''')
                    break
                else: 
                    is_correct = 0
                    cor_incor_text.setText("Incorrect, sorry")
                    pixmap = QtGui.QPixmap(path.join("front_end", "incorrect.png"))
                    cor_incor_icon.setPixmap(pixmap)
                    cor_incor_icon.setHidden(False)
            buttons_stackedLayout.setCurrentIndex(1)
            rb_text1.setText(rb_text1.text() + ' = ' + self.answer_opt_transl[rb_text1.text()])
            rb_text2.setText(rb_text2.text() + ' = ' + self.answer_opt_transl[rb_text2.text()])
            rb_text3.setText(rb_text3.text() + ' = ' + self.answer_opt_transl[rb_text3.text()])
            self.video.num_correct_ex.append(is_correct)
            self.video.adjust_difficulty()
            self.video.choose_ex_ind(self.video.cur_ex_ind)
        submit_button.clicked.connect(checkAnswer)                             


        self.skip_num = 3 # Number of skips                                                      
        # Styling Skip button
        skip_button = QtWidgets.QPushButton("Skip (" + str(self.skip_num) + ")")
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
            if self.skip_num:
                self.skip_num -= 1
                skip_button.setText("Skip (" + str(self.skip_num) + ")")
                switchToDict()
                hideDictionary()
                buttons_stackedLayout.setCurrentIndex(0)
                exercise_tab.setHidden(True)
                self.video.play_button.setEnabled(True)
                self.video.player.play()
                self.video.choose_ex_ind(self.video.cur_ex_ind)
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
            hideDictionary()
            cor_incor_text.setText("") #hide (in)correct message
            cor_incor_icon.setHidden(True)
            buttons_stackedLayout.setCurrentIndex(0)
            exercise_tab.setHidden(True)
            self.video.play_button.setEnabled(True)
            self.video.player.play()
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

        self.dict_hide_setting = False
        self.dual_subs_setting = False

        def hideDictionary():
            if self.dict_hide_setting or not self.appIsOn:
                if grid.count() == 2:
                    grid.removeItem(side_layout)
                    self.showLayoutChildren(layout = side_layout, show = False)
                settings_button.setHidden(False)
            elif not self.dict_hide_setting or self.appIsOn:
                if grid.count() == 1:
                    grid.addItem(side_layout)
                switchToExercise()
                exercise_tab.setHidden(True)
                dictionary_tab.setHidden(False)
                settings_button.setHidden(False)
                switchToDict()
        
        self.video.cue_app_on.connect(hideDictionary)
        self.video.cue_app_off.connect(hideDictionary)

        # Functions for switching between tabs
        def switchToDict():
            #dictionary_tab.moveToThread(tabs_layout.thread())
            stackedLayout.setCurrentIndex(1)
            dictionary_tab.setStyleSheet('QPushButton {border: 0px; color: white; font-weight: 800; font-size: 16px; image: url("Icons/tab_image1.png"); text-align: center; background-position: center right;}')
            exercise_tab.setStyleSheet('QPushButton {border: 0px; color: #A7A7A7; font-weight: 800; font-size: 16px;} QPushButton::hover {color: #CACACA;}')
        
        def switchToExercise():
            #stackedLayout.moveToThread(self.thread())
            if grid.count() == 1:
                grid.addItem(side_layout)
            stackedLayout.setCurrentIndex(0)
            exercise_tab.setHidden(False)
            exercise_tab.setVisible(True)
            exercise_tab.setStyleSheet('QPushButton {border: 0px; color: white; font-weight: 800; font-size: 16px; image: url("Icons/tab_image2.png"); text-align: center; background-position: center left;}')
            dictionary_tab.setStyleSheet('QPushButton {border: 0px; color: #A7A7A7; font-weight: 800; font-size: 16px;} QPushButton::hover {color: #CACACA;}')

        # Create and connect tabs to switch between pages
        dictionary_tab = QtWidgets.QPushButton("  Dictionary")
        #dictionary_tab.setFont(QtGui.QFont(families[0]))
        dictionary_tab.setStyleSheet('''QPushButton 
                                        {border: 0px; 
                                        color: white; 
                                        font-weight: 800; 
                                        font-size: 16px; 
                                        image: url("Icons/tab_image1.png"); 
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
                                        image: url("Icons/tab_image2.png"); 
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


        #### START
        settings_button = QtWidgets.QPushButton('')
        settings_button.setStyleSheet('''QPushButton 
                                    {border: 0px; 
                                    width: 20px;
                                    image: url("Icons/settings.png");} 
                                    QPushButton::hover
                                    {image: url("Icons/settings_hover.png");
                                }''')
        
        # Create text of the settings
        setting1Header = QtWidgets.QLabel('Hide dictionary')
        setting1Header.setStyleSheet('QLabel {padding-left: 10px; color: #FEFEFE; font-size: 12px; font-weight: 780; background-color: #1E1E1E;}')
        setting1Text = QtWidgets.QLabel('Watch video in full screen with no dictionary')
        setting1Text.setStyleSheet('QLabel {padding-left: 10px; padding-right: 23px; color: #D9D9D9; font-size: 12px; font-weight: 700; background-color: #1E1E1E;}')
        setting2Header = QtWidgets.QLabel('Double subtitles')
        setting2Header.setStyleSheet('QLabel {padding-left: 10px; color: #FEFEFE; font-size: 12px; font-weight: 780; background-color: #1E1E1E;}')
        setting2Text = QtWidgets.QLabel('Show subtitles in both English and your\nlanguage')
        setting2Text.setStyleSheet('QLabel {padding-left: 10px; color: #D9D9D9; font-size: 12px; font-weight: 700; background-color: #1E1E1E;}')
        setting3Header = QtWidgets.QLabel('Translation in dictionary')
        setting3Header.setStyleSheet('QLabel {padding-left: 10px; color: #FEFEFE; font-size: 12px; font-weight: 780; background-color: #1E1E1E;}')
        # Hovering options buttons for settings
        option_hover = QtWidgets.QRadioButton('On hover')
        option_hover.setStyleSheet(style2)
        option_hover.setChecked(True)
        option_always = QtWidgets.QRadioButton('Always')
        option_always.setStyleSheet(style2)
        def setHover():
            self.display_type = "Hover"
        def setAlways():
            self.display_type = "Always"
        option_hover.clicked.connect(setHover)
        option_always.clicked.connect(setAlways)
        # Toggles for settings
        toggle1 = PyToggle()
        toggle1.setStyleSheet('QCheckBox {padding-right: 10px;}')
        toggle2 = PyToggle()
        toggle2.setStyleSheet('QCheckBox {padding-right: 10px;}')
        def hideDict():
            if toggle1.checkState() == QtCore.Qt.Checked:
                self.dict_hide_setting = True
            else:
                self.dict_hide_setting = False
            hideDictionary()

        def setDoubleSubs():
            if toggle2.checkState() == QtCore.Qt.Checked:
                self.video.subs_are_dual = True
            else:
                self.video.subs_are_dual = False
            self.video.set_subtitles()

        toggle1.clicked.connect(hideDict)
        toggle2.clicked.connect(setDoubleSubs)
        # Add all settings components in a layout
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Plain)
        separator.setStyleSheet('QFrame {color: #252525; background-color: #1E1E1E;}')
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(QtWidgets.QFrame.HLine)
        separator2.setFrameShadow(QtWidgets.QFrame.Plain)
        separator2.setStyleSheet('QFrame {color: #252525; background-color: #1E1E1E;}')
        setting1_layout = QtWidgets.QHBoxLayout()
        setting1_layout.setContentsMargins(0,0,12,0)
        setting1_layout.addWidget(setting1Header)
        setting1_layout.addWidget(toggle1)
        setting2_layout = QtWidgets.QHBoxLayout()
        setting2_layout.setContentsMargins(0,0,12,0)
        setting2_layout.addWidget(setting2Header)
        setting2_layout.addWidget(toggle2)
        settingsScreen = QtWidgets.QVBoxLayout()
        settingsScreen.setContentsMargins(2,0,2,0)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 12, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settingsScreen.addLayout(setting1_layout)
        settingsScreen.addWidget(setting1Text)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settingsScreen.addWidget(separator)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settingsScreen.addLayout(setting2_layout)
        settingsScreen.addWidget(setting2Text)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settingsScreen.addWidget(separator2)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settingsScreen.addWidget(setting3Header)
        settingsScreen.addWidget(option_hover)
        settingsScreen.addWidget(option_always)
        settingsScreen.addItem(QtWidgets.QSpacerItem(2, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        settings = SettingsDialog(self)
        settings.setLayout(settingsScreen)
        self.opened = True
        def showSettings():
            if self.opened:
                settings.show()
                self.opened = False
            else:
                settings.hide()
                self.opened = True
        settings_button.clicked.connect(showSettings)
        tabs_layout = QtWidgets.QHBoxLayout()
        tabs_layout.addWidget(dictionary_tab, alignment=QtCore.Qt.AlignLeft)
        tabs_layout.addWidget(exercise_tab, alignment=QtCore.Qt.AlignLeft)
        tabs_layout.addWidget(settings_button, alignment=QtCore.Qt.AlignRight)    
        tabs_layout.setContentsMargins(0,0,15,0)
        tabs_layout.setSpacing(0)
        #### END

        # Create side-menu layout that will contain tabs and stackedLayout
        side_layout = QtWidgets.QVBoxLayout()
        # Create stacked layout to switch between tabs
        stackedLayout = QtWidgets.QStackedLayout()
        
        # Function to generate a new exercise
        def generateExercise(sentence, word1, word2, word3, cor_word, ex_type = 3):
            if ex_type == 3:
                exercise_text.setText("What do you think is going to be said next? Pick a word that fits the sentence below best.")
                exercise_sentence.setText('"' + sentence + '"')
            elif ex_type ==1:
                exercise_text.setText("What is the translation of the highlighted word?")
                exercise_sentence.setText("")
            rb_text1.setText(word1)
            rb_text2.setText(word2)
            rb_text3.setText(word3)
            self.correct_word = cor_word

        # connect the cue exercise signal to the switchToExercise function, because they happen in different threads
        self.video.cue_ex_sig.connect(switchToExercise)

        # Create the exercise page       
        page1 = QtWidgets.QWidget()
        page1.setFixedWidth(350)
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

        self.display_type = 'Hover'

        # Function to add a new word to dictionary
        def addWordToDict(word, translation):
            row = QtWidgets.QHBoxLayout()
            new_word = QtWidgets.QLabel(word)
            new_word.setMouseTracking(True)
            new_word.setFont(QtGui.QFont(families[0]))
            ###
            new_word.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; padding-left: 16px; border-top-left-radius: 8px; border-bottom-left-radius: 8px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')
            ###
            row.setAlignment(new_word, QtCore.Qt.AlignCenter)
            equals = QtWidgets.QLabel("=")
            equals.setObjectName('equals')
            ###
            equals.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; height: 30; color: #CACACA; font-weight: 700; font-size: 15px; background-color: #171717;}')
            ###  
            size3 = (24, 45)
            ###
            equals.setFixedSize(*size3)
            ###
            equals.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum,  QtWidgets.QSizePolicy.Policy.Fixed)
            ###
            equals.setAlignment(QtCore.Qt.AlignCenter)
            ###
            row.setAlignment(equals, QtCore.Qt.AlignCenter)
            word_translation = QtWidgets.QLabel(translation)
            ###
            word_translation.setFont(QtGui.QFont(families[0])) 
            ###
            word_translation.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-top-left-radius: 0px; border-bottom-left-radius: 0px; border-top-right-radius: 8px; border-bottom-right-radius: 8px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')
            word_translation.setBuddy(equals)
            
            ###
            word_translation.installEventFilter(self)
            row.setAlignment(word_translation, QtCore.Qt.AlignCenter)
            row.addWidget(new_word)
            row.addWidget(equals)
            row.addWidget(word_translation)
            row.setSpacing(0)
            page2Layout.addLayout(row)

        # Create the dictionary page
        page2 = QtWidgets.QWidget()
        page2.setFixedWidth(350)
        page2.setObjectName("page2")
        page2.setStyleSheet('#page2 {border: 2px solid; border-color: #121212; border-radius: 3px; background-color: #1E1E1E;}')
        page2Layout = QtWidgets.QVBoxLayout()
        page2Layout.setAlignment(QtCore.Qt.AlignTop)
        spacer1 = QtWidgets.QSpacerItem(2, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        page2Layout.addItem(spacer1)
        page2Layout.setSpacing(2)
        page2.setLayout(page2Layout)
        stackedLayout.addWidget(page2)

        # Add the tabs and the stacked layout to the side layout
        side_layout.addLayout(tabs_layout)
        side_layout.addLayout(stackedLayout)
        side_layout.setSpacing(0)
        
        # Main grid with all stuff (side layout, video, subtitles)
        grid = QtWidgets.QHBoxLayout()
        grid.addWidget(self.video, 8)
        grid.addLayout(side_layout, 2)

        # Put the grid in a container
        vidWindow = QtWidgets.QWidget()
        vidWindow.setLayout(grid)

        # Create choosing CEFR level window
        levelsWindow = QtWidgets.QWidget()
        levelsWindow.setStyleSheet("""background-color: #171717;""")
        levelsLayout = QtWidgets.QVBoxLayout()
        levelsLayout.setAlignment(QtCore.Qt.AlignCenter)
        levelsWidget = QtWidgets.QWidget()
        levelsWidget.width = 350
        levelsWidget.setSizePolicy( QtWidgets.QSizePolicy.Policy.Fixed,  QtWidgets.QSizePolicy.Policy.Expanding)
        levelsWidget.setLayout(levelsLayout)
        final_levelsLayout = QtWidgets.QVBoxLayout()
        final_levelsLayout.setAlignment(QtCore.Qt.AlignCenter)
        final_levelsLayout.addWidget(levelsWidget)
        logo = QtWidgets.QLabel()
        pixmap3 = QtGui.QPixmap('Icons/logo.png')
        #### START
        logo.setFixedSize(50,50)
        logo.setScaledContents(True)
        #### END
        logo.setPixmap(pixmap3)
        #logo.setAlignment(QtCore.Qt.AlignCenter)
        welcomeText = QtWidgets.QLabel(" Welcome to LangFlix –")
        welcomeText.setAlignment(QtCore.Qt.AlignCenter)
        welcomeText.setStyleSheet('QLabel {color: #CACACA; font-size: 22px; font-weight: 650; background-color: #171717;}')
        welcomeText2 = QtWidgets.QLabel("app for learning new vocabulary \nwhile watching shows!")
        welcomeText2.setAlignment(QtCore.Qt.AlignCenter)
        welcomeText2.setStyleSheet('QLabel {color: #CACACA; font-size: 16px; font-weight: 650; background-color: #171717;}')
        levelsText = QtWidgets.QLabel("Choose your current language level:")
        #levelsText.setFont(QtGui.QFont(families[0]))
        levelsText.setStyleSheet('QLabel {color: #CACACA; font-size: 16px; font-weight: 780; background-color: #171717;}')

        # Language level buttons
        a1 = QtWidgets.QPushButton("A1")
        a2 = QtWidgets.QPushButton("A2")
        b1 = QtWidgets.QPushButton("B1")
        b2 = QtWidgets.QPushButton("B2")
        c1 = QtWidgets.QPushButton("C1")
        c2 = QtWidgets.QPushButton("C2")
        btn_grp = QtWidgets.QButtonGroup()
        btn_grp.setExclusive(True)
        
        # Function for changing level buttons color when pressed
        def toggle():
            for btn in btn_grp.buttons(): 
                btn.setStyleSheet('''QPushButton 
                                        {border: 0px;
                                        border-radius: 6px; 
                                        color: 171717; 
                                        background-color: #CACACA;
                                        font-weight: 800; 
                                        font-size: 16px; 
                                        height: 32px; 
                                        text-align: center;} 
                                    QPushButton::hover
                                       {background-color: #76E6FF;}
                                    QPushButton::pressed
                                       {color: white;
                                        background-color: #0045AD;
                                    }''')
                btn.setChecked(False)
            btn_grp.checkedButton().setStyleSheet('''QPushButton 
                                                        {border: 0px;
                                                        border-radius: 6px; 
                                                        color: white; 
                                                        background-color: #0045AD;
                                                        font-weight: 800; 
                                                        font-size: 16px; 
                                                        height: 32px; 
                                                        text-align: center;
                                                    }''')
        # Styling level buttons
        for level in [a1,a2,b1,b2,c1,c2]:
            btn_grp.addButton(level)
            level.setStyleSheet('''QPushButton 
                                        {border: 0px;
                                        border-radius: 6px; 
                                        color: 171717; 
                                        background-color: #CACACA;
                                        font-weight: 800; 
                                        font-size: 16px; 
                                        height: 32px; 
                                        text-align: center;} 
                                    QPushButton::hover
                                       {background-color: #76E6FF;}
                                    QPushButton::pressed
                                       {color: white;
                                        background-color: #0045AD;
                                    }''')
            level.clicked.connect(toggle)
            level.setCheckable(True)

        # Button for proceeding to the video
        setLevel_button = QtWidgets.QPushButton("Apply")
        setLevel_button.setStyleSheet("""QPushButton
                                      {background-color: #0043A8; 
                                       color: #00D1FF;
                                       border-radius: 13px;
                                       border: 1px solid;
                                       border-color: #0043A8;
                                       height: 25px;
                                       width: 84px;
                                       font-weight: 750;}
                                       QPushButton::hover
                                       {background-color: #003585;
                                        border-color: #003585;
                                    }""")
        setLevel_button.setSizePolicy( QtWidgets.QSizePolicy.Policy.Fixed,  QtWidgets.QSizePolicy.Policy.Minimum)
        self.CEFRlevel = '' # variable to store the current user's level
        def switchToMain():
            levelsToMain_stackedLayout.setCurrentIndex(1)
            self.CEFRlevel = [btn.text() for btn in btn_grp.buttons() if btn.isChecked()]
            self.video.set_zipf(cefr_to_zipf_func(self.CEFRlevel[0]))
            
        setLevel_button.clicked.connect(switchToMain)
        
    
        # Wrapping the levels page in layouts
        a_layout = QtWidgets.QHBoxLayout()
        b_layout = QtWidgets.QHBoxLayout()
        c_layout = QtWidgets.QHBoxLayout()
        a_layout.addWidget(a1)
        a_layout.addWidget(a2)
        a_layout.setContentsMargins(89,0,89,0)
        b_layout.addWidget(b1)
        b_layout.addWidget(b2)
        b_layout.setContentsMargins(89,0,89,0)
        c_layout.addWidget(c1)
        c_layout.addWidget(c2)
        c_layout.setContentsMargins(89,0,89,0)
        #### START
        levelsLayout.addWidget(logo, alignment=QtCore.Qt.AlignCenter)
        #### END
        #levelsLayout.addWidget(logo)
        levelsLayout.addWidget(welcomeText)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addWidget(welcomeText2)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addWidget(levelsText)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addLayout(a_layout)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 6, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addLayout(b_layout)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 6, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addLayout(c_layout)
        levelsLayout.addItem(QtWidgets.QSpacerItem(2, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        levelsLayout.addWidget(setLevel_button, alignment=QtCore.Qt.AlignCenter)

        # Put levels page and video page in a container 
        levelsWindow.setLayout(final_levelsLayout)     
        levelsToMain_stackedLayout = QtWidgets.QStackedLayout()
        levelsToMain_stackedLayout.addWidget(levelsWindow)
        levelsToMain_stackedLayout.addWidget(vidWindow)
        container = QtWidgets.QWidget()
        container.setLayout(levelsToMain_stackedLayout)
        self.setCentralWidget(container)

        #state of interface at start of the app
        switchToDict()
        exercise_tab.setHidden(True)

        # function for triggering events connected to video time
        def react_to_time_change(indices):
            #update slider position
            self.video.time_slider.setValue(self.video.player.get_position()*1000)
            # update time text
            total_time = str(timedelta(microseconds = self.video.player.get_length()*1000)).split('.')[0]
            cur_time = str(timedelta(microseconds = self.video.player.get_time()*1000)).split('.')[0]
            self.video.time_text.setText(f'{cur_time}/{total_time}')
            try:
                ind = indices[0]
                if self.video.cur_ex_ind % 3 != 0: ind -= 1 #pause one scene prior to target to ask question about the future if exercise is type 3
            except:
                return 
            #pause video at target subtitle
            sub_start = self.video.subs_cur[ind].start
            sub_time = timedelta(hours=sub_start.hours, minutes=sub_start.minutes, 
                                seconds=sub_start.seconds, microseconds=sub_start.milliseconds * 1000)   
            player_time = timedelta(microseconds=self.video.player.get_time()*1000)
            up_time_bound = sub_time + timedelta(microseconds= 10**6)
            #switch to exercise
            if player_time >= sub_time and player_time <= up_time_bound:
                self.video.player.pause()
                self.video.play_button.setEnabled(False)
                ex_type = 1
                if self.video.cur_ex_ind % 3 != 0: 
                    ind += 1 # if it is exercise type 3 increment the index to target the future subtitle
                    ex_type = 3
                target_word_data = self.video.get_word_data_from_sub(ind)[0]
                word_options = target_word_data[3][1:-1].split(', ') #list of answer options
                if len(word_options) == 1: word_options.append('')
                sentence = re.sub(r''+target_word_data[0], '_____', self.video.subs_cur[ind].text) # sentence in English
                #words = [target_word_data[1]] 
                word_options.append(target_word_data[1])
                random.shuffle(word_options) # shuffle word order
                for i in range(len(word_options)):
                    if episode[:2] == 'de':
                        word_options[i] = word_options[i].capitalize()
                    self.answer_opt_transl[word_options[i]] = translator.translate(word_options[i])
                self.video.cur_ex_ind+=1
                #compute one exercise in advance
                self.video.ind_to_stop_at_stack.pop(0)
                #self.video.choose_ex_ind(self.video.sub_ind_for_ex[self.video.cur_ex_ind])
                generateExercise(sentence, word_options[0], word_options[1], word_options[2], target_word_data[1], ex_type)
                self.video.cue_ex_sig.emit()

        # function for triggering events connected to video time when LangFlix is off
        def react_to_time_change_LangFlix_Off(indices):
            #update slider position
            self.video.time_slider.setValue(self.video.player.get_position()*1000)
            # update time text
            total_time = str(timedelta(microseconds = self.video.player.get_length()*1000)).split('.')[0]
            cur_time = str(timedelta(microseconds = self.video.player.get_time()*1000)).split('.')[0]
            self.video.time_text.setText(f'{cur_time}/{total_time}')
            try:
                ind = indices[0]
                if self.video.cur_ex_ind % 3 != 0: ind -= 1 #pause one scene prior to target to ask question about the future if exercise is type 3
            except:
                return 
            #pause video at target subtitle
            sub_start = self.video.subs_cur[ind].start
            sub_time = timedelta(hours=sub_start.hours, minutes=sub_start.minutes, 
                                seconds=sub_start.seconds, microseconds=sub_start.milliseconds * 1000)   
            player_time = timedelta(microseconds=self.video.player.get_time()*1000)
            up_time_bound = sub_time + timedelta(microseconds= 10**6)
            #switch to exercise
            if player_time >= sub_time and player_time <= up_time_bound:
                self.video.cur_ex_ind+=1
                #compute one exercise in advance
                self.video.ind_to_stop_at_stack.pop(0)
                self.video.choose_ex_ind(self.video.cur_ex_ind)

    # function for showing and hiding screen elements
    def showLayoutChildren(self, layout, show = True):
        for i in range(layout.count()):
            if layout.itemAt(i).widget() is None:
                    self.showLayoutChildren(layout.itemAt(i).layout(), show)
            else:
                if show:
                    layout.itemAt(i).widget().show()  
                else:
                    layout.itemAt(i).widget().hide()

    # function for triggering interface events 
    def eventFilter(self, source, event):
        if self.display_type == 'Hover':
            if event.type() == QtCore.QEvent.Enter:
                source.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-top-left-radius: 0px; border-bottom-left-radius: 0px; border-top-right-radius: 8px; border-bottom-right-radius: 8px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')
                source.buddy().setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-radius: 0px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')
            elif event.type() == QtCore.QEvent.Leave:
                source.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-top-left-radius: 0px; border-bottom-left-radius: 0px; border-top-right-radius: 8px; border-bottom-right-radius: 8px; height: 30; color: #171717; font-weight: 800; font-size: 15px; background-color: #171717;}')
                source.buddy().setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-radius: 0px; height: 30; color: #171717; font-weight: 800; font-size: 15px; background-color: #171717;}')
        elif self.display_type == "Always":
            if event.type() == QtCore.QEvent.Enter or event.type() == QtCore.QEvent.Leave:
                source.setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-top-left-radius: 0px; border-bottom-left-radius: 0px; border-top-right-radius: 8px; border-bottom-right-radius: 8px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')
                source.buddy().setStyleSheet('QLabel {padding: 12px, 12px, 0px, 0px; border-radius: 0px; height: 30; color: #CACACA; font-weight: 800; font-size: 15px; background-color: #171717;}')

        return super().eventFilter(source, event)

# App initialized
vlcApp = QtWidgets.QApplication([])

window = MainWindow()
window.show()

vlcApp.exec()