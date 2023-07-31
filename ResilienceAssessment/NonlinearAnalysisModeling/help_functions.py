# This file is used to define helpful functions that are used in either main
# main program or user defined class
# Originally developed by GUAN, XINGQUAN @ UCLA in June 2018
# Edited by Jiajun Du @ Tongji University in July 2023

import numpy as np
import re
import sys

# from global_variables import SECTION_DATABASE

# def determine_Fa_coefficient(site_class, Ss):

# def determine_Fv_coefficient(site_class, S1):

# def calculate_DBE_acceleration(Ss, S1, Fa, Fv):

# def determine_Cu_coefficient(SD1):

def determine_floor_height(NumOfStroy, first_story_height, typical_story_height):
    """
    This function is used to calculate the height for each floor.
    Unit: ft
    :param NumOfStory: a scalar which describes the number of story
    :param first_story_height: a scalar which describes the 1st story height
    :param typical_story_height: a scalar which describes the typical story height
                                for other floors except 1st story
    :return: an array which includes the height for each floor level
    """
    floor_height = np.zeros([NumOfStroy + 1, 1])
    for level in range(1, NumOfStroy + 2):
        if level == 1: # ground level
            floor_height[level - 1] = 0
        elif level == 2:
            floor_height[level - 1] = first_story_height
        else:
            floor_height[level - 1] = first_story_height + typical_story_height * (level - 2)
        
    return floor_height


# def calculate_Cs_coefficient(SDS, SD1, S1, T, TL, R, Ie, for_drift):

# def determine_k_coeficient(period):

# def calculate_seismic_force(base_shear, floor_weight, floor_height, k):

# def find_section_candidate(target_depth, section_database):

# def search_member_size(target_name, target_quantity, candidate, section_database):

def search_section_property(target_size, section_database):
    """
    This function is used to obtain the section property when section size is given.
    The output will be stored in a dictionary.
    :param target_size: a string which defines section size, e.g. 'W14X500'
    :param section_database: a dataframe read from SMF_Section_Property.csv in 'Library' folder
    :return: section_info: a dictionary which includes section size, index, and associated properties.
    """
    # Loop over the sections in the SMF section database and find the one which mathces the target size
    # Then the property of the target section is returned as a dictionary
    # If target size cannot match any existing sizes in database, a warning message should be given.
    try:
        for indx in np.array(section_database['index']):
            if target_size == section_database.loc[indx, 'section size']:
                section_info = section_database.loc[indx, :]
        return section_info.to_dict()
    except:
        sys.stderr.write('Error: wrong size nominated!\nNo such size exists in section database!')
        sys.exit(1)

    





