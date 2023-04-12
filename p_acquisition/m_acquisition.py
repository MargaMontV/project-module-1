import pandas as pd
import requests


# acquisition functions

def acquire_1():
    end_point_1 = 'https://datos.madrid.es/egob/' # Main End-Point
    body_1 = 'catalogo/202311-0-colegios-publicos.json'# Body
    pulls_response_1 = requests.get(end_point_1 + body_1)
    pulls_json_1 = pulls_response_1.json()
    df_col_pub = pd.json_normalize(pulls_json_1, ['@graph'])
    return df_col_pub

def acquire_2():
    bicimad_stations = pd.read_csv('../data/bicimad_stations.csv')
    return bicimad_stations