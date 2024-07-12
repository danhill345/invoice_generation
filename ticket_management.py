
from utils import total_distance
import os
from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
import math
import pandas as pd
import sqlite3
import logging
from datetime import datetime


class TicketManagement: #ticket management
    def load_tickets(self, customer_table, ticket_table): #loads the tickets based on the customer selected
        try:
            customer_id = int(customer_table.item(customer_table.currentRow(), 0).text())
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ticket_id, distance, price FROM tickets WHERE customer_id = ?",
                (customer_id,)
            )
            tickets = cursor.fetchall()
            conn.close()

            ticket_table.setRowCount(len(tickets)) #needed information put into table
            for row, ticket in enumerate(tickets):
                for col, data in enumerate(ticket):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    ticket_table.setItem(row, col, item)

        except Exception as e:
            logging.error(f"Error loading tickets: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while loading tickets: {e}")

    def upload_locate_details(self, customer_id, load_tickets_callback): #uploading the locate details
        ticket_file, _ = QFileDialog.getOpenFileName(None, "Upload Locate Details", "", "CSV files (*.csv)") #opens file dialog to get csv
        if ticket_file: #if upload is success then try to get the information you need from the csv and add to the db
            try:
                ticket_id = self.generate_unique_ticket_id()
                distance, avg_sat_quality, avg_hdop_quality, avg_locate_quality, utility_type = self.process_csv_file(ticket_file)
                modification_time = os.path.getmtime(ticket_file) #gets the last time the csv was modified, this should be the locate date
                dateoflocate = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')
                price_per_metre = 0.1 #price per metre covered (in gbp without vat)
                pricecalculate = distance * price_per_metre
                pricecalculate = round(pricecalculate, 2)

                conn = sqlite3.connect('invoice_system.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tickets (ticket_id, customer_id, distance, price, dateoflocate, csv_file_path, satelite_quality, hdop_quality, locate_quality, utility_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (ticket_id, customer_id, distance, pricecalculate, dateoflocate, ticket_file, avg_sat_quality, avg_hdop_quality, avg_locate_quality, utility_type),
                )
                conn.commit()
                conn.close()
                load_tickets_callback()
                QMessageBox.information(None, "Ticket Uploaded", f"Ticket '{ticket_id}' has been uploaded.")
            except Exception as e: #unexpected error
                logging.error(f"Error uploading locate details: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred while uploading the ticket: {e}")

    def process_csv_file(self, file_path):
        try:
            df = pd.read_csv(file_path)

            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce') #dataframe of all the important headings
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
            df['Number of Sats'] = pd.to_numeric(df['Number of Sats'], errors='coerce')
            df['HDOP'] = pd.to_numeric(df['HDOP'], errors='coerce')

            latitude_list = df['Latitude'].tolist() #list of longs and lats
            longitude_list = df['Longitude'].tolist()

            coordinates = list(zip(latitude_list, longitude_list)) #tuple list of longs and lates
            coordinates = [(lat, lon) for lat, lon in coordinates if not (math.isnan(lat) or math.isnan(lon))] #removes NaN values
            distance = total_distance(coordinates) #calculates distance and rounds it
            distance = round(distance, 2)

            sat_quality = df['Number of Sats'].apply(self.calculate_satellite_quality) #quality of readings found
            hdop_quality = df['HDOP'].apply(self.calculate_hdop_quality)
            locate_quality = pd.concat([sat_quality, hdop_quality], axis=1).min(axis=1) #is the lowest quality

            avg_sat_quality = sat_quality.mean() #average quality for each
            avg_hdop_quality = hdop_quality.mean()
            avg_locate_quality = locate_quality.mean()

            utility_type = df['Utility type'].iloc[0]

            return distance, avg_sat_quality, avg_hdop_quality, avg_locate_quality, utility_type #returns information found
        except Exception as e:
            logging.error(f"Error processing CSV file: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while processing the CSV file: {e}")
            return None, None, None, None, None #unexpected error

    def calculate_satellite_quality(self, sats):
        if sats <= 7: #quality ranked 1-3 (red amber green)
            return 1
        elif sats == 8:
            return 2
        elif sats > 8:
            return 3
        return 3

    def calculate_hdop_quality(self, hdop):
        if hdop >= 1:
            return 1
        elif 0 < hdop < 1:
            return 2
        elif hdop == 0:
            return 3
        return 3

    def generate_unique_ticket_id(self): #generate unique ticket id by adding one to the number of tickets currently there
        try:
            conn = sqlite3.connect('invoice_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tickets")
            ticket_count = cursor.fetchone()[0]
            conn.close()
            return ticket_count + 1
        except Exception as e:
            logging.error(f"Error generating ticket ID: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while generating the ticket ID: {e}")
            return None
