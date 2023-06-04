import csv
import os

"""
Filter out locations without any data present.
"""

# A folder for the files with data
os.makedirs('data_raw/with_data', exist_ok=True)

files = os.listdir('data_raw/')
done_files = os.listdir('data_raw/with_data/')

data_files = []
no_data_files = []
for ff in files:
    if ff == 'with_data': 
        continue # Ignore folder used for outputs
    if ff in done_files:
        continue # Has already been done
    
    found = False
    lines_data = []
    with open('data_raw/%s' %ff) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ii = 0
        for row in reader:
            if ii >= 1 and row[3] != '':
                found = True
                lines_data.append(row)
            if ii == 0:
                lines_data.append(row)
            ii += 1
    if found:
        print('File %s includes data' %ff)
        data_files.append(ff)
        # Store the data
        with open('data_raw/with_data/%s' %ff, 
                  'w', newline='') as csv_outfile:
            writer = csv.writer(csv_outfile, delimiter=',')
            for ll in lines_data:
                writer.writerow(ll)
    else:
        no_data_files.append(ff)
    
print('Number of files with data: %s' %len(data_files))
print('Number of files without data: %s' %len(no_data_files))