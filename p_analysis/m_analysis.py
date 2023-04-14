import numpy as np
import pandas as pd 
import re
from shapely.geometry import Point
import geopandas as gpd   
from pyproj import CRS

#Analysis functions
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
    closest_point.to_csv('./data/raw_closest_station.csv')
    return closest_point

def all_closest_stations(df_i, df_j):
    all_closest_stations_1 = df_i.apply(lambda x: closest_station(df_j, x["Latitude"], 
                                            x["Longitude"]), axis=1)
    all_closest_stations_1.to_csv('./data/raw_all_closest_stations.csv')
    return all_closest_stations_1

def get_csv(df_final):  
    return df_final.to_csv('./data/nearest_bicimad_cp.csv', index=False, encoding='utf-8')