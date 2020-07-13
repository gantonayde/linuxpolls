import os
import urllib.request
from django.conf import settings
from IP2Location import IP2Location
from zipfile import ZipFile
from .tools import measure

ip2location_path = getattr(settings, "IP2LOCATION_PATH")
ip2location_token = getattr(settings, "IP2LOCATION_TOKEN")
ip2location_dbcode = getattr(settings, "IP2LOCATION_DBCODE")

def ip2location_dbname(dbcode):
    ''' Converts IP2Location LITE database BIN code to BIN database name. '''

    if dbcode == "DB1LITEBINIPV6":
        ip2location_dbname = "IP2LOCATION-LITE-DB1.IPV6.BIN" 
    elif dbcode == "DB3LITEBINIPV6":
        ip2location_dbname = "IP2LOCATION-LITE-DB3.IPV6.BIN"
    elif dbcode == "DB5LITEBINIPV6":
        ip2location_dbname = "IP2LOCATION-LITE-DB5.IPV6.BIN"
    elif dbcode == "DB9LITEBINIPV6":
        ip2location_dbname = "IP2LOCATION-LITE-DB9.IPV6.BIN" 
    elif dbcode == "DB11LITEBINIPV6":
        ip2location_dbname = "IP2LOCATION-LITE-DB11.IPV6.BIN"
    elif dbcode == "DB1LITEBIN":
        ip2location_dbname = "IP2LOCATION-LITE-DB1.BIN"
    elif dbcode == "DB3LITEBIN":
        ip2location_dbname = "IP2LOCATION-LITE-DB3.BIN"
    elif dbcode == "DB5LITEBIN":
        ip2location_dbname = "IP2LOCATION-LITE-DB5.BIN"
    elif dbcode == "DB9LITEBIN":
        ip2location_dbname = "IP2LOCATION-LITE-DB9.BIN" 
    elif dbcode == "DB11LITEBIN":
        ip2location_dbname = "IP2LOCATION-LITE-DB11.BIN"
    else:
        raise ValueError("Unknown IP2Location LITE database code")
    return ip2location_dbname

ip2location_dbname = ip2location_dbname(ip2location_dbcode)
ip2location_db = os.path.join(ip2location_path, ip2location_dbname)

@measure
def download_ip2location_database():
    db_name = ip2location_db + '.ZIP'
    url = f'https://www.ip2location.com/download/?token={ip2location_token}&file={ip2location_dbcode}'
    try:
        urllib.request.urlretrieve(url, db_name)
    except:
        print("Could not download database.")
        update_successful = False
    else:
        try:
            zf = ZipFile(db_name, 'r')
            zf.extractall(ip2location_path)
            zf.close()  
        except:
            update_successful = False
        else:
            files = os.listdir(ip2location_path)
            for file in files:
                print(file)
                if file != ip2location_dbname:
                    os.remove(os.path.join(ip2location_path, file))
            update_successful = True
    return ip2location_dbcode, update_successful

@measure
def get_geodata(ip_address):
    try:  
        with IP2Location(ip2location_db) as geo_db:
            try:
                geo_data = geo_db.get_all(ip_address)
            except:
                geo_data = geo_db.get_all('0.0.0.0')     
    except FileNotFoundError:
        print("Database file not found. Using generic values.")
        country_code = '-'
        country_name = '-'
        city         = '-'
    else:
        country_code = geo_data.country_short
        country_name = geo_data.country_long
        city         = geo_data.city
    return country_code, country_name, city


