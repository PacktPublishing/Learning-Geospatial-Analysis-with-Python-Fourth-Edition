import laspy
from osgeo import gdal
import numpy as np

def read_geotiff(geotiff_path):
    # Open the GeoTIFF file
    raster = gdal.Open(geotiff_path)
    geotransform = raster.GetGeoTransform()
    bands = [raster.GetRasterBand(i + 1).ReadAsArray() for i in range(3)] # RGB bands
    return bands, geotransform

def get_pixel_value(x, y, geotransform, bands):
    col = int((x - geotransform[0]) / geotransform[1])
    row = int((y - geotransform[3]) / geotransform[5])

    if row < 0 or row >= bands[0].shape[0] or col < 0 or col >= bands[0].shape[1]:
        print(f"Invalid coordinates: x={x}, y={y}, row={row}, col={col}")
        return [0, 0, 0]  # Return a default value if out of bounds

    return [int(band[row, col]) for band in bands]

def colorize_las(las_path, geotiff_path, output_path):
    # Read the GeoTIFF file
    bands, geotransform = read_geotiff(geotiff_path)
    
    # Read the LAS file
    las_file = laspy.read(las_path)
    scale_x, scale_y = las_file.header.scale[0:2]
    offset_x, offset_y = las_file.header.offset[0:2]

    # Create a new array to store the RGB values
    rgb_values = np.zeros((len(las_file.points), 3), dtype=np.uint16)
    
    # Iterate through the points and fetch the RGB values from the GeoTIFF
    for i, point in enumerate(las_file.points):
        x = point.X * scale_x + offset_x
        y = point.Y * scale_y + offset_y
        rgb = get_pixel_value(x, y, geotransform, bands)
        rgb_values[i] = rgb

    # Create a new LAS file with the same header as the original
    new_las = laspy.create(file_version=las_file.header.version,
                           point_format=las_file.header.point_format)
    new_las.points = las_file.points
    new_las.header = las_file.header  # Assign the header directly

    # Set the RGB values
    new_las.red = rgb_values[:, 0]
    new_las.green = rgb_values[:, 1]
    new_las.blue = rgb_values[:, 2]
    
    # Write the new LAS file
    new_las.write(output_path)  # Use the write method on the LasData object


# Example usage
las_path = "DeerIslandLidar.las"
geotiff_path = "DeerIslandAerial.tif"
output_path = "DeerIslandColorLidar.las"
colorize_las(las_path, geotiff_path, output_path)
