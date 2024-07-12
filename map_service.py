import sqlite3
import pandas as pd
import plotly.express as px

class MapService:
    def map_creation(self, ticket):
        conn = sqlite3.connect('invoice_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT csv_file_path FROM tickets WHERE ticket_id = ?", (ticket,))
        csv_file_path = cursor.fetchone()[0]
        conn.close()

        try:
            df = pd.read_csv(csv_file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading '{csv_file_path}': {e}")

        if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            raise ValueError(f"Latitude or Longitude columns missing in '{csv_file_path}'.")

        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        df = df.dropna(subset=['Latitude', 'Longitude'])

        if df.empty:
            raise ValueError(f"No valid Latitude and Longitude data found in '{csv_file_path}'.")

        #returns all the information needed to make the map screenshot, only uses 1 in 8 values so the final plot is less cluttered
        df = df.iloc[::8]

        return df

    def map_screenshot(self, ticket):
        try:
            df = self.map_creation(ticket)

            #create the map figures
            fig = px.scatter_mapbox(df,
                                    lat="Latitude",
                                    lon="Longitude",
                                    color_discrete_sequence=["red"], #colour of markers
                                    zoom=15,  #zoom level
                                    height=800, #height and width of view
                                    width=800)

            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}) #removes white border from map so only detailed parts are shown

            #saves the map as a png
            screenshot_file = f"{ticket}.png"
            fig.write_image(screenshot_file, engine="kaleido") #writes the image to the path specified

            return screenshot_file

        except Exception as e:
            raise Exception(f"Error in map_screenshot: {e}")


