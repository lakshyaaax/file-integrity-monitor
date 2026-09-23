import sys

from baseline import create_baseline, load_baseline
from scanner import scan_files


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py init | scan")
        return

    command = sys.argv[1]

    if command == "init":
        create_baseline()

    elif command == "scan":
        baseline = load_baseline()

        if baseline is None:
            return

        scan_files(baseline)

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()