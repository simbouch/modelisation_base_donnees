# Modélisation de Base de Données

Ce projet consiste à créer une base de données relationnelle à l'aide de **SQLite** pour la gestion des clients et des commandes. Le projet comprend la création de tables, l'importation de données depuis des fichiers CSV, et l'exécution de diverses requêtes SQL pour vérifier les données.

## Structure du Projet

- `my_database.db` : La base de données SQLite créée.
- `clients.csv` et `commandes.csv` : Fichiers CSV utilisés pour importer des données de clients et de commandes.
- `import_data.py` : Script Python pour importer les données des fichiers CSV dans la base de données.
- `equeries.py` : Script Python pour exécuter des requêtes SQL et vérifier les données.

## Étapes du Projet

### 1. Création de la Base de Données

La base de données a été créée avec les tables suivantes :

- **Client** : Informations sur les clients (ID, nom, prénom, email, etc.).
- **Commande** : Informations sur les commandes passées par les clients (ID de commande, date, montant, etc.).

### 2. Importation des Données

Les données ont été importées à partir de fichiers CSV (`clients.csv` et `commandes.csv`) en utilisant le script Python `import_data.py`. Ce script permet de lire les fichiers CSV et de remplir les tables de la base de données.

### 3. Exécution des Requêtes

Des requêtes SQL ont été exécutées pour vérifier l'intégrité des données et répondre à des questions spécifiques :

- **Clients ayant consenti à recevoir des communications marketing**.
- **Commandes passées par un client spécifique** (exemple avec l'ID client `1`).
- **Montant total des commandes pour le client avec l'ID `1`**.
- **Clients ayant passé des commandes de plus de 100 euros**.
- **Clients ayant passé des commandes après le `01/01/2023`**.

Ces requêtes peuvent être exécutées via le script `equeries.py`.



