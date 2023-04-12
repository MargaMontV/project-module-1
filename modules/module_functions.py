#Imports
import pandas as pd
import numpy as np
import requests 
import re
from shapely.geometry import Point
import geopandas as gpd  
from pyproj import CRS

#Functions
def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

def closest_station(df_bici, lat_cp, long_cp):
    dist_min = 5000000
    for i, j in df_bici.iterrows():
        #print(i)
        #print(j)
        dist = distance_meters(j[-2], j[-1], lat_cp, long_cp)[0]
        #print(dist)
        if (dist < dist_min):
            dist_min = dist
            closest_point = j
    return closest_point
