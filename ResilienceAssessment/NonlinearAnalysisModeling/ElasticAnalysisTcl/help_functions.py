import csv
import numpy as np


def read_tworow_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data_dict = next(reader)  # 读取第一行的数据并转换为字典
    return data_dict

def determine_floor_height(number_of_story, first_story_height, typical_story_height):
    """
    This function is used to calculate the height for each floor level: from ground floor to roof
    Obviously, the height for ground floor level is zero
    Unit: foot (ft)
    :param number_of_story: a scalar which describes the number of story for a certain building
    :param first_story_height: a scalar which describes the 1st story height of the building
    :param typical_story_height: a scalar which describes the typical story height for other stories
           except 1st story
    :return: an array which includes the height for each floor level (ground to roof)
    """
    floor_height = np.zeros([number_of_story + 1, 1])
    for level in range(1, number_of_story + 2):
        if level == 1:
            floor_height[level - 1] = 0
        elif level == 2:
            floor_height[level - 1] = 0 + first_story_height
        else:
            floor_height[level - 1] = first_story_height + typical_story_height * (level - 2)

    return floor_height

def determine_Fa_coefficient(site_class, Ss):
    """
    This function is used to determine Fa coefficient, which is based on ASCE 7-10 Table 11.4-1
    :param Ss: a scalar given in building class
    :param site_class: a string: 'A', 'B', 'C', 'D', or 'E' given in building information
    :return: a scalar which is Fa coefficient
    """
    if site_class == 'A':
        Fa = 0.8
    elif site_class == 'B':
        Fa = 1.0
    elif site_class == 'C':
        if Ss <= 0.5:
            Fa = 1.2
        elif Ss <= 1.0:
            Fa = 1.2 - 0.4*(Ss - 0.5)
        else:
            Fa = 1.0
    elif site_class == 'D':
        if Ss <= 0.25:
            Fa = 1.6
        elif Ss <= 0.75:
            Fa = 1.6 - 0.8*(Ss - 0.25)
        elif Ss <= 1.25:
            Fa = 1.2 - 0.4*(Ss - 0.75)
        else:
            Fa = 1.0
    elif site_class == 'E':
        if Ss <= 0.25:
            Fa = 2.5
        elif Ss <= 0.5:
            Fa = 2.5 - 3.2*(Ss - 0.25)
        elif Ss <= 0.75:
            Fa = 1.7 - 2.0*(Ss - 0.5)
        elif Ss <= 1.0:
            Fa = 1.2 - 1.2*(Ss - 0.75)
        else:
            Fa = 0.9
    else:
        Fa = None
        print("Site class is entered with an invalid value")

    return Fa


def determine_Fv_coefficient(site_class, S1):
    """
    This function is used to determine Fv coefficient, which is based on ASCE 7-10 Table 11.4-2
    :param S1: a scalar given in building class
    :param site_class: a string 'A', 'B', 'C', 'D' or 'E' given in building class
    :return: a scalar which is Fv coefficient
    """
    if site_class == 'A':
        Fv = 0.8
    elif site_class == 'B':
        Fv = 1.0
    elif site_class == 'C':
        if S1 <= 0.1:
            Fv = 1.7
        elif S1 <= 0.5:
            Fv = 1.7 - 1.0*(S1 - 0.1)
        else:
            Fv = 1.3
    elif site_class == 'D':
        if S1 <= 0.1:
            Fv = 2.4
        elif S1 <= 0.2:
            Fv = 2.4 - 4*(S1 - 0.1)
        elif S1 <= 0.4:
            Fv = 2.0 - 2*(S1 - 0.2)
        elif S1 <= 0.5:
            Fv = 1.6 - 1*(S1 - 0.4)
        else:
            Fv = 1.5
    elif site_class == 'E':
        if S1 <= 0.1:
            Fv = 3.5
        elif S1 <= 0.2:
            Fv = 3.5 - 3*(S1 - 0.1)
        elif S1 <= 0.4:
            Fv = 3.2 - 4*(S1 - 0.2)
        else:
            Fv = 2.4
    else:
        Fv = None
        print("Site class is entered with an invalid value")

    return Fv


def calculate_DBE_acceleration(Ss, S1, Fa, Fv):
    """
    This function is used to calculate design spectrum acceleration parameters,
    which is based ASCE 7-10 Section 11.4
    Note: All notations for these variables can be found in ASCE 7-10.
    :param Ss: a scalar given in building information (problem statement)
    :param S1: a scalar given in building information (problem statement)
    :param Fa: a scalar computed from determine_Fa_coefficient
    :param Fv: a scalar computed from determine_Fv_coefficient
    :return: SMS, SM1, SDS, SD1: four scalars which are required for lateral force calculation
    """
    SMS = Fa * Ss
    SM1 = Fv * S1
    SDS = 2/3 * SMS
    SD1 = 2/3 * SM1
    return SMS, SM1, SDS, SD1


def determine_Cu_coefficient(SD1):
    """
    This function is used to determine Cu coefficient, which is based on ASCE 7-10 Table 12.8-1
    Note: All notations for these variables can be found in ASCE 7-10.
    :param SD1: a scalar calculated from funtion determine_DBE_acceleration
    :return: Cu: a scalar
    """
    if SD1 <= 0.1:
        Cu = 1.7
    elif SD1 <= 0.15:
        Cu = 1.7 - 2 * (SD1 - 0.1)
    elif SD1 <= 0.2:
        Cu = 1.6 - 2 * (SD1 - 0.15)
    elif SD1 <= 0.3:
        Cu = 1.5 - 1 * (SD1 - 0.2)
    elif SD1 <= 0.4:
        Cu = 1.4
    else:
        Cu = 1.4

    return Cu


def calculate_Cs_coefficient(SDS, SD1, S1, T, TL, R, Ie, for_drift):
    """
    This function is used to calculate the seismic response coefficient based on ASCE 7-10 Section 12.8.1
    Unit: kips, g (gravity constant), second
    Note: All notations for these variables can be found in ASCE 7-10.
    :param SDS: a scalar determined using Equation 11.4-3; output from "calculate_DBE_acceleration" function
    :param SD1: a scalar determined using Equation 11.4-4; output from "calculate_DBE_acceleration" function
    :param S1: a scalar given in building information (problem statement)
    :param T: building period; a scalar determined using Equation 12.8-1 and Cu;
              implemented in "BuildingInformation" object attribute.
    :param TL: long-period transition
    :param R: a scalar given in building information
    :param Ie: a scalar given in building information
    :param for_drift: a Boolean variable to denote whether the Cs coefficient is computed for drift.
    :return: Cs: seismic response coefficient; determined using Equations 12.8-2 to 12.8-6
    """
    # Equation 12.8-2
    Cs_initial = SDS/(R/Ie)

    # Equation 12.8-3 or 12.8-4, Cs coefficient should not exceed the following value
    if T <= TL:
        Cs_upper = SD1/(T * (R/Ie))
    else:
        Cs_upper = SD1 * TL/(T ** 2 * (R/Ie))

    # Equation 12.8-2 results shall be smaller than upper bound of Cs
    if Cs_initial <= Cs_upper:
        Cs = Cs_initial
    else:
        Cs = Cs_upper

    # Equation 12.8-5, Cs shall not be less than the following value
    Cs_lower_1 = np.max([0.044*SDS*Ie, 0.01])

    # Compare the Cs value with lower bound: if the Cs coefficient is used to compute the lateral force for drift, then
    # Equation 12.8-5 need not be considered.
    if not for_drift:
        if Cs >= Cs_lower_1:
            pass
        else:
            Cs = Cs_lower_1

    # Equation 12.8-6. if S1 is equal to or greater than 0.6g, Cs shall not be less than the following value
    if S1 >= 0.6:
        Cs_lower_2 = 0.5*S1/(R/Ie)
        if Cs >= Cs_lower_2:
            pass
        else:
            Cs = Cs_lower_2
    else:
        pass

    return Cs


def determine_k_coeficient(period):
    """
    This function is used to determine the coefficient k based on ASCE 7-10 Section 12.8.3
    :param period: building period;
    :return: k: a scalar will be used in Equation 12.8-12 in ASCE 7-10
    """
    if period <= 0.5:
        k = 1
    elif period >= 2.5:
        k = 2
    else:
        k = 1 + 0.5*(period - 0.5)

    return k


def calculate_seismic_force(base_shear, floor_weight, floor_height, k):
    """
    This function is used to calculate the seismic story force for each floor level
    Unit: kip, foot
    :param base_shear: a scalar, total base shear for the building
    :param floor_weight: a vector with a length of number_of_story
    :param floor_height: a vector with a length of (number_of_story+1)
    :param k: a scalar given by "determine_k_coefficient"
    :return: Fx: a vector describes the lateral force for each floor level
    """
    # Calculate the product of floor weight and floor height
    # Note that floor height includes ground floor, which will not be used in the actual calculation.
    # Ground floor is stored here for completeness.
    weight_floor_height = floor_weight * floor_height[1:, 0]**k
    # Equation 12.8-12 in ASCE 7-10
    Cvx = weight_floor_height/np.sum(weight_floor_height)
    # Calculate the seismic story force
    seismic_force = Cvx * base_shear
    # Calculate the shear force for each story: from top story to bottom story
    story_shear = np.zeros([len(floor_weight), 1])
    for story in range(len(floor_weight)-1, -1, -1):
        story_shear[story] = np.sum(seismic_force[story:])

    return seismic_force, story_shear