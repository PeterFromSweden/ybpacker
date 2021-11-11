import os
import pickle
import zlib
import gpxpy
import gpxpy.gpx


def process_zlib(file_name):
    with open(file_name, 'rb') as f:
        pz = f.read()
    #os.rename(file_name, file_name.replace('.zlib', '.zbk'))
    p = zlib.decompress(pz)
    positions_speed = pickle.loads(p)

    adrena_file_name = file_name.replace('.zlib', '.txt')
    with open(adrena_file_name, 'w') as f:
        f.write('POSADRENA\n')
        for pos in positions_speed:
            f.write(';'.join(pos[0:5]))
            f.write('\n')


def load_gpx():
    with open('TrackSpeed.gpx', 'r') as f:
        gpx = gpxpy.parse(f)
    print(gpx)
    #print('GPX:', gpx.to_xml())

    for track in gpx.tracks:
        print(track.name)
        for segment in track.segments:
            for point in segment.points:
                print(point.name)

    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, elevation=1234, name='2.1kn 180'))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235, name='2.1kn 180'))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1236, 5.1236, elevation=1236, name='2.1kn 180'))
    with open('output.gpx', 'w') as f:
        f.write(gpx.to_xml())


if __name__ == "__main__":
    load_gpx()
    #process_zlib('arcplus2021-11-11_1155.zlib')
    # save_adrena()
