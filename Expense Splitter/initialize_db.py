import sqlite3

# Define the database path
DB_PATH = 'expenses.db'

# Initialize the database and create the table if it doesn't exist
def init_db():
    # Connect to the database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the expenses table with equal and custom split functionality
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL,
            participants TEXT,
            split_amount TEXT  -- Store the split amounts as a comma-separated string
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Database '{DB_PATH}' initialized successfully.")

# Run the script
if __name__ == '__main__':
    init_db()
