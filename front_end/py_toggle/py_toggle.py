
#import PySide6.QtWidgets as QtWidgets
#import PySide6.QtGui as QtGui
#import PySide6.QtCore as QtCore

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class PyToggle(QCheckBox):
    def __init__(
            self, 
            width = 30,
            bg_color = "#777",
            circle_color = "#DDD",
            active_color = "#21BDDF",
            animation_curve = QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)

        # set default parameters
        self.setFixedSize(width, 14)

        # colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        # create animation
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500) # time in miliseconds

        # connect state changed
        self.stateChanged.connect(self.start_transition)

    # create new set and get properties
    @Property(float)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def start_transition(self, value):
        self.animation.stop() # stop animation if running
        if value:
            self.animation.setEndValue(self.width() - 12.2)
        else:
            self.animation.setEndValue(3) 
        
        # start animation
        self.animation.start()

        print(f"Status: {self.isChecked()}")

    # set new hit areas
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        # set painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # set as no pen
        p.setPen(Qt.NoPen)

        # draw rectangle
        rect = QRect(0, 0, self.width(), self.height())

        # draw bg
        p.setBrush(QColor(self._bg_color))
        p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)

        # draw circle
        p.setBrush(QColor(self._circle_color))
        p.drawEllipse(3, 3, 10.5, 10.5)

        # check if is checked
        if not self.isChecked():
            # draw bg
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)

            # draw circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 2.8, 10.5, 10.5)
        else:
            # draw bg
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)

            # draw circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 2.8, 10.5, 10.5)

        # end draw
        p.end()