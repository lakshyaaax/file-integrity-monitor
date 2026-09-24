import sqlite3
from datetime import datetime


DATABASE = "events.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            old_hash TEXT,
            new_hash TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_event(event_type, file_path, old_hash=None, new_hash=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO security_events
        (timestamp, event_type, file_path, old_hash, new_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (
        timestamp,
        event_type,
        file_path,
        old_hash,
        new_hash
    ))

    connection.commit()
    connection.close()


def get_events():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, event_type, file_path, old_hash, new_hash
        FROM security_events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()

    connection.close()

    return events