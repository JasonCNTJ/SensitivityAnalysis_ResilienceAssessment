# This file is used to generate nonlinear opensees model by OpenSeesPy
# Created by Jiajun Du @ Tongji University in July 2023

from openseespy.opensees import ops
import numpy as np
from Functions import NodesAroundPanelZone, CreateIMKMaterial, SectionProperty


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
    # Define the fixity at all column
    for j in range(1, n_Xbay + 2):
        nodetag = int('%i%i%i%i' % (j, 1, 1, 0))
        ops.fix(nodetag, 1, 1, 1)
    # Leaning column base
    nodetag = int('%i%i' % (n_Xbay + 2, 1))
    ops.fix(nodetag, 1, 1, 0)
    print('All column base fixities are defined!')

    ################ Define floor constraint ################
    # Define floor constraint
    # Nodes at same floor level have identical lateral displacement
    # Select mid right node of each panel zone as the constrained node
    ConstrainDOF = 1  # X-direction
    for i in range(2, n_story + 2):
        nodetag1 = ('1%i11' % (i))  # Pier 1
        for j in range(1, n_Xbay + 2):
            nodetag2 = ('%i%i11' % (j, i))  # Pier j
            ops.equalDOF(nodetag1, nodetag2, ConstrainDOF)
        # Include the leaning column nodes to floor constraint
        nodetag3 = ('%i%i' % (n_Xbay + 2, i))
        ops.equalDOF(nodetag1, nodetag3, ConstrainDOF)
    print('Floor constraints are defined!')

    ################ Define beam hinge material models ################
    # Define all beam plastic hinge materials using Modified IMK material model
    material_tag = 70001
    for i in range(2, n_story + 2):
        for j in range(1, n_Xbay + 1):
            # Tag, K0, As, My, Lambda, ThetaP, ThetaPc, Residual, ThetaU
            BeamHingeMaterialLevelBaySet = np.zeros([9])
            BeamHingeMaterialLevelBaySet[0] = material_tag
            BeamHingeMaterialLevelBaySet[1] = beams[i -
                                                    2][j-1].plastic_hinge['K0']
            BeamHingeMaterialLevelBaySet[2] = beams[i -
                                                    2][j-1].plastic_hinge['as']
            BeamHingeMaterialLevelBaySet[3] = beams[i -
                                                    2][j-1].plastic_hinge['My']
            BeamHingeMaterialLevelBaySet[4] = beams[i -
                                                    2][j-1].plastic_hinge['Lambda']
            BeamHingeMaterialLevelBaySet[5] = beams[i -
                                                    2][j-1].plastic_hinge['theta_p']
            BeamHingeMaterialLevelBaySet[6] = beams[i -
                                                    2][j-1].plastic_hinge['theta_pc']
            BeamHingeMaterialLevelBaySet[7] = beams[i -
                                                    2][j-1].plastic_hinge['residual']
            BeamHingeMaterialLevelBaySet[8] = beams[i -
                                                    2][j-1].plastic_hinge['theta_u']
            CreateIMKMaterial(BeamHingeMaterialLevelBaySet[0],
                              BeamHingeMaterialLevelBaySet[1],
                              n,
                              BeamHingeMaterialLevelBaySet[2],
                              BeamHingeMaterialLevelBaySet[3],
                              BeamHingeMaterialLevelBaySet[4],
                              BeamHingeMaterialLevelBaySet[5],
                              BeamHingeMaterialLevelBaySet[6],
                              BeamHingeMaterialLevelBaySet[7],
                              BeamHingeMaterialLevelBaySet[8])
            material_tag += 1
    print('Beam hinge materials defined!')

    ################ Define column hinge material models ################
    # Define column hinge material models
    material_tag = 60001
    for i in range(1, n_story + 1):
        for j in range(1, n_Xbay + 2):
            # Tag, K0, As, My, Lambda, ThetaP, ThetaPc, Residual, ThetaU
            ColumnHingeMaterialLevelBaySet = np.zeros([9])
            ColumnHingeMaterialLevelBaySet[0] = material_tag
            ColumnHingeMaterialLevelBaySet[1] = columns[i -
                                                        1][j-1].plastic_hinge['K0']
            ColumnHingeMaterialLevelBaySet[2] = columns[i -
                                                        1][j-1].plastic_hinge['as']
            ColumnHingeMaterialLevelBaySet[3] = columns[i -
                                                        1][j-1].plastic_hinge['My']
            ColumnHingeMaterialLevelBaySet[4] = columns[i -
                                                        1][j-1].plastic_hinge['Lambda']
            ColumnHingeMaterialLevelBaySet[5] = columns[i -
                                                        1][j-1].plastic_hinge['theta_p']
            ColumnHingeMaterialLevelBaySet[6] = columns[i -
                                                        1][j-1].plastic_hinge['theta_pc']
            ColumnHingeMaterialLevelBaySet[7] = columns[i -
                                                        1][j-1].plastic_hinge['residual']
            ColumnHingeMaterialLevelBaySet[8] = columns[i -
                                                        1][j-1].plastic_hinge['theta_u']
            CreateIMKMaterial(ColumnHingeMaterialLevelBaySet[0],
                              ColumnHingeMaterialLevelBaySet[1],
                              n,
                              ColumnHingeMaterialLevelBaySet[2],
                              ColumnHingeMaterialLevelBaySet[3],
                              ColumnHingeMaterialLevelBaySet[4],
                              ColumnHingeMaterialLevelBaySet[5],
                              ColumnHingeMaterialLevelBaySet[6],
                              ColumnHingeMaterialLevelBaySet[7],
                              ColumnHingeMaterialLevelBaySet[8])
            material_tag += 1
    print('Column hinge materials are defined!')

    ################ Define beam elements ################
    # Define beam section sizes
    SectionDatabase = pd.read_csv(
        r'C:\Users\12734\OneDrive\重要文件\可参考文件\AutoSDAPlatform-master\AutoSDAPlatform-master\AllSectionDatabase.csv')
    for i in range(2, n_story + 2):
        BeamInfo = SectionProperty(
            building.member_size['beam'][i-2], SectionDatabase)
        for j in range(1, n_Xbay + 1):
            beamElementTag = int('%i%i%i%i%i%i%i' %
                                 (2, j, i, 1, j+1, i, 1))  # Beam element tag
            startNode = int('%i%i%i%i' % (j, i, 1, 5))
            endNode = int('%i%i%i%i' % (j+1, i, 1, 3))
            ModifiedMI = (n + 1.0) / n * (BeamInfo['Ix'])
            ops.element('elasticBeamColumn', beamElementTag, startNode,
                        endNode, BeamInfo['A'], Es, ModifiedMI, LinearTransf)

        # Truss elements connecting frame and leaning column
        trussElementTag = int('%i%i%i%i%i%i' %
                              (2, n_Xbay+1, i, 1, n_Xbay+2, i))
        startNode = int('%i%i%i%i' % (n_Xbay + 1, i, 1, 1))
        endNode = int('%i%i' % (n_Xbay+2, i))
        ops.element('Truss', trussElementTag, startNode,
                    endNode, AreaRigid, TrussMatID)
        print('Beams are defined!')

    ################ Define column elements ################
    # Define exterior section sizes
    for i in range(1, n_story + 1):
        ExteriorColumn = SectionProperty(
            building.member_size['exterior column'][i-1], SectionDatabase)
        InteriorColumn = SectionProperty(
            building.member_size['interior column'][i-1], SectionDatabase)
        for j in range(1, n_Xbay+2):
            columnElementTag = int('%i%i%i%i%i%i%i' % (3, j, i, 1, j, i+1, 1))
            startNode = int('%i%i%i%i' % (j, i, 1, 4))
            endNode = int('%i%i%i%i' % (j, i+1, 1, 6))
            # Determine whether the column is interior or exterior column
            # this would affect the column section size
            if 1 < j < building.geometry['number of X bay'] + 1:
                Column = InteriorColumn
            else:
                Column = ExteriorColumn
            ModifiedMI = (n + 1.0) / n * Column['Ix']
            ops.element('elasticBeamColumn', columnElementTag, startNode,
                        endNode, Column['A'], Es, ModifiedMI, PDeltaTransf)

        # Leaning column elements
        if i == 1:
            leaningElementTag = int('%i%i%i%i%i%i' % (3, n_Xbay + 2, i, n_Xbay + 2, i+1, 2))
            startNode = int('%i%i', (n_Xbay+2, i))
            endNode = int('%i%i%i' % (n_Xbay+2, i+1, 2))
        else:
            leaningElementTag = int('%i%i%i%i%i%i%i' % (3, n_Xbay + 2, i, 4, n_Xbay + 2, i+1, 2))
            startNode = int('%i%i%i', (n_Xbay+2, i, 4))
            endNode = int('%i%i%i' % (n_Xbay+2, i+1, 2))
        ops.element('elasticBeamColumn', leaningElementTag, startNode, 
                    endNode, AreaRigid, Es, IRigid, PDeltaTransf)
        print('Columns are defined!')

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
