from billing_app import BillingApp #imports billing app to run
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        #set the theme for the application
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(21, 32, 43))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 39, 52))
        dark_palette.setColor(QPalette.AlternateBase, QColor(21, 32, 43))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(21, 32, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(29, 161, 242))
        dark_palette.setColor(QPalette.Highlight, QColor(29, 161, 242))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)

        #sets a dark style for the application
        app.setStyleSheet("""
            QWidget {
                background-color: #15202B;
                color: #FFFFFF; 
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #192734; 
                border: 1px solid #38444D;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #1DA1F2;
                border: 1px solid #1A91DA;
                border-radius: 5px;
                padding: 10px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #1A91DA;
            }
            QTableWidget {
                background-color: #192734;
                border: 1px solid #38444D;
                border-radius: 5px;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #FFFFFF;
            }
        """)

        main_window = BillingApp() #main window is the billing app
        main_window.show() #shows main window
        sys.exit(app.exec_()) #starts event loop and ensures application exits cleanly
    except Exception as e:
        logging.error(f"Application crashed: {e}")
