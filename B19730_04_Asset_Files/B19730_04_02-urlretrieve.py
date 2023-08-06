# Retrieve a file using urllib
import urllib.request
import urllib.parse
import urllib.error
url = "https://github.com/PacktPublishing/Learning-Geospatial-Analysis-with-Python-4th-Edition/raw/main/B19730_02_Asset_Files/hancock.zip"
fileName = "hancock.zip"
urllib.request.urlretrieve(url, fileName)
