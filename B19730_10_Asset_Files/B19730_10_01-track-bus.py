from google.transit import gtfs_realtime_pb2
from urllib.request import Request, urlopen

feed = gtfs_realtime_pb2.FeedMessage()
req = Request('https://api.wmata.com/gtfs/bus-gtfsrt-vehiclepositions.pb')
req.add_header('api_key', 'd4d713a59a9f477fab8c1e9fbadbd467')
response = urlopen(req)
feed.ParseFromString(response.read())
bus = feed.entity[0]
bus_id = bus.id
bus_lat = bus.vehicle.position.latitude
bus_lon = bus.vehicle.position.longitude
print(f'Bus {bus_id} is at latitude: {bus_lat}, longitude: {bus_lon}')
