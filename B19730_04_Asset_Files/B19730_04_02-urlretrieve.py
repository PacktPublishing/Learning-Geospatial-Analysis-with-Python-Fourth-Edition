# Retrieve a file using urllib
import urllib.request
url = "https://github.com/PacktPublishing/Learning-Geospatial-Analysis-with-Python-4th-Edition/raw/main/B19730_02_Asset_Files/hancock.zip"
fileName = "hancock.zip"
out,response = urllib.request.urlretrieve(url, fileName) 
print(f"successfully downloaded {out}")
print(response)
