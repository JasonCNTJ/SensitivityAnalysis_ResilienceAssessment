from global_variables import PERIOD_FOR_DRIFT_LIMIT
from help_functions import determine_Fa_coefficient, determine_Fv_coefficient, determine_Cu_coefficient, determine_k_coeficient, determine_floor_height
from help_functions import calculate_Cs_coefficient, calculate_DBE_acceleration, calculate_seismic_force
import os
import pandas as pd
import numpy as np


class Building_object:
    """
    Create a building object.
    """
    def __init__(self, directory, member_size, gravity_loads):
        self.directory = directory
        self.geometry = {}
        self.member_size = member_size
        self.gravity_loads = gravity_loads
        self.elf_parameters = {}
        self.seismic_force_for_drift = {}
        self.seismic_force_for_strength = {}

        # call methods
        self.read_geometry()
        self.read_elf_parameters()
        self.compute_seismic_force()

    def read_geometry(self):
        """
        This method is used to read the building geometry information from .csv files:
        (1) Change the working directory to the folder where .csv data are stored
        (2) Open the .csv file and save all relevant information to the object itself
        """
        os.chdir(self.directory['building data'])
        with open('Geometry.csv', 'r') as csvfile:
            geometry_data = pd.read_csv(csvfile, header=0)

        # Each variable is a scalar
        number_of_story = geometry_data.loc[0, 'number of story']
        number_of_X_bay = geometry_data.loc[0, 'number of X bay']
        number_of_Z_bay = geometry_data.loc[0, 'number of Z bay']
        first_story_height = geometry_data.loc[0, 'first story height']
        typical_story_height = geometry_data.loc[0, 'typical story height']
        X_bay_width = geometry_data.loc[0, 'X bay width']
        Z_bay_width = geometry_data.loc[0, 'Z bay width']
        number_of_X_LFRS = geometry_data.loc[0, 'number of X LFRS']  # number of lateral resisting frame in X direction
        number_of_Z_LFRS = geometry_data.loc[0, 'number of Z LFRS']  # number of lateral resisting frame in Z direction
        # Call function defined in "help_functions.py" to determine the height for each floor level
        floor_height = determine_floor_height(number_of_story, first_story_height, typical_story_height)
        # Store all necessary information into a dictionary named geometry
        self.geometry = {'number of story': number_of_story,
                         'number of X bay': number_of_X_bay,
                         'number of Z bay': number_of_Z_bay,
                         'first story height': first_story_height,
                         'typical story height': typical_story_height,
                         'X bay width': X_bay_width,
                         'Z bay width': Z_bay_width,
                         'number of X LFRS': number_of_X_LFRS,
                         'number of Z LFRS': number_of_Z_LFRS,
                         'floor height': floor_height}

    def read_elf_parameters(self):
        """
        This method is used to read equivalent lateral force (in short: elf) parameters and calculate SDS and SD1
        (1) Read equivalent lateral force parameters
        (2) Calculate SMS, SM1, SDS, SD1 values and save them into the attribute
        """
        elf_parameters_data = pd.read_csv(os.path.join(self.directory['building data'], 'ELFParameters.csv'), header=0)

        # Determine Fa and Fv coefficient based on site class and Ss and S1 (ASCE 7-10 Table 11.4-1 & 11.4-2)
        # Call function defined in "help_functions.py" to calculate two coefficients: Fa and Fv
        Fa = determine_Fa_coefficient(elf_parameters_data.loc[0, 'site class'], elf_parameters_data.loc[0, 'Ss'])
        Fv = determine_Fv_coefficient(elf_parameters_data.loc[0, 'site class'], elf_parameters_data.loc[0, 'S1'])
        # Determine SMS, SM1, SDS, SD1 using the defined function in "help_functions.py"
        SMS, SM1, SDS, SD1 = calculate_DBE_acceleration(elf_parameters_data.loc[0, 'Ss'],
                                                        elf_parameters_data.loc[0, 'S1'], Fa, Fv)
        # Determine Cu using the defined function in "help_functions.py"
        Cu = determine_Cu_coefficient(SD1)

        # Calculate the building period: approximate fundamental period and upper bound period
        approximate_period = elf_parameters_data.loc[0, 'Ct'] \
                             * (self.geometry['floor height'][-1]**elf_parameters_data.loc[0, 'x'])
        upper_period = Cu * approximate_period

        # Save all coefficient into the dictionary named elf_parameters
        self.elf_parameters = {'Ss': elf_parameters_data.loc[0, 'Ss'], 'S1': elf_parameters_data.loc[0, 'S1'],
                               'TL': elf_parameters_data.loc[0, 'TL'], 'Cd': elf_parameters_data.loc[0, 'Cd'],
                               'R': elf_parameters_data.loc[0, 'R'], 'Ie': elf_parameters_data.loc[0, 'Ie'],
                               'rho': elf_parameters_data.loc[0, 'rho'],
                               'site class': elf_parameters_data.loc[0, 'site class'],
                               'Ct': elf_parameters_data.loc[0, 'Ct'], 'x': elf_parameters_data.loc[0, 'x'],
                               'Fa': Fa, 'Fv': Fv, 'SMS': SMS, 'SM1': SM1, 'SDS': SDS, 'SD1': SD1, 'Cu': Cu,
                               'approximate period': approximate_period, 'period': upper_period, 'modal period': 1.0}  # !
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compute_seismic_force(self):
        """
        This method is used to calculate the seismic story force using ELF procedure specified in ASCE 7-10 Section 12.8
        (1) Determine the floor level height and save it in a list (array)
        (2) Determine the correct period between first mode period and CuTa
        (3) Determine the Cs coefficient
        (4) Determine the lateral force at each floor level (ground to roof) and save it in an arrary
        """
        # Please note that the period for computing the required strength should be bounded by CuTa
        period_for_strength = min(self.elf_parameters['modal period'], self.elf_parameters['period'])
        # The period used for computing story drift is not required to be bounded by CuTa
        if PERIOD_FOR_DRIFT_LIMIT:
            period_for_drift = min(self.elf_parameters['modal period'], self.elf_parameters['period'])
        else:
            period_for_drift = self.elf_parameters['modal period']
        # Call function defined in "help_functions.py" to determine the seismic response coefficient
        Cs_for_strength = calculate_Cs_coefficient(self.elf_parameters['SDS'], self.elf_parameters['SD1'],
                                                   self.elf_parameters['S1'], period_for_strength,
                                                   self.elf_parameters['TL'], self.elf_parameters['R'],
                                                   self.elf_parameters['Ie'], False)
        Cs_for_drift = calculate_Cs_coefficient(self.elf_parameters['SDS'], self.elf_parameters['SD1'],
                                                self.elf_parameters['S1'], period_for_drift,
                                                self.elf_parameters['TL'], self.elf_parameters['R'],
                                                self.elf_parameters['Ie'], True)
        # Calculate the base shear
        base_shear_for_strength = Cs_for_strength * np.sum(self.gravity_loads['floor weight'])
        base_shear_for_drift = Cs_for_drift * np.sum(self.gravity_loads['floor weight'])
        # Call function defined in "help_functions.py" to compute k coefficient
        k = determine_k_coeficient(self.elf_parameters['period'])
        # Call function defined in "help_functions.py" to determine the lateral force for each floor level
        lateral_story_force_for_strength, story_shear_for_strength \
            = calculate_seismic_force(base_shear_for_strength, self.gravity_loads['floor weight'], \
                                      self.geometry['floor height'], k)
        lateral_story_force_for_drift, story_shear_for_drift \
            = calculate_seismic_force(base_shear_for_drift, self.gravity_loads['floor weight'], \
                                      self.geometry['floor height'], k)
        # Store information into class attribute
        self.seismic_force_for_strength = {'lateral story force': lateral_story_force_for_strength, \
                                           'story shear': story_shear_for_strength, \
                                           'base shear': base_shear_for_strength, 'Cs': Cs_for_strength}
        self.seismic_force_for_drift = {'lateral story force': lateral_story_force_for_drift, \
                                           'story shear': story_shear_for_drift, \
                                           'base shear': base_shear_for_drift, 'Cs': Cs_for_drift}