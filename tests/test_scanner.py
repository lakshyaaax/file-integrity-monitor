from pathlib import Path

from hashing import calculate_hash
from scanner import scan_files


def test_modified_file():
    file_path = str(Path("protected/settings.txt"))

    baseline = {
        file_path: "fake_original_hash"
    }

    events = scan_files(baseline)

    assert ("MODIFIED", file_path) in events


def test_deleted_file():
    file_path = str(Path("protected/users.txt"))

    baseline = {
        file_path: "original_hash"
    }

    events = scan_files(baseline)

    assert ("DELETED", file_path) in events


def test_new_file():
    file_path = str(Path("protected/config.txt"))

    baseline = {}

    events = scan_files(baseline)

    assert ("NEW", file_path) in events


def test_unchanged_file():
    file_path = str(Path("protected/config.txt"))

    current_hash = calculate_hash(file_path)

    baseline = {
        file_path: current_hash
    }

    events = scan_files(baseline)

    assert ("MODIFIED", file_path) not in events
    assert ("NEW", file_path) not in events
    assert ("DELETED", file_path) not in events


def test_recursive_file_detection(tmp_path):
    from scanner import get_files

    nested_folder = tmp_path / "protected" / "system"
    nested_folder.mkdir(parents=True)

    test_file = nested_folder / "config.txt"
    test_file.write_text("test configuration")

    files = get_files(tmp_path / "protected")

    assert test_file in files