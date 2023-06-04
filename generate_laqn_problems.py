import argparse
import datetime
import numpy as np
import os
import pickle

from setup_helper import Problem_obj, convert_lat_lon_km, add_val, get_lat_and_lon_mins

"""
Generate the problems.
"""

#############################################################
# Parse inputs                                              #
#############################################################
parser = argparse.ArgumentParser(
                    prog = 'generate_laqn_problems.py',
                    description = 'Generate active learning problems based on LAQN data.')
parser.add_argument('year', type=int)
args = parser.parse_args()

#############################################################
# Settings                                                  #
#############################################################
poll = 'NO2' 
min_stations_for_problem = 40 # Ignore days fow which less than this number of stations have readings
classes = ['Roadside'] # Choose the classes you want to include
year = args.year # Year to generate problems for
generation_seed = 13 # Used to initiate numpy.random
year_normalisation = 2015 # Year to use for normalisation (we want to use training data for this)

#############################################################
# Load data, locations, classifications and summary stats   #
#############################################################
data = pickle.load(open(
    'data_sorted/%s_year_%s_ratified.p' %(poll, year), 'rb')) # Use the ratified data
loc_dict = pickle.load(open('lat_lon_dict.p', 'rb'))
clss_dict = pickle.load(open(
    'classification_dict.p', 'rb'))
summ_file = 'data_sorted/%s_year_%s_ratified_summary_statistics.p' %(poll, year_normalisation)
summ_stats = pickle.load(open(summ_file, 'rb'))
print('Using file %s for normalisation.' %summ_file)

############################################################# 
# Folders for the generated problems                        #
#############################################################
problem_dir = 'data_sorted/%s_problems' %year
problem_dir_pre = problem_dir+'/preprocessed'
problem_dir_raw = problem_dir+'/not_preprocessed'
for new_dir in [problem_dir, problem_dir_pre, problem_dir_raw]:
    os.makedirs(new_dir, exist_ok=True)

############################################################# 
# Sort data into days                                       #
#############################################################
days_data = {}
for dd in data:
    if clss_dict[dd[0]] in classes: # Filter out classes we're not considering
        day = (dd[1] - datetime.datetime(year-1, 12, 31)).days
        add_val([dd[2], dd[4], dd[5]], days_data, day)
for key in days_data.keys():
    days_data[key] = np.array(days_data[key])
        
############################################################# 
# Prepare to make problems                                  #
#############################################################
classes_str = '_'.join(classes)
lat_min, lon_min = get_lat_and_lon_mins(loc_dict)
# Filter out days we don't have enough data for
cand = [ii for ii in range(1, 366) if len(days_data[ii]) >= min_stations_for_problem]
np.random.seed(generation_seed)

############################################################# 
# Make problems                                             #
#############################################################
for ii in cand:
    
    prob_str = '%s_%s_msfp_%s_day-%s' %(poll, classes_str, min_stations_for_problem, ii)
    dat = days_data[ii]
    domain = convert_lat_lon_km(dat[:,[1, 2]], lat_min, lon_min)
    labels = dat[:,0]
    
    # Select 5 random stations to start problems with
    idx = np.random.randint(0, len(dat), 5)
    xx = domain[idx,:]
    yy = labels[idx]

    #########################################################
    # Generate the problem without preprocessing the labels # 
    #########################################################
    prob = Problem_obj(
        xx_nn=xx,
        yy_nn=yy,
        domain=domain,
        labels=labels,
        identifier='Not_preprocessed-%s-%s-%s' %(poll, year, ii),
    )
    
    pickle.dump(
        prob, 
        open(problem_dir_raw+'/laqn-al_notpre_%s.p' %prob_str, 'wb')) 
    
    #########################################################
    # Generate the problem with preprocessed labels         # 
    #########################################################
    # Preprocess the labels
    prepro_labels = (np.log(labels) - summ_stats['mean_log_Y'])/summ_stats['std_log_Y']
    prepro_yy = (np.log(yy) - summ_stats['mean_log_Y'])/summ_stats['std_log_Y']
    
    prob = Problem_obj(
        xx_nn=xx,
        yy_nn=prepro_yy,
        domain=domain,
        labels=prepro_labels,
        identifier='Preprocessed-%s-%s-%s' %(poll, year, ii),
    )
    
    pickle.dump(
        prob, 
        open(problem_dir_pre+'/laqn-al_prepro_%s.p' %prob_str, 'wb'))

print('Problems generated for %s' %year)
print('The files are located in:')
print(problem_dir_raw)
print(problem_dir_pre)