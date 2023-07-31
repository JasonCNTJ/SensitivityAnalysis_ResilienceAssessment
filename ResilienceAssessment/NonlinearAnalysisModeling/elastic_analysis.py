# This file is used to run elastic analysis
# Developed by Jiajun Du @ Tongji University in July 2023
import openseespy.opensees as ops
from Functions import SectionProperty, rotLeaningCol
import pandas as pd
import math
import opsvis as opsv


# ################ Generate OpenSeesPy model for elastic analysis ################
def ElasticAnalysis(building):
    """
    This function establish and run the OpenSeesPy for elastic analysis
    :params building:
    """
    # Clear the memory
    ops.wipe()

    # Defining model builder
    ops.model('basic', '-ndm', 2, '-ndf', 3)

    # ################ Define Variables ################
    # Units: kips, inches, seconds
    PDeltaTransf = 1
    LinearTransf = 2
    # Set up geometric transformation of element
    ops.geomTransf('PDelta', PDeltaTransf)
    ops.geomTransf('Linear', LinearTransf)
    # Define Young's modulus of steel
    Es = 29000
    # Define very small number
    Negligible = 1e-12
    # Define gravity constant
    g = 386.4
    # Define rigid links between leaning column and frame
    TrussMatID = 600  # Material tag
    AreaRigid = 1e9  # Large area
    IRigid = 1e9  # Large moment of inertia
    ops.uniaxialMaterial('Elastic', TrussMatID, Es)
    # Define very stiff material used for axial stiffness of beam/column hinges ?
    StiffMatID = 1200
    LargeNumber = 1e12
    ops.uniaxialMaterial('Elastic', StiffMatID, LargeNumber)

    print('Variables are defined!')

    # ################ Define all nodes ################
    # Define all nodes
    # Units: inch
    BayWidth = float(building.geometry['X bay width']) * 12
    FirstStory = float(building.geometry['first story height']) * 12
    TypicalStory = float(building.geometry['typical story height']) * 12

    # Define nodes at corner of frames and leaning column
    n_story = int(building.geometry['number of story'])
    n_Xbay = int(building.geometry['number of X bay'])
    for i in range(1, n_story + 2):
        # Define nodes at corner of frames
        for j in range(1, n_Xbay + 2):
            nodetag = int('%i%i%i' % (j, i, 1))  # Node label
            Xc = (j - 1) * BayWidth
            if i <= 2:
                Yc = (i-1) * FirstStory
            else:
                Yc = FirstStory + (i-2) * TypicalStory
            ops.node(nodetag, Xc, Yc)

        # Define the nodes for leaning column
        leaningNodeTag = int('%i%i' % (n_Xbay + 2, i))
        Xlc = (n_Xbay + 1) * BayWidth
        if i <= 2:
            Ylc = (i-1) * FirstStory
        else:
            Ylc = FirstStory + (i-2) * TypicalStory
        ops.node(leaningNodeTag, Xlc, Ylc)
    print('Nodes at frame corner and leaning column are defined!')

    # Write the extra nodes for leaning column springs
    Xec = (n_Xbay + 1) * BayWidth
    for i in range(2, n_story + 2):
        # The node below floor level
        extraNodeTagB = int('%i%i%i' % (n_Xbay + 2, i, 2))
        Yec = FirstStory + (i-2) * TypicalStory
        ops.node(extraNodeTagB, Xec, Yec)

        # If it's top story, node above roof is not needed
        # because no leaning column above roof
        if i < n_story + 1:
            # The node above floor level
            extraNodeTagT = int('%i%i%i' % (n_Xbay + 2, i, 4))
            ops.node(extraNodeTagT, Xec, Yec)
        else:
            pass
    print('Extra nodes for leaning column springs are defined!')

    # ################ Write_fixities ################
    # Define all fixities at all column bases
    for j in range(1, n_Xbay + 2):
        fixNode = int('%i%i%i' % (j, 1, 1))
        ops.fix(fixNode, 1, 1, 1)
    # Leaning column base
    leaningFixNode = int('%i%i' % (n_Xbay + 2, 1))
    ops.fix(leaningFixNode, 1, 1, 0)
    print('All column base fixities have been defined!')

    # ################ Write floor constraint ################
    # Define floor constrain, i.e., equal DOF
    ConstrainDOF = 1  # Nodes at same floor level have identical lateral displacement
    for i in range(2, n_story + 2):
        for j in range(2, n_Xbay + 2):
            startNode = int('%i%i%i' % (1, i, 1))
            endNode = int('%i%i%i' % (j, i, 1))
            ops.equalDOF(startNode, endNode, ConstrainDOF)
        # Include the leaning column nodes to floor constrain
        endLNode = int('%i%i' % (n_Xbay + 2, i))
        ops.equalDOF(startNode, endLNode, ConstrainDOF)

    print('Floor constraints are defined!')

    # ################ Write beam ################
    # Define beam section sizes
    SectionDatabase = pd.read_csv(
        r'C:\Users\12734\OneDrive\重要文件\可参考文件\AutoSDAPlatform-master\AutoSDAPlatform-master\AllSectionDatabase.csv')
    for i in range(2, n_story + 2):
        BeamInfo = SectionProperty(building.member_size['beam'][i-2],
                                   SectionDatabase)
        for j in range(1, n_Xbay + 1):
            beamElementTag = int('%i%i%i%i%i%i%i' %
                                 (2, j, i, 1, j+1, i, 1))  # Beam element tag
            startNode = int('%i%i%i' % (j, i, 1))
            endNode = int('%i%i%i' % (j+1, i, 1))
            ops.element('elasticBeamColumn', beamElementTag, startNode,
                        endNode, BeamInfo['A'], Es, BeamInfo['Ix'], LinearTransf)

        # Truss elements connecting frame and leaning column
        trussElementTag = int('%i%i%i%i%i%i' %
                              (2, n_Xbay + 1, i, 1, n_Xbay + 2, i))
        startNode = int('%i%i%i' % (n_Xbay + 1, i, 1))
        endNode = int('%i%i' % (n_Xbay+2, i))
        ops.element('Truss', trussElementTag, startNode,
                    endNode, AreaRigid, TrussMatID)
    print('Beams are defined!')
    
    # ################ Write column ################
    # Define exterior column section sizes
    for i in range(1, n_story + 1):
        ExteriorColumn = SectionProperty(
            building.member_size['exterior column'][i-1], SectionDatabase)
        InteriorColumn = SectionProperty(
            building.member_size['interior column'][i-1], SectionDatabase)
        for j in range(1, n_Xbay+2):
            columnElementTag = int('%i%i%i%i%i%i%i' % (3, j, i, 1, j, i+1, 1))
            startNode = int('%i%i%i' % (j, i, 1))
            endNode = int('%i%i%i' % (j, i+1, 1))
            # Determine whether the column is interior or exterior column
            # this would affect the column section size
            if 1 < j < n_Xbay + 1:
                Column = InteriorColumn
            else:
                Column = ExteriorColumn
            ops.element('elasticBeamColumn', columnElementTag, startNode,
                        endNode, Column['A'], Es, Column['Ix'], PDeltaTransf)

        # Leaning column elements
        if i == 1:
            leaningElementTag = int('%i%i%i%i%i%i' % (
                3, n_Xbay + 2, i, n_Xbay + 2, i+1, 2))
            startNode = int('%i%i' % (n_Xbay+2, i))
            endNode = int('%i%i%i' % (n_Xbay+2, i+1, 2))
        else:
            leaningElementTag = int('%i%i%i%i%i%i%i' % (
                3, n_Xbay + 2, i, 4, n_Xbay + 2, i+1, 2))
            startNode = int('%i%i%i' % (n_Xbay+2, i, 4))
            endNode = int('%i%i%i' % (n_Xbay+2, i+1, 2))
        ops.element('elasticBeamColumn', leaningElementTag, startNode,
                    endNode, AreaRigid, Es, IRigid, PDeltaTransf)
    print('Columns are defined!')
    
    # ################ Write leaning column spring ################
    # Rotational spring for leaning column
    for i in range(2, n_story + 2):
        # write the springs below floor level i
        leaningSpringTagB = int('%i%i%i%i%i' % (n_Xbay + 2, i, 
                                                n_Xbay + 2, i, 2))
        nodeRLB = int('%i%i' % (n_Xbay + 2, i))
        nodeCLB = int('%i%i%i' % (n_Xbay + 2, i, 2))
        rotLeaningCol(leaningSpringTagB, nodeRLB, nodeCLB, StiffMatID)
        
        # write the springs above floor level i
        # If it is roof, no springs above the roof
        if i < n_story + 1:
            leaningSpringTagT = int('%i%i%i%i%i' % (n_Xbay + 2, i,
                                                    n_Xbay + 2, i, 4))
            nodeRLT = int('%i%i' % (n_Xbay + 2, i))
            nodeCLT = int('%i%i%i' % (n_Xbay + 2, i, 4))
            rotLeaningCol(leaningSpringTagT, nodeRLT, nodeCLT, StiffMatID)
        else:
            pass
        
    # ################ Write Mass ################
    # Define Nodal Mass
    # Define floor weights and each nodal mass
    FrameTributaryMassRatio = 1.0 / float(building.geometry['number of X LFRS'])
    TotalNodesPerFloor = n_Xbay + 2
    for i in range(2, n_story + 2):
        FloorWeight = building.gravity_loads['floor weight'][i-2]
        # Mass along X direction
        NodalMassFloor = FloorWeight * FrameTributaryMassRatio / TotalNodesPerFloor / g
        
        # Write nodal masses for each floor level
        for j in range(1, n_Xbay + 2):
            nodetag = int('%i%i%i' % (j, i, 1))
            ops.mass(nodetag, NodalMassFloor, Negligible, Negligible)
    print('Nodal mass are defined!')

    # do eigenvalue analysis
    PI = 2 * math.asin(1.0)
    numEigenvalues = 3
    lambdaN = ops.eigen('-genBandArpack', numEigenvalues)
    w1 = lambdaN[0]**0.5
    w3 = lambdaN[2]**0.5
    T1 = 2 * PI / w1
    T3 = 2 * PI / w3
    print(w1, w3)
    print(T1, T3)
    
    # opsv.plot_mode_shape(1, sfac=False, nep=17, unDefoFlag=1, 
    # fmt_undefo='g:', interpFlag=0, endDispFlag=0, fmt_interp='b-', 
    # fmt_nodes='rs', Eo=0, az_el=(- 60.0, 40.0), fig_wi_he=(60.0, 40.0), 
    # fig_lbrt=(0.04, 0.04, 0.96, 0.96))
    
    
