import sqlite3
import csv
import hashlib
import base64
from data_protection import DataProtection

# Generate a 32-byte key from the given string "0907" by hashing it, and then base64 encode it
hashed_key = hashlib.sha256(b"0907").digest()[:32]
base64_key = base64.urlsafe_b64encode(hashed_key)

# Initialize the data protection tool with the base64 encoded key
data_protection = DataProtection(base64_key)

# File paths for the CSV files containing client and order data
clients_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\clients.csv'
commandes_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\commandes.csv'

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Step 2: Read and import data from the client CSV file with encryption and pseudonymization
with open(clients_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            # Encrypt sensitive data
            encrypted_nom = data_protection.encrypt_data(row['Nom'])
            encrypted_prenom = data_protection.encrypt_data(row['Prénom'])
            encrypted_email = data_protection.encrypt_data(row['Email'])
            encrypted_telephone = data_protection.encrypt_data(row['Téléphone']) if row['Téléphone'] else None
            encrypted_adresse = data_protection.encrypt_data(row['Adresse']) if row['Adresse'] else None

            # Pseudonymize the date of birth (optional)
            pseudonymized_date_naissance = data_protection.pseudonymize_data(row['Date_Naissance']) if row['Date_Naissance'] else None

            # Insert encrypted and pseudonymized data into the Client table
            cursor.execute('''
                INSERT INTO Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                encrypted_nom,
                encrypted_prenom,
                encrypted_email,
                encrypted_telephone,
                pseudonymized_date_naissance,
                encrypted_adresse,
                int(row['Consentement_Marketing'])  # Mandatory field: 1 (consent) or 0 (refusal)
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting client: {e}")

# Step 3: Read and import data from the orders CSV file
with open(commandes_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            # Encrypt the order date (optional, depending on sensitivity)
            encrypted_date_commande = data_protection.encrypt_data(row['Date_Commande'])
            # The order amount is not encrypted here as it may be useful in clear text for analysis

            # Insert the encrypted data into the Commande table
            cursor.execute('''
                INSERT INTO Commande (Date_Commande, Montant_Commande, Client_ID)
                VALUES (?, ?, ?)
            ''', (
                encrypted_date_commande,
                float(row['Montant_Commande']),
                int(row['Client_ID'])  # Foreign key; must refer to an existing Client_ID
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting order: {e}")

# Step 4: Commit changes and close the connection to the database
conn.commit()
conn.close()

print("Secure import of client and order data completed successfully!")
