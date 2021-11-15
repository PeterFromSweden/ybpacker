import datetime
import glob
import json
import os
import gpxpy
import numpy as np
from datetime import datetime


def rename(file_name):
    data = np.genfromtxt(file_name, delimiter=',')
    timestamp = int(np.max(data[:, 3]))
    tmp = file_name.split('.')
    tmp[0] = tmp[0].split(' ')[0]
    new_file_name = tmp[0] + '-' + str(timestamp) + '.' + tmp[1]
    try:
        os.rename(file_name, new_file_name)
    except FileExistsError:
        print("Removing " + file_name)
        os.remove(file_name)
        pass


def find_files(new=False):
    if new:
        # Remove dirs and expedition-*.txt
        file_list = glob.glob('expedition*.txt')
        file_list = [f for f in file_list if os.path.isfile(f) and f.find('-') == -1]
    else:
        file_list = glob.glob('expedition-*.txt')

    return file_list


def read_all():
    data = np.empty((0, 4), int)
    for file_name in find_files():
        data = np.append(data, np.genfromtxt(file_name, delimiter=','), axis=0)
    data = np.unique(data, axis=0)
    return data


def read_boats():
    boats = np.genfromtxt('boat-ids.txt', delimiter=',', dtype=None, encoding='utf8')
    boats = np.sort(boats, order=['f1'])
    return [list(boat) for boat in boats]


def write_gpx(data):
    gpx = gpxpy.gpx.GPX()
    boats = read_boats()

    gpx.name = 'ARC'
    gpx_bounds = gpxpy.gpx.GPXBounds()
    gpx_bounds.max_latitude = '30'
    gpx_bounds.min_latitude = '10'
    gpx_bounds.max_longitude = '-10'
    gpx_bounds.min_longitude = '-65'
    gpx.bounds = gpx_bounds
    gpx.time = datetime.utcnow()

    for boat in boats:
        boat_id = boat[0]
        boat_name = boat[1]

        boat_data = data[np.where(data[:, 0] == boat_id)]
        boat_data = boat_data[boat_data[:, 3].argsort()]

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = boat_name
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for position in boat_data:
            lat = position[1]
            lon = position[2]
            time_str = str(int(position[3]))
            time_stamp = datetime.strptime(time_str, "%y%m%d%H%M")  # 2111121200
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, 0.0, time=time_stamp))
            # gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, 0.0, time=time_stamp, name=boat_name))

    with open(expedition['gpx-filename'], 'w') as f:
        f.write(gpx.to_xml())


def main():
    for file_name in find_files(new=True):
        rename(file_name)

    data = read_all()
    write_gpx(data)
    # print(read_boats())


if __name__ == "__main__":
    with open('expedition.json', 'r') as f:
        expedition = json.load(f)
    os.chdir(expedition['folder'])
    main()

