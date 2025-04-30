# Read NOAA weather buoy location data via ftp

# UPDATE Apr. 29, 2025: NOAA changed this to an encrypted
# FTP server. The first part of the example has been updated
# to accomodate, but will be different from the book until
# I can get Packt to update it. Thank you to Ryan Burnside
# for bringing this to my attention. There's a lot of changes
# occuring in the US government right now, especially at NOAA.
# - Joel Lawhead

import ftplib
server = "ftp.pmel.noaa.gov"
dir = "taodata"
fileName = "taobuoypos.dat"
ftp = ftplib.FTP_TLS(server)
ftp.login()
ftp.prot_p()
ftp.cwd(dir)
with open(fileName, "wb") as out:
    ftp.retrbinary("RETR " + fileName, out.write)

with open(fileName) as tao:
    buoy = tao.readlines()[5]
    loc = buoy.split()
    print(f"Buoy {loc[0]} is located at {' '.join(loc[4:8])}")

# Now do the same thing with urllib
# UPDATE Apr. 29, 2025: urllib can't handle encrypted ftp which
# NOAA has switched to. This example will be updated.
#  

"""
import urllib.request

tao = urllib.request.urlopen("ftp://" + server + "/" + dir + "/" + fileName)
buoy = str(tao.readlines()[5], encoding="utf8")
loc = buoy.split()
print(f"Buoy {loc[0]} is located at {' '.join(loc[4:8])}")"
"""
