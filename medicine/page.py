import subprocess
import json

def pg(pg):
    data = json.dumps({"page": pg})  # Convert dictionary to JSON string

    subprocess.run([
        "curl", "-X", "POST", "https://baymax-ui.vercel.app/api/page-tracking",
        "-H", "Content-Type: application/json",
        "-d", data  # Pass properly formatted JSON data
    ])
pg(9)