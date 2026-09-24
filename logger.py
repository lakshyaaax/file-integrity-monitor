from datetime import datetime

from database import initialize_database, save_event


# Make sure the database exists
initialize_database()


def log_event(event_type, file_path, old_hash=None, new_hash=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{timestamp} | {event_type} | {file_path}"

    if old_hash:
        log_entry += f" | OLD: {old_hash}"

    if new_hash:
        log_entry += f" | NEW: {new_hash}"

    log_entry += "\n"

    # Save to text log
    with open("security_events.log", "a") as file:
        file.write(log_entry)

    # Save to SQLite database
    save_event(
        event_type,
        file_path,
        old_hash,
        new_hash
    )