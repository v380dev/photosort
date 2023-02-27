# -*- coding: utf-8 -*-

from pathlib import Path
from abc import abstractmethod

from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget, QFileDialog, QDialog)

from model.service import Service
from model.exceptions_photosort import SourceExists

from view.ui_popup import Popup


class UiEditWindow(QDialog):
    def __init__(self, service: Service):
        super().__init__()
        self.setObjectName("MainWindow")
        self.service = service
        self.new_folder: str=None

        self.resize(300, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(370, 0))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 2, 5, 5)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(1, 15, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_add_folder = QPushButton(self.centralwidget)
        self.btn_add_folder.setObjectName("btn_add_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_add_folder.sizePolicy().hasHeightForWidth())
        self.btn_add_folder.setSizePolicy(sizePolicy2)
        self.btn_add_folder.setMinimumHeight(30)
        self.btn_add_folder.clicked.connect(self.open_file_dialog)

        self.verticalLayout_2.addWidget(self.btn_add_folder)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 10, -1, -1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")

        self.combo_exclude = QComboBox(self.centralwidget)
        self.combo_exclude.setObjectName("combo_exclude")
        self.combo_exclude.addItem(None)

        self.combo_exclude.currentText()

        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.combo_exclude.sizePolicy().hasHeightForWidth())
        self.combo_exclude.setSizePolicy(sizePolicy3)
        self.combo_exclude.setMinimumSize(QSize(80, 0))

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.vertical_spacer)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.combo_exclude)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontal_spacer)

        self.btn_cancel = QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.cancel)

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.btn_ok = QPushButton(self.centralwidget)
        self.btn_ok.setObjectName("btn_ok")
        self.btn_ok.clicked.connect(self.ok)


        self.horizontalLayout.addWidget(self.btn_ok)
        self.horizontalLayout.setContentsMargins(0,0,6,0)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.btn_add_folder.setText("Add folder")
        self.label.setText("Exclude folder")
        self.btn_cancel.setText("Cancel")
        self.btn_ok.setText("Confirm")
    # retranslateUi

    def cancel(self):
        self.new_folder = None
        self.combo_exclude.setCurrentText("")
        self.close()

    @abstractmethod
    def open_file_dialog(self):
        pass

    @abstractmethod
    def ok(self):
        pass

    @abstractmethod
    def update_combo_box(self):
        pass


class UiSourceEditWindow(UiEditWindow):
    def __init__(self, service: Service):
        super().__init__(service)
        self.setWindowTitle("Edit Source Folders")
        list_sources = list(s.name for s in self.service.get_sources_by_session_id(self.service.get_current_session_id()))
        self.combo_exclude.addItems(list_sources)


    def open_file_dialog(self):
        self.new_folder = QFileDialog.getExistingDirectory(self)
        self.close()
        if self.new_folder:
            try:
                self.service.add_new_source_folder(self.new_folder)
            except SourceExists:
                message = f"{Path(self.new_folder).name}\nalready added as a resource, in this or another session"
                popup = Popup(message)
                popup.setWindowModality(Qt.WindowModality.ApplicationModal)
                popup.show()

                print(message)
            self.new_folder = None
            self.update_combo_box()


    def ok(self):
        if self.combo_exclude.currentText():
            self.service.delete_source(self.combo_exclude.currentText())
            self.update_combo_box()
        self.close()


    def update_combo_box(self):
        self.combo_exclude.clear()
        self.combo_exclude.addItem("")
        list_sources = list(s.name for s in self.service.get_sources_by_session_id(self.service.get_current_session_id()))
        self.combo_exclude.addItems(list_sources)
        self.combo_exclude.setCurrentText("")



class UiTargetEditWindow(UiEditWindow):
    def __init__(self, service: Service):
        super().__init__(service)
        self.setWindowTitle("Edit Target Folders")
        list_sources = list(t['name'] for t in self.service.get_full_targets_dict_on_session())
        self.combo_exclude.addItems(list_sources)


    def open_file_dialog(self):
        self.new_folder = QFileDialog.getExistingDirectory(self)
        self.close()
        if self.new_folder:
            self.service.add_new_target_folder(self.new_folder)
            self.new_folder = None
            self.update_combo_box()

    def ok(self):
        if self.combo_exclude.currentText():
            self.service.delete_target(self.combo_exclude.currentText())
            self.update_combo_box()
        self.close()

    def update_combo_box(self):
        self.combo_exclude.clear()
        self.combo_exclude.addItem("")
        list_targets = list(s['name'] for s in self.service.get_full_targets_dict_on_session())
        self.combo_exclude.addItems(list_targets)
        self.combo_exclude.setCurrentText("")

