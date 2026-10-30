from flask import Flask, render_template, jsonify
from data_collector import fetch_data
import time
from database import init_db, load_cache, save_cache
from datetime import datetime, timezone
import time

app = Flask(__name__)
leagues = []
last_fetch = 0
refresh_interval = 60
db_initialized = False


def refresh_data():
    global last_fetch, leagues

    now = time.time()
    if now - last_fetch >= refresh_interval:
        leagues_list = fetch_data()
        if leagues_list is not None:
            leagues = leagues_list
            last_fetch = now


# def refresh_data():
#     global leagues, last_fetch, db_initialized

#     try:
#         if not db_initialized:
#             init_db()
#             db_initialized = True

#         cached = load_cache()

#     except Exception:
#         app.logger.exception("Database read failed")
#         return leagues

#     if cached is not None:
#         cached_leagues, fetched_at = cached
#         leagues = cached_leagues

#         now = datetime.now(timezone.utc)
#         age = (now - fetched_at).total_seconds()

#         if age < refresh_interval:
#             return leagues

#     new_data = fetch_data()

#     if new_data is None:
#         return leagues

#     try:
#         save_cache(new_data)
#         leagues = new_data
#         last_fetch = time.time()

#     except Exception:
#         app.logger.exception("Database save failed")
#         leagues = new_data

#     return leagues


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
