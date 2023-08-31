# Extract a zipped shapefile via a url
import urllib.request
import zipfile
import io
import struct

url = "https://github.com/PacktPublishing/Learning-Geospatial-Analysis-with-Python-4th-Edition/raw/main/B19730_04_Asset_Files/hancock.zip"
cloudshape = urllib.request.urlopen(url)
memoryshape = io.BytesIO(cloudshape.read())
zipshape = zipfile.ZipFile(memoryshape)
cloudshp = zipshape.read("hancock.shp")
# Access Python string as an array
print(struct.unpack("<dddd", cloudshp[36: 68]))
