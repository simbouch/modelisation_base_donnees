from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import csv
from sqlalchemy import func
import os

# Define the base class for SQLAlchemy models
Base = declarative_base()

# File paths for CSV data
clients_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\clients.csv'
commandes_file = r'C:\data\simplon_dev_ia_projects\modelisation_base_donnees\commandes.csv'

# Define the Client model
class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
    date_naissance = Column(Date, nullable=True)
    adresse = Column(String, nullable=True)
    consentement_marketing = Column(Boolean, nullable=False)
    
    commandes = relationship('Commande', back_populates='client')

# Define the Commande model
class Commande(Base):
    __tablename__ = 'Commande'
    id = Column(Integer, primary_key=True)
    date_commande = Column(Date, nullable=False)
    montant_commande = Column(Float, nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)

    client = relationship('Client', back_populates='commandes')

# Create the database engine and session
engine = create_engine('sqlite:///my_database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Import client data
if os.path.exists(clients_file):
    with open(clients_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                client = Client(
                    nom=row['Nom'],
                    prenom=row['Prénom'],  # Corrected to match CSV header
                    email=row['Email'],
                    telephone=row.get('Téléphone', None),  # Corrected to match CSV header
                    date_naissance=datetime.strptime(row['Date_Naissance'], '%Y-%m-%d').date() if row['Date_Naissance'] else None,
                    adresse=row.get('Adresse', None),
                    consentement_marketing=bool(int(row['Consentement_Marketing']))
                )
                session.add(client)
            except Exception as e:
                print(f"Error adding client '{row['Nom']} {row['Prénom']}': {e}")

    # Commit the transaction for clients
    try:
        session.commit()
        print("Client data committed successfully.")
    except Exception as e:
        print(f"Error committing client data: {e}")
        session.rollback()
else:
    print(f"Clients file not found at: {clients_file}")

# Import commandes data
if os.path.exists(commandes_file):
    with open(commandes_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                commande = Commande(
                    date_commande=datetime.strptime(row['Date_Commande'], '%Y-%m-%d').date(),
                    montant_commande=float(row['Montant_Commande']),
                    client_id=int(row['Client_ID'])
                )
                session.add(commande)
            except Exception as e:
                print(f"Error adding commande on '{row['Date_Commande']}': {e}")

    # Commit the transaction for commandes
    try:
        session.commit()
        print("Commande data committed successfully.")
    except Exception as e:
        print(f"Error committing commande data: {e}")
        session.rollback()
else:
    print(f"Commandes file not found at: {commandes_file}")

# Queries for requested information

# 1. Clients who have consented to receive marketing communications
clients_with_consent = session.query(Client).filter(Client.consentement_marketing == True).all()
print("\nClients with marketing consent:")
for client in clients_with_consent:
    print(f"{client.id}: {client.nom} {client.prenom}")

# 2. Orders of a specific client (e.g., client ID 61)
client_id = 61
commandes_of_client = session.query(Commande).filter(Commande.client_id == client_id).all()
print(f"\nOrders of client ID {client_id}:")
for commande in commandes_of_client:
    print(f"Commande ID: {commande.id}, Date: {commande.date_commande}, Amount: {commande.montant_commande}")

# 3. Total amount of orders for the client with ID 61
total_amount = session.query(func.sum(Commande.montant_commande)).filter(Commande.client_id == client_id).scalar()
print(f"\nTotal amount of orders for client ID {client_id}: {total_amount} euros")

# 4. Clients who have placed orders over 100 euros
clients_with_large_orders = session.query(Client).join(Commande).filter(Commande.montant_commande > 100).distinct().all()
print("\nClients with orders over 100 euros:")
for client in clients_with_large_orders:
    print(f"{client.id}: {client.nom} {client.prenom}")

# 5. Clients who have placed orders after 01/01/2023
after_date = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
clients_with_recent_orders = session.query(Client).join(Commande).filter(Commande.date_commande > after_date).distinct().all()
print("\nClients with orders after 01/01/2023:")
for client in clients_with_recent_orders:
    print(f"{client.id}: {client.nom} {client.prenom}")

# Close the session
session.close()
print("Database session closed.")
