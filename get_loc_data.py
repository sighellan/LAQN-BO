import pickle
import urllib.request
import time

"""
Get the latitude and longitude coordinates for the stations, and write to file.
"""

codes = pickle.load(open('station_codes.p', 'rb'))
locations = {}
out_file = open('lat_lon_coords.txt', 'a')
num_retries = 10

for code_idx in range(len(codes)):
    code = codes[code_idx]
    print('Obtaining location for %s. (%s/%s)' %(code, code_idx+1, len(codes)))
    url_str = 'https://www.londonair.org.uk/london/asp/publicdetails.asp?region=0&site=%s&details=location&mapview=all&la_id=&network=All&MapType=Google' %code
    count = 0
    while count < num_retries:
        try:
            text = str(urllib.request.urlopen(url_str, timeout=10).read())
            lat_lon_str = text.split('Latitude')[1].split('static google map')[0].split('<em>')[1].split('</em>')[0]
            lat_lon_split = lat_lon_str.split(', ')
            lat = float(lat_lon_split[0])
            lon = float(lat_lon_split[1])
            print(code, lat, lon)

            out_file.write('%s, %s, %s\n' %(code, lat, lon))
            locations[code] = [lat, lon]
            count = num_retries
        except:
            print('Site took too long to respond. Trying again.')
            if count + 1 == num_retries:
                print('Could not find location for %s.' %code)
                out_file.write('%s, %s, %s\n' %(code, '', ''))
                locations[code] = [None, None]
            else:
                time.sleep(2)
        count += 1
out_file.close()
pickle.dump(locations, open('lat_lon_dict.p', 'wb'))