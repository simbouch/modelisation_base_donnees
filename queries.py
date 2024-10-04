import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Function to display and save query results
def display_and_save_results(query, filename, description, headers):
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Print the description
    print(f"\n{description}")
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in rows:
            # Format and print row in a readable way
            if len(row) == 2:
                print(f"{row[0]}: {row[1]}")
            elif len(row) == 4:
                print(f"Commande ID: {row[0]}, Date: {row[1]}, Amount: {row[2]}")
            else:
                print(f"{row[0]}: {row[1]} {row[2]}")
            
            # Write row to CSV
            writer.writerow(row)

# Requête 1: Clients ayant consenti à recevoir des communications marketing
query_clients_marketing = '''
    SELECT Client_ID, Nom, Prenom FROM Client WHERE Consentement_Marketing = 1
'''
display_and_save_results(query_clients_marketing, 'clients_marketing.csv', "Clients with marketing consent:", ['Client_ID', 'Nom', 'Prenom'])

# Requête 2: Commandes pour un client spécifique (Client_ID = 61)
query_orders_client_61 = '''
    SELECT Commande_ID, Date_Commande, Montant_Commande, Client_ID FROM Commande WHERE Client_ID = 61
'''
display_and_save_results(query_orders_client_61, 'orders_for_client_61.csv', "Orders of client ID 61:", ['Commande_ID', 'Date_Commande', 'Montant_Commande', 'Client_ID'])

# Requête 3: Montant total des commandes pour un client spécifique (Client_ID = 61)
cursor.execute('''
    SELECT SUM(Montant_Commande) FROM Commande WHERE Client_ID = 61
''')
total_amount = cursor.fetchone()[0]
print(f"\nTotal amount of orders for client ID 61: {total_amount} euros")

# Save total amount to CSV
with open('total_order_amount_client_61.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Total_Montant_Commande'])
    writer.writerow([total_amount])

# Requête 4: Clients ayant passé des commandes de plus de 100 euros
query_clients_large_orders = '''
    SELECT DISTINCT Client.Client_ID, Nom, Prenom 
    FROM Client
    JOIN Commande ON Client.Client_ID = Commande.Client_ID
    WHERE Commande.Montant_Commande > 100
'''
display_and_save_results(query_clients_large_orders, 'clients_with_large_orders.csv', "Clients with orders over 100 euros:", ['Client_ID', 'Nom', 'Prenom'])

# Requête 5: Clients ayant passé des commandes après le 01/01/2023
query_clients_recent_orders = '''
    SELECT DISTINCT Client.Client_ID, Nom, Prenom 
    FROM Client
    JOIN Commande ON Client.Client_ID = Commande.Client_ID
    WHERE Commande.Date_Commande > '2023-01-01'
'''
display_and_save_results(query_clients_recent_orders, 'clients_with_recent_orders.csv', "Clients with orders after 01/01/2023:", ['Client_ID', 'Nom', 'Prenom'])

# Close the connection to the database
conn.close()

print("\nQueries executed and results saved to CSV files successfully!")
