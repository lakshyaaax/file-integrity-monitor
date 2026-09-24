from flask import Flask, render_template

from baseline import load_baseline
from scanner import create_file_hashes, scan_files
from database import get_events


app = Flask(__name__)


def get_dashboard_data(baseline, events):
    current_hashes = create_file_hashes("protected")

    if current_hashes is None:
        current_hashes = {}

    new_files = sum(
        1 for event in events
        if event[0] == "NEW"
    )

    modified_files = sum(
        1 for event in events
        if event[0] == "MODIFIED"
    )

    deleted_files = sum(
        1 for event in events
        if event[0] == "DELETED"
    )

    file_status = {}

    # Check files that currently exist
    for file, current_hash in current_hashes.items():

        if file not in baseline:
            status = "NEW"

        elif current_hash != baseline[file]:
            status = "MODIFIED"

        else:
            status = "OK"

        file_status[file] = status

    # Check deleted files
    for file in baseline:

        if file not in current_hashes:
            file_status[file] = "DELETED"

    return {
        "total_files": len(current_hashes),
        "new_files": new_files,
        "modified_files": modified_files,
        "deleted_files": deleted_files,
        "file_status": file_status
    }


@app.route("/")
def home():

    baseline = load_baseline()

    if baseline is None:
        return "Baseline not found. Please create a baseline first."

    # Check current status without creating new log entries
    events = scan_files(
        baseline,
        log_events=False
    )

    dashboard_data = get_dashboard_data(
        baseline,
        events
    )

    # Get historical events from SQLite
    event_history = get_events()

    return render_template(
        "index.html",
        events=events,
        dashboard=dashboard_data,
        event_history=event_history
    )


@app.route("/scan")
def scan():

    baseline = load_baseline()

    if baseline is None:
        return "Baseline not found. Please create a baseline first."

    # Perform real scan and save events
    events = scan_files(
        baseline,
        log_events=True
    )

    dashboard_data = get_dashboard_data(
        baseline,
        events
    )

    # Get historical events from SQLite
    event_history = get_events()

    return render_template(
        "index.html",
        events=events,
        dashboard=dashboard_data,
        event_history=event_history
    )


if __name__ == "__main__":
    app.run(debug=True)