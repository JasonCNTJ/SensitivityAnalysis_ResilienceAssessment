# This file is used to define the class of beam

import numpy as np

# from global_variables import SECTION_DATABASE
from help_functions import search_section_property


class Beam(object):
    """
    This class is used to define a beam member, which has the following attributes:
    Beam section, a dictionary including size and associated properties.
    """

    def __init__(self, section_size, length, steel, SECTION_DATABASE):

        self.section = search_section_property(section_size, SECTION_DATABASE)
        # length = building.geometry['X bay width']
        self.length = length
        self.plastic_hinge = {}

        self.determine_spacing_between_lateral_support(steel)
        self.calculate_hinge_parameters(steel)

    def determine_spacing_between_lateral_support(self, steel):
        """
        This method is used to compute the spacing between two lateral supports.
        :param steel: a class defined in "steel_material.py" file.
        :return: a float number indicating the spacing.
        """
        # Compute limit for spacing (Remember to convert from inches to feet)
        spacing_limit = 0.086 * self.section['ry'] * steel.E / steel.Fy * 1/12.0
        # Start with the number of lateral support equal to 1
        # Check whether the current lateral support is enough
        # If it is not sufficient, increase the number of lateral support until the requirement is satisfied
        number_lateral_support = 1
        while self.length/(number_lateral_support+1) > spacing_limit:
            number_lateral_support += 1
        # Check whether the spacing is less than Lp
        # If the spacing greater than Lp, then reduce the spacing such that the flexural strength is governed by
        # plastic yielding.
        Lp = 1.76 * self.section['ry'] * np.sqrt(steel.E/steel.Fy)
        while (self.length/number_lateral_support+1) > Lp:
            number_lateral_support += 1
        self.spacing = self.length/(number_lateral_support+1)

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
        # unit: kips, inches
        # beam spacing and length is in feet, remember to convert it to inches
        c1 = 25.4  # c1_unit
        c2 = 6.895  # c2_unit
        McMy = 1.10  # Capping moment to yielding moment ratio. Lignos et al. used 1.05 whereas Prof. Burton used 1.11.
        h = self.section['d'] - 2*self.section['tf']  # Web depth
        self.plastic_hinge['K0'] = 6 * steel.E * self.section['Ix'] / (self.length*12.0)
        self.plastic_hinge['Myp'] = self.section['Zx'] * steel.Fy
        self.plastic_hinge['My'] = 1.00 * self.plastic_hinge['Myp']
        self.plastic_hinge['Lambda'] = 585 * (h/self.section['tw'])**(-1.14) \
                                       * (self.section['bf']/(2*self.section['tf']))**(-0.632) \
                                       * (self.spacing*12.0/self.section['ry'])**(-0.205) \
                                       * (c2*steel.Fy/355)**(-0.391)
        # Pre-capping rotation
        self.plastic_hinge['theta_p'] = 0.19 * (h/self.section['tw'])**(-0.314) \
                                        * (self.section['bf']/(2*self.section['tf']))**(-0.100) \
                                        * (self.spacing*12.0/self.section['ry'])**(-0.185) \
                                        * (self.length*12.0/self.section['d'])**0.113 \
                                        * (c1*self.section['d']/533)**(-0.760) \
                                        * (c2*steel.Fy/355)**(-0.070)
        # Pre-capping rotation is further revised to exclude the elastic deformation
        self.plastic_hinge['theta_p'] = self.plastic_hinge['theta_p'] \
                                        - (McMy - 1.0) * self.plastic_hinge['My'] / self.plastic_hinge['K0']
        # Post-capping rotation
        self.plastic_hinge['theta_pc'] = 9.52 * (h/self.section['tw'])**(-0.513) \
                                         * (self.section['bf']/(2*self.section['tf']))**(-0.863) \
                                         * (self.spacing*12.0/self.section['ry'])**(-0.108) \
                                         * (c2*steel.Fy/355)**(-0.360)
        # Post-capping rotation is further revised to account for elastic deformation
        self.plastic_hinge['theta_y'] = self.plastic_hinge['My'] / self.plastic_hinge['K0']
        self.plastic_hinge['theta_pc'] = self.plastic_hinge['theta_pc'] \
                                         + self.plastic_hinge['theta_y'] \
                                         + (McMy - 1.0) * self.plastic_hinge['My'] / self.plastic_hinge['K0']
        self.plastic_hinge['as'] = (McMy-1.0)*self.plastic_hinge['My']\
                                   /(self.plastic_hinge['theta_p']*self.plastic_hinge['K0'])
        self.plastic_hinge['residual'] = 0.40
        self.plastic_hinge['theta_u'] = 0.20


