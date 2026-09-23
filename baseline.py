import json
from pathlib import Path

from scanner import create_file_hashes


def create_baseline():
    protected_folder = Path("protected")

    if not protected_folder.exists():
        print("[ERROR] Protected directory not found.")
        return

    file_hashes = create_file_hashes("protected")

    with open("baseline.json", "w") as file:
        json.dump(file_hashes, file, indent=4)

    print("Baseline created successfully!")


def load_baseline():
    baseline_file = Path("baseline.json")

    if not baseline_file.exists():
        print("[ERROR] Baseline file not found.")
        return None

    try:
        with open(baseline_file, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("[ERROR] Baseline file contains invalid JSON.")
        return None