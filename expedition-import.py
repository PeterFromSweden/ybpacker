import datetime
import glob
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
    except Exception as err:
        print("Warning " + err)
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
    with open('boatids.txt', 'r') as f:
        boats = f.read().split('\n')
    return [boat.split(',') for boat in boats if len(boat)]


def write_gpx(data):
    gpx = gpxpy.gpx.GPX()
    boats = read_boats()
    for boat in boats:
        boat_id = int(boat[0])
        boat_name = boat[1]

        boat_data = data[np.where(data[:, 0] == boat_id)]
        boat_data = boat_data[boat_data[:, 3].argsort()]

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = boat_name
        gpx.tracks.append(gpx_track)

        for position in boat_data:
            lat = position[1]
            lon = position[2]
            time_str = str(int(position[3]))
            time_stamp = datetime.strptime(time_str, "%y%m%d%H%M")  # 2111121200
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, 0.0, time=time_stamp))

    with open('output.gpx', 'w') as f:
        f.write(gpx.to_xml())


def main():
    for file_name in find_files(new=True):
        rename(file_name)

    data = read_all()
    write_gpx(data)


if __name__ == "__main__":
    main()
