import sqlite3

# Create a connection to the database file
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
import csv

def import_csv_to_database(csv_filename):
    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        
        # Read the header row
        header = next(csv_reader)
        
        # Create the table based on the header columns
        table_name = 'products'  # Adjust table name as per your requirement
        columns = ','.join(header)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(create_table_query)
        
        # Insert data rows into the table
        insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?']*len(header))})"
        for row in csv_reader:
            cursor.execute(insert_query, row)
        
        # Commit the changes to the database
        conn.commit()
