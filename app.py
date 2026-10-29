from flask import Flask, render_template,jsonify
from data_collector import fetch_data
import time

app = Flask(__name__)
leagues  = []
last_fetch = 0
refresh_interval = 15*60

def refresh_data():
    global last_fetch , leagues

    now = time.time()
    if now - last_fetch >= refresh_interval:
        leagues_list = fetch_data()
        if leagues_list is not None:
            leagues = leagues_list
            last_fetch = now

@app.route("/")
def home():
    refresh_data()
    return render_template("index.html", leagues=leagues)

@app.route("/api/matches")
def get_matches():
    refresh_data()
    return jsonify(leagues)



if __name__ == "__main__":
    app.run(debug=True)

