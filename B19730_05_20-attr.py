"""Attribute selection for subset"""

# https://github.com/PacktPublishing/Learning-Geospatial-Analysis-with-Python-4th-Edition/raw/main/B19730_05_Asset_Files/MS_UrbanAnC10.zip

import shapefile

# Create a reader instance
r = shapefile.Reader("MS_UrbanAnC10")
# Create a writer instance
with shapefile.Writer("MS_Urban_Subset", r.shapeType) as w:
    # Copy the fields to the writer
    w.fields = list(r.fields)
    # Grab the geometry and records from all features
    # with the correct population
    selection = []
    for rec in enumerate(r.records()):
        if rec[1][15] < 5000:
            selection.append(rec)
    # Add the geometry and records to the writer
    for rec in selection:
        w.poly([r.shape(rec[0]).points])
        w.record(*list(rec[1]))
