# Read and write GeoJson using the geojson module
from shapely.geometry import shape
import geojson
p = geojson.Point([-92, 37])
geojs = geojson.dumps(p, indent=4)
print(geojs)
# Use __geo_interface__ between geojson and shapely
point = shape(p)
print(point.wkt)
