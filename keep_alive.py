from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running", 200

def run():
    port = 8080
    repl_slug = os.environ.get('REPL_SLUG')
    repl_owner = os.environ.get('REPL_OWNER')
    if repl_slug and repl_owner:
        print("🔗 رابط المشروع: https://" + repl_slug + "." + repl_owner + ".repl.co")
    else:
        print("❌ لم يتم العثور على بيانات REPL. استخدم Deploy بدلاً من Run.")
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
