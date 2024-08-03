from flask import Flask, render_template, redirect
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return 'Alive'

@app.route('/eglink/<path:path>')
def redirect_to_epic_games(path):
    target_url = f"com.epicgames.launcher://store/{path}"
    return render_template('redirect.html', target_url=target_url)
def run():
    app.run(host='0.0.0.0', port=56565)

def keep_alive():
    t = Thread(target=run)
    t.start()
