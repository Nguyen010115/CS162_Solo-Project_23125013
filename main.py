from route_data.ClassBuild import (RouteVarQuery, PathQuery, StopQuery, lat_lng_to_xy, calculate_distance,
                                   calculate_distance_xy, newPath_Query)
import geopy.distance

query = RouteVarQuery('route_data/vars.json')




path_query = PathQuery('route_data/paths.json')

#x1, y1 = lat_lng_to_xy(106.70585632, 10.77678967)
#x2, y2 = lat_lng_to_xy(106.58197784, 10.97655869)
#print(calculate_distance(106.70585632, 10.77678967, 106.58197784, 10.97655869))

stop_query = StopQuery('route_data/stops.json')

pair_stop_path = []

for path in path_query.paths:
    for stop in stop_query.stop_routes:
        if path.get_route_id() == stop.get_route_id and path.get_route_var_id() == stop.get_route_var_id:
            pair_stop_path.append([stop, path])
            break

new_paths = newPath_Query(pair_stop_path)
new_paths.output_as_json('output_files/new_paths.json')












