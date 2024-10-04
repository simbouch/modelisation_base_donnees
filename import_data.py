import sqlite3
import csv

# File paths
clients_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\clients.csv'
commandes_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\commandes.csv'

# Step 1: Connect to SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Step 2: Create Client table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Client (
        Client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT NOT NULL,
        Prenom TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Telephone TEXT,
        Date_Naissance DATE,
        Adresse TEXT,
        Consentement_Marketing BOOLEAN NOT NULL
    )
''')

# Step 3: Create Commande table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Commande (
        Commande_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_Commande DATE NOT NULL,
        Montant_Commande REAL NOT NULL,
        Client_ID INTEGER NOT NULL,
        FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
    )
''')

# Step 4: Import data into Client table
with open(clients_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            cursor.execute('''
                INSERT INTO Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Nom'],
                row['Prénom'],  # Match with CSV header: 'Prénom'
                row['Email'],
                row['Téléphone'] if row['Téléphone'] else None,  # Match with CSV header: 'Téléphone'
                row['Date_Naissance'] if row['Date_Naissance'] else None,
                row['Adresse'] if row['Adresse'] else None,
                int(row['Consentement_Marketing'])  # Mandatory field
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting client: {e}")

# Step 5: Import data into Commande table
with open(commandes_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            cursor.execute('''
                INSERT INTO Commande (Date_Commande, Montant_Commande, Client_ID)
                VALUES (?, ?, ?)
            ''', (
                row['Date_Commande'],
                float(row['Montant_Commande']),
                int(row['Client_ID'])  # Foreign key; must refer to an existing Client_ID
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting commande: {e}")

# Step 6: Commit changes and close the connection
conn.commit()
conn.close()

print("Data import completed successfully!")
