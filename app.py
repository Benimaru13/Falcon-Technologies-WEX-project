from flask import Flask, render_template_string
import sqlite3
import matplotlib
# This line is important on Windows — it tells matplotlib not to try
# opening a display window, since we're running inside a web server
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# Create the Flask app — think of this as turning the restaurant lights on
app = Flask(__name__)

def get_chart():
    """
    Reads the latest snapshot from the database and returns
    the chart as a base64-encoded image string.
    
    base64 is a way of converting binary image data (the PNG)
    into plain text so it can be embedded directly in a webpage
    without needing a separate image file.
    """
    conn = sqlite3.connect("brew_data.db")
    cursor = conn.cursor()

    # Get the most recent snapshot date
    cursor.execute("SELECT MAX(snapshot_date) FROM snapshots")
    latest_date = cursor.fetchone()[0]

    # Get the top 20 packages from that date
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

    # Build the chart
    plt.figure(figsize=(14, 7))
    plt.bar(range(20), counts, color="steelblue")
    plt.xticks(range(20), names, rotation=45, ha="right")
    plt.xlabel("Package Name")
    plt.ylabel("Install Events (last 30 days)")
    plt.title(f"Top 20 Most Installed Homebrew Packages — Snapshot: {latest_date}")
    plt.tight_layout()

    # Instead of saving to a file, we save to a memory buffer
    # Think of this as taking the chart and holding it in RAM
    # rather than writing it to your hard drive
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Convert the image bytes to a base64 string so we can
    # embed it directly into the HTML page
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return image_base64, latest_date


# This decorator tells Flask: "when someone visits the homepage (/),
# run this function and send back whatever it returns"
@app.route("/")
def index():
    image_base64, latest_date = get_chart()

    # render_template_string lets us write HTML directly in Python
    # {{ }} is how we insert Python variables into the HTML
    html = """
    <html>
    <head>
        <title>Homebrew Analytics Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }
            h1 { color: #333; }
            p { color: #666; }
            img { max-width: 100%; border: 1px solid #ddd; background: white; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Homebrew Analytics Dashboard</h1>
        <p>Showing latest snapshot: {{ latest_date }}</p>
        <img src="data:image/png;base64,{{ image_base64 }}">
    </body>
    </html>
    """
    return render_template_string(html, image_base64=image_base64, latest_date=latest_date)


# This block runs the web server when you execute this file directly
if __name__ == "__main__":
    # debug=True means Flask will show helpful error messages
    # and auto-restart when you change the code
    app.run(debug=True)
