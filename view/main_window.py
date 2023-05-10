# -*- coding: utf-8 -*-

from PySide6.QtGui import QAction, QPixmap, QResizeEvent, QIcon, QFont, QShortcut
from PySide6.QtCore import QMetaObject, QRect, QSize, Qt, QEvent, Signal
from PySide6.QtWidgets import (QHBoxLayout, QMainWindow,
                               QMenu, QMenuBar, QPushButton, QSizePolicy,
                               QSpacerItem, QStatusBar, QWidget, QLabel,
                               QVBoxLayout, QProgressBar, QScrollArea, QSplitter)

from model.service import Service
from model.exceptions_photosort import PhotoExistsInTarget
from view.menu_edit_folders import UiEditWindow
from view.menu_new_session import CreateSession
from view.menu_open_delete_session import OpenSession, DeleteSession
from view.menu_rename_session import RenameSession
from view.menu_about import About
from view.window_conflict import WindowConflict, AnswerFileConflict

StyleCSS = str
STYLE_SCC_SELECTED_TARGET = "background-color : #A9A9A9; color : #F5F5F5;"
STYLE_SCC_UNSELECTED_TARGET = "background-color : None"

class MainWindow(QMainWindow):
    def __init__(self,
                 service: Service,
                 window_edit_source: UiEditWindow,
                 window_edit_target: UiEditWindow,
                 window_create_new_session: CreateSession,
                 window_open_session: OpenSession,
                 window_delete_session: DeleteSession,
                 window_rename_session: RenameSession,
                 window_about: About,
                 window_conflict: WindowConflict,
                 ):
        super().__init__()
        self.service = service
        self.list_of_targets_dict = self.service.get_short_targets_dict_on_session()
        self.current_name_photo = self.service.get_current_link_photo()

        self.current_targets_id_on_photo = self.service.get_targets_on_current_photo()
        self.dict_target_buttons = {}  # {id:btn_trg, ...}

        self.window_edit_source = window_edit_source
        self.window_edit_target = window_edit_target
        self.window_create_new_session = window_create_new_session
        self.window_open_session = window_open_session
        self.window_delete_session = window_delete_session
        self.window_rename_session = window_rename_session
        self.window_about = window_about
        self.window_conflict = window_conflict

        self.resize(600, 400)

        self.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.v_layout_1 = QVBoxLayout(self.centralwidget)
        self.v_layout_1.setSpacing(1)
        self.v_layout_1.setObjectName("verticalLayout")
        self.v_layout_1.setContentsMargins(0, 0, 0, 0)

        self._img = QPixmap()
        # self._photo_label = QLabel(self.centralwidget)
        self._photo_label = QLabel()
        w = self.size().width()
        h = self.size().height()
        self._photo_label.setGeometry(QRect(0, 0, w, h))
        self._photo_label.setPixmap(self._img)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self._photo_label.sizePolicy().hasHeightForWidth())
        # self._photo_label.setMinimumSize(QSize(200, 100))
        self._photo_label.setMinimumSize(QSize(100, 50))

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumHeight(4)
        self.progress_bar.setTextVisible(False)

        self.v_layout_1.addWidget(self.progress_bar)
        # self.v_layout_1.addWidget(self._photo_label)
        self.h_layout_1_1 = QHBoxLayout()
        self.h_layout_1_1.setObjectName("horizontal_layout_1_1")
        # self.h_layout_1_1.setContentsMargins(0,1,0,3)


        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")

        self.btn_back = QPushButton(self.widget)
        self.btn_back.setObjectName("btn_back")
        # self.btn_back.setText("<")
        icon_back = QIcon(QIcon.fromTheme("go-previous"))
        self.btn_back.setIcon(icon_back)
        self.btn_back.setShortcut("Left")
        shortcut = QShortcut(Qt.SHIFT | Qt.Key_Tab, self.btn_back)
        shortcut.activated.connect(self.btn_back.click)
        # self.btn_back.setMaximumWidth(20)
        # self.btn_back.setMinimumWidth(80)
        self.btn_back.setFixedWidth(80)
        # self.btn_back.setMinimumHeight(50)
        self.btn_back.setMinimumHeight(20)
        self.btn_back.clicked.connect(self._click_button_back)

        splitter = QSplitter()
        self.v_layout_1.addWidget(splitter)
        splitter.splitterMoved.connect(self.update_main_window)
        button_widget = QWidget()

        self.h_layout_1_1.addWidget(self.btn_back)
        self.right = QScrollArea()

        self.v_layout_target_buttons = QVBoxLayout(button_widget)
        self.v_layout_target_buttons.setObjectName("v_layout_target_buttons")
        self.v_layout_target_buttons.setContentsMargins(0, 0, 0, 0)
        self.v_layout_target_buttons.setSpacing(0)

        left_widget = QWidget()
        # left_widget.setStyleSheet("background-color: grey;")
        # left_layout = QVBoxLayout()
        left_layout = QVBoxLayout(left_widget)
        # left_layout.addWidget(self._photo_label)
        left_layout.addWidget(self._photo_label)
        # left_widget.setContentsMargins(0, 0, 0, 0)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(1)
        left_layout.addStretch(0)
        self._photo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self._photo_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        left_widget.setLayout(left_layout)
        left_layout.setAlignment(Qt.Alignment.AlignTop)


        self.right.setWidget(button_widget)
        self.right.setWidgetResizable(True)
        # splitter.addWidget(self._photo_label)
        splitter.addWidget(left_widget)
        self._photo_label.setAlignment(Qt.Alignment.AlignTop)
        splitter.addWidget(self.right)
        splitter.setSizes([400, splitter.width() - 400])
        splitter.widget(0).setMinimumWidth(50)
        splitter.widget(1).setMinimumWidth(50)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        # self.h_layout_1_1.addLayout(self.h_layout_1_1_1)
        # self.horizontal_spacer_forward = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.h_layout_1_1.addItem(self.horizontal_spacer_forward)

        self.label_name_current_photo = QLabel()
        # self.label_name_current_photo.adjustSize()
        self.h_layout_1_1.addStretch()
        self.h_layout_1_1.addWidget(self.label_name_current_photo)
        self.h_layout_1_1.addStretch()


        self.btn_forward = QPushButton(self.widget)
        self.btn_forward.setObjectName("btn_forward")
        # self.btn_forward.setText(">")
        icon_forward = QIcon(QIcon.fromTheme("go-next"))
        self.btn_forward.setIcon(icon_forward)
        self.btn_forward.setShortcut("Right")
        self.btn_forward.setShortcut(Qt.Key_Tab)
        # self.btn_forward.setMaximumWidth(20)
        # self.btn_forward.setMinimumWidth(80)
        # self.btn_forward.setMaximumWidth(80)
        self.btn_forward.setFixedWidth(80)
        # self.btn_forward.setMinimumHeight(50)
        self.btn_forward.setMinimumHeight(20)
        self.btn_forward.clicked.connect(self._click_button_forward)
        # add second shortcut to step right ...
        self.act_step_right_use_space = QAction(self)
        self.act_step_right_use_space.setShortcut("Space")
        self.act_step_right_use_space.triggered.connect(self._click_button_forward)
        self.addAction(self.act_step_right_use_space)

        self.btn_forward.setShortcut(Qt.Key_Tab)
        # shortcut_tab = QShortcut(QKeySequence(Qt.Key_Tab), button_tab)
        # shortcut_tab.activated.connect(button_tab.click)

        self.h_layout_1_1.addWidget(self.btn_forward)
        self.v_layout_1.addLayout(self.h_layout_1_1)

        self.setCentralWidget(self.centralwidget)

        # menu bar
        icon_new = QIcon(QIcon.fromTheme("window-new"))
        self.act_create_new_session = QAction(self)
        self.act_create_new_session.setIcon(icon_new)
        self.act_create_new_session.setObjectName("actioncreate_new_session")
        self.act_create_new_session.triggered.connect(self._open_dialog_new_session)
        self.act_create_new_session.setText("create new session")
        self.act_create_new_session.setShortcut("Ctrl+N")

        icon_delete = QIcon(QIcon.fromTheme("edit-delete"))
        self.act_delete_session = QAction(self)
        self.act_delete_session.setIcon(icon_delete)
        self.act_delete_session.setObjectName("action_delete_session")
        self.act_delete_session.triggered.connect(self._open_dialog_to_delete_session)
        self.act_delete_session.setText("delete session")

        icon_rename = QIcon(QIcon.fromTheme("edit-find-replace"))
        self.act_rename_session = QAction(self)
        self.act_rename_session.setIcon(icon_rename)
        self.act_rename_session.setObjectName("action_rename_session")
        self.act_rename_session.triggered.connect(self._open_dialog_to_rename_session)
        self.act_rename_session.setText("rename session")

        # self.act_folders = QAction(self)
        # self.act_folders.setObjectName("actionfolders")
        # self.act_folders.setText("folders")
        # self.act_folders.setShortcut("Ctrl+F")

        icon_open = QIcon(QIcon.fromTheme("document-open"))
        self.act_open_session = QAction(self, "actionopen_session")
        self.act_open_session.setIcon(icon_open)
        self.act_open_session.triggered.connect(self._open_dialog_to_open_session)
        self.act_open_session.setText("open session")
        self.act_open_session.setShortcut("Ctrl+O")

        icon_folder = QIcon(QIcon.fromTheme("folder-open"))
        self.act_edit_source = QAction(self)
        self.act_edit_source.setIcon(icon_folder)
        self.act_edit_source.setObjectName("action_edit_source")
        self.act_edit_source.triggered.connect(self._open_source_editor)
        self.act_edit_source.setText("edit source")
        self.act_edit_source.setShortcut("Ctrl+E")

        self.act_edit_target = QAction(self)
        self.act_edit_target.setIcon(icon_folder)
        self.act_edit_target.setObjectName("action_edit_target")
        self.act_edit_target.triggered.connect(self._open_target_editor)
        self.act_edit_target.setText("edit target")
        self.act_edit_target.setShortcut("Ctrl+T")

        # self.act_language = QAction(self)
        # self.act_language.setObjectName("actionlanguage")
        # self.act_language.setText("language")
        # self.act_language.setShortcut("Ctrl+L")

        # self.act_hot_keys = QAction(self)
        # self.act_hot_keys.setObjectName("actionhot_keys")
        # self.act_hot_keys.setText("hot keys")
        # self.act_hot_keys.setShortcut("Ctrl+H")

        self.act_move_photos = QAction(self)
        # self.act_move_photos.setText("move photos")
        icon_shared = QIcon(QIcon.fromTheme("emblem-shared"))
        self.act_move_photos.setIcon(icon_shared)
        self.act_move_photos.setObjectName("action_move_photos")
        self.act_move_photos.setShortcut("Ctrl+Return")
        self.act_move_photos.triggered.connect(lambda: self.replace_photos())


        icon_exit = QIcon(QIcon.fromTheme("application-exit"))
        self.act_quit = QAction(self)
        self.act_quit.setIcon(icon_exit)
        self.act_quit.setObjectName("actionquit")
        self.act_quit.setText("quit")
        self.act_quit.setShortcut("Ctrl+Esc")
        self.act_quit.triggered.connect(lambda: self.close())

        icon_about = QIcon(QIcon.fromTheme("help-about"))
        self.act_about = QAction(self)
        self.act_about.setIcon(icon_about)
        self.act_about.setObjectName("about")
        self.act_about.setText("About")
        self.act_about.triggered.connect(self._open_about)

        self.menu_bar = QMenuBar(self)

        self.menu_bar_file = QMenu(self.menu_bar)
        self.menu_bar_file.setObjectName("menuFile")
        self.menu_bar_file.setTitle("File")
        self.menu_bar_file.addAction(self.act_create_new_session)
        self.menu_bar_file.addAction(self.act_delete_session)
        self.menu_bar_file.addAction(self.act_rename_session)
        self.menu_bar_file.addAction(self.act_open_session)
        # self.menu_bar_file.addSeparator()
        # self.menu_bar_file.addAction(self.act_edit_source)
        # self.menu_bar_file.addAction(self.act_edit_target)
        self.menu_bar_file.addSeparator()
        self.menu_bar_file.addAction(self.act_quit)

        self.menu_bar_edit = QMenu(self.menu_bar)
        self.menu_bar_edit.setObjectName("menuEdit")
        self.menu_bar_edit.setTitle("Edit")
        self.menu_bar_edit.addAction(self.act_edit_source)
        self.menu_bar_edit.addAction(self.act_edit_target)
        # self.menu_bar_edit.addAction(self.act_folders)

        # self.menu_bar_settings = QMenu(self.menu_bar)
        # self.menu_bar_settings.setObjectName("menuSettings")
        # self.menu_bar_settings.setTitle("Settings")
        # self.menu_bar_settings.addAction(self.act_language)
        # self.menu_bar_settings.addAction(self.act_hot_keys)

        self.menu_bar_help = QMenu(self.menu_bar)
        self.menu_bar_help.setObjectName("menuFile")
        self.menu_bar_help.setTitle("File")
        self.menu_bar_help.setTitle("Help")
        self.menu_bar_help.addAction(self.act_about)

        self.menu_bar.setObjectName("menubar")
        self.menu_bar.setGeometry(QRect(0, 0, 1204, 22))
        self.menu_bar.addAction(self.menu_bar_file.menuAction())
        self.menu_bar.addAction(self.menu_bar_edit.menuAction())
        self.menu_bar.addAction(self.menu_bar_help.menuAction())
        self.menu_bar.addAction(self.act_move_photos)

        self.setMenuBar(self.menu_bar)

        # self.statusbar = QStatusBar(self)
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(self)


    # First, there is a flag for deletion - True, if there are no selected in
    # the photo options where to copy (target folder), then this photo will be
    # skipped in a loop and the deletion will not occur.
    # If the user chooses Cancel in the event of a name conflict, exit
    # with this method, the current and subsequent photos will not be deleted
    # If the user chooses to skip (Skip), the photo will be marked as
    # such that it is forbidden to delete, even if there are others with this photo
    # conflicts and other options for resolving them - the photo will not be
    # deleted.
    # In all other cases, the photo is deleted from the resource folder
    def replace_photos(self):
        list_dict_photos = self.service.get_dict_photos_in_session()
        if len(list_dict_photos):
            count_progress = 0
            step_progress = int(100/len(list_dict_photos))
        for photo in list_dict_photos:
            can_delete_photo = True
            name_photo = photo['name']
            list_targets = self.service.get_targets_name_by_photo_id(photo['id'])
            if not len(list_targets): # if there are no selected options in the photo - skip it
                continue
            for name_target in list_targets:
                try:
                    self.service.copy_photo(name_photo, name_target)
                except PhotoExistsInTarget as ex:
                    self.window_conflict.set_photo_target_names(ex.photo_name, ex.target_folder)
                    conflict_resolved = False
                    while not conflict_resolved:
                        if not self.window_conflict.check_box_appply_to_all.isChecked():
                            self.window_conflict.exec_()
                        if self.window_conflict.type_answer == AnswerFileConflict.skip:
                            can_delete_photo = False
                            conflict_resolved = True
                        elif self.window_conflict.type_answer == AnswerFileConflict.cancel:
                            return
                        elif self.window_conflict.type_answer == AnswerFileConflict.replace:
                            self.service.copy_photo_without_exception_for_replace(name_photo, name_target)
                            conflict_resolved = True
                            # can_delete_photo = True
                        elif self.window_conflict.type_answer == AnswerFileConflict.duplicate:
                            new_name = self.service.generate_new_name(name_photo, name_target)
                            self.service.copy_photo(name_photo, name_target, new_name)
                            conflict_resolved = True
                            # can_delete_photo = True
                        elif self.window_conflict.type_answer == AnswerFileConflict.rename:
                            new_name = self.window_conflict.new_name_photo
                            try:
                                self.service.copy_photo(name_photo, name_target, new_name)
                                conflict_resolved = True
                                # can_delete_photo = True
                            except PhotoExistsInTarget as exc:
                                conflict_resolved = False
            if can_delete_photo:
                self.service.delete_photo(name_photo)
            self.progress_bar.setValue(count_progress)
            self.progress_bar.update()
            count_progress += step_progress
        self.progress_bar.setValue(100)
        self.update_main_window()
        self.window_conflict.check_box_appply_to_all.setChecked(False)
        self.progress_bar.setValue(0)


    def _open_source_editor(self):
        """opens a new window for editing resource folders from the 'edit source' menu"""
        self.window_edit_source.setWindowModality(Qt.WindowModality.ApplicationModal)
        # self.window_edit_source.show()
        self.window_edit_source.exec_()

    def _open_target_editor(self):
        """opens a new window for editing resource folders from the 'edit source' menu"""
        self.window_edit_target.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_edit_target.show()

    def _open_dialog_new_session(self):
        """opens from the 'edit source' menu a dialog box for entering the name of the new session"""
        self.window_create_new_session.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_create_new_session.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        self.window_create_new_session.show()

    def _open_dialog_to_open_session(self):
        self.window_open_session.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_open_session.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        self.window_open_session.show()

    def _open_dialog_to_delete_session(self):
        self.window_delete_session.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_delete_session.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        self.window_delete_session.show()

    def _open_dialog_to_rename_session(self):
        self.window_rename_session.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_rename_session.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        self.window_rename_session.show()

    def _open_about(self):
        self.window_about.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_about.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        self.window_about.show()

    def changeEvent(self, event: QEvent):
        """when there are changes in the window, an event is called,
        and the method loads the current photo, actual selected targets,
        status bar ..."""
        if event.type() == QEvent.ActivationChange:
            self.update_main_window()

    def update_main_window(self):
        self.current_targets_id_on_photo = self.service.get_targets_on_current_photo()
        self.setWindowTitle(self.service.get_current_session_name())
        self.set_photo(self.service.get_current_link_photo())
        self._update_buttons_target()
        self.current_name_photo = self.service.get_current_link_photo()
        if self.current_name_photo:
            self.label_name_current_photo.setText(self.current_name_photo)
            self.label_name_current_photo.adjustSize()
        else:
            self.label_name_current_photo.setText("")


    def resizeEvent(self, e: QResizeEvent):
        """reaction to changing the size of the main window - changing the size of the photo"""
        self.set_photo(self.service.get_current_link_photo())

    def set_photo(self, photo_name):
        if photo_name:
            self._img.load(photo_name)
            # self._img = self._get_resized_photo(self._img, self._photo_label)
            self._img = self._get_resized_photo(self._img, self._photo_label.parent())
            self._photo_label.setPixmap(self._img)
            # self._photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self._photo_label.clear()

    def _get_resized_photo(self, img: QPixmap, label: QLabel) -> QPixmap:
        """adjusts the size of the photo relative to the proportions
        of the photo itself to the proportions of the label"""
        try:
            img_w_h_proport = (img.width() / img.height())
            label_w_h_proport = (label.width() / label.height())
        except ZeroDivisionError:
            img_w_h_proport = 0
            label_w_h_proport = 0
        if img_w_h_proport > label_w_h_proport:
            return img.scaledToWidth(label.width())
        else:
            return img.scaledToHeight(label.height())

    def _click_button_back(self):
        self.current_name_photo = self.service.get_previous_link_photo()
        self._update_views_after_step()
        # self.statusbar.showMessage(self.current_name_photo)

    def _click_button_forward(self):
        self.current_name_photo = self.service.get_next_link_photo()
        self._update_views_after_step()
        # self.statusbar.showMessage(self.current_name_photo)

    def _update_views_after_step(self):
        self.current_targets_id_on_photo = self.service.get_targets_on_current_photo()
        # self.update_main_window()
        self.set_photo(self.current_name_photo)
        self._update_target_widget_style(self.current_targets_id_on_photo)
        self.label_name_current_photo.setText(self.current_name_photo)
        self.label_name_current_photo.adjustSize()
        # self.statusbar.showMessage(self.current_name_photo)

    def _update_target_widget_style(self, targets_id: list):
        self._remove_selection_targets_widget()
        self._set_selection_target_widget(targets_id)

    # StyleCSS = str
    def set_style_to_target_widget(self, target: QWidget, style: StyleCSS) -> None:
        # target.setFont(QFont("Arial", 10))
        target.setStyleSheet(style)

    def _remove_selection_targets_widget(self):
        for dict in self.list_of_targets_dict:
            btn = self.dict_target_buttons[(dict['id'])]
            self.set_style_to_target_widget(btn, STYLE_SCC_UNSELECTED_TARGET)

    def _set_selection_target_widget(self, targets_id):
        for name_btn in targets_id:
            btn = self.dict_target_buttons[name_btn]
            self.set_style_to_target_widget(btn, STYLE_SCC_SELECTED_TARGET)

    def press_target_widget(self):
        btn_target = self.sender()
        name_btn_int = int(btn_target.objectName())

        if name_btn_int in self.current_targets_id_on_photo:
            self.set_style_to_target_widget(btn_target, STYLE_SCC_UNSELECTED_TARGET)
            self.current_targets_id_on_photo.remove(name_btn_int)
            self.service.deselect_target(name_btn_int)
        else:
            self.set_style_to_target_widget(btn_target, STYLE_SCC_SELECTED_TARGET)
            self.current_targets_id_on_photo.append(name_btn_int)
            self.service.select_target(name_btn_int)


    def generate_target_widget(self, dict_id_name: dict) -> QPushButton:
        id, name = dict_id_name.values()
        # target = QPushButton(self.widget)
        target = ClickableLabel (self.widget)
        target.setObjectName(str(id))
        target.setMinimumSize(QSize(10, 24))
        target.setText(name)
        self.set_style_to_target_widget(target, STYLE_SCC_UNSELECTED_TARGET)
        target.clicked.connect(self.press_target_widget)
        self.dict_target_buttons[id] = target
        return target

    def _update_buttons_target(self):
        if len(self.dict_target_buttons):
            while self.v_layout_target_buttons.count() > 0:
                item = self.v_layout_target_buttons.takeAt(0)
                widget_item = item.widget()
                if widget_item is not None:
                    widget_item.deleteLater()
        # self.list_of_targets_dict = self.service.get_short_targets_dict_on_session()
        self.list_of_targets_dict = self.service.get_full_targets_dict_on_session()
        for dict in self.list_of_targets_dict:
            self.v_layout_target_buttons.addWidget(self.generate_target_widget(dict))
        self.v_layout_target_buttons.addStretch()
        self._set_selection_target_widget(self.current_targets_id_on_photo)

    def update_pull_photo(self):
        self.service.get_sources_by_session_id()


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # відправляємо сигнал, що елемент був натиснутий

    # визначаємо новий сигнал для натискань на QLabel
    clicked = Signal()