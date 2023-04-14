import pandas as pd
import numpy as np
import requests 
import re

#wrangling functions

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
    df_col_pub_4.to_csv('./data/raw_wrangling_1.csv')
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
    bicimad_stations_1.to_csv('./data/raw_wrangling_2.csv')
    return bicimad_stations_1

def drop_columns(df_k):
    bicimad_stations_2 = df_k[["BiciMAD station", "Station location"]]
    return bicimad_stations_2
def drop_columns_2(df_l):
    df_col_pub_5 = df_l[["Place of interest", "Type of place", "Place address"]]
    df_col_pub_5.to_csv('./data/raw_drop_columns.csv')
    return df_col_pub_5

def concatenate(df_x, df_y):
    nearest_bicimad_cp = pd.concat([df_x, df_y], axis=1)
    nearest_bicimad_cp.to_csv('./data/raw_concatenate.csv')
    return nearest_bicimad_cp