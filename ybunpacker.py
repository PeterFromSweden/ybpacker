import json
import os
import pickle
import zlib
from datetime import datetime

import gpxpy
import gpxpy.gpx


def process_zlib(file_name):
    with open(file_name, 'rb') as f:
        pz = f.read()
    # os.rename(file_name, file_name.replace('.zlib', '.zbk'))
    p = zlib.decompress(pz)
    positions_speed = pickle.loads(p)

    adrena_file_name = file_name.replace('.zlib', '.txt')
    with open(adrena_file_name, 'w') as f:
        f.write('POSADRENA\n')
        for pos in positions_speed:
            f.write(';'.join(pos[0:5]))
            f.write('\n')

    with open(file_name.replace('.zlib', '.json'),'w') as f:
        json.dump(positions_speed,f)

def load_gpx():
    with open('TrackSpeed.gpx', 'r') as f:
        gpx = gpxpy.parse(f)
    print(gpx)
    # print('GPX:', gpx.to_xml())

    for track in gpx.tracks:
        print(track.name)
        for segment in track.segments:
            for point in segment.points:
                print(point.name)

    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name = "Plessur"
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    gpx_segment.points.append(
        gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, time=datetime(2009, 10, 17, 18, 37, 26), name='2.1kn 180'))
    gpx_segment.points.append(
        gpxpy.gpx.GPXTrackPoint(2.2235, 5.3235, time=datetime(2009, 10, 17, 20, 37, 26), name='2.1kn 180'))
    gpx_segment.points.append(
        gpxpy.gpx.GPXTrackPoint(2.4236, 5.4236, time=datetime(2009, 10, 17, 22, 37, 26), name='2.1kn 180'))
    with open('output.gpx', 'w') as f:
        f.write(gpx.to_xml())


if __name__ == "__main__":
    try:
        with open('pos_speed_list.p', 'rb') as f:
            pos_speed_list = pickle.load(f)
    except:
        pos_speed_list = []
    print(pos_speed_list)

    pos_speed_new = ['1', '2', '3', '4']
    pos_speed_list_new = []
    for pos_speed in pos_speed_list:
        if pos_speed not in pos_speed_list_new:
            pos_speed_list.append(pos_speed_new)

    with open('pos_speed_list.p', 'wb') as f:
        pickle.dump(pos_speed_list, f)

    # load_gpx()
    process_zlib('arcplus2021-11-11_1414.zlib')
