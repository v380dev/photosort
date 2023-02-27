from abc import abstractmethod
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import QSize
from PySide6.QtGui import QShowEvent

from model.service import Service

class OpenDeleteSessionAbs(QDialog):
    def __init__(self, service: Service):
        super().__init__()
        self.service = service
        self.items = []
        self.items = list(d for d in self.service.get_dict_sessions().values())
        self.combo_choose_session = QComboBox(self)
        self.combo_choose_session.setObjectName("combo_list_session")
        self.button_ok=QPushButton()
        self.button_ok.clicked.connect(lambda: self.choose_session(self.combo_choose_session.currentText()))
        self.resize(220, 125)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.addWidget(self.combo_choose_session)
        self.verticalSpacer = QSpacerItem(77, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.button_ok.setMinimumSize(QSize(200, 30))
        self.button_ok.setMaximumSize(QSize(200, 30))
        self.verticalLayout.addWidget(self.button_ok)
        self.verticalLayout_2.addLayout(self.verticalLayout)

    @abstractmethod
    def choose_session(self, name_session):
        pass

    def showEvent(self, event: QShowEvent) -> None:
        self.items = list(d for d in self.service.get_dict_sessions().values())
        current_session_name = self.service.get_current_session_name()
        self.combo_choose_session.clear()
        self.combo_choose_session.addItems(self.items)
        self.combo_choose_session.setCurrentText(current_session_name)


class OpenSession(OpenDeleteSessionAbs):
    def __init__(self, service: Service):
        super().__init__(service)
        self.setWindowTitle("Open session")
        self.button_ok.setText('Load session')

    def choose_session(self, name_session):
        if name_session:
            self.service.load_session_by_name(name_session)
            self.close()

class DeleteSession(OpenDeleteSessionAbs):
    def __init__(self, service: Service):
        super().__init__(service)
        self.setWindowTitle("Delete session")
        self.button_ok.setText('Видалити сесію')

    def choose_session(self, name_session):
        if name_session:
            self.service.delete_session_by_id(self.service.get_id_session_by_name(name_session))
            self.service.update_service()
            self.close()
