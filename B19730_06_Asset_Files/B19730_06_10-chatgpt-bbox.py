from osgeo import gdal, ogr

def geotiff_to_geojson(geotiff_path, geojson_path):
    # Open the GeoTIFF file
    dataset = gdal.Open(geotiff_path)
    
    # Get the raster's footprint geometry
    raster_layer = dataset.GetRasterBand(1)
    transform = dataset.GetGeoTransform()
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    ulx = transform[0]
    uly = transform[3]
    lrx = ulx + width * transform[1]
    lry = uly + height * transform[5]
    
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(ulx, uly)
    ring.AddPoint(lrx, uly)
    ring.AddPoint(lrx, lry)
    ring.AddPoint(ulx, lry)
    ring.AddPoint(ulx, uly)
    
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    
    # Create a GeoJSON file and write the polygon feature
    driver = ogr.GetDriverByName('GeoJSON')
    output_dataset = driver.CreateDataSource(geojson_path)
    output_layer = output_dataset.CreateLayer('footprint', geom_type=ogr.wkbPolygon)
    feature = ogr.Feature(output_layer.GetLayerDefn())
    feature.SetGeometry(poly)
    output_layer.CreateFeature(feature)
    
    # Clean up
    feature = None
    output_dataset = None
    dataset = None

# Usage example
geotiff_path = 'stretched.tif'
geojson_path = 'bbox.geojson'
geotiff_to_geojson(geotiff_path, geojson_path)
