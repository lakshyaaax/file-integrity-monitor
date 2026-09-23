import hashlib

from hashing import calculate_hash


def test_calculate_hash():
    expected_hash = hashlib.sha256(
        open("protected/config.txt", "rb").read()
    ).hexdigest()

    actual_hash = calculate_hash("protected/config.txt")

    assert actual_hash == expected_hash