# Read NOAA weather buoy location data via ftp
import ftplib
server = "ftp.pmel.noaa.gov"
dir = "taodata"
fileName = "taobuoypos.dat"
ftp = ftplib.FTP(server)
ftp.login()
ftp.cwd(dir)
with open(fileName, "wb") as out:
    ftp.retrbinary("RETR " + fileName, out.write)

with open(fileName) as tao:
    buoy = tao.readlines()[5]
    loc = buoy.split()
    print(f"Buoy {loc[0]} is located at {' '.join(loc[4:8])}")

# Now do the same thing with urllib

import urllib.request

tao = urllib.request.urlopen("ftp://" + server + "/" + dir + "/" + fileName)
buoy = str(tao.readlines()[5], encoding="utf8")
loc = buoy.split()
print(f"Buoy {loc[0]} is located at {' '.join(loc[4:8])}")