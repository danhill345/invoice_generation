from fpdf import FPDF #import FPDF to make the pdf look better and write to it

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14) #header of the pdf
        self.cell(0, 10, 'Invoice Report', 0, 1, 'C')
        self.ln(2) #leaves gap between header and the next element

    def add_table(self, title, data):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_font('Arial', '', 10)
        line_height = self.font_size * 1.2

        for key, value in data.items():
            self.cell(50, line_height, f'{key}:', border=1)
            self.cell(140, line_height, value, border=1)
            self.ln(line_height)

        self.ln(2)  # Add space after the table

    def add_locate_report_table(self, data, col_widths): #adds locate report table
        self.set_font('Arial', 'B', 10)  # Smaller heading font size
        total_width = sum(col_widths)
        self.cell(total_width, 8, 'Locate Report', 1, 1, 'C')
        self.set_font('Arial', '', 10)

        for row in data: #fills out the data passed into the locate report, fills the cell in
            #with the colour of the quality of the locate (red, amber or green)
            for datum, width in zip(row, col_widths):
                if datum == 'RED':
                    self.set_fill_color(255, 0, 0)
                    self.cell(width, 8, 'RED', border=1, fill=True)
                elif datum == 'AMBER':
                    self.set_fill_color(255, 191, 0)
                    self.cell(width, 8, 'AMBER', border=1, fill=True)
                elif datum == 'GREEN':
                    self.set_fill_color(0, 255, 0)
                    self.cell(width, 8, 'GREEN', border=1, fill=True)
                else:
                    self.cell(width, 8, datum, border=1)
            self.ln(8)

    def add_average_activity_scoring_table(self, data): #average activity scoring data
        self.set_font('Arial', 'B', 10)
        total_width = 190
        self.cell(total_width, 8, 'Average Activity Scoring', 1, 1, 'C')
        self.set_font('Arial', '', 10)
        col_widths = [130, 60]

        for row in data: #adds the data and colours the cells
            for i, (datum, width) in enumerate(zip(row, col_widths)):
                if i == 1:
                    if datum == 'RED':
                        self.set_fill_color(255, 0, 0)
                        self.cell(width, 8, 'RED', border=1, fill=True)
                    elif datum == 'AMBER':
                        self.set_fill_color(255, 191, 0)
                        self.cell(width, 8, 'AMBER', border=1, fill=True)
                    elif datum == 'GREEN':
                        self.set_fill_color(0, 255, 0)
                        self.cell(width, 8, 'GREEN', border=1, fill=True)
                else:
                    self.cell(width, 8, datum, border=1)
            self.ln(8)

    def add_image(self, image_path):
        #adjusts the image size for the space available in the page
        available_width = 190
        available_height = 90
        self.image(image_path, x=10, y=self.get_y(), w=available_width, h=available_height) #adds the image passed to be
        #after the average activity scoring table in the pdf
        self.ln(available_height + 5) #adds space after image

    def add_payable_on_account(self, details): #payable on account info
        self.set_font('Arial', 'B', 10)
        total_width = 190
        self.cell(total_width, 8, 'Payable on account', 1, 1, 'L') #1, 1 the first 1 means a border is drawn around the cell
        #and the second 1 moves the cursos to the next line after drawing the cell
        self.set_font('Arial', '', 10)
        line_height = self.font_size * 1.2

        # Create the table
        for key, value in details.items(): #for each key and value in the items
            if isinstance(value, list): #if the value associated with the key is in the list
                self.cell(40, line_height * len(value), f'{key}:', border=1) #adjusts the cell to fit the size of the key
                self.multi_cell(150, line_height, '\n'.join(value), border=1) #multi cell value if needed (for the first row of the table)
            else:
                self.cell(40, line_height, f'{key}:', border=1) #rows that don't need multi cell values
                self.multi_cell(150, line_height, value, border=1)
