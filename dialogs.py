import re
from PyQt5.QtWidgets import QPushButton, QMessageBox, QFormLayout, QLineEdit, QDialog

class AddCompanyDialog(QDialog): #add company dialog
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Company")
        self.setGeometry(100, 100, 400, 500)
        self.company_name = QLineEdit()
        self.building_number = QLineEdit()
        self.street_name = QLineEdit()
        self.town = QLineEdit()
        self.country = QLineEdit()
        self.postcode = QLineEdit()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow("Company Name", self.company_name)
        layout.addRow("Building Number", self.building_number)
        layout.addRow("Street Name", self.street_name)
        layout.addRow("City or Town", self.town)
        layout.addRow("Country", self.country)
        layout.addRow("Postcode", self.postcode)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_submit) #on clicked, check data
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def validate_and_submit(self):
        if not (self.company_name.text().strip() and self.street_name.text().strip() and self.town.text().strip() and self.country.text().strip() and self.postcode.text().strip()):
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled apart from building number.")
        else:
            self.accept()


class EditCompanyDialog(QDialog): #same as add company, but edit
    def __init__(self, company):
        super().__init__()
        self.setWindowTitle("Edit Company")
        self.setGeometry(100, 100, 400, 500)
        self.company_name = QLineEdit(company[0])
        self.building_number = QLineEdit(company[1])
        self.street_name = QLineEdit(company[2])
        self.town = QLineEdit(company[3])
        self.country = QLineEdit(company[4])
        self.postcode = QLineEdit(company[5])
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow("Company Name", self.company_name)
        layout.addRow("Building Number", self.building_number)
        layout.addRow("Street Name", self.street_name)
        layout.addRow("City or Town", self.town)
        layout.addRow("Country", self.country)
        layout.addRow("Postcode", self.postcode)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_submit)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def validate_and_submit(self):
        if not (self.company_name.text().strip() and self.street_name.text().strip() and self.town.text().strip() and self.country.text().strip() and self.postcode.text().strip()):
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled apart from building number.")
        else:
            self.accept()


class AddCustomerDialog(QDialog): #add customer, same as add company
    def __init__(self, company_id):
        super().__init__()
        self.setWindowTitle("Add Customer")
        self.setGeometry(100, 100, 400, 300)
        self.company_id = company_id
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.email = QLineEdit()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow("First Name", self.first_name)
        layout.addRow("Last Name", self.last_name)
        layout.addRow("Email", self.email)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_submit)
        layout.addWidget(submit_button)
        self.setLayout(layout)
        
    def validate_email(self, email):
        #validate email is in the right format
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    def validate_and_submit(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email = self.email.text().strip()

        if not (first_name and last_name and email):
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled.")
        elif not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
        else:
            self.accept()


class EditCustomerDialog(QDialog):#edit customer, same as edit company
    def __init__(self, customer):
        super().__init__()
        self.setWindowTitle("Edit Customer")
        self.setGeometry(100, 100, 400, 300)
        self.first_name = QLineEdit(customer[0])
        self.last_name = QLineEdit(customer[1])
        self.email = QLineEdit(customer[2])
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow("First Name", self.first_name)
        layout.addRow("Last Name", self.last_name)
        layout.addRow("Email", self.email)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_submit)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def validate_email(self, email):
        #validate email is in the right format
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    def validate_and_submit(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email = self.email.text().strip()

        if not (first_name and last_name and email):
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled.")
        elif not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
        else:
            self.accept()



class EditBankingInfoDialog(QDialog): #edit banking info
    def __init__(self, banking_info):
        super().__init__()
        self.setWindowTitle("Edit Banking Info")
        self.setGeometry(100, 100, 400, 500)
        self.company_name = QLineEdit(banking_info[1])
        self.building_number = QLineEdit(banking_info[2])
        self.street_name = QLineEdit(banking_info[3])
        self.town = QLineEdit(banking_info[4])
        self.postcode = QLineEdit(banking_info[5])
        self.phone_number = QLineEdit(banking_info[6])
        self.email = QLineEdit(banking_info[7])
        self.account_holder = QLineEdit(banking_info[8])
        self.account_number = QLineEdit(banking_info[9])
        self.sort_code = QLineEdit(banking_info[10])
        self.payment_terms = QLineEdit(banking_info[11])
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow("Company Name", self.company_name)
        layout.addRow("Building Number", self.building_number)
        layout.addRow("Street Name", self.street_name)
        layout.addRow("City or Town", self.town)
        layout.addRow("Postcode", self.postcode)
        layout.addRow("Phone Number", self.phone_number)
        layout.addRow("Email", self.email)
        layout.addRow("Account Holder", self.account_holder)
        layout.addRow("Account Number", self.account_number)
        layout.addRow("Sort Code", self.sort_code)
        layout.addRow("Payment Terms", self.payment_terms)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_submit)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def validate_email(self, email):
        #email validation
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    def validate_and_submit(self):
        if not (self.company_name.text().strip() and self.street_name.text().strip() and
                self.town.text().strip() and self.postcode.text().strip() and self.phone_number.text().strip() and
                self.email.text().strip() and self.account_holder.text().strip() and self.account_number.text().strip() and
                self.sort_code.text().strip() and self.payment_terms.text().strip()):
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled apart from building number.")
        elif not self.validate_email(self.email.text().strip()):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
        else:
            self.accept()
