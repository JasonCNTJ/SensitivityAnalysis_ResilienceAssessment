# This file is used to define the class of column, which includes the axial, shear, and flexural strengths of column
# Developed by GUAN, XINGQUAN @ UCLA in Apr. 2018
# Updated in Oct. 2018

import numpy as np

from scipy import interpolate

from help_functions import search_section_property
# from global_variables import SECTION_DATABASE

# #########################################################################
#                           Define a class of column                      #
# #########################################################################

class Column(object):
    """
    This class is used to define a column member, which has the following attributes:
    (1) Column section, a dictionary including the size and associated properties.
    (2) Column demand, a dictionary including axial, shear, and flexural demands.
    (3) Column strength, a dictionary including axial, shear, and flexural strengths.
    (4) Column flag, an integer with value of zero or nonzero. If it's zero, the column is feasible.
    """

    def __init__(self, section_size, axial_demand, Lx, Ly, steel, SECTION_DATABASE):
        """
        This function initializes the attributes of class of column.
        :param section_size: a string which specifies the size for column.
        :param axial_demand: a float number which describes axial demand.
        :param shear_demand: a float number which describes shear demand.
        :param moment_demand_bot: a float number which describes moment demand at bottom of column.
        :param moment_demand_top: a float number which describes moment demand at top of column.
        :param Lx: unbraced length in x direction.
        :param Ly: unbraced length in y direction.
        """
        # Assign the necessary information for column class
        self.section = search_section_property(section_size, SECTION_DATABASE)
        self.demand = {'axial': axial_demand}
        self.unbraced_length = {'x': Lx, 'y': Ly}

        # Initialize the strength dictionary with an empty dictionary
        self.strength = {}
        # Initialize the dictionary to denote the possible failure mode (if any) of column
        self.is_feasible = {}
        # Initialize the dictionary to indicate the demand to capacity ratios
        self.demand_capacity_ratio = {}
        # Define a boolean flag to indicate the overall check results.
        self.flag = None

        # Define a hinge dictionary to store each parameters of OpenSees bilinear property
        self.plastic_hinge = {}

        # Using the following method to compute the strength and check whether strength is sufficient

        self.check_axial_strength(steel)
        # self.check_shear_strength(steel)
        # self.check_flexural_strength(steel)
        # self.check_combined_loads()
        self.compute_demand_capacity_ratio()
        self.calculate_hinge_parameters(steel)



    def check_axial_strength(self, steel):
        """
        This method is used to check the axial strength of the column.
        :param steel: a class defined in "steel_material.py" file.
        :return: a float number denoting the axial strength
                 and a boolean variable denoting whether the column strength is enough.
        """
        # Default values for two coefficient
        Kx = 1.0
        Ky = 1.0
        slenderness_ratio = max([Kx*self.unbraced_length['x']/self.section['rx'],
                                 Ky*self.unbraced_length['y']/self.section['ry']])
        # Compute elastic buckling stress
        Fe = np.pi**2 * steel.E / (slenderness_ratio**2)
        # Calculate critical stress
        if slenderness_ratio <= (4.71 * np.sqrt(steel.E/steel.Fy)):
            Fcr = 0.658**(steel.Fy/Fe) * steel.Fy
        else:
            Fcr = 0.877 * Fe
        # Compute nominal compressive strength
        Pn = Fcr * self.section['A']
        # Store axial strength into "strength" dictionary
        phi = 0.9
        self.strength['axial'] = phi * Pn


    def compute_demand_capacity_ratio(self):
        """
        This method is used to calculate the demand to capacity ratios for column components
        :return: a dictionary which includes ratios for axial force, shear force, flexural moment, and combined loading.
        """
        self.demand_capacity_ratio['axial'] = self.demand['axial'] / self.strength['axial']


    def calculate_hinge_parameters(self, steel):
        """
        This method is used to compute the modeling parameters for plastic hinge using modified IMK material model.
        :return: a dictionary including each parameters required for nonlinear modeling in OpenSees.
        """
        # Following content is based on the following reference:
        # [1] Hysteretic models tha incorporate strength and stiffness deterioration
        # [2] Deterioration modeling of steel components in support of collapse prediction of steel moment frames under
        #     earthquake loading
        # [3] Global collapse of frame structures under seismic excitations
        # [4] Sidesway collapse of deteriorating structural systems under seismic excitations
        # dictionary keys explanations:
        #                              K0: beam stiffness, 6*E*Iz/L
        #                              Myp: bending strength, product of section modulus and material yield strength
        #                              My: effective yield strength, 1.06 * bending strength
        #                              Lambda: reference cumulative plastic rotation
        #                              theta_p: pre-capping plastic rotation
        #                              theta_pc: post-capping plastic rotation
        #                              as: strain hardening before modified by n (=10)
        #                              residual: residual strength ratio, use 0.40 per Lignos' OpenSees example
        #                              theta_u: ultimate rotation, use 0.40 per Lignos' OpenSees example
        # Note that for column, the unbraced length is the column length itself.
        # units: kips, inches
        # Note that column unbraced length is in feet, remember to convert it to inches
        c1 = 25.4  # c1_unit
        c2 = 6.895  # c2_unit
        h = self.section['d'] - 2*self.section['tf']  # Web depth
        # Capping moment to yielding moment ratio. Lignos et al. used 1.05 whereas Prof. Burton used 1.11.
        McMy = 12.5 * (h/self.section['tw'])**(-0.2) \
               * (self.unbraced_length['x']*12.0/self.section['ry'])**(-0.4) \
               * (1-self.demand_capacity_ratio['axial']) ** (0.4)
        if McMy < 1.0:
            McMy = 1.0
        if McMy > 1.3:
            McMy = 1.3
        # Beam component rotational stiffness
        self.plastic_hinge['K0'] = 6 * steel.E * self.section['Ix'] / (self.unbraced_length['x']*12.0)
        # Flexual strength
        self.plastic_hinge['Myp'] = self.section['Zx'] * steel.Fy
        # Effective flexural strength
        if self.demand_capacity_ratio['axial'] <= 0.2:
            self.plastic_hinge['My'] = 1.15 * steel.Ry * self.plastic_hinge['Myp'] \
                                       * (1-0.5*self.demand_capacity_ratio['axial'])
        else:
            self.plastic_hinge['My'] = 1.15 * steel.Ry * self.plastic_hinge['Myp'] \
                                       * 9/8 * (1-self.demand_capacity_ratio['axial'])
        # Reference cumulative plastic rotation:
        if self.demand_capacity_ratio['axial'] <= 0.35:
            self.plastic_hinge['Lambda'] = 25000 * (h/self.section['tw'])**(-2.14) \
                                           * (self.unbraced_length['x']/self.section['ry']) ** (-0.53) \
                                           * (1-self.demand_capacity_ratio['axial'])**4.92
        else:
            self.plastic_hinge['Lambda'] = 268000 * (h/self.section['tw'])**(-2.30) \
                                           * (self.unbraced_length['x']/self.section['ry'])**(-1.30) \
                                           * (1-self.demand_capacity_ratio['axial'])**1.19
        # Pre-capping rotation:
        self.plastic_hinge['theta_p'] = 294 * (h/self.section['tw'])**(-1.7) \
                                        * (self.unbraced_length['x']/self.section['ry'])**(-0.7) \
                                        * (1-self.demand_capacity_ratio['axial'])**(1.6)
        self.plastic_hinge['theta_p'] = min(self.plastic_hinge['theta_p'], 0.20)
        # Pre-capping rotation is further revised to exclude the elastic deformation
        self.plastic_hinge['theta_p'] = self.plastic_hinge['theta_p'] \
                                        - (McMy-1.0)*self.plastic_hinge['My'] / self.plastic_hinge['K0']
        # Post-capping rotation:
        self.plastic_hinge['theta_pc'] = 90 * (h/self.section['tw'])**(-0.8) \
                                         * (self.unbraced_length['x']/self.section['ry'])**(-0.8) \
                                         * (1-self.demand_capacity_ratio['axial'])**2.5
        # Post-capping rotation is further revised to account for elastic deformation
        self.plastic_hinge['theta_y'] = self.plastic_hinge['My'] / self.plastic_hinge['K0']
        self.plastic_hinge['theta_pc'] = self.plastic_hinge['theta_pc'] \
                                         + self.plastic_hinge['theta_y'] \
                                         + (McMy-1.0)*self.plastic_hinge['My']/self.plastic_hinge['K0']
        self.plastic_hinge['as'] = (McMy-1.0)*self.plastic_hinge['My']\
                                   /(self.plastic_hinge['theta_p']*self.plastic_hinge['K0'])
        self.plastic_hinge['residual'] = 0.5 - 0.4*self.demand_capacity_ratio['axial']
        self.plastic_hinge['theta_u'] = 0.15
