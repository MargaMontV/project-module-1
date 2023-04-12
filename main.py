# Import libraries
import pandas as pd
import numpy as np
import requests 
import re
from shapely.geometry import Point
import geopandas as gpd   # conda install -c conda-forge geopandas
from pyproj import CRS

# acquisition functions

def acquire_1():
    end_point_1 = 'https://datos.madrid.es/egob/' # Main End-Point
    body_1 = 'catalogo/202311-0-colegios-publicos.json'# Body
    pulls_response_1 = requests.get(end_point_1 + body_1)
    pulls_json_1 = pulls_response_1.json()
    df_col_pub = pd.json_normalize(pulls_json_1, ['@graph'])
    return df_col_pub

def acquire_2():
    bicimad_stations = pd.read_csv('./data/bicimad_stations.csv')
    return bicimad_stations

#wrangling functions
df_col_pub_a = acquire_1()
bicimad_stations_a = acquire_2()

def wrangling_1(df_1):
    df_col_pub_2 = df_1[["title", "address.street-address", "location.latitude", "location.longitude", 
                 "organization.organization-name"]]
    df_col_pub_2["Type of place"] = df_col_pub_2["organization.organization-name"].str.split(" ", 
    expand = True)[0] + " " + df_col_pub_2["organization.organization-name"].str.split(" ", expand = True)[1]
    df_col_pub_2['Place address'] = df_col_pub_2['address.street-address'].apply(lambda x: x.title())
    df_col_pub_2["Place address"] = df_col_pub_2["Place address"].str.replace("Plaza Pe&Amp;Ntilde;A Morraz 1", 
                                                                              "Plaza Peña Morraz 1")
    df_col_pub_2["Place address"] = df_col_pub_2["Place address"].str.replace("Calle Jose Ortu&Amp;Ntilde;O Ponce 2", 
                                                                              "Calle Jose Ortuño Ponce 2")
    df_col_pub_3 = df_col_pub_2[["title", "location.latitude", "location.longitude", "Type of place", "Place address"]]
    df_col_pub_3['Latitude'] = df_col_pub_3['location.latitude'].astype(float)
    df_col_pub_3['Longitude'] = df_col_pub_3['location.longitude'].astype(float)
    df_col_pub_4 = df_col_pub_3[["title", "Type of place", "Place address", "Latitude", "Longitude"]]
    df_col_pub_4.rename(columns = {'title':'Place of interest'}, inplace = True)
    return df_col_pub_4

def wrangling_2(df_2):
    df_2["Station location"] = df_2["Station location"].str.replace(" nº", "")
    df_2["Longitude"] = df_2["Coordinates"].str.split(",", 
                        expand = True)[0].str.split("[", expand = True)[1]
    df_2["Latitude"] = df_2["Coordinates"].str.split(",", 
                        expand = True)[1].str.split("]", expand = True)[0]
    df_2["BiciMAD station"] = df_2["BiciMAD station"].str.split("- ", expand = True)[1]
    bicimad_stations_1 = df_2[["BiciMAD station", "Station location", "Latitude", "Longitude"]]
    bicimad_stations_1['Latitude'] = bicimad_stations_1['Latitude'].astype(float)
    bicimad_stations_1['Longitude'] = bicimad_stations_1['Longitude'].astype(float)
    return bicimad_stations_1

def drop_columns(df_k):
    bicimad_stations_2 = df_k[["BiciMAD station", "Station location"]]
    return bicimad_stations_2
def drop_columns_2(df_l):
    df_col_pub_5 = df_l[["Place of interest", "Type of place", "Place address"]]
    return df_col_pub_5

def concatenate(df_x, df_y):
    nearest_bicimad_cp = pd.concat([df_x, df_y], axis=1)
    return nearest_bicimad_cp

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
    return closest_point

def all_closest_stations(df_i, df_j):
    all_closest_stations_1 = df_i.apply(lambda x: closest_station(df_j, x["Latitude"], 
                                            x["Longitude"]), axis=1)
    return all_closest_stations_1

df_col_pub_a = acquire_1()

bicimad_stations_a = acquire_2()

df_col_pub_b = wrangling_1(df_col_pub_a)

bicimad_stations_b = wrangling_2(bicimad_stations_a)

all_closest_stations_2 = all_closest_stations(df_col_pub_b, bicimad_stations_b)

bicimad_stations_3 = drop_columns(all_closest_stations_2)

df_col_pub_6 = drop_columns_2(df_col_pub_b)

nearest_bicimad_cp_1 = concatenate(df_col_pub_6, bicimad_stations_3)

def get_csv():
    return nearest_bicimad_cp.to_csv('../data/nearest_bicimad_cp.csv', index=False, encoding='utf-8')

get_csv()

