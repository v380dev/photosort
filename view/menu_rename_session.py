# -*- coding: utf-8 -*-

from PySide6.QtCore import QMetaObject, QSize
from PySide6.QtWidgets import (QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout)

from model.service import Service


class RenameSession(QDialog):
    def __init__(self, service: Service):
        super().__init__()
        self.service = service
        self.setWindowTitle("Rename session")
        self.resize(220, 120)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)

        self.label_line_edit = QLabel(self)
        self.label_line_edit.setObjectName("label")
        self.label_line_edit.setText("Enter new session name:")
        self.line_edit = QLineEdit(self)
        self.line_edit.setObjectName("new_name")
        self.vertical_spacer_line_button = QSpacerItem(77, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(200, 30))
        self.pushButton.setMaximumSize(QSize(200, 16777215))
        self.pushButton.setText("Rename")
        self.pushButton.clicked.connect(lambda: self.rename_session(self.line_edit.text()))

        self.verticalLayout.addWidget(self.label_line_edit)
        self.verticalLayout.addWidget(self.line_edit)
        self.verticalLayout.addItem(self.vertical_spacer_line_button)
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        QMetaObject.connectSlotsByName(self)


    def rename_session(self, new_name):
        if  new_name:
            self.service.rename_current_session(new_name)
            self.service.update_service()
            self.line_edit.clear()
            self.close()
