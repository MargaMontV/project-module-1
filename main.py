# Import libraries
import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man
    
# Argument parser function
def argument_parser():
    parser = argparse.ArgumentParser(description= 'Find the nearest BiciMAD station to Colegios Públicos')
    help_message ='Use option "all" to get the full table for nearest BiciMAD stations to Colegios Públicos. \
        Use option "Name of the colegio público" to specify the name of the colegio público.\
            You will get a table with the nearest BiciMad station to that colegio público.'
    parser.add_argument('-p', '--place', help=help_message, type=str)
    args = parser.parse_args()
    return args

# Pipeline execution
if __name__ == '__main__':
    if argument_parser().place == "all":
        df_col_pub_a = mac.acquire_1()
        bicimad_stations_a = mac.acquire_2()
        df_col_pub_b = mwr.wrangling_1(df_col_pub_a)
        bicimad_stations_b = mwr.wrangling_2(bicimad_stations_a)
        print("Please wait 20 min, the distances are being calculated")
        all_closest_stations_2 = man.all_closest_stations(df_col_pub_b, bicimad_stations_b)
        bicimad_stations_3 = mwr.drop_columns(all_closest_stations_2)
        df_col_pub_6 = mwr.drop_columns_2(df_col_pub_b)
        nearest_bicimad_cp_1 = mwr.concatenate(df_col_pub_6, bicimad_stations_3)
        man.get_csv(nearest_bicimad_cp_1)
        print("You can find your file in the data folder")
    else:      
        df_col_pub_a = mac.acquire_1()
        bicimad_stations_a = mac.acquire_2()
        df_col_pub_b = mwr.wrangling_1(df_col_pub_a)
        bicimad_stations_b = mwr.wrangling_2(bicimad_stations_a)
        print("Please wait 20 min, the distances are being calculated")
        all_closest_stations_2 = man.all_closest_stations(df_col_pub_b, bicimad_stations_b)
        bicimad_stations_3 = mwr.drop_columns(all_closest_stations_2)
        df_col_pub_6 = mwr.drop_columns_2(df_col_pub_b)
        nearest_bicimad_cp_1 = mwr.concatenate(df_col_pub_6, bicimad_stations_3)
        table_for_user = nearest_bicimad_cp_1[nearest_bicimad_cp_1['Place of interest'] == argument_parser().place]
        table_for_user.to_csv('./data/specific_bicimad_st.csv', index=False, encoding='utf-8')
        print("You can find your file in the data folder")
    
        