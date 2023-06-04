"""Active learning problem class definition and helper functions"""
import numpy as np

def convert_lat_lon_km(domain, min_lat, min_lon):
    # Uses London-specific values
    R = 6371
    lat = domain[:,0]
    lon = domain[:,1]
    x1 = (lat - min_lat) * 111
    x0 = (lon - min_lon) * np.pi/180*R*np.cos(np.pi/180*lat)
    return np.vstack([x1, x0]).T

def get_lat_and_lon_mins(loc_dict):
    lat_min, lon_min = np.inf, np.inf
    for key in loc_dict.keys():
        lat, lon = loc_dict[key]
        if lat is not None and lon is not None:
            lat_min = min(lat_min, lat)
            lon_min = min(lon_min, lon)
    return lat_min, lon_min

def add_val(val, dic, key):
    if key in dic.keys():
        dic[key].append(val)
    else:
        dic[key] = [val]

class Problem_obj:
    """Class to hold active learning problems"""

    def __init__(
        self,
        xx_nn, # features of initial data points
        yy_nn, # labels of initial data points
        domain, # features of all avaiable data points
        labels, # labels of all available data points
        identifier # problem identifier
    ):
        self.xx = xx_nn
        self.yy = yy_nn
        self.domain = domain
        self.labels = labels
        self.maximum = np.max(labels)
        self.maximiser = domain[np.argmax(labels)]
        self.minimum = np.min(labels)
        self.minimiser = domain[np.argmin(labels)]
        self.identifier = identifier