# This file is used to generate nonlinear opensees model by OpenSeesPy
# Created by Jiajun Du @ Tongji University in July 2023

from openseespy.opensees import ops
import numpy as np
from Functions import NodesAroundPanelZone


def NonlinearAnalysis(building, columns, beams, joints, analysis_type):
    """
    This function is used to establish the NonlinearAnalysis Model and return
    the required response.
    :param building: a class defined in "building_information.py"
    :param columns: a two-dimensional list[x][y] and 
                    each element is a column object  defined in "column.py"
                    x: from 0 to (NumOfStory - 1)
                    y: from 0 to (NumOfBay + 1)
    :param beams: a two-dimensional lis[x][y] and 
                    each element is a beam object defined in "beam.py"
                    x: from 0 to (NumOfStory - 1)
                    y: from 0 to (NumOfBay)                         
    :param joints: a two-dimensional list[x][y] and
                    each element is a joint object defined in "joint.py"
                    x: from 0 to (NumOfStory - 1)
                    y: from 0 to (NumOfBay + 1)
    :param anlaysis_type: a string represents the current model's 
                            anlaysis type:
                            'EigenValueAnalysis',
                            'PushoverAnalysis',
                            'DynamicAnalysis'
    """

    # Clear the memory
    ops.wipe()

    # Defining model builder
    ops.model('basic', '-ndm', 2, '-ndf', 3)

    # TODOS: Define the periods to use for the Rayleigh damping calculations

    ################ Defining variables ################
    # Define Geometric Transformation
    PDeltaTransf = 1
    LinearTransf = 2
    # Set up geometric transformations of element
    ops.geomTransf('PDelta', PDeltaTransf)
    ops.geomTransf('Linear', LinearTransf)
    # Define n factor used for modified IMK material model
    n = 10
    # Define Young's modulus for steel material
    Es = 29000
    # Define Yielding stress for steel material
    Fy = 50.00
    # Define a very small number
    Negligible = 1e-12
    # Define a very large number
    LargeNumber = 1e12
    # Define gravity constant
    g = 386.4
    # Define rigid links between leaning column and frame
    TrussMatID = 600  # Material tag
    AreaRigid = 1e12  # Large area
    IRigid = 1e12  # Large moment of inertia
    ops.uniaxialMaterial('Elastic', TrussMatID, Es)
    # Define very stiff material used for axial stiffness of beam/column hinges
    StiffMatID = 1200
    ops.uniaxialMaterial('Elastic', StiffMatID, LargeNumber)
    print('Variable defined!')

    ################ Defining nodes (building, beams, columns) ################
    # Create all node tags and coordinates for nonlinear analysis model
    # Units: inch
    # Set bay width and story height
    BayWidth = building.geometry['X bay width'] * 12
    FirstStory = building.geometry['first story height'] * 12
    TypicalStory = building.geometry['typical story height'] * 12

    # Define the panel sizes before building the node coordinates
    # Set panel zone size as column depth and beam depth
    n_story = building.geometry['number of story']
    n_Xbay = building.geometry['number of X bay']
    PanelSizeLevelColumn = np.zeros([n_story + 1, n_Xbay + 1, 2])
    for i in range(1, n_story + 2):
        # i is floor level number (1 for ground level)
        for j in range(1, n_Xbay + 2):
            if i == 1:
                PanelSizeLevelColumn[i - 1, j - 1, :] = [0, 0]
            else:
                # Note that beam size is identical in one floor level.
                # Therefore second index for beams doesn't need to be changed
                PanelSizeLevelColumn[i - 1, j - 1, :] = [
                    columns[i - 2][j - 1].section['d'],
                    beams[i - 2][0].section['d']
                ]

    # Create nodes for frame using pre-defined function "NodesAroundPanelZone"
    # Set max number of columns (excluding leaning column)
    # and floors (counting 1 for ground level)
    MaximumFloor = n_story + 1
    MaximumCol = n_Xbay + 1

    # Define nodes for the frame
    for i in range(1, n_story + 2):  # i is the floor level number
        for j in range(1, n_Xbay + 2):  # j is the column label
            if i <= 2:
                Height = (i - 1) * FirstStory
            else:
                Height = FirstStory + (i - 2) * TypicalStory
                NodesAroundPanelZone(j, i, (j - 1) * BayWidth, Height,
                                     PanelSizeLevelColumn[i - 1, j - 1, :],
                                     MaximumFloor, MaximumCol)
    print('Nodes for frame are defined!')

    # Create the nodes for leaning column
    # Define nodes for leaning column
    x_LeanCol = (n_Xbay + 1) * BayWidth
    for i in range(1, n_story + 2):
        nodetag = int('%i%i' % (n_Xbay + 2, i))
        if i <= 2:
            Height = (i - 1) * FirstStory
        else:
            Height = FirstStory + (i - 2) * TypicalStory
        ops.node(nodetag, x_LeanCol, Height)

    print('Nodes for leaning column defined!')

    # Create extra nodes for leaning column springs
    for i in range(2, n_story + 2):
        # The node below floor level
        nodetag = int('%i%i%i' % (n_Xbay + 2, i, 2))
        Height = FirstStory + (i - 2) * TypicalStory
        ops.node(nodetag, x_LeanCol, Height)
        # If it's top story, node above roof is not needed
        # because no leaning column above roof
        if i < n_story + 1:
            # The node above floor level
            nodetag = int('%i%i%i' % (n_Xbay + 2, i, 4))
            ops.node(nodetag, x_LeanCol, Height)
        else:
            pass
    print('Extra nodes for leaning column springs defined!')


################ Define node fixities ################

################ Define floor constraint ################

################ Define beam hinge material models ################

################ Define column hinge material models ################

################ Define beam elements ################

################ Define column elements ################

################ Define beam hinges ################

################ Define column hinges ################

################ Define masses ################

################ Define elements in panel zone ################

################ Define springs in panel zone ################

################ Define gravity loads ################

################ Define gravity analysis ################

################ Define damping ################

################ Define ground motion scale factor ################

################ Define Time History ################

print('Analysis Completed!')
