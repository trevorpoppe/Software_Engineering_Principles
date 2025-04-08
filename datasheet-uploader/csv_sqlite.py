import pandas as pd
import sqlite3

# Function to upload CSV to SQLite
def upload_csv_to_sqlite(csv_file, db_name, table_name):
    # Step 1: Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    print(f"Loaded CSV data:\n{df.head()}\n")  # Display the first few rows for verification

    # Step 2: Connect to SQLite database (it creates the database if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Step 3: Create the table dynamically based on the CSV schema
    create_table_query = generate_create_table_query(df, table_name)
    cursor.execute(create_table_query)

    # Step 4: Insert data into the table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Data successfully inserted into the {table_name} table.")

    # Step 5: Commit and close the connection
    conn.commit()
    conn.close()

# Helper function to generate CREATE TABLE query from DataFrame
def generate_create_table_query(df, table_name):
    # Mapping DataFrame columns to SQLite data types
    columns_with_types = ', '.join([f"{col} {map_data_type(df[col].dtype)}" for col in df.columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
    return create_table_query

# Helper function to map pandas data types to SQLite types
def map_data_type(pandas_dtype):
    if pandas_dtype == 'int64':
        return 'INTEGER'
    elif pandas_dtype == 'float64':
        return 'REAL'
    elif pandas_dtype == 'object':
        return 'TEXT'
    else:
        return 'TEXT'  # Default to TEXT for unknown types

# Example of how to call the function
csv_file = 'your_file.csv'  # Path to your CSV file
db_name = 'bookkeeper.db'   # SQLite database file name
table_name = 'example_table'  # Name of the table to create or update

# Upload CSV to SQLite
upload_csv_to_sqlite(csv_file, db_name, table_name)
