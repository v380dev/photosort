from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit

from model.service import Service

class CreateSession(QDialog):
    def __init__(self, service: Service):
        super().__init__()

        self.service = service
        self.setWindowTitle("Create new session")
        self.edit = QLineEdit('імʼя сесії')
        self.edit.selectAll()

        self.button = QPushButton('Create new session')
        self.button.clicked.connect(lambda: self.create_new_session(self.edit.text()))

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def create_new_session(self, name_session):
        self.service.create_new_session(name_session)
        self.close()
