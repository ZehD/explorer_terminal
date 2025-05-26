import sqlite3

DATABASE_FILE = 'file_log.db'

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_path TEXT,
            dest_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_operation(file_name, operation_type, source_path=None, dest_path=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO file_operations (file_name, operation_type, source_path, dest_path)
        VALUES (?, ?, ?, ?)
    ''', (file_name, operation_type, source_path, dest_path))
    conn.commit()
    conn.close()
