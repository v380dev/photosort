# -*- coding: utf-8 -*-

from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (QDialog, QLabel,
            QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout)

class Popup(QDialog):
    def __init__(self, message):
        super().__init__()
        self.resize(100, 100)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(30)
        self.label = QLabel(self)
        self.label.setObjectName("label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)

        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(50, 24))
        self.pushButton.setMaximumSize(QSize(90, 24))
        self.pushButton.clicked.connect(lambda: self.close())

        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setWindowTitle("Warning")
        self.label.setText(message)
        self.pushButton.setText("Ok")

        QMetaObject.connectSlotsByName(self)


    def showEvent(self, arg__1: QShowEvent) -> None:
        pass

