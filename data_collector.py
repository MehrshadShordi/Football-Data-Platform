import requests
import pandas
from datetime import datetime
import time

today_date = datetime.now().strftime("%Y%m%d")

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Referer": "https://www.fotmob.com/",
}


def fetch_page(url):
    try:
        response = requests.get(
            url=url,
            timeout=5,
            headers=header,
            params={
                "date": today_date,
                "timezone": None,
                "ccode3": None,
                "includeNextDayLateNight": "true",
            },
        )
        if response.status_code == 200:
            return response
        else:
            print(f"Status code Error : {response.status_code}")
            return None
    except requests.exceptions.ConnectTimeout:
        print("Can't Reach site")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection Error - Check Your network connection")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error : {e}")
        return None
    except requests.exceptions.ReadTimeout:
        print("Read timeout - try again")
        return None


def fetch_data():
    response = fetch_page("https://www.fotmob.com/api/data/matches")
    if response == None:
        print("Failed to fetch data from page")
        return
    data = response.json()
    leagues_list = []

    for leagues in data["leagues"]:
        ccode = leagues["ccode"]
        league_name = f'{ccode}-{leagues["name"]}'
        league_data = {
            "league_full": league_name,
            "league": leagues["name"],
            "league_id" : leagues["primaryId"],
            "matches": [],
        }

        for matches in leagues["matches"]:
            if matches["status"].get("reason"):
                reason = matches["status"]["reason"]["long"]
            elif matches["status"].get("ongoing"):
                reason = matches["status"]["liveTime"]["short"]
            elif matches["status"]["started"] == False:
                reason = "Not Started"
            else:
                reason = None

            match_data = {
                "home_id" : matches["home"]["id"],
                "home": matches["home"]["name"],
                "home_score": matches["home"]["score"],
                "away_id" : matches["away"]["id"],
                "away": matches["away"]["name"],
                "away_score": matches["away"]["score"],
                "time": matches["time"],
                "started": matches["status"]["started"],
                "finished": matches["status"]["finished"],
                "cancelled": matches["status"]["cancelled"],
                "reason": reason,
            }
            league_data["matches"].append(match_data)

        leagues_list.append(league_data)
    return leagues_list
    # with pandas.ExcelWriter("matches.xlsx") as writer:
    #     df = pandas.json_normalize(leagues_list, record_path="matches", meta=["league"])
    #     df.to_excel(writer, sheet_name="All Games", index=False)
    #     df = df[((df["home_score"] + df["away_score"]) > 3) & (df["finished"])]
    #     df.to_excel(writer, sheet_name="Over 3 Goals Games", index=False)
    #     df = df[
    #         (df["home_score"] == df["away_score"])
    #         & (df["finished"])
    #         & (df["cancelled"] == False)
    #     ]
    #     df.to_excel(writer, sheet_name="Draw Games", index=False)
    #     for league in leagues_list:
    #         df = pandas.DataFrame(league["matches"])
    #         df.to_excel(writer, sheet_name=league["league"][:31], index=False)

    # df = pandas.json_normalize(leagues_list, record_path="matches", meta=["league"])
    # print(f"All games : {len(df)}")
    # print(f"High score : ")
    # df["total_goals"] = df["home_score"] + df["away_score"]
    # high_score_match = df.loc[df["total_goals"].idxmax()]
    # print(high_score_match[["home", "home_score", "away", "away_score", "league"]])
    # draws = df[
    #     (df["home_score"] == df["away_score"])
    #     & (df["finished"] == True)
    #     & (df["cancelled"] == False)
    # ]
    # print(f"Draw Games : {len(draws)}")
    # print(f'Avg Goals P/G : {df["total_goals"].mean():.2f}')
