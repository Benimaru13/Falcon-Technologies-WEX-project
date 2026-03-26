import requests
import sqlite3
import matplotlib.pyplot as plt
from datetime import date

URL = "https://formulae.brew.sh/api/analytics/install/30d.json"

def fetch_and_store():
    """
    Fetches a snapshot from the Homebrew API and stores
    every package record in the SQLite database.
    """
    print(f"Fetching data for {date.today()}...")

    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Request failed. Status code: {response.status_code}")
        return

    data = response.json()
    items = data["items"]

    conn = sqlite3.connect("brew_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT,
            formula TEXT,
            count INTEGER,
            percent REAL
        )
    """)

    today = str(date.today())

    for item in items:
        clean_count = int(item["count"].replace(",", ""))
        clean_percent = float(item["percent"])

        cursor.execute("""
            INSERT INTO snapshots (snapshot_date, formula, count, percent)
            VALUES (?, ?, ?, ?)
        """, (today, item["formula"], clean_count, clean_percent))

    conn.commit()
    conn.close()

    print(f"Done! {len(items)} records saved for {today}.")


def generate_chart():
    """
    Reads the most recent snapshot from the database
    and generates a bar chart of the top 20 packages.
    """
    conn = sqlite3.connect("brew_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(snapshot_date) FROM snapshots")
    latest_date = cursor.fetchone()[0]

    cursor.execute("""
        SELECT formula, count FROM snapshots
        WHERE snapshot_date = ?
        ORDER BY count DESC
        LIMIT 20
    """, (latest_date,))

    rows = cursor.fetchall()
    conn.close()

    names = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.figure(figsize=(14, 7))
    plt.bar(range(20), counts, color="steelblue")
    plt.xticks(range(20), names, rotation=45, ha="right")
    plt.xlabel("Package Name")
    plt.ylabel("Install Events (last 30 days)")
    plt.title(f"Top 20 Most Installed Homebrew Packages — Snapshot: {latest_date}")
    plt.tight_layout()
    plt.savefig("brew_chart.png")
    print("Chart saved as brew_chart.png")


# Run both jobs once, then exit cleanly.
# Windows Task Scheduler handles calling this script on a schedule.
fetch_and_store()
generate_chart()