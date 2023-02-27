# -*- coding: utf-8 -*-

from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QSpacerItem)


class About(QDialog):
    def __init__(self, version):
        super().__init__()
        self.version=version
        self.setWindowTitle("About")
        self.setObjectName("about")
        self.resize(450, 250)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_title = QLabel(self)
        self.label_title.setObjectName("label_title")
        self.label_title.setMinimumSize(QSize(20, 0))
        font = QFont()
        font.setPointSize(12)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_title)

        self.label_text_body = QLabel(self)
        self.label_text_body.setObjectName("label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_text_body.sizePolicy().hasHeightForWidth())
        self.label_text_body.setSizePolicy(sizePolicy)
        self.label_text_body.setMaximumSize(QSize(500, 16777215))
        self.label_text_body.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_text_body)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.push_button = QPushButton(self)
        self.push_button.setObjectName("push_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.push_button.sizePolicy().hasHeightForWidth())
        self.push_button.setSizePolicy(sizePolicy1)
        self.push_button.setLayoutDirection(Qt.LeftToRight)
        self.push_button.clicked.connect(lambda: self.close())

        self.horizontalLayout.addWidget(self.push_button)
        self.verticalSpacer = QSpacerItem(77, 70, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.set_text()

        QMetaObject.connectSlotsByName(self)


    def set_text(self):
        self.label_title.setText("Photosort")
        self.label_text_body.setText(f"""
Develop in february 2023\nversion {self.version}\n\nMaidannyk Vadym""")
        self.push_button.setText("Close")
