
from dialogs import EditCustomerDialog
from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QMessageBox,
    QDialog,
)
from PyQt5.QtCore import Qt

import sqlite3
import logging


class CustomerManagement: #customer management class
    def load_customers(self, company_table, customer_table, ticket_table):
        try:
            customer_table.clearSelection()
            ticket_table.clearSelection()
            ticket_table.setRowCount(0)

            company_id = int(company_table.item(company_table.currentRow(), 0).text())
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT customer_id, first_name, last_name, email FROM customers WHERE company_id = ?",
                (company_id,)
            )
            customers = cursor.fetchall()
            conn.close()

            customer_table.setRowCount(len(customers))
            for row, customer in enumerate(customers):
                for col, data in enumerate(customer):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    customer_table.setItem(row, col, item)

        except Exception as e:
            logging.error(f"Error loading customers: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while loading customers: {e}")

    def add_customer(self, dialog, load_customers_callback):
        first_name = dialog.first_name.text().strip()
        last_name = dialog.last_name.text().strip()
        email = dialog.email.text().strip()

        if not self.validate_fields(first_name, last_name, email):
            return

        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (first_name, last_name, email, company_id) VALUES (?, ?, ?, ?)",
                (first_name, last_name, email, dialog.company_id),
            )
            conn.commit()
            conn.close()
            load_customers_callback()
            QMessageBox.information(None, "Customer Added", f"Customer '{first_name} {last_name}' has been added.")
        except Exception as e:
            logging.error(f"Error adding customer: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while adding the customer: {e}")

    def edit_customer(self, customer_id, load_customers_callback):
        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, last_name, email FROM customers WHERE customer_id = ?", (customer_id,))
            customer_info = cursor.fetchone()
            conn.close()
        except Exception as e:
            logging.error(f"Error fetching customer info: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while fetching customer info: {e}")
            return

        edit_dialog = EditCustomerDialog(customer_info)
        if edit_dialog.exec_() == QDialog.Accepted:
            first_name = edit_dialog.first_name.text()
            last_name = edit_dialog.last_name.text()
            email = edit_dialog.email.text()

            if not self.validate_fields(first_name, last_name, email):
                return

            try:
                conn = sqlite3.connect('invoice_system.db')
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE customers SET first_name = ?, last_name = ?, email = ? WHERE customer_id = ?",
                    (first_name, last_name, email, customer_id),
                )
                conn.commit()
                conn.close()
                load_customers_callback()
                QMessageBox.information(None, "Customer Edited", f"Customer '{first_name} {last_name}' has been edited.")
            except Exception as e:
                logging.error(f"Error editing customer: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred while editing the customer: {e}")

    def validate_fields(self, first_name, last_name, email):
        try:
            if not (first_name and last_name and email):
                raise ValueError("All fields must be filled.")


            if (
                not first_name.replace(" ", "").isalnum()
                or not last_name.replace(" ", "").isalnum()
            ):
                raise ValueError("Names can only contain alphanumeric characters and spaces.")

            if (
                len(first_name) > 50
                or len(last_name) > 50
                or len(email) > 100
            ):
                raise ValueError("Field lengths exceed maximum allowed size.")

            if (
                len(first_name) < 2
                or len(last_name) < 2
            ):
                raise ValueError("Fields must contain at least two characters.")
        except ValueError as e:
            QMessageBox.warning(None, "Invalid Input", str(e))
            return False

        return True
