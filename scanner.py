from pathlib import Path

from hashing import calculate_hash
from logger import log_event


def get_files(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("[ERROR] Protected directory not found.")
        return None

    files = []

    for file in folder.iterdir():
        if file.is_file():
            files.append(file)

    return files


def create_file_hashes(folder_path):
    files = get_files(folder_path)

    if files is None:
        return None

    file_hashes = {}

    for file in files:
        file_hashes[str(file)] = calculate_hash(file)

    return file_hashes

def scan_files(baseline):
    current_hashes = create_file_hashes("protected")

    if current_hashes is None:
        return []

    events = []

    # Check for new, modified, and unchanged files
    for file, current_hash in current_hashes.items():

        if file not in baseline:
            print(f"+ NEW FILE: {file}")

            log_event(
                "NEW",
                file,
                new_hash=current_hash
            )

            events.append(("NEW", file))

        elif current_hash != baseline[file]:
            print(f"🚨 MODIFIED: {file}")

            log_event(
                "MODIFIED",
                file,
                old_hash=baseline[file],
                new_hash=current_hash
            )

            events.append(("MODIFIED", file))

        else:
            print(f"✓ OK: {file}")

    # Check for deleted files
    for file in baseline:

        if file not in current_hashes:
            print(f"❌ DELETED: {file}")

            log_event(
                "DELETED",
                file,
                old_hash=baseline[file]
            )

            events.append(("DELETED", file))

    return events