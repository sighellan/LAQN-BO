import numpy as np
import csv
import os
import pickle
import datetime
import json

"""
Sort the collected data into years.
"""

folder = 'data_raw/with_data/'
files = os.listdir(folder)
poll = 'NO2'

# A folder for the data sorted into years.
os.makedirs('data_sorted', exist_ok=True)

# Might have other pollutants stored as well
files_poll = [ff for ff in files if ff[6:10] == 'NO2_']


# Gather all data
all_data = []
for ff in files_poll:
    with open('%s%s' %(folder, ff)) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ii = 0
        for row in reader:
            if ii >= 1:
                all_data.append(row)
            ii += 1
            
with open('lat_lon_dict.json', 'r') as json_file:
    loc_dict = json.load(json_file)
# Interpret dates, values and ratification to allow comparisons 
data_array = []
for dd in all_data:
    code = dd[0]
    date = datetime.datetime.strptime(dd[2], 
                                      '%d/%m/%Y %H:%M')
    value = float(dd[3])
    ratif = dd[5] == 'R'
    lat = loc_dict[code][0]
    lon = loc_dict[code][1]
    
    # Filter out negative values
    if value >= 0:
        data_array.append([code, date, value, ratif, lat, lon])
    
# Sort by year
year_part = {}
year_part_ratif = {}
for dd in data_array:
    yy = dd[1].year
    if yy in year_part.keys():
        year_part[yy].append(dd)
    else:
        year_part[yy] = [dd]
    if dd[3]: # If ratified, also add to dict of ratified values
        if yy in year_part_ratif.keys():
            year_part_ratif[yy].append(dd)
        else:
            year_part_ratif[yy] = [dd]
            
print('Year: total\tratified')
for yy in sorted(year_part.keys()):
    ratif = len(year_part_ratif[yy]) if yy in year_part_ratif.keys() else ''
    print('%s: %s\t%s' %(yy, len(year_part[yy]),
                         ratif))
    
def produce_summary_statistics(data):
    Y = np.array(data)[:, 2].astype('float64')
    return {
        'mean_Y': np.mean(Y),
        'std_Y': np.std(Y, ddof=1),
        'mean_log_Y': np.mean(np.log(Y)),
        'std_log_Y': np.std(np.log(Y), ddof=1)
    }

# Store yearly data
for yy in year_part.keys():
    pickle.dump(year_part[yy],
               open('data_sorted/%s_year_%s.p' %(poll, yy), 'wb'))
    pickle.dump(produce_summary_statistics(year_part[yy]),
                open('data_sorted/%s_year_%s_summary_statistics.p' %(poll, yy), 'wb'))
for yy in year_part_ratif.keys():
    pickle.dump(year_part_ratif[yy],
        open('data_sorted/%s_year_%s_ratified.p' %(poll, yy), 'wb'))
    pickle.dump(produce_summary_statistics(year_part_ratif[yy]),
                open('data_sorted/%s_year_%s_ratified_summary_statistics.p' %(poll, yy), 'wb'))
