import sqlite3

def delete_all_tables():
    try:
        conn = sqlite3.connect('invoice_system.db')
        cursor = conn.cursor()

        # Disable foreign key checks
        cursor.execute("PRAGMA foreign_keys = OFF")

        # Fetch all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Do not drop sqlite_sequence
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Clear the sqlite_sequence table
        cursor.execute("DELETE FROM sqlite_sequence")

        # Enable foreign key checks
        cursor.execute("PRAGMA foreign_keys = ON")

        conn.commit()
        conn.close()
        print("All tables deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_all_tables()
