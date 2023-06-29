"""Extract Polygons with holes"""

#https://github.com/GeospatialPython/Learn/raw/master/BuildingFootprintsOSM.gpkg

import fiona
from shapely.geometry import shape, MultiPolygon

with fiona.open("BuildingFootprintsOSM.gpkg", "r") as city:
    # Collection of footprints with holes
    hole_footprints = []

    # Loop through footprints and check
    # for interior rings (holes). If at
    # least one is present, copy it
    # to our list
    for footprint in city:
        shapes = MultiPolygon(shape(footprint["geometry"]))
        for s in shapes.geoms:
            if len(s.interiors):
                hole_footprints.append(footprint)

    # Create a new geopackage and write out the hole features
    with fiona.open("holes.gpkg", "w", **city.meta) as holes:
        for hole_footprint in hole_footprints:
            holes.write(hole_footprint)
    
        