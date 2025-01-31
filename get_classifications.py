import json
import urllib.request
import time

"""
Get classifications for the stations, and write to file.
"""

codes = json.load(open('station_codes.json', 'r'))
clss_dict = {}
num_retries = 10

for code_idx in range(len(codes)):
    code = codes[code_idx]
    print('Obtaining classification for %s. (%s/%s)' %(code, code_idx+1, len(codes)))
    url_str = 'https://www.londonair.org.uk/london/asp/publicdetails.asp?region=0&site=%s&details=general&mapview=all&la_id=&network=All&VenueCode=' %code
    count = 0
    while count < num_retries:
        try:
            text = str(urllib.request.urlopen(url_str, timeout=10).read())
            classification = text.split(
                    'Classification')[1].split('title=')[1].split(' ')[0][1:-1]
            print('%s: %s' %(code, classification))
            clss_dict[code] = classification
            count = num_retries
        except:
            print('Site took too long to respond. Trying again.')
            if count + 1 == num_retries:
                print('Could not find classification for %s.' %code)
            else:
                time.sleep(2)
        count += 1
    
with open("classification_dict.json", "w") as json_file:
    json.dump(clss_dict, json_file)
