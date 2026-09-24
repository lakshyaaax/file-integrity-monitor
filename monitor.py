import time

from baseline import load_baseline
from scanner import scan_files


SCAN_INTERVAL = 30


def monitor():

    print("======================================")
    print("   FILE INTEGRITY MONITOR")
    print("======================================")

    print(f"Monitoring protected/ every {SCAN_INTERVAL} seconds...")
    print("Press CTRL+C to stop.\n")

    baseline = load_baseline()

    if baseline is None:
        print("[ERROR] Baseline not found.")
        print("Create a baseline first using:")
        print("python main.py init")
        return

    try:

        while True:

            print("\n--------------------------------------")
            print("Running integrity scan...")
            print("--------------------------------------")

            events = scan_files(
                baseline,
                log_events=True
            )

            if events:
                print(f"\n⚠ {len(events)} security event(s) detected.")

            else:
                print("\n✓ No changes detected.")

            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:

        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    monitor()