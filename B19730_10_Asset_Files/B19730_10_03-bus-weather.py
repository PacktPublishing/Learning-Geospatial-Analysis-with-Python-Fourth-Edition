import sys
from google.transit import gtfs_realtime_pb2
from urllib.request import Request, urlopen
from xml.dom import minidom
import math
try:
    import Image
except:
    from PIL import Image

def get_bus():
    """Returns the most recent latitude and
    longitude of the selected bus line using
    the GTFS Real-Time Washington Metropolitan Area 
    Transit Authority API to grab the first available
    public bus in the feed.
    """
    bus_lat = False
    bus_lon = False
    feed = gtfs_realtime_pb2.FeedMessage()
    req = Request('https://api.wmata.com/gtfs/bus-gtfsrt-vehiclepositions.pb')
    req.add_header('api_key', 'd4d713a59a9f477fab8c1e9fbadbd467')
    response = urlopen(req)
    feed.ParseFromString(response.read())
    bus = feed.entity[0]
    bus_lat = bus.vehicle.position.latitude
    bus_lon = bus.vehicle.position.longitude
    return(bus_lat, bus_lon)


def ll2m(lon, lat):
    """Lat/lon to meters"""
    x = lon * 20037508.34 / 180.0
    y = math.log(math.tan((90.0 + lat) *
                 math.pi / 360.0)) / (math.pi / 180.0)
    y = y * 20037508.34 / 180
    return (x, y)

from PIL import Image, ImageDraw, ImageFont

# Function to check if the image is all white
def no_precip(image):
    gray_image = image.convert('L')  # Convert image to grayscale
    for pixel in gray_image.getdata():
        if pixel != 255:  # Not a white pixel
            return False
    return True

def wms(minx, miny, maxx, maxy, service, lyr, img, w, h):
    """Retrieve a wms map image from
    the specified service and saves it as a PNG."""
    wms = service
    wms += "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&"
    wms += "LAYERS=%s" % lyr
    wms += "&STYLES=&"
    wms += "SRS=EPSG:900913&"
    wms += "BBOX=%s,%s,%s,%s&" % (minx, miny, maxx, maxy)
    wms += "WIDTH=%s&" % w
    wms += "HEIGHT=%s&" % h
    wms += "FORMAT=image/png"
    wmsmap = urlopen(wms)
    with open(img + ".png", "wb") as f:
        f.write(wmsmap.read())

# OpenStreetMap WMS service
basemap = " https://ows.terrestris.de/osm/service"

# Name of the WMS street layer
streets = "OSM-WMS"

# Name of the basemap image to save
mapimg = "basemap"

# NOAA Radar WMS Service
weather = "https://opengeo.ncep.noaa.gov/geoserver/conus/conus_pcpn_typ/ows"

# If the sky is clear over New York,
# use the following url which contains
# a notional precipitation sample:
# weather = "http://git.io/vl4r1"

# WMS weather layer
weather_layer = "conus_pcpn_typ"

# Name of the weather image to save
skyimg = "weather"

# Name of the finished map to save
final = "next-weather"

# Transparency level for weather layer
# when we blend it with the base map.
# 0 = invisible, 1 = no transparency
opacity = .5

# Pixel width and height of the
# output map images
w = 1000
h = 1000

# Pixel width/height of the the

# bus marker icon
icon = 30

# Get the bus location

lat, lon = get_bus()
if not lat:
    print("No bus data available.")
    print("Please try again later")
    sys.exit()

# Convert strings to floats
lat = float(lat)
lon = float(lon)

# Convert the degrees to Web Mercator
# to match the WMS map
x, y = ll2m(lon, lat)

# Create a bounding box 1600 meters
# in each direction around the bus
minx = x - 1600
maxx = x + 1600
miny = y - 1600
maxy = y + 1600

# Download the street map
wms(minx, miny, maxx, maxy, basemap, streets, mapimg, w, h)

# Download the weather map
# wms(minx, miny, maxx, maxy, weather, weather_layer, skyimg, w, h)
wms(minx, miny, maxx, maxy, weather, weather_layer, skyimg, w, h)

# Open the basemap image in PIL
im1 = Image.open("basemap.png").convert('RGBA')

# Open the weather image in PIL
im2 = Image.open("weather.png").convert('RGBA')
if no_precip(im2):
    draw = ImageDraw.Draw(im2)
    
    # Load a font
    font_size = 60
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Position for the text: 15 pixels from the bottom left corner
    text_position = (15, im2.height - font_size - 15)
    
    # Draw text on image
    draw.text(text_position, "No precipitation in the area.", (0, 0, 0), font=font)

# Create a blended image combining
# the base map with the weather map
im3 = Image.blend(im1, im2, opacity)

# Open up the bus icon image to
# use as a location marker.
# http://git.io/vlgHl  
im4 = Image.open("busicon.png")

# Shrink the icon to the desired
# size
im4.thumbnail((icon, icon))

# Use the blended map image
# and icon sizes to place
# the icon in the center of
# the image since the map
# is centered on the bus
# location.
w, h = im3.size
w2, h2 = im4.size

# Paste the icon in the center of the image
center_width = int((w/2)-(w2/2))
center_height = int((h/2)-(h2/2))
im3.paste(im4, (center_width, center_height), im4)

# Save the finished map
im3.save(final + ".png")
