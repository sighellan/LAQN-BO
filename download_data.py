import urllib.request
import json
import os

"""
Download raw pollution data from LAQN website. 
"""

codes = json.load(open('station_codes.json', 'r'))

start='1-jan-2015'
end='31-dec-2016'
poll='NO2'

# Store downloaded data to folder called data_raw
os.makedirs('data_raw', exist_ok=True)
for ii in range(len(codes)):
    print('Downloading %s' %codes[ii])

    url = 'https://www.londonair.org.uk/london/asp/downloadspecies.asp?species=%s&site1=%s&site2=&site3=&site4=&site5=&site6=&start=%s&end=%s&res=6&period=daily&units=' %(
        poll, codes[ii], start, end)
    urllib.request.urlretrieve(url, 
        'data_raw/daily_%s_from_%s_to_%s_%s.csv' %(poll, start, end, codes[ii]))
