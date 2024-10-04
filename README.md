# Modélisation de Base de Données

Ce projet consiste à créer une base de données relationnelle à l'aide de **SQLite** et à utiliser **SQLAlchemy** pour la gestion des clients et des commandes. Le projet comprend la création de tables, l'importation de données depuis des fichiers CSV, l'application de mesures de protection des données sensibles, et l'exécution de diverses requêtes SQL pour vérifier les données.

## Structure du Projet

- `my_database.db` : La base de données SQLite créée.
- `clients.csv` et `commandes.csv` : Fichiers CSV utilisés pour importer des données de clients et de commandes.
- `import_data.py` : Script Python pour importer les données des fichiers CSV dans la base de données.
- `secure_import.py` : Script Python pour importer de manière sécurisée les données chiffrées et pseudonymisées.
- `orm_sqlalchemy.py` : Script utilisant SQLAlchemy pour importer les données et exécuter des requêtes.
- `equeries.py` : Script Python pour exécuter des requêtes SQL et vérifier les données.
- `data_protection.py` : Module qui gère le chiffrement et la pseudonymisation des données sensibles.
- `clients_marketing.csv`, `clients_with_large_orders.csv`, `clients_with_recent_orders.csv`, `orders_for_client_61.csv`, `total_order_amount_client_61.csv` : Fichiers CSV générés à partir des résultats des requêtes.

## Étapes du Projet

### 1. Création de la Base de Données

La base de données a été créée avec les tables suivantes :

- **Client** : Informations sur les clients (ID, nom, prénom, email, etc.).
- **Commande** : Informations sur les commandes passées par les clients (ID de commande, date, montant, etc.).

### 2. Importation des Données

Les données ont été importées à partir de fichiers CSV (`clients.csv` et `commandes.csv`) en utilisant deux méthodes :

- **Importation simple** avec le script `import_data.py`.
- **Importation sécurisée** avec chiffrement et pseudonymisation des données sensibles via le script `secure_import.py`. Ce script utilise la bibliothèque `cryptography` pour chiffrer des champs comme le nom, prénom, email, téléphone, et adresse, et pseudonymise la date de naissance.

### 3. Utilisation de SQLAlchemy

Le script `orm_sqlalchemy.py` utilise **SQLAlchemy** pour définir des modèles ORM et interagir avec la base de données. Cela permet de travailler avec les objets Python et de simplifier les opérations sur la base de données, telles que l'importation de données et les requêtes.

### 4. Exécution des Requêtes

Des requêtes SQL ont été exécutées pour vérifier l'intégrité des données et répondre à des questions spécifiques :

- **Clients ayant consenti à recevoir des communications marketing**.
- **Commandes passées par un client spécifique** (exemple avec l'ID client `61`).
- **Montant total des commandes pour le client avec l'ID `61`**.
- **Clients ayant passé des commandes de plus de 100 euros**.
- **Clients ayant passé des commandes après le `01/01/2023`**.

Les résultats des requêtes sont affichés et enregistrés dans des fichiers CSV pour un examen ultérieur. Ces requêtes peuvent être exécutées via le script `equeries.py` pour la méthode directe, ou via `orm_sqlalchemy.py` pour la méthode ORM.

## Sécurité des Données

Conformément au RGPD, certaines données sensibles des clients (nom, prénom, email, etc.) sont protégées de la manière suivante :

- **Chiffrement** : Utilisé pour protéger les données sensibles au sein de la base de données (ex. : nom, prénom, email, téléphone, adresse). Le chiffrement est implémenté avec la bibliothèque `cryptography`.
- **Pseudonymisation** : La date de naissance est pseudonymisée à l'aide de la fonction de hachage SHA-256 pour empêcher toute identification directe d'une personne à partir de cette information.

Ces fonctionnalités sont implémentées dans le module `data_protection.py` et utilisées dans `secure_import.py` pour garantir la conformité avec les normes de protection des données.

## Exécution du Projet

Pour exécuter ce projet :

1. Créez et activez un environnement virtuel Python.
2. Installez les dépendances en utilisant la commande :
   ```sh
   pip install -r requirements.txt
