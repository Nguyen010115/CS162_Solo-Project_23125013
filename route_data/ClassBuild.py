import json
import csv
import pyproj
from math import radians, cos, sin, sqrt, atan2
import heapq
from decimal import Decimal


def calculate_distance_xy(x1, y1, x2, y2):
    # Using Haversine formula to calculate distance between two points
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def lat_lng_to_xy(longitude, latitude):
    # Define the projection from geographic coordinates (lat/lon) to Cartesian (x/y)
    projection = pyproj.Proj(proj='merc', ellps='WGS84')

    # Convert lat/lon to x/y
    x, y = projection(longitude, latitude)

    return x, y


def calculate_distance(lng1, lat1, lng2, lat2):
    # Using Haversine formula to calculate distance between two points
    R = 6371000  # Radius of the Earth in meters
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])  # Convert degrees to radians
    dlat = lat2 - lat1
    dlon = lng2 - lng1
    a = (dlat / 2) ** 2 + cos(lat1) * cos(lat2) * (dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


class RouteVar:

    def __init__(self, data_dictionary):
        self._route_id = data_dictionary['RouteId']
        self._route_var_id = data_dictionary['RouteVarId']
        self._route_var_name = data_dictionary['RouteVarName']
        self._route_var_short_name = data_dictionary['RouteVarShortName']
        self._route_no = data_dictionary['RouteNo']
        self._start_stop = data_dictionary['StartStop']
        self._end_stop = data_dictionary['EndStop']
        self._distance = data_dictionary['Distance']
        self._out_bound = data_dictionary['Outbound']
        self._running_time = data_dictionary['RunningTime']
        self.data_list = data_dictionary

    def getter(self, properties):
        return self.data_list[properties]

    @property
    def route_id(self):
        return self._route_id

    @route_id.setter
    def route_id(self, value):
        self._route_id = value
        self.data_list['RouteId'] = value

    @property
    def route_var_id(self):
        return self._route_var_id

    @route_var_id.setter
    def route_var_id(self, value):
        self._route_var_id = value
        self.data_list['RouteVarId'] = value

    @property
    def route_var_name(self):
        return self._route_var_name

    @route_var_name.setter
    def route_var_name(self, value):
        self._route_var_name = value
        self.data_list['RouteVarName'] = value

    @property
    def route_var_short_name(self):
        return self._route_var_short_name

    @route_var_short_name.setter
    def route_var_short_name(self, value):
        self._route_var_short_name = value
        self.data_list['RouteVarShortName'] = value

    @property
    def route_no(self):
        return self._route_no

    @route_no.setter
    def route_no(self, value):
        self._route_no = value
        self.data_list['RouteNo'] = value

    @property
    def start_stop(self):
        return self._start_stop

    @start_stop.setter
    def start_stop(self, value):
        self._start_stop = value
        self.data_list['StartStop'] = value

    @property
    def end_stop(self):
        return self._end_stop

    @end_stop.setter
    def end_stop(self, value):
        self._end_stop = value
        self.data_list['EndStop'] = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
        self.data_list['Distance'] = value

    @property
    def out_bound(self):
        return self._out_bound

    @out_bound.setter
    def out_bound(self, value):
        self._out_bound = value
        self.data_list['Outbound'] = value

    @property
    def running_time(self):
        return self._running_time

    @running_time.setter
    def running_time(self, value):
        self._running_time = value
        self.data_list['RunningTime'] = value


class RouteVarQuery:
    property_list = ["RouteId", "RouteVarId", "RouteVarName", "RouteVarShortName",
                     "RouteNo", "StartStop", "EndStop", "Distance", "Outbound", "RunningTime"]

    def __init__(self, json_file):
        self.route_vars = []
        try:
            with open(json_file, 'r', encoding='utf8') as f:
                for line in f:
                    v = json.loads(line)
                    for data in v:
                        self.route_vars.append(RouteVar(data))
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def search_by_properties(self, properties, search_data):
        data = []
        if properties in self.property_list:
            for var in self.route_vars:
                if str(var.data_list[properties]).lower() == str(search_data).lower():
                    data.append(
                        ['Id: ' + var.data_list['RouteId'], 'Name: ' + var.data_list['RouteVarName'],
                         'Short Name' + var.data_list['RouteVarShortName']])
            return data
        else:
            print("There is no property found")

    def output_as_json(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf8') as jsonfile:
                for route_var in self.route_vars:
                    json.dump(route_var.data_list, jsonfile, ensure_ascii=False)
                    jsonfile.write('\n')
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def output_as_csv(self, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.route_vars[0].data_list)
                for var in self.route_vars:
                    ss = []
                    for com in var.data_list:
                        ss.append(var.data_list[com])
                    writer.writerow(ss)
        except Exception as e:
            print("An error occurred while opening the file:", e)


class Stop:
    def __init__(self, data_array):
        self._stop_id_list = data_array['Stops']
        self._route_id = data_array['RouteId']
        self._route_var_id = data_array['RouteVarId']
        self.data_list = data_array

    def get_coordinates(self):
        coordinates = []
        for var in self._stop_id_list:
            coordinates.append([var['Lng'], var['Lat'], var["StopId"]])
        return coordinates

    @property
    def get_stop_id_list(self):
        id_list = []
        for stop in self._stop_id_list:
            id_list.append(stop["StopId"])
        return id_list

    def get_stops_list(self):
        return self._stop_id_list

    @get_stop_id_list.setter
    def get_stop_id_list(self, list_of_stops):
        self._stop_id_list = list_of_stops

    @property
    def get_route_id(self):
        return self._route_id

    @get_route_id.setter
    def get_route_id(self, value):
        self._route_id = value

    @property
    def get_route_var_id(self):
        return self._route_var_id

    @get_route_var_id.setter
    def get_route_var_id(self, value):
        self._route_var_id = value


class StopQuery:
    stops_property = ["StopId", "Code", "Name", "StopType", "Zone", "Ward", "AddressNo", "Street", "SupportDisability",
                      "Status", "Lng", "Lat", "Search", "Routes"]

    def __init__(self, json_file):
        self.stop_routes = []
        try:
            with open(json_file, 'r', encoding='utf8') as f:
                for line in f:
                    v = json.loads(line)
                    self.stop_routes.append(Stop(v))
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def stop_id_list(self):
        id_list = []
        appear = set()
        for stop in self.stop_routes:
            for stop_id in stop.get_stops_list():
                if stop_id["StopId"] in appear:
                    continue
                else:
                    appear.add(stop_id["StopId"])
                    id_list.append({"StopId": stop_id["StopId"], "Lng": stop_id["Lng"], "Lat": stop_id["Lat"]})
        return id_list

    def belongings(self, stop_id: int):
        list1 = []
        for stop in self.stop_routes:
            if stop_id in stop.get_stop_id_list:
                list1.append([stop.get_route_id, stop.get_route_var_id])
        return list1

    def search_by_properties(self, properties, search_data):
        datas = []
        if properties == "RouteId" or properties == "RouteVarId":
            for var in self.stop_routes:
                if var.data_list[properties] == str(search_data):
                    datas.append([var.data_list['RouteId'], var.data_list['RouteVarId']])
            return datas
        elif properties in self.stops_property:
            for var in self.stop_routes:
                for stop_id in var.get_stop_id_list:
                    if str(stop_id[properties]) == str(search_data):
                        datas.append(['Stop Id: ' + str(stop_id['StopId']), "Code: " + stop_id['Code'],
                                      'Route Id: ' + str(var.get_route_id),
                                      'Route Var Id: ' + str(var.get_route_var_id)])
            return datas
        else:
            print("There is no property found")

    def output_as_json(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf8') as jsonfile:
                for route_var in self.stop_routes:
                    json.dump(route_var.data_list, jsonfile, ensure_ascii=False)
                    jsonfile.write('\n')
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def output_as_csv(self, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.stop_routes[0].data_list)
                for var in self.stop_routes:
                    ss = []
                    for com in var.data_list:
                        ss.append(var.data_list[com])
                    writer.writerow(ss)
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def geojson_write(self, filename):
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for var in self.stop_routes:
            coordinates = var.get_coordinates()
            geo_data["features"].append({
                "type": "Feature",
                "properties": {
                    "name": var.get_route_id
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                }
            })

        # Write the GeoJSON data to the specified file
        with open(filename, 'w') as file:
            json.dump(geo_data, file)


class Path:
    def __init__(self, data):
        self._lat = data['lat']
        self._lng = data['lng']
        self._route_id = data['RouteId']
        self._route_var_id = data['RouteVarId']
        self._xy_coordinate = []
        self._ll_coordinate = []
        for xl, yl in zip(self._lng, self._lat):
            x, y = lat_lng_to_xy(xl, yl)
            self._xy_coordinate.append([x, y])
        for lng, lat in zip(self._lng, self._lat):
            self._ll_coordinate.append([lng, lat])

    def get_route_id(self):
        return self._route_id

    def get_xy(self):
        return self._xy_coordinate

    def get_ll_coordinate(self):
        return self._ll_coordinate

    def get_route_var_id(self):
        return self._route_var_id

    def get_lng(self):
        return self._lng

    def get_lat(self):
        return self._lat

    def get_coordinates(self):
        coordinates = []
        for i in range(len(self._lat)):
            coordinates.append([self._lng[i], self._lat[i]])
        return coordinates


class PathQuery:

    def __init__(self, json_file):
        self.paths = []
        try:
            with open(json_file, 'r', encoding='utf8') as f:
                for line in f:
                    v = json.loads(line)
                    self.paths.append(Path(v))
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def geojson_paths_write(self, filename):
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for var in self.paths:
            coordinates = var.get_coordinates()
            geo_data["features"].append({
                "type": "Feature",
                "properties": {
                    "name": var.get_route_id()
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                }
            })

        # Write the GeoJSON data to the specified file
        with open(filename, 'w') as file:
            json.dump(geo_data, file)

    '''def distance_between(self, lng, lat):
        for path in self.paths:
            for [lngs, lats] in path.get_ll_coordinate():
                if lngs == lng and lats == lat:'''

    def search_lng_lat(self, stop_id, stop_query: StopQuery, lng, lat):
        result_set = []
        for path in self.paths:
            if [str(path.get_route_id()), str(path.get_route_var_id())] in stop_query.belongings(stop_id):
                for i, [lng1, lat1] in enumerate(path.get_ll_coordinate()):
                    if str(lng) == str(lng1) and str(lat) == str(lat1):
                        result_set.append(1)
                        result_set.append({
                            "RouteId": path.get_route_id(),
                            "RouteVarId": path.get_route_var_id(),
                            "Pos": i
                        })
        return result_set


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, dis, time):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, dis, time))

    def dijkstra_fastest_path(self, start):
        distances = {vertex: float('inf') for vertex in self.graph}
        times = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        times[start] = 0

        priority_queue = [(0, start)]  # (time, vertex)
        while priority_queue:
            current_time, current_vertex = heapq.heappop(priority_queue)
            if current_time > times[current_vertex]:
                continue

            for neighbor, dis, time in self.graph[current_vertex]:
                total_time = current_time + time
                if total_time < times[neighbor]:
                    times[neighbor] = total_time
                    distances[neighbor] = distances[current_vertex] + dis
                    heapq.heappush(priority_queue, (total_time, neighbor))

        return distances, times


class newPath:
    def __init__(self, stops: Stop, path: Path):
        self.newPath = []

        old_path = path.get_ll_coordinate()
        temp_stop = stops.get_coordinates()
        len_path = len(old_path)
        len_stop = len(temp_stop)

        self.newPath.append([temp_stop[0][0], temp_stop[0][1], temp_stop[0][2]])
        cur_stop = 1
        cur_path = 0

        while cur_stop != len_stop or cur_path != len_path:
            if cur_stop == len(temp_stop):
                self.newPath.append([old_path[cur_path][0], old_path[cur_path][1], -1])
                cur_path += 1
            elif cur_path == len(old_path):
                self.newPath.append([temp_stop[cur_stop][0], temp_stop[cur_stop][1], temp_stop[cur_stop][2]])
                cur_stop += 1
            else:
                if (calculate_distance(self.newPath[-1][0], self.newPath[-1][1],
                                       temp_stop[cur_stop][0], temp_stop[cur_stop][1])
                        < calculate_distance(self.newPath[-1][0], self.newPath[-1][1],
                                             old_path[cur_path][0], old_path[cur_path][1])):
                    self.newPath.append([temp_stop[cur_stop][0], temp_stop[cur_stop][1], temp_stop[cur_stop][2]])
                    cur_stop += 1
                else:
                    self.newPath.append([old_path[cur_path][0], old_path[cur_path][1], -1])
                    cur_path += 1


class newPath_Query:

    def __init__(self, pair_stop_path: list):
        self.newPaths = []
        for [stop, path] in pair_stop_path:
            self.newPaths.append(newPath(stop, path))

    def output_as_json(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf8') as jsonfile:
                for new_path in self.newPaths:
                    json.dump(new_path.newPath, jsonfile, ensure_ascii=False)
                    jsonfile.write('\n')
        except Exception as e:
            print("An error occurred while opening the file:", e)
