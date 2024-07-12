import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginScreen(QWidget): #login screen class
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window  # directly setting the main window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("CAT Invoice Generator", self)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(
            "Welcome to CAT Invoice Generator!\nPlease log in to manage your invoices and tickets.\n"
            "If you don't have an account, please contact your administrator.", self)
        description_label.setFont(QFont("Arial", 14))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #AAAAAA; padding: 10px;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 14))
        self.username_input.setFixedHeight(35)
        self.username_input.setStyleSheet("border-radius: 5px; padding: 5px;")
        self.username_input.returnPressed.connect(self.login)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setFixedHeight(35)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("border-radius: 5px; padding: 5px;")
        self.password_input.returnPressed.connect(self.login)

        login_button = QPushButton("Login", self)
        login_button.setFont(QFont("Arial", 14))
        login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover { 
                background-color: #45a049;
            }
        """)
        login_button.clicked.connect(self.login)

        footer_label = QLabel("CAT Invoice Generator v1.0\nFor support, contact support@catinvoices.com", self)
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #AAAAAA; padding: 10px;")

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(footer_label)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return

        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT user_type FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                user_type = result[0]
                self._main_window.show_invoice_management_screen(user_type)  #shows the invoice management screen
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while logging in: {e}")
