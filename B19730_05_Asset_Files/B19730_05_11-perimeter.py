import json
from math import hypot

def calculate_perimeter(geojson_string):
    try:
        data = json.loads(geojson_string)
        if data['type'] == 'Polygon':
            coordinates = data['coordinates'][0]  # Extracting the outer ring of the polygon
            perimeter = 0.0
            for i in range(len(coordinates) - 1):
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[i + 1]
                perimeter += hypot(x2 - x1, y2 - y1)
            return perimeter
        else:
            raise ValueError("Invalid GeoJSON type. Expected 'Polygon', got '{}'".format(data['type']))
    except (ValueError, KeyError) as e:
        print("Error:", e)

# Example usage from ChatGPT
polygon_geojson = '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}'
perimeter = calculate_perimeter(polygon_geojson)
print("Perimeter:", perimeter)

# Example using a geospatial polygon
poly = '{"type": "Polygon","coordinates": [[[269562.117101155803539, 3360119.08169707050547],[277642.670304813073017, 3359982.998913598246872],[277499.190223414334469, 3351589.872332769446075],[269576.938840636401437, 3351658.483336582779884],[269562.117101155803539, 3360119.08169707050547]]],"crs": {"type": "name","properties": {"name": "urn:ogc:def:crs:EPSG::26916"}}}'

print("Perimeter: ", calculate_perimeter(poly))