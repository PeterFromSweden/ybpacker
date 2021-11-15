from datetime import datetime
import json
import requests
import lat_lon_parser

from send_mail import send_mail


def download(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('unable to download ' + url)
        raise ValueError
    return response.text


def get_boat():
    response = download("https://yb.tl/l/" + ybmarinetraffic['race'] + "?class=allboats")
    resp2 = "\n".join(response.split("\n")[4:])  # Skip first 4 lines
    leaderboard = [item.split(",") for item in resp2.split("\n") if len(item)]
    boat = [boat for boat in leaderboard if boat[1] == ybmarinetraffic['boatname']]
    if len(boat):
        boat = boat[0]
    return boat


def main():
    boat = get_boat()
    if len(boat) == 0:
        print('Boat ' + ybmarinetraffic['boatname'] + " is not found in " + ybmarinetraffic['race'])
        return
    time_stamp = datetime.strptime(boat[3], "%d/%m/%Y %H:%M:%S")  # 12/11/2021 16:00:05
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")  # 2021-10-24 19:15:03
    lat = str(lat_lon_parser.parse(boat[4]))
    lon = str(lat_lon_parser.parse(boat[5]))
    cog = boat[6]
    sog = boat[7]
    secrets['to'] = ybmarinetraffic['To']
    message = "MMSI=" + ybmarinetraffic['MMSI'] + '\n'
    message = message + "LAT=" + lat + '\n'
    message = message + "LON=" + lon + '\n'
    message = message + "SPEED=" + sog + '\n'
    message = message + "COURSE=" + cog + '\n'
    message = message + "TIMESTAMP=" + time_stamp + '\n'
    print(message)
    send_mail(secrets, 'Report', message)
    print("Mail sent to: " + secrets['to'])

if __name__ == "__main__":
    with open('secrets.json', 'r') as f:
        secrets = json.load(f)
    with open('ybmarinetraffic.json', 'r') as f:
        ybmarinetraffic = json.load(f)
    main()
