import json
import csv


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
        self.datalist = data_dictionary

    def getter(self, properties):
        return self.datalist[properties]

    @property
    def route_id(self):
        return self._route_id

    @route_id.setter
    def route_id(self, value):
        self._route_id = value
        self.datalist['RouteId'] = value

    @property
    def route_var_id(self):
        return self._route_var_id

    @route_var_id.setter
    def route_var_id(self, value):
        self._route_var_id = value
        self.datalist['RouteVarId'] = value

    @property
    def route_var_name(self):
        return self._route_var_name

    @route_var_name.setter
    def route_var_name(self, value):
        self._route_var_name = value
        self.datalist['RouteVarName'] = value

    @property
    def route_var_short_name(self):
        return self._route_var_short_name

    @route_var_short_name.setter
    def route_var_short_name(self, value):
        self._route_var_short_name = value
        self.datalist['RouteVarShortName'] = value

    @property
    def route_no(self):
        return self._route_no

    @route_no.setter
    def route_no(self, value):
        self._route_no = value
        self.datalist['RouteNo'] = value

    @property
    def start_stop(self):
        return self._start_stop

    @start_stop.setter
    def start_stop(self, value):
        self._start_stop = value
        self.datalist['StartStop'] = value

    @property
    def end_stop(self):
        return self._end_stop

    @end_stop.setter
    def end_stop(self, value):
        self._end_stop = value
        self.datalist['EndStop'] = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
        self.datalist['Distance'] = value

    @property
    def out_bound(self):
        return self._out_bound

    @out_bound.setter
    def out_bound(self, value):
        self._out_bound = value
        self.datalist['Outbound'] = value

    @property
    def running_time(self):
        return self._running_time

    @running_time.setter
    def running_time(self, value):
        self._running_time = value
        self.datalist['RunningTime'] = value


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
                if str(var.datalist[properties]).lower() == str(search_data).lower():
                    data.append(
                        ['Id: ' + var.datalist['RouteId'], 'Name: ' + var.datalist['RouteVarName'],
                         'Short Name' + var.datalist['RouteVarShortName']])
            return data
        else:
            print("There is no property found")

    def output_as_json(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf8') as jsonfile:
                for route_var in self.route_vars:
                    json.dump(route_var.datalist, jsonfile, ensure_ascii=False)
                    jsonfile.write('\n')
        except Exception as e:
            print("An error occurred while opening the file:", e)

    def output_as_csv(self, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.route_vars[0].datalist)
                for var in self.route_vars:
                    ss = []
                    for com in var.datalist:
                        ss.append(var.datalist[com])
                    writer.writerow(ss)
        except Exception as e:
            print("An error occurred while opening the file:", e)


# ["RouteId", "RouteVarId", "RouteVarName", "RouteVarShortName",
# "RouteNo", "StartStop", "EndStop", "Distance", "Outbound", "RunningTime"]
# [var.datalist['RouteId'], var.datalist['RouteVarId'], var.datalist["RouteVarName"], var.datalist["RouteVarShortName"], var.datalist["RouteNo"], var.datalist["StartStop"], var.datalist["EndStop"], var.datalist["Distance"], var.datalist["Outbound"], var.datalist["RunningTime"]]

class Stop:
    def __init__(self, data_array):
        self._stop_id_list = data_array['Stops']
        self._route_id = data_array['RouteId']
        self._route_var_id = data_array['RouteVarId']
        self.data_list = data_array

    def get_coordinates(self):
        coordinates = []
        for var in self._stop_id_list:
            coordinates.append([var['Lng'], var['Lat']])
        return coordinates

    @property
    def get_stop_id_list(self):
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

    def get_route_id(self):
        return self._route_id

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