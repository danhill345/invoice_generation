from dialogs import EditCompanyDialog, EditBankingInfoDialog

from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QMessageBox,
    QDialog
)

from PyQt5.QtCore import Qt
import sqlite3
import logging


class CompanyManagement: #managing companies
    def load_companies(self, company_table):
        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT companies.company_id, companies.company_name, addresses.town FROM companies JOIN addresses ON companies.address_id = addresses.address_id"
            )
            companies = cursor.fetchall() #selects the company information needed in the table and the town from address table
            conn.close()

            company_table.setRowCount(len(companies))
            for row, company in enumerate(companies):
                for col, data in enumerate(company):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    company_table.setItem(row, col, item)

        except Exception as e:
            logging.error(f"Error loading companies: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while loading companies: {e}")

    def add_company(self, dialog, load_companies): #add company
        company_name = dialog.company_name.text().strip()
        building_number = dialog.building_number.text().strip()
        street_name = dialog.street_name.text().strip()
        town = dialog.town.text().strip()
        postcode = dialog.postcode.text().strip()
        country = dialog.country.text().strip()

        if not self.validate_fields(company_name, building_number, street_name, town, postcode, country):
            return #if incorrect data added, move on

        try: #tries to add the data
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO addresses (building_number, street_name, town, postcode, country) VALUES (?, ?, ?, ?, ?)",
                (building_number, street_name, town, postcode, country),
            )
            address_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO companies (company_name, address_id) VALUES (?, ?)",
                (company_name, address_id),
            )
            conn.commit()
            conn.close()
            load_companies()
            QMessageBox.information(None, "Company Added", f"Company '{company_name}' has been added.") #success
        except Exception as e:
            logging.error(f"Error adding company: {e}") #error
            QMessageBox.critical(None, "Error", f"An error occurred while adding the company: {e}") #error

    def edit_company(self, company_id, load_companies): #edit company, works the same as add
        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT companies.company_name, addresses.building_number, addresses.street_name, addresses.town, addresses.postcode, addresses.country "
                "FROM companies JOIN addresses ON companies.address_id = addresses.address_id WHERE companies.company_id = ?",
                (company_id,)
            )
            company_info = cursor.fetchone()
            conn.close()
        except Exception as e:
            logging.error(f"Error fetching company info: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while fetching company info: {e}")
            return

        edit_dialog = EditCompanyDialog(company_info)
        if edit_dialog.exec_() == QDialog.Accepted:
            company_name = edit_dialog.company_name.text()
            building_number = edit_dialog.building_number.text()
            street_name = edit_dialog.street_name.text()
            town = edit_dialog.town.text()
            postcode = edit_dialog.postcode.text()
            country = edit_dialog.country.text()

            if not self.validate_fields(company_name, building_number, street_name, town, postcode, country):
                return

            try:
                conn = sqlite3.connect('invoice_system.db')
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE addresses SET building_number = ?, street_name = ?, town = ?, postcode = ?, country = ? WHERE address_id = (SELECT address_id FROM companies WHERE company_id = ?)",
                    (building_number, street_name, town, postcode, country, company_id),
                )
                cursor.execute(
                    "UPDATE companies SET company_name = ? WHERE company_id = ?",
                    (company_name, company_id),
                )
                conn.commit()
                conn.close()
                load_companies()
                QMessageBox.information(None, "Company Edited", f"Company '{company_name}' has been edited.")
            except Exception as e:
                logging.error(f"Error editing company: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred while editing the company: {e}")

    def edit_banking_info(self): #edit banking info works the same as edit company but about a different table
        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM banking_information WHERE company_id = 1")
            banking_info = cursor.fetchone()
            conn.close()
        except Exception as e:
            logging.error(f"Error fetching banking info: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while fetching banking info: {e}")
            return

        if not banking_info:
            QMessageBox.warning(None, "Error", "Banking information not found.")
            return

        edit_dialog = EditBankingInfoDialog(banking_info)
        if edit_dialog.exec_() == QDialog.Accepted:
            company_name = edit_dialog.company_name.text().strip()
            building_number = edit_dialog.building_number.text().strip()
            street_name = edit_dialog.street_name.text().strip()
            town = edit_dialog.town.text().strip()
            postcode = edit_dialog.postcode.text().strip()
            phone_number = edit_dialog.phone_number.text().strip()
            email = edit_dialog.email.text().strip()
            account_holder = edit_dialog.account_holder.text().strip()
            account_number = edit_dialog.account_number.text().strip()
            sort_code = edit_dialog.sort_code.text().strip()
            payment_terms = edit_dialog.payment_terms.text().strip()

            if not (
                company_name
                and building_number
                and street_name
                and town
                and postcode
                and phone_number
                and email
                and account_holder
                and account_number
                and sort_code
                and payment_terms
            ):
                QMessageBox.warning(None, "Invalid Input", "All fields must be filled.")
                return

            try:
                conn = sqlite3.connect('invoice_system.db')
                cursor = conn.cursor()
                cursor.execute(
                    '''UPDATE banking_information
                       SET company_name = ?, building_number = ?, street_name = ?, town = ?, postcode = ?, phone_number = ?, email = ?, account_holder = ?, account_number = ?, sort_code = ?, payment_terms = ?
                       WHERE company_id = 1''',
                    (
                        company_name,
                        building_number,
                        street_name,
                        town,
                        postcode,
                        phone_number,
                        email,
                        account_holder,
                        account_number,
                        sort_code,
                        payment_terms,
                    ),
                )
                conn.commit()
                conn.close()
                QMessageBox.information(None, "Banking Info Edited", "Banking information has been edited.")
            except Exception as e:
                logging.error(f"Error editing banking info: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred while editing the banking info: {e}")

    def validate_fields(self, company_name, building_number, street_name, town, postcode, country):
        try:
            if not (
                company_name and street_name and town and postcode and country
            ):
                raise ValueError("All fields must be filled except Building Number.")

            if not (
                company_name.replace(" ", "").isalnum()
                and street_name.replace(" ", "").isalnum()
                and town.replace(" ", "").isalnum()
                and postcode.replace(" ", "").isalnum()
                and country.replace(" ", "").isalnum()
            ):
                raise ValueError(
                    "Fields can only contain alphanumeric characters and spaces."
                )

            if (
                len(company_name) > 50
                or len(street_name) > 50
                or len(town) > 50
                or len(postcode) > 20
                or len(country) > 50
            ):
                raise ValueError("Field lengths exceed maximum allowed size.")

            if (
                len(company_name) < 2
                or len(street_name) < 2
                or len(town) < 2
                or len(postcode) < 2
                or len(country) < 2
            ):
                raise ValueError("Fields must contain at least two characters.")
        except ValueError as e:
            QMessageBox.warning(None, "Invalid Input", str(e))
            return False

        return True
