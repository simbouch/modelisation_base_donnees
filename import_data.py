import sqlite3
import csv

# File paths
clients_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\clients.csv'
commandes_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\commandes.csv'

# Step 1: Connect to SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Step 2: Import data into Client table
with open(clients_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        try:
            cursor.execute('''
                INSERT INTO Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Nom'],
                row['Prénom'],  # Match with CSV header: 'Prénom' with an accent
                row['Email'],
                row['Téléphone'] if row['Téléphone'] else None,  # Match with CSV header: 'Téléphone' with an accent
                row['Date_Naissance'] if row['Date_Naissance'] else None,
                row['Adresse'] if row['Adresse'] else None,
                int(row['Consentement_Marketing'])  # Mandatory field
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting client: {e}")

# Step 3: Import data into Commande table
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

# Step 4: Commit changes and close the connection
conn.commit()
conn.close()

print("Data import completed successfully!")

