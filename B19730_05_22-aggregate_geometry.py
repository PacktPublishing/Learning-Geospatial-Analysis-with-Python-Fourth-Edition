"""
aggregate_geometry.py - combine a group of polygons into one.
"""

# https://github.com/PacktPublishing/Learning-Geospatial-Analysis-with-Python-4th-Edition/blob/ee8b1be67808e0f8b77fa422d36b049dea6a57ce/B19730_05_Asset_Files/ms_counties.geojson

# Used OrderedDict to control the order
# of data attributes
from collections import OrderedDict
# Import the shapely geometry classes and methods.
# The "mapping" method returns a geojson representation
# of a geometry.
from shapely.geometry import shape, mapping, Polygon
# Import the shapely union function which combines
# geometries
from shapely.ops import unary_union
# Import Fiona to read and write datasets
import fiona

# Open the counties dataset
with fiona.open('ms_counties.geojson') as src:
	# copy the metadata
	schema = src.meta.copy()
	# Create a new field type for our
	# state dataset
	fields = {"State": "str:80"}
	# Create a new property for our dataset
	# using the new field
	prop = OrderedDict([("State", "Mississippi")])
	# Change the metadata geometry type to Polygon
	schema['geometry'] = 'Polygon'
	schema['schema']['geometry'] = 'Polygon'
	# Add the new field
	schema['properties'] = fields
	schema['schema']['properties'] = fields
	# Open the output geojson dataset
	with fiona.open('combined.geojson', 'w', **schema) as dst:
		# Extract the properties and geometry from the counties dataset
		props, geom = zip(*[(f['properties'],shape(f['geometry'])) for f in src])
		# Write the new state dataset out while combining the polygons into a
		# single polygon and add the new property
		dst.write({'geometry': mapping(Polygon(unary_union(geom).exterior)), 
		           'properties': prop})

