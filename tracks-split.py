import gpxpy


if __name__ == "__main__":
    with open('Arctracks.gpx', 'r') as f:
        gpx = gpxpy.parse(f)

    for track in gpx.tracks:
        boat_gpx = gpxpy.gpx.GPX()
        boat_gpx.name = track.name
        boat_gpx.time = gpx.time

        gpx_bounds = gpxpy.gpx.GPXBounds()
        gpx_bounds.max_latitude = '30'
        gpx_bounds.min_latitude = '10'
        gpx_bounds.max_longitude = '-10'
        gpx_bounds.min_longitude = '-65'
        boat_gpx.bounds = gpx_bounds

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track = track
        boat_gpx.tracks.append(gpx_track)

        # for segment in track.segments:
            # print(segment.)
            # for point in segment.points:
                # print('{0},{1},{2}'.format(point.latitude, point.longitude, point.time))

        with open('Tracks/' + track.name + '.gpx', 'w') as f:
            f.write(boat_gpx.to_xml())

