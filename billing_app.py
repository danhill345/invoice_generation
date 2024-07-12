from login_screen import LoginScreen #all ui elements needed imported
from invoice_management import InvoiceManagement
from pdf_preview import PDFPreview
from PyQt5.QtWidgets import QMainWindow

class BillingApp(QMainWindow):
    def __init__(self): #initializes the class
        super().__init__()
        self.setWindowTitle("CAT Invoice Generator") #window title
        self.setGeometry(100, 100, 800, 600) #initial window size
        self._login_screen = None #initially no ui elements are open
        self._invoice_management_screen = None
        self._pdf_preview_screen = None
        self.init_ui()

    def init_ui(self): #initializes the ui by openning the login screen
        self.login_screen = LoginScreen(self) #creates an instance of login screen
        self.setCentralWidget(self.login_screen) #made focus (central widget)

    def show_invoice_management_screen(self, user_type): #showing the invoice management screen
        self.invoice_management_screen = InvoiceManagement(self, user_type) #instance created based on user type
        self.setCentralWidget(self.invoice_management_screen)

    def show_pdf_preview_screen(self, customer_id, ticket_id, distance, utility_type): #instance of the pdf preview screen
        self.pdf_preview_screen = PDFPreview(self, customer_id, ticket_id, distance, utility_type) #generates preview based on parameters
        self.setCentralWidget(self.pdf_preview_screen)

    def closeEvent(self, event): #if closed then cleanup temporary files
        if self.pdf_preview_screen is not None:
            self.pdf_preview_screen.cleanup_files()
        event.accept()


