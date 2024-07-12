import os
import sqlite3
import logging
from datetime import datetime
import random
from PIL import Image
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from pdf_report import PDF


class PDFPreview(QWidget):
    def __init__(self, main_window, customer_id, ticket_id, distance, utility_type):
        super().__init__()
        self.main_window = main_window
        self.customer_id = customer_id
        self.ticket_id = ticket_id
        self.distance = distance
        self.utility_type = utility_type
        self.date_of_invoice = datetime.now().strftime("%Y-%m-%d") #date of invoice is when the pdf preview is created

        #fetches price, date of locate, and rating metrics from the db
        conn = sqlite3.connect('invoice_system.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price, dateoflocate, satelite_quality, hdop_quality, locate_quality FROM tickets WHERE ticket_id = ?",
            (self.ticket_id,))
        result = cursor.fetchone()
        self.price = result[0]
        self.dateoflocate = result[1]
        self.satellite_quality = result[2]
        self.hdop_quality = result[3]
        self.locate_quality = result[4]

        #reads company information
        cursor.execute("SELECT * FROM banking_information WHERE company_id = 1")
        self.company_info = cursor.fetchone()

        #reads customer information
        cursor.execute(
            "SELECT customers.first_name, customers.last_name, companies.company_name, addresses.building_number, addresses.street_name, addresses.town, addresses.postcode "
            "FROM customers JOIN companies ON customers.company_id = companies.company_id "
            "JOIN addresses ON companies.address_id = addresses.address_id "
            "WHERE customers.customer_id = ?",
            (self.customer_id,))
        self.customer_info = cursor.fetchone()

        #generates an invoice reference
        company_name_initials = self.company_info[1][:2].upper()
        random_number = random.randint(1, 1000)
        self.invoice_reference = f"{company_name_initials}-{self.ticket_id}-{random_number}"

        conn.close()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()  #makes a vertical box layout

        title_label = QLabel("PDF Preview", self)  #title
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FFFFFF; padding: 20px;")

        ticket_label = QLabel(f"Ticket Number: {self.ticket_id}", self)  #ticket number displayed on the preview
        ticket_label.setFont(QFont("Arial", 18))

        distance_label = QLabel(f"Distance Covered: {self.distance:.2f} meters", self)  #distance covered
        distance_label.setFont(QFont("Arial", 18))

        dateoflocate_label = QLabel(f"Date of Locate: {self.dateoflocate}", self)  #date of locate
        dateoflocate_label.setFont(QFont("Arial", 18))

        date_of_invoice_label = QLabel(f"Date of Invoice: {self.date_of_invoice}", self)  #date of invoice
        date_of_invoice_label.setFont(QFont("Arial", 18))

        invoice_reference_label = QLabel(f"Invoice Reference: {self.invoice_reference}", self)  #invoice reference
        invoice_reference_label.setFont(QFont("Arial", 18))

        price_label = QLabel(f"Price: £{self.price:.2f}", self)  #price
        price_label.setFont(QFont("Arial", 18))

        #customer name
        customer_name_label = QLabel(f"Customer Name: {self.customer_info[0]} {self.customer_info[1]}", self)
        customer_name_label.setFont(QFont("Arial", 18))

        #company name (of the customer)
        company_name_label = QLabel(f"Customer's Company Name: {self.customer_info[2]}", self)  #company name
        company_name_label.setFont(QFont("Arial", 18))

        map_image_path = f"{self.ticket_id}.png"  #image is the image generated when creating the pdf preview
        map_image = QPixmap(map_image_path)
        max_width = 800
        max_height = 500
        #max dimensions of the image

        #resizes the image but keeps the aspect ratio
        map_image = map_image.scaled(max_width, max_height, aspectRatioMode=1)

        map_label = QLabel(self)
        map_label.setPixmap(map_image)  #Map label is the resized image
        map_label.setAlignment(Qt.AlignCenter)  #Puts on the ui centrally

        back_button = QPushButton("Back to PDF Preview Creation", self)  #Back button, on the preview
        back_button.clicked.connect(self.back_to_invoice_management_screen)  #Clicking the back button takes you back to the invoice management screen
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #1DA1F2;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1A91DA;
            }
        """)

        save_button = QPushButton("Save as PDF", self)  #Save as pdf button
        save_button.clicked.connect(self.save_as_pdf)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        #Adds all elements to the layout
        layout.addWidget(save_button, alignment=Qt.AlignRight)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(ticket_label, alignment=Qt.AlignCenter)
        layout.addWidget(distance_label, alignment=Qt.AlignCenter)
        layout.addWidget(dateoflocate_label, alignment=Qt.AlignCenter)
        layout.addWidget(date_of_invoice_label, alignment=Qt.AlignCenter)
        layout.addWidget(invoice_reference_label, alignment=Qt.AlignCenter)
        layout.addWidget(price_label, alignment=Qt.AlignCenter)
        layout.addWidget(customer_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(company_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(map_label, alignment=Qt.AlignCenter)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)
        self.setLayout(layout)

    def back_to_invoice_management_screen(self):
        self.cleanup_files()  #When going back to invoice management screen, delete the temporarily made files and go back to the screen
        self.main_window.show_invoice_management_screen("user") #only users can generate pdf previews so go back to user view

    def save_as_pdf(self):  #Saves as pdf
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return  #If user cancelled saving to pdf then close

        try:
            #Resizes the image
            image_path = f"{self.ticket_id}.png"
            resized_image_path = self.resize_image(image_path)

            #Creates the pdf
            self.create_pdf(file_path, resized_image_path)

            QMessageBox.information(self, "PDF Saved", f"PDF saved successfully to {file_path}")  # Successful message
        except Exception as e:
            logging.error(f"Error saving PDF: {e}")  # Error message with error code
            QMessageBox.critical(self, "Error", f"Error saving PDF: {str(e)}")
        finally:
            self.cleanup_files()  # Cleans up files after everything is done

    def resize_image(self, image_path):
        #Opens the image
        image = Image.open(image_path)

        #New size of image
        max_width_mm = 190  # Maximum width in mm
        max_height_mm = 270  # Maximum height in mm

        #Converts dimensions to pixels
        dpi = 300
        max_width_px = int(max_width_mm * dpi / 25.4)  # 1 inch = 25.4 mm
        max_height_px = int(max_height_mm * dpi / 25.4)

        #Original image size
        original_width_px, original_height_px = image.size

        aspect_ratio = original_width_px / original_height_px  #Calculate the aspect ratio
        if original_width_px > max_width_px or original_height_px > max_height_px:  #If original image is too big
            if original_width_px / max_width_px > original_height_px / max_height_px:  #Checks which dimension needs to be reduced more to fit
                #Compares the width reduction ratio and the height reduction ratio
                new_width_px = max_width_px  #If width reduction is bigger sets the new width to be the max width
                new_height_px = int(max_width_px / aspect_ratio)  #New height calculated depending on the aspect ratio
            else:
                new_height_px = max_height_px  #If height reduction is bigger sets the new height to be the max height
                new_width_px = int(max_height_px * aspect_ratio)  #New width calculated depending on the aspect ratio
        else:
            new_width_px, new_height_px = original_width_px, original_height_px  #Else (no resizing is needed)

        #Resizes the image
        resized_image = image.resize((new_width_px, new_height_px), Image.LANCZOS)  #LANCZOS filter for high-quality downscaling

        #Saves the resized image (will be deleted later)
        resized_image_path = "resized_ticket.png"
        resized_image.save(resized_image_path)

        return resized_image_path  #Returns the path of the image

    def create_pdf(self, pdf_path, image_path):  #Creation of the pdf
        #Instance of FPDF class
        pdf = PDF()

        #Fetch the data needed for the pdf
        company_info = {
            "Company Name": self.company_info[1],
            "Address": f"{self.company_info[2]} {self.company_info[3]}, {self.company_info[4]}, {self.company_info[5]}",
            "Contact": f"Phone: {self.company_info[6]}, Email: {self.company_info[7]}"
        }

        customer_info = {
            "Customer Name": f"{self.customer_info[0]} {self.customer_info[1]}",
            "Company Name": self.customer_info[2],
            "Address": f"{self.customer_info[3]} {self.customer_info[4]}, {self.customer_info[5]}, {self.customer_info[6]}"
        }

        locate_report_data = [
            ["Invoice Reference", self.invoice_reference, "Date Of Locate", self.dateoflocate],
            ["Utility Type", self.utility_type, "Date of Invoice", self.date_of_invoice],
            ["Distance Walked", f"{self.distance:.2f} meters", "Price", f"£{self.price:.2f}"],
            ["Locate Quality", self.get_quality_color(self.locate_quality), "Price Incl V.A.T", f"£{self.price * 1.2:.2f}"],
        ]

        average_activity_scoring_data = [
            ["Horizontal Dilution of Precision (HDOP)", self.get_quality_color(self.hdop_quality)],
            ["Satellites", self.get_quality_color(self.satellite_quality)]
        ]

        payable_on_account_details = {
            "Bank details": [
                f"Account holder: {self.company_info[8]}",
                f"Account number: {self.company_info[9]}",
                f"Sort code: {self.company_info[10]}"
            ],
            "Payment terms": self.company_info[11],
            "Payment Reference": self.invoice_reference,
            "Payment amount": f"£{self.price * 1.2:.2f}"
        }

        #Adds the content to the pdf
        pdf.add_page()
        pdf.add_table("Company Information", company_info)
        pdf.add_table("Customer Information", customer_info)
        pdf.add_locate_report_table(locate_report_data, [40, 50, 40, 50])
        pdf.ln(3)
        pdf.add_average_activity_scoring_table(average_activity_scoring_data)
        pdf.ln(3)
        pdf.add_image(image_path)
        pdf.ln(3)
        pdf.add_payable_on_account(payable_on_account_details)

        #Outputs the pdf
        pdf.output(pdf_path)

    def get_quality_color(self, quality):  #Assigns the quality rating with a color
        if quality == 1:
            return "RED"
        elif quality == 2:
            return "AMBER"
        elif quality == 3:
            return "GREEN"
        return "UNKNOWN"

    def cleanup_files(self):  #Deletes the picture of the map after use
        image_path = f"{self.ticket_id}.png"
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                logging.info(f"Deleted file: {image_path}")
            except Exception as e:
                logging.error(f"Error deleting file {image_path}: {e}")

        resized_image_path = "resized_ticket.png"
        if os.path.exists(resized_image_path):
            try:
                os.remove(resized_image_path)
                logging.info(f"Deleted file: {resized_image_path}")
            except Exception as e:
                logging.error(f"Error deleting file {resized_image_path}: {e}")