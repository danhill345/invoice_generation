from company_management import CompanyManagement #imports classes needed
from customer_management import CustomerManagement
from ticket_management import TicketManagement
from map_service import MapService
#from pdf_service import PDFService
from dialogs import AddCompanyDialog, AddCustomerDialog
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QMessageBox,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QSizePolicy
)
from PyQt5.QtCore import Qt
import sqlite3
import logging


class InvoiceManagement(QWidget): #invoice management class
    def __init__(self, main_window, user_type):
        super().__init__() #initializes everything needed
        self.main_window = main_window
        self.user_type = user_type
        self.company_management = CompanyManagement()
        self.customer_management = CustomerManagement()
        self.ticket_management = TicketManagement()
        self.map_service = MapService()
        self.init_ui()
        self.load_companies()

    def init_ui(self):
        layout = QVBoxLayout() #vertical box layout for button
        top_layout = QHBoxLayout() #horizontal box for all other elements
        self.logout_button = QPushButton("Log Out", self)
        self.logout_button.setFont(QFont("Arial", 12))
        self.logout_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) #makes it so button expands to size of text in it
        self.logout_button.setStyleSheet( #makes logout button red
            """
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.logout_button.clicked.connect(self.logout) #when clicked, logout

        top_layout.addWidget(self.logout_button, alignment=Qt.AlignLeft) #top left

        if self.user_type == "admin": #if user type is admin, add edit banking info button
            self.edit_banking_info_button = QPushButton("Edit Banking Info", self)
            self.edit_banking_info_button.setFont(QFont("Arial", 12))
            self.edit_banking_info_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.edit_banking_info_button.clicked.connect(self.edit_banking_info)
            top_layout.addWidget(self.edit_banking_info_button, alignment=Qt.AlignRight)

        layout.addLayout(top_layout) #adds buttons to the layout

        title_label = QLabel("CAT Invoice Generator", self)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("color: #FFFFFF; padding: 20px;") #adds title

        company_title = QLabel("Companies", self) #adds titles for the tables
        company_title.setFont(QFont("Arial", 18, QFont.Bold))
        company_title.setAlignment(Qt.AlignLeft)
        company_title.setStyleSheet("color: #FFFFFF; padding: 10px;")

        customer_title = QLabel("Customers", self)
        customer_title.setFont(QFont("Arial", 18, QFont.Bold))
        customer_title.setAlignment(Qt.AlignLeft)
        customer_title.setStyleSheet("color: #FFFFFF; padding: 10px;")

        self.company_table = QTableWidget(self) #company table
        self.company_table.setColumnCount(3)
        self.company_table.setHorizontalHeaderLabels(["ID", "Company Name", "City or Town"]) #only these headers needed
        self.company_table.verticalHeader().setVisible(False) #vertical header not visible
        self.company_table.setSelectionBehavior(QTableWidget.SelectRows) #select row when selecting cell
        self.company_table.setEditTriggers(QTableWidget.NoEditTriggers) #read only
        self.company_table.cellClicked.connect(self.enable_company_buttons) #when company selected, enable company buttons
        self.company_table.cellClicked.connect(lambda row, column: self.load_customers(row, column)) #when cell clicked, load customers associated
        self.company_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #stretches to the size of the screen

        self.customer_table = QTableWidget(self) #customer table (works the same as company table)
        self.customer_table.setColumnCount(4)
        self.customer_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Email"])
        self.customer_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2c3e50; color: white; }"
        )
        self.customer_table.verticalHeader().setVisible(False)
        self.customer_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.customer_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customer_table.cellClicked.connect(self.enable_customer_buttons)
        self.customer_table.cellClicked.connect(lambda row, column: self.load_tickets(row, column))
        self.customer_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ticket_table = QTableWidget(self)
        if self.user_type == "admin": #if admin then hide tickets table
            self.ticket_table.setVisible(False)
        elif self.user_type == "user": #if user then show tickets table
            self.ticket_table.setVisible(True)
        self.ticket_table.setColumnCount(3) #works the same as other tables
        self.ticket_table.setHorizontalHeaderLabels(["Ticket ID", "Distance", "Cost"])
        self.ticket_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2c3e50; color: white; }"
        )
        self.ticket_table.verticalHeader().setVisible(False)
        self.ticket_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ticket_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ticket_table.cellClicked.connect(self.enable_pdf_preview_button) #when customer and company selected, enable pdf preview button
        self.ticket_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        button_layout = QHBoxLayout() #horizontal layout for buttons at the bottom
        if self.user_type == "admin":
            add_company_button = QPushButton("Add Company", self)
            add_company_button.setFont(QFont("Arial", 12))
            add_company_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            add_company_button.clicked.connect(self.add_company) #add company button

            self.edit_company_button = QPushButton("Edit Company", self)
            self.edit_company_button.setFont(QFont("Arial", 12))
            self.edit_company_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.edit_company_button.setStyleSheet(
                """
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                """
            )
            self.edit_company_button.clicked.connect(self.edit_company)
            self.edit_company_button.setEnabled(False) #initially disabled

            self.add_customer_button = QPushButton("Add Customer", self)
            self.add_customer_button.setFont(QFont("Arial", 12))
            self.add_customer_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            self.add_customer_button.clicked.connect(self.add_customer)
            self.add_customer_button.setEnabled(False) #initially disabled

            self.add_customer_button.setStyleSheet(
                """
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                """
            )

            self.edit_customer_button = QPushButton("Edit Customer", self)
            self.edit_customer_button.setFont(QFont("Arial", 12))
            self.edit_customer_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.edit_customer_button.setStyleSheet(
                """
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                """
            )
            self.edit_customer_button.clicked.connect(self.edit_customer)
            self.edit_customer_button.setEnabled(False) #initially disabled

            button_layout.addWidget(add_company_button)
            button_layout.addWidget(self.edit_company_button)
            button_layout.addWidget(self.add_customer_button)
            button_layout.addWidget(self.edit_customer_button) #adds buttons to layouts
        elif self.user_type == "user": #if user type is user
            self.upload_locate_details_button = QPushButton("Upload Locate Details", self) #show the upload locate details button
            self.upload_locate_details_button.setFont(QFont("Arial", 12))
            self.upload_locate_details_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.upload_locate_details_button.clicked.connect(self.upload_locate_details)
            self.upload_locate_details_button.setStyleSheet(
                """
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                """
            )
            self.upload_locate_details_button.setEnabled(False) #intially disabled
            button_layout.addWidget(self.upload_locate_details_button)

            self.generate_pdf_preview_button = QPushButton("Generate PDF Preview", self) #generate pdf preview button
            self.generate_pdf_preview_button.setFont(QFont("Arial", 12))
            self.generate_pdf_preview_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.generate_pdf_preview_button.setStyleSheet( #makes it green when selected
                """
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                """
            )
            self.generate_pdf_preview_button.setEnabled(False)
            self.generate_pdf_preview_button.clicked.connect(self.generate_pdf_preview)

            button_layout.addWidget(self.generate_pdf_preview_button)

        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(company_title)
        layout.addWidget(self.company_table)
        layout.addWidget(customer_title)
        layout.addWidget(self.customer_table) #adds every widget to the layout
        if self.user_type == "user":
            ticket_title = QLabel("Locate Details", self) #if user type is user, adds title for tickets table
            ticket_title.setFont(QFont("Arial", 18, QFont.Bold))
            ticket_title.setAlignment(Qt.AlignLeft)
            ticket_title.setStyleSheet("color: #FFFFFF; padding: 10px;")
            layout.addWidget(ticket_title)
            layout.addWidget(self.ticket_table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_companies(self): #load companies, handled in comapny_management.py
        self.company_management.load_companies(self.company_table)

    def load_customers(self, row, column): #load customers, handled in customer_management.py
        self.customer_management.load_customers(self.company_table, self.customer_table, self.ticket_table)

    def load_tickets(self, row, column): #loads tickets, handled in ticket_management.py
        self.ticket_management.load_tickets(self.customer_table, self.ticket_table)

    def enable_company_buttons(self): #enables company buttons if a company is selected
        company_selected = self.company_table.currentRow() >= 0
        if self.user_type == "admin":
            self.edit_company_button.setEnabled(company_selected)
            self.edit_banking_info_button.setEnabled(company_selected)
            self.add_customer_button.setEnabled(company_selected)

    def enable_customer_buttons(self): #enables customer buttons if a company and customer is selected
        company_selected = self.company_table.currentRow() >= 0
        customer_selected = self.customer_table.currentRow() >= 0
        if self.user_type == "admin": #different buttons enable based on user type
            self.edit_customer_button.setEnabled(company_selected and customer_selected)
        elif self.user_type == "user":
            self.upload_locate_details_button.setEnabled(company_selected and customer_selected)
            if customer_selected:
                self.load_tickets(self.customer_table.currentRow(), 0)

    def enable_pdf_preview_button(self): #enable pdf preview button when company, customer and ticket are selected
        company_selected = self.company_table.currentRow() >= 0
        customer_selected = self.customer_table.currentRow() >= 0
        ticket_selected = self.ticket_table.currentRow() >= 0
        self.generate_pdf_preview_button.setEnabled(company_selected and customer_selected and ticket_selected)

    def add_company(self): #add company opens the add company dialog
        dialog = AddCompanyDialog()
        if dialog.exec_() == QDialog.Accepted: #if dialog is accepted
            self.company_management.add_company(dialog, self.load_companies) #add the company (handled in company_management

    def edit_company(self): #edit company
        if self.company_table.currentRow() < 0:
            QMessageBox.warning(self, "No Company Selected", "Please select a company to edit.")
            return #company has to be selected

        row = self.company_table.currentRow()
        company_id = int(self.company_table.item(row, 0).text()) #gets the current company id selected
        self.company_management.edit_company(company_id, self.load_companies) #opens edit company dialog based on parameters, handled in company_management

    def add_customer(self): #add customer
        if self.company_table.currentRow() < 0: #if company selected
            QMessageBox.warning(self, "No Company Selected", "Please select a company to add a customer.")
            return

        company_id = int(self.company_table.item(self.company_table.currentRow(), 0).text()) #current company ID
        dialog = AddCustomerDialog(company_id) #opens dialog
        if dialog.exec_() == QDialog.Accepted: #if accepted, add customer
            self.customer_management.add_customer(dialog, lambda: self.load_customers(self.company_table.currentRow(), 0))

    def edit_customer(self): #edit customer, same as edit company
        if self.customer_table.currentRow() < 0:
            QMessageBox.warning(self, "No Customer Selected", "Please select a customer to edit.")
            return

        row = self.customer_table.currentRow()
        customer_id = int(self.customer_table.item(row, 0).text())
        self.customer_management.edit_customer(customer_id, lambda: self.load_customers(self.company_table.currentRow(), 0))

    def edit_banking_info(self): #edit banking info, handled in company_management
        self.company_management.edit_banking_info()

    def upload_locate_details(self): #uploading locate details
        if self.company_table.currentRow() < 0 or self.customer_table.currentRow() < 0:
            QMessageBox.warning(self, "No Company or Customer Selected", "Please select a company and customer to upload a ticket.")
            return

        customer_id = int(self.customer_table.item(self.customer_table.currentRow(), 0).text())
        self.ticket_management.upload_locate_details(customer_id, lambda: self.load_tickets(self.customer_table.currentRow(), 0))#uploads and processes upload,
        #handled in ticket_management

    def generate_pdf_preview(self): #generate pdf preview
        try:
            user_item = self.customer_table.currentRow()
            ticket_item = self.ticket_table.currentRow()

            if user_item < 0:
                logging.error("No user selected")
                return
            if ticket_item < 0:
                logging.error("No ticket selected")
                return

            customer_id = self.customer_table.item(user_item, 0).text()
            ticket = self.ticket_table.item(ticket_item, 0).text()

            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT distance, utility_type FROM tickets WHERE ticket_id = ?", (ticket,))
            result = cursor.fetchone()
            conn.close()

            if result is None:
                logging.error(f"No distance or utility type found for ticket {ticket}")
                return #gets the needed information from db

            distance, utility_type = result
            logging.info(f"Distance found: {distance}")
            logging.info(f"Utility type found: {utility_type}")

            html_file = self.map_service.map_creation(ticket) #creates a map
            self.map_service.map_screenshot(ticket) #screenshots the map

            self.main_window.show_pdf_preview_screen(customer_id, ticket, distance, utility_type) #opens a window of the preview of the pdf based on parameters
        except Exception as e: #unexpected error
            logging.error(f"Error in generate_pdf_preview: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while generating the PDF preview: {e}")

    def logout(self): #logout takes you back to login screen
        self.main_window.init_ui()
