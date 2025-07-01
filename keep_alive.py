from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running", 200

def run():
    # Render يمرّر رقم البورت في متغير PORT
    port = int(os.environ.get("PORT", 8080))
    print(f"🔗 Flask server running on port {port}")
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    Thread(target=run, daemon=True).start()
