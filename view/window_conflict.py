# -*- coding: utf-8 -*-
import enum

class AnswerFileConflict(enum.Enum):
    not_resolved = 0
    cancel = 1
    skip = 2
    duplicate = 3
    replace = 4
    rename = 5


from functools import partial

from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtWidgets import (QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout)

from model.service import Service

class WindowConflict(QDialog):
    def __init__(self, service: Service):
        super().__init__()
        self.service = service
        self.input_name_photo = ""
        self.new_name_photo = ""
        self.name_target = ""
        self.type_answer = AnswerFileConflict.not_resolved

        self.setObjectName("file_conflict")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(346, 332)

        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_1 = QLabel(self)
        self.label_1.setObjectName("label")
        self.label_1.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.label_1)

        self.label_2 = QLabel(self)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(self.verticalSpacer)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 5, -1, 5)

        self.check_box_select_new_name = QCheckBox(self)
        self.check_box_select_new_name.setObjectName("checkBox_2")

        self.verticalLayout.addWidget(self.check_box_select_new_name)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line_edit_new_name = QLineEdit(self)
        self.line_edit_new_name.setObjectName("lineEdit")
        self.line_edit_new_name.setMinimumSize(QSize(242, 0))
        self.line_edit_new_name.setText("")

        self.horizontalLayout_2.addWidget(self.line_edit_new_name)

        self.btn_reset = QPushButton(self)
        self.btn_reset.setObjectName("pushButton")
        self.btn_reset.setMinimumSize(QSize(80, 0))
        self.btn_reset.setMaximumSize(QSize(80, 16777215))
        self.btn_reset.clicked.connect(lambda: self.line_edit_new_name.clear())

        self.horizontalLayout_2.addWidget(self.btn_reset)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.check_box_appply_to_all = QCheckBox(self)
        self.check_box_appply_to_all.setObjectName("checkBox")

        self.verticalLayout_2.addWidget(self.check_box_appply_to_all)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.btn_skip = QPushButton(self)
        self.btn_skip.setObjectName("pushButton_3")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_skip.sizePolicy().hasHeightForWidth())
        self.btn_skip.setSizePolicy(sizePolicy)
        self.btn_skip.setMinimumSize(QSize(80, 50))
        self.btn_skip.setMaximumSize(QSize(80, 50))
        self.btn_skip.clicked.connect(self.do_btn_skip)

        self.horizontalLayout.addWidget(self.btn_skip)

        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setObjectName("pushButton_2")
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)
        self.btn_cancel.setMinimumSize(QSize(80, 50))
        self.btn_cancel.setMaximumSize(QSize(80, 50))
        self.btn_cancel.clicked.connect(self.do_btn_cancel)

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.btn_duplicate = QPushButton(self)
        self.btn_duplicate.setObjectName("pushButton_4")
        sizePolicy.setHeightForWidth(self.btn_duplicate.sizePolicy().hasHeightForWidth())
        self.btn_duplicate.setSizePolicy(sizePolicy)
        self.btn_duplicate.setMinimumSize(QSize(80, 50))
        self.btn_duplicate.setMaximumSize(QSize(80, 50))
        self.btn_duplicate.clicked.connect(self.do_btn_duplicate)

        self.horizontalLayout.addWidget(self.btn_duplicate)

        self.btn_replace = QPushButton(self)
        self.btn_replace.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.btn_replace.sizePolicy().hasHeightForWidth())
        self.btn_replace.setSizePolicy(sizePolicy)
        self.btn_replace.setMinimumSize(QSize(80, 50))
        self.btn_replace.setMaximumSize(QSize(80, 50))
        self.btn_replace.clicked.connect(self.do_btn_replace)

        self.horizontalLayout.addWidget(self.btn_replace)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi()

        enable_slot = partial(self.enable_mod, self.check_box_select_new_name)
        disable_slot = partial(self.disable_mod, self.check_box_select_new_name)
        self.check_box_select_new_name.stateChanged.connect(lambda x: enable_slot() if x else disable_slot())
        self.check_box_select_new_name.toggled.connect(
            lambda checked: checked and self.check_box_appply_to_all.setChecked(False))
        self.check_box_appply_to_all.toggled.connect(
            lambda checked: checked and self.check_box_select_new_name.setChecked(False))


        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle("conflict file")
        self.label_1.setText(f"Replace file: \"{self.input_name_photo}\"?")
        self.label_2.setText(f"An older file with the same name\nalredy exists in \"{self.name_target}\"")
        self.label_3.setText("Replacing it will overwrite its content")
        self.check_box_select_new_name.setText("Select new name for the destination")
        self.btn_reset.setText("Reset")
        self.check_box_appply_to_all.setText("Apply this action to all files")
        self.btn_skip.setText("Skip")
        self.btn_cancel.setText("Cancel")
        self.btn_duplicate.setText("Duplicate")
        self.btn_replace.setText("Replace")


    def set_photo_target_names(self, name_photo, name_target):
        self.input_name_photo = name_photo
        self.name_target = name_target
        self.retranslateUi()

    def do_btn_skip(self):
        self.close()
        self.type_answer = AnswerFileConflict.skip

    def do_btn_cancel(self):
        self.close()
        self.type_answer = AnswerFileConflict.cancel

    def do_btn_replace(self):
        if not self.check_box_select_new_name.isChecked():
            self.close()
            self.type_answer = AnswerFileConflict.replace
        else:
            print("self.line_edit_new_name.text()=",self.line_edit_new_name.text())
            if self.line_edit_new_name.text():
                self.close()
                self.type_answer = AnswerFileConflict.rename
                self.new_name_photo=self.line_edit_new_name.text()

    def do_btn_duplicate(self):
        self.close()
        self.type_answer = AnswerFileConflict.duplicate

    def enable_mod(self, checkbox):
        self.btn_replace.setText("Rename")
        self.btn_replace.update()

    def disable_mod(self, checkbox):
        self.btn_replace.setText("Replace")
        self.btn_replace.update()
