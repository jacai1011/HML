from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
import sys

class TaskInput(QtWidgets.QWidget):
    submitted = QtCore.pyqtSignal(list)
    canceled = QtCore.pyqtSignal()
    def __init__(self, category_id=None, parent=None):
        super().__init__(parent)
        self.category = category_id
        self.db_handler = DatabaseHandler()

        self.layout = QtWidgets.QVBoxLayout(self)

        # Activity Title
        self.task_input = QtWidgets.QLineEdit(self)
        line_style = """
            QLineEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
            }
        """
        self.task_input.setStyleSheet(line_style)
        self.layout.addWidget(QtWidgets.QLabel("Activity Title:"))
        self.layout.addWidget(self.task_input)
        
        self.priority_input = QtWidgets.QLineEdit(self)
        line_style = """
            QLineEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
            }
        """
        self.priority_input.setStyleSheet(line_style)
        self.layout.addWidget(self.priority_input)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("Add Task", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        button_style = """
            QPushButton {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: lightgrey;
            }
        """
        self.ok_button.setStyleSheet(button_style)
        self.cancel_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)

    def on_cancel(self):
        self.canceled.emit()
        self.close()

    def on_ok(self):
        proj_name = self.task_input.text()
        proj_priority = self.priority_input.text()
        proj_category = self.category
        check = self.db_handler.insert_project(proj_category, proj_name, proj_priority)
        if check:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Timeslot taken")
        else:
            output = self.db_handler.get_all_projects(proj_category)
            print(output)
            input_data = self.db_handler.get_all_projects(proj_category)[-1]
            self.submitted.emit(input_data)
            self.close()