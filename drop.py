import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Drop each user-defined table (skip sqlite_sequence)
for table in tables:
    if table[0] != 'sqlite_sequence':
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
        print(f"Table '{table[0]}' dropped.")

# Commit changes and close the connection
conn.commit()
conn.close()

print("All user-defined tables have been removed.")
