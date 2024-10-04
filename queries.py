import sqlite3

# Se connecter à la base de données SQLite
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Requête 1 : Clients ayant consenti à recevoir des communications marketing
print("Clients ayant consenti à recevoir des communications marketing :")
cursor.execute("SELECT * FROM Client WHERE Consentement_Marketing = 1")
clients_consent_marketing = cursor.fetchall()
for client in clients_consent_marketing:
    print(client)

# Requête 2 : Commandes du client avec ID 1
client_id = 1
print(f"\nCommandes pour le client avec ID {client_id} :")
cursor.execute("SELECT * FROM Commande WHERE Client_ID = ?", (client_id,))
commandes_pour_client = cursor.fetchall()
for commande in commandes_pour_client:
    print(commande)

# Requête 3 : Montant total des commandes du client avec ID 1
print(f"\nMontant total des commandes pour le client avec ID {client_id} :")
cursor.execute("SELECT SUM(Montant_Commande) AS Total_Montant FROM Commande WHERE Client_ID = ?", (client_id,))
montant_total = cursor.fetchone()[0]
print(montant_total)

# Requête 4 : Clients ayant passé des commandes de plus de 100 euros
print("\nClients ayant passé des commandes de plus de 100 euros :")
cursor.execute('''
    SELECT DISTINCT Client.*
    FROM Client
    JOIN Commande ON Client.Client_ID = Commande.Client_ID
    WHERE Commande.Montant_Commande > 100
''')
clients_plus_100 = cursor.fetchall()
for client in clients_plus_100:
    print(client)

# Requête 5 : Clients ayant passé des commandes après le 01/01/2023
print("\nClients ayant passé des commandes après le 01/01/2023 :")
cursor.execute('''
    SELECT DISTINCT Client.*
    FROM Client
    JOIN Commande ON Client.Client_ID = Commande.Client_ID
    WHERE Date_Commande > '2023-01-01'
''')
clients_apres_2023 = cursor.fetchall()
for client in clients_apres_2023:
    print(client)

# Fermer la connexion
conn.close()
