import sqlite3
import pandas as pd
import openai
import logging

# Set up OpenAI API key (get your own API key from OpenAI)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up error logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Load CSV into SQLite (from Step 1)
def load_csv_to_sqlite(csv_file, db_name, table_name):
    try:
        # Load CSV file into pandas DataFrame
        df = pd.read_csv(csv_file)
        print(f"Loaded CSV data:\n{df.head()}\n")

        # Connect to SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Generate CREATE TABLE query and create table
        create_table_query = generate_create_table_query(df, table_name)
        cursor.execute(create_table_query)

        # Insert data into the table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data inserted into {table_name} table.")

        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Error during CSV loading: {e}")
        print(f"Error during CSV loading. Check 'error_log.txt' for details.")

# Step 2: Generate CREATE TABLE query from DataFrame (from Step 2)
def generate_create_table_query(df, table_name):
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
        return 'TEXT'

# Step 3: Handle Schema Conflicts (from Step 3)
def load_csv_to_sqlite_with_conflict_handling(csv_file, db_name, table_name):
    try:
        # Load CSV file into pandas DataFrame
        df = pd.read_csv(csv_file)
        print(f"Loaded CSV data:\n{df.head()}\n")

        # Connect to SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Check if table exists
        if table_exists(cursor, table_name):
            print(f"Table '{table_name}' already exists.")
            handle_schema_conflict(cursor, df, table_name)
        else:
            create_and_insert_table(cursor, df, table_name)

        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Error during CSV loading and table creation: {e}")
        print(f"Error during CSV loading. Check 'error_log.txt' for details.")

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    return cursor.fetchone() is not None

def handle_schema_conflict(cursor, df, table_name):
    print("Select an option to resolve the schema conflict:")
    print("1: Overwrite table")
    print("2: Rename existing table")
    print("3: Skip creation")

    option = input("Enter your choice (1/2/3): ").strip()

    if option == '1':  # Overwrite the table
        print(f"Overwriting table '{table_name}'...")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        create_and_insert_table(cursor, df, table_name)

    elif option == '2':  # Rename the existing table
        new_table_name = input("Enter a new name for the existing table: ").strip()
        print(f"Renaming table '{table_name}' to '{new_table_name}'...")
        cursor.execute(f"ALTER TABLE {table_name} RENAME TO {new_table_name}")
        create_and_insert_table(cursor, df, table_name)

    elif option == '3':  # Skip the creation
        print(f"Skipping table creation for '{table_name}'.")

    else:
        print("Invalid option selected. Skipping the operation.")

def create_and_insert_table(cursor, df, table_name):
    create_table_query = generate_create_table_query(df, table_name)
    cursor.execute(create_table_query)
    df.to_sql(table_name, cursor.connection, if_exists='replace', index=False)
    print(f"Data inserted into the {table_name} table.")

# Step 4: Simulate AI Interaction with CLI (from Step 4)
def start_cli(db_name):
    while True:
        print("\n--- AI Bookkeeper CLI ---")
        print("1: Load CSV into Database")
        print("2: Run SQL Query")
        print("3: List Tables")
        print("4: Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            csv_file = input("Enter the CSV file path: ").strip()
            table_name = input("Enter the table name: ").strip()
            load_csv_to_sqlite_with_conflict_handling(csv_file, db_name, table_name)

        elif choice == '2':
            sql_query = input("Enter your SQL query: ").strip()
            execute_sql_query(db_name, sql_query)

        elif choice == '3':
            list_tables(db_name)

        elif choice == '4':
            print("Exiting the application...")
            break

        else:
            print("Invalid option. Please try again.")

def execute_sql_query(db_name, sql_query):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()

        if sql_query.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.close()

    except Exception as e:
        print(f"Error executing query: {e}")

def list_tables(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            print("No tables found.")
        conn.close()

    except Exception as e:
        print(f"Error listing tables: {e}")

# Step 5: Enable AI-powered interaction (from Step 5)
def generate_sql_from_ai(query):
    prompt = f"Generate an SQL query based on the following description: {query}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate model
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )
        sql_query = response.choices[0].text.strip()
        print(f"Generated SQL query: {sql_query}")
        return sql_query
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None

def execute_sql_query_from_ai(db_name, query):
    sql_query = generate_sql_from_ai(query)
    
    if sql_query:
        execute_sql_query(db_name, sql_query)

def ai_interaction(db_name):
    while True:
        print("\n--- AI Bookkeeper Chat ---")
        query = input("Enter your question (or type 'exit' to quit): ").strip()

        if query.lower() == 'exit':
            print("Exiting the chat...")
            break

        execute_sql_query_from_ai(db_name, query)

def main():
    db_name = 'bookkeeper.db'

    while True:
        print("\n🎯 Welcome to AI Bookkeeper")
        print("1: Use Command Line Interface (CLI)")
        print("2: Chat with AI to generate SQL")
        print("3: Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            start_cli(db_name)
        elif choice == '2':
            ai_interaction(db_name)
        elif choice == '3':
            print("👋 Exiting. Have a great day!")
            break
        else:
            print("❌ Invalid input. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
