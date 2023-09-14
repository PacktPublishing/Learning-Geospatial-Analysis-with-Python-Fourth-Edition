"""
Classify an NDVI tiff using 7 classes
by "pushing" the NDVI through
masks defined by the desired
range of values for each class.
"""

# Import required libraries
from osgeo import gdal_array as gd
from osgeo import gdal
import operator
from functools import reduce

# Enable GDAL exceptions for better error handling
gdal.UseExceptions()

# Define function to compute histogram of multi-dimensional array
def histogram(a, bins=list(range(256))):
    fa = a.flat
    n = gd.numpy.searchsorted(gd.numpy.sort(fa), bins)
    n = gd.numpy.concatenate([n, [len(fa)]])
    hist = n[1:]-n[:-1]
    return hist

# Define function to perform histogram stretch
def stretch(a):
    hist = histogram(a)
    lut = []
    for b in range(0, len(hist), 256):
        step = reduce(operator.add, hist[b:b+256]) / 255
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hist[i+b]
    gd.numpy.take(lut, a, out=a)
    return a

# Initialize source and target file paths
source = "ndvi.tif"
target = "ndvi_color.tif"

# Load the NDVI image and convert data type
ndvi = gd.LoadFile(source).astype(gd.numpy.float32)

# Normalize NDVI to 0-255, but only for non-zero values
ndvi_normalized = gd.numpy.zeros(ndvi.shape, dtype=gd.numpy.uint8)
mask = ndvi != 0.0
ndvi_normalized[mask] = ((ndvi[mask] + 1) / 2.0 * 255).astype(gd.numpy.uint8)

# Apply histogram stretching to normalized NDVI
ndvi_normalized = stretch(ndvi_normalized)

# Create 3-band image of zeros with the same dimensions as NDVI
rgb = gd.numpy.zeros((3, len(ndvi), len(ndvi[0])), gd.numpy.uint8)

# Set NDVI values of zero to black in RGB
mask_zero = ndvi_normalized == 0
for j in range(3):
    rgb[j] = gd.numpy.where(mask_zero, 0, rgb[j])

# Define the classes and their corresponding RGB colors
classes = [58, 73, 110, 147, 184, 220, 255]
lut = [[120, 69, 25], [255, 178, 74], [255, 237, 166], [173, 232, 94], [135, 181, 64], [3, 156, 0], [1, 100, 0]]

# Initialize the starting value for class ranges
start = 1

# Classify and colorize each NDVI range based on predefined classes
for i in range(len(classes)):
    mask = gd.numpy.logical_and(start <= ndvi_normalized, ndvi_normalized <= classes[i])
    for j in range(3):
        rgb[j] = gd.numpy.where(mask, lut[i][j], rgb[j])
    start = classes[i] + 1

# Save the classified and colorized image
gd.SaveArray(rgb, target, format="GTiff", prototype=source)
