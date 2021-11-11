import sys
import json
import pickle
import zlib
import requests
from datetime import datetime
from send_mail import send_mail


def download(url):
    resonse = requests.get(url)
    if resonse.status_code != 200:
        print('unable to download ' + url)
        raise ValueError
    return resonse.text


def main(argv):
    if len(argv) < 2:
        print("Race missing")
        raise ValueError
    race = argv[1]

    response = download("https://yb.tl/" + race + "-boatids.txt")
    boatlist = dict(item.split(",") for item in response.split("\n") if len(item))

    response = download("https://yb.tl/l/" + race + "?class=allboats")
    resp2 = "\n".join(response.split("\n")[4:]) # Skip first 4 lines
    leaderboard = [item.split(",") for item in resp2.split("\n") if len(item)]

    response = download("https://yb.tl/" + race + "-adrena.txt")
    resp2 = "\n".join(response.split("\n")[1:])  # Skip first line
    positions = [item.split(";") for item in resp2.split("\n") if len(item)]

    positions_speed = []
    for boat in positions:
        boat_id = boat[1]
        boat_name = boatlist[boat_id]
        boat_speed = [item[6:8] for item in leaderboard if item[1] == boat_name][0]
        positions_speed.append(boat + boat_speed)

    now = datetime.utcnow()
    filename = race + '-' + now.strftime('%m-%d_%H%M') + '.zlib'

    p = pickle.dumps(positions_speed)
    pz = zlib.compress(p)
    with open(filename, 'wb') as f:
        f.write(pz)

    send_mail(secrets, "Auto", "", [filename])


if __name__ == "__main__":
    # arg: <yb-racename, ex arcplus2021>
    with open('secrets.json', 'r') as f:
        secrets = json.load(f)
    main(sys.argv)
