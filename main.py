from route_data.ClassBuild import RouteVarQuery
from route_data.ClassBuild import StopQuery

query = RouteVarQuery('route_data/vars.json')

#print(query.route_vars[0].getter('RouteVarName'))

#print(query.search_by_properties('RouteId', 3))

#print(query.search_by_properties('Outbound', "False"))

#query.output_as_json('output_files/package.json')
#query.output_as_csv('output_files/output.csv')

stop_query = StopQuery('route_data/stops.json')
print(stop_query.stops[0].datalist["RouteId"])
print(stop_query.search_by_properties("Name", "Bến xe Chợ Lớn"))

stop_query.output_as_json('output_files/output_stops.json')
stop_query.output_as_csv('output_files/output2_stops.csv')
