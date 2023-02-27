import sys

from PySide6.QtWidgets import QApplication

from model.connect_db import SqlConnector
from model.service import Service
from model.move_photo import Mover
from view.main_window import MainWindow
from view.menu_edit_folders import UiSourceEditWindow, UiTargetEditWindow
from view.menu_new_session import CreateSession
from view.menu_open_delete_session import OpenSession, DeleteSession
from view.menu_rename_session import RenameSession
from view.menu_about import About
from view.window_conflict import WindowConflict


class Container:
    def __init__(self, settings):
        settings = settings
        self.db_connect = SqlConnector(settings["db"]["name"])
        self.copyist = Mover()
        self.service = Service(settings["session"]["name_default"], self.db_connect, self.copyist)
        self.app = QApplication(sys.argv)
        self.window_source_edit = UiSourceEditWindow(self.service)
        self.window_target_edit = UiTargetEditWindow(self.service)
        self.window_create_session = CreateSession(self.service)
        self.window_open_session = OpenSession(self.service)
        self.window_delete_session = DeleteSession(self.service)
        self.window_rename_session = RenameSession(self.service)
        self.window_about = About(settings["version"])
        self.window_conflict = WindowConflict(self.service)
        self.window = MainWindow(self.service,
                                 self.window_source_edit,
                                 self.window_target_edit,
                                 self.window_create_session,
                                 self.window_open_session,
                                 self.window_delete_session,
                                 self.window_rename_session,
                                 self.window_about,
                                 self.window_conflict,
                                 )