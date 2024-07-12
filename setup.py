import sqlite3

def create_database():
    conn = sqlite3.connect('invoice_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('admin', 'user'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS addresses (
        address_id INTEGER PRIMARY KEY AUTOINCREMENT,
        building_number VARCHAR(50),
        street_name VARCHAR(50),
        town VARCHAR(50),
        postcode VARCHAR(20),
        country VARCHAR(50)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name VARCHAR(50),
        address_id INTEGER,
        FOREIGN KEY (address_id) REFERENCES addresses(address_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(100),
        company_id INTEGER,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        distance REAL,
        price REAL,
        dateoflocate VARCHAR(50),
        csv_file_path VARCHAR(255),
        satelite_quality INTEGER,
        hdop_quality INTEGER,
        locate_quality INTEGER,
        utility_type VARCHAR(50),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS banking_information (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name VARCHAR(50),
        building_number VARCHAR(50),
        street_name VARCHAR(50),
        town VARCHAR(50),
        postcode VARCHAR(20),
        phone_number VARCHAR(20),
        email VARCHAR(100),
        account_holder VARCHAR(50),
        account_number VARCHAR(50),
        sort_code VARCHAR(10),
        payment_terms VARCHAR(255)
    )
    ''')

    conn.commit()
    conn.close()

def insert_dummy_data():
    conn = sqlite3.connect('invoice_system.db')
    cursor = conn.cursor()

    addresses_data = [
        (1, "1", "High Street", "London", "SW1A 1AA", "UK"),
        (2, "2", "Station Road", "Birmingham", "B1 1AA", "UK"),
        (3, "3", "Main Street", "Leeds", "LS1 1AA", "UK"),
        (4, "4", "Park Road", "Glasgow", "G1 1AA", "UK"),
        (5, "5", "Church Road", "Sheffield", "S1 1AA", "UK"),
        (6, "6", "Church Street", "Bradford", "BD1 1AA", "UK"),
        (7, "7", "London Road", "Liverpool", "L1 1AA", "UK"),
        (8, "8", "Victoria Road", "Edinburgh", "EH1 1AA", "UK"),
        (9, "9", "Green Lane", "Manchester", "M1 1AA", "UK"),
        (10, "10", "Manor Road", "Bristol", "BS1 1AA", "UK")
    ]

    cursor.executemany('''
    INSERT INTO addresses (address_id, building_number, street_name, town, postcode, country)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', addresses_data)

    companies_data = [
        ("BP", 1),
        ("HSBC", 2),
        ("Tesco", 3),
        ("Barclays", 4),
        ("Vodafone", 5),
        ("Unilever", 6),
        ("Lloyds", 7),
        ("Prudential", 8),
        ("GSK", 9),
        ("BT", 10)
    ]

    cursor.executemany('''
    INSERT INTO companies (company_name, address_id)
    VALUES (?, ?)
    ''', companies_data)

    customers_data = [
        ("Oliver", "Smith", "oliver.smith@bp.com", 1),
        ("George", "Jones", "george.jones@hsbc.com", 2),
        ("Harry", "Taylor", "harry.taylor@tesco.com", 3),
        ("Jack", "Brown", "jack.brown@barclays.com", 4),
        ("Jacob", "Williams", "jacob.williams@vodafone.com", 5),
        ("Noah", "Wilson", "noah.wilson@unilever.com", 6),
        ("Charlie", "Johnson", "charlie.johnson@lloyds.com", 7),
        ("Thomas", "Davies", "thomas.davies@prudential.com", 8),
        ("Oscar", "Patel", "oscar.patel@gsk.com", 9),
        ("William", "Wright", "william.wright@bt.com", 10)
    ]

    cursor.executemany('''
    INSERT INTO customers (first_name, last_name, email, company_id)
    VALUES (?, ?, ?, ?)
    ''', customers_data)

    banking_info_data = (
        "Apple", "57", "Business Park", "London", "EC1A 1BB", "+44 20 7946 0958",
        "bill.gates@apple.com", "Bill Gates", "12345678", "12-34-56", "30 days"
    )

    cursor.execute('''
    INSERT INTO banking_information (company_name, building_number, street_name, town, postcode, phone_number, email, account_holder, account_number, sort_code, payment_terms)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', banking_info_data)

    users_data = [
        ('admin', 'password', 'admin'),
        ('user', 'password', 'user'),
        ('adam', 'password', 'admin'),
        ('ian', 'password', 'user')
    ]

    cursor.executemany('''
    INSERT INTO users (username, password, user_type)
    VALUES (?, ?, ?)
    ''', users_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    insert_dummy_data()

