# Define functions and procedures
import openseespy.opensees as ops
import numpy as np
import sys


################ Function: NodesAroundPanelZone ################


def NodesAroundPanelZone(no_Pier, no_Floor, Xc, Yc, PanelSize, MaximumFloor,
                         MaximumCol):
    """
    :params no_Pier: the column ID, starting from 1 to the number of columns in each frame
    :params no_Floor: the floor level for frame, ground floor is 1
    :params Xc: X coordinate of the column centerline
    :params Yc: Y coordinate of the beam centerline
    :params PanelSize: a list with two elements [a, b]
                        a: the depth of column
                        b: the depth of beam

    # Node Label Convention:
    # Pier number_Level_Position ID
    # Pier number: 1,2,3,4... used to indicate which column pier;
    # Level:1,2,3,4... used to indicate the floor level
    # Position ID: two digits: 
    #                   00: specially used for ground floor
    #                   01-12: nodes for Panel Zone
    #                   01: top left node
    #                   02: top left node
    #                   03: top right node
    #                   04: top right node
    #                   05: bottom right node
    #                   06: bottom right node
    #                   07: bottom left node
    #                   08: bottom left node
    #                   09: mid left node
    #                   10: top mid node
    #                   11: mid right node
    #                   12: bottom mid node
    #                   13-18: nodes for Plastic Hinge
    #                   13: left(negative) beam node
    #                   14: Top(positive) column node
    #                   15: right(positive) beam node
    #                   16: Bottom(negative) column node
    """

    if no_Floor == 1:
        nodetag = int('%i%i%i' % (no_Pier, no_Floor, 10))
        ops.node(nodetag, Xc, Yc)
    else:
        dc = PanelSize[0] / 2.0
        db = PanelSize[1] / 2.0

        # define nodes in X direction panel zone
        nodetag1 = int('%s%s%s' % (no_Pier, no_Floor, '01'))
        nodetag2 = int('%s%s%s' % (no_Pier, no_Floor, '02'))
        nodetag3 = int('%s%s%s' % (no_Pier, no_Floor, '03'))
        nodetag4 = int('%s%s%s' % (no_Pier, no_Floor, '04'))
        nodetag5 = int('%s%s%s' % (no_Pier, no_Floor, '05'))
        nodetag6 = int('%s%s%s' % (no_Pier, no_Floor, '06'))
        nodetag7 = int('%s%s%s' % (no_Pier, no_Floor, '07'))
        nodetag8 = int('%s%s%s' % (no_Pier, no_Floor, '08'))
        nodetag9 = int('%s%s%s' % (no_Pier, no_Floor, '09'))
        nodetag10 = int('%s%s%s' % (no_Pier, no_Floor, '10'))
        nodetag11 = int('%s%s%s' % (no_Pier, no_Floor, '11'))
        nodetag12 = int('%s%s%s' % (no_Pier, no_Floor, '12'))
        nodetag13 = int('%s%s%s' % (no_Pier, no_Floor, '13'))
        nodetag14 = int('%s%s%s' % (no_Pier, no_Floor, '14'))
        nodetag15 = int('%s%s%s' % (no_Pier, no_Floor, '15'))
        nodetag16 = int('%s%s%s' % (no_Pier, no_Floor, '16'))
        ops.node(nodetag1, Xc - dc, Yc + db)
        ops.node(nodetag2, Xc - dc, Yc + db)
        ops.node(nodetag3, Xc + dc, Yc + db)
        ops.node(nodetag4, Xc + dc, Yc + db)
        ops.node(nodetag5, Xc + dc, Yc - db)
        ops.node(nodetag6, Xc + dc, Yc - db)
        ops.node(nodetag7, Xc - dc, Yc - db)
        ops.node(nodetag8, Xc - dc, Yc - db)
        ops.node(nodetag9, Xc - dc, Yc)
        ops.node(nodetag11, Xc + dc, Yc)
        ops.node(nodetag10, Xc, Yc + db)
        ops.node(nodetag12, Xc, Yc - db)

        # define nodes for column hinge
        ops.node(nodetag16, Xc, Yc - db)
        if no_Floor != MaximumFloor:
            ops.node(nodetag14, Xc, Yc + db)
        # define nodes for xBeam hinge
        if no_Pier != 1:
            ops.node(nodetag13, Xc - dc, Yc)
        if no_Pier != MaximumCol:
            ops.node(nodetag15, Xc + dc, Yc)


################ Function: CreateIMKMaterial ################


def CreateIMKMaterial(matTag, K0, n, a_men, My, Lambda, theta_p, theta_pc, residual, theta_u):
    # Input argument explanation:
    # matTag: a unique ID to represent the material
    # K0: Initial stiffness of beam component before the modification of n
    #     i.e., 6*E*Iz/L where E, Iz, and L are Young's modulus, moment of inertia, and length of beam
    # n: a coefficient which is equal to 10 based on reference suggestion
    # a_men: strain hardening ratio before modification of n
    # My: effective yield strength, slightly greater than predicted bending strength, which is Fy*Z.
    # Lambda: reference cumulative plastic rotation
    # theta_p: pre-capping plastic rotation
    # theta_pc: post-capping plastic rotation
    # residual: residual strength ratio
    # theta_u: ultimate rotation.
    # Reference:
    #           [1] Ibarra et al. (2005) Hysteretic models that incorporate strength and stiffness deterioration.
    #           [2] Ibarra and Krawinkler. (2005)  Global collapse of frame structures under seismic excitation.
    #           [3] Lignos (2008) Sidesway collapse of deteriorating structural systems under seismic excitation.
    #           [4] Lignos and Krawinkler. (2011) Deterioration modeling of steel component in support of collapse prediction of
    #                                         steel moment frames under earthquake loading.
    # [5] Lignos et al. (2019) Proposed updates to the ASCE 41 nonlinear modeling parameters for wide-flange steel
    # columns in support performance-based seismic engineering.
    Ks = (n + 1.0) * K0  # Initial stiffness for rotational spring (hinge)
    asPosScaled = a_men / (1.0 + n * (1.0 - a_men))
    asNegScaled = asPosScaled
    Lambda_S = (0.0 + 1.0) * Lambda  # basic strength deterioration
    Lambda_C = (0.0 + 1.0) * Lambda  # post-capping strength deterioration
    # accelerated reloading stiffness deterioration (a very large number = no cyclic deterioration)
    Lambda_A = (0.0 + 1.0) * Lambda
    # unloading stiffness deterioration (a very large number = no cyclic deterioration)
    Lambda_K = (0.0 + 1.0) * Lambda
    # Built-in command:
    # (OpenSees: Tcl)
    # uniaxialMaterial Bilin $matTag $K0 $as_Plus $as_Neg $My_Plus $My_Neg $Lambda_S $Lambda_C $Lambda_A $Lambda_K
    #                       $c_S $c_C $c_A $c_K $theta_p_Plus $theta_p_Neg $theta_pc_Plus $theta_pc_Neg $Res_Pos $Res_Neg
    #                       $theta_u_Plus $theta_u_Neg $D_Plus $D_Neg
    # Argument explanation:
    # http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Bilinear_Hysteretic_Response_(Bilin_Material)
    # (OpenSeesPy: Python)
    # uniaxialMaterial('Bilin', matTag, K0, as_Plus, as_Neg, My_Plus, My_Neg, Lamda_S, Lamda_C, Lamda_A, Lamda_K,
    #                   c_S, c_C, c_A, c_K, theta_p_Plus, theta_p_Neg, theta_pc_Plus, theta_pc_Neg, Res_Pos, Res_Neg,
    #                   theta_u_Plus, theta_u_Neg, D_Plus, D_Neg, nFactor=0.0)
    # Argument explanation:
    # https://openseespydoc.readthedocs.io/en/latest/src/Bilin.html
    # Create the modified Ibarra-Medina-Krawinkler material model
    ops.uniaxialMaterial('Bilin', matTag, Ks, asPosScaled, asNegScaled, My, -My,
                         Lambda_S, Lambda_C, Lambda_A, Lambda_K, 1.0, 1.0, 1.0, 1.0,
                         theta_p, theta_p, theta_pc, theta_pc, residual, residual,
                         theta_u, theta_u, 1.0, 1.0)


################ Function: SectionProperty ################


def SectionProperty(target_size, sectionDataBase):
    """
    This function is used to obtain the section property when section size is given.
    The output will be stored in a dictionary.
    :params target_size: a string which defines section size, e.g. 'W14X500'
    :param sectionDataBaseFile: a dataframe read from .csv file
    :return: section_info: a dictionary which includes section size, index, and associated properties
    """
    try:
        for indx in np.array(sectionDataBase['index']):
            if target_size == sectionDataBase.loc[indx, 'section size']:
                section_info = sectionDataBase.loc[indx, :]
        return section_info.to_dict()
    except:
        sys.stderr.write(
            'Error: wrong size nominated!\nNo such size exists in section database!')
        sys.exit(1)

################ Function: rotBeamSpring ################


def rotBeamSpring(eleID, nodeR, nodeC, matID, stiffMatID):
    """
    Create a zero length element to represent the beam hinge
    Axial stiffness is extremely large
    Flexural stiffness is defined by Modified IMK material
    Input argument explanation:
    :params eleID: a unique ID to label the element
    :params nodeR: master node
    :params nodeC: slave node
    :params matID: the associated modified IMK material ID
    :params stiffMatID: the ID associated with the stiff material (defined in 'Variables')
    1,2,3 - translation along local x,y,z axes, respectively;
    4,5,6 - rotation about local x,y,z axes, respectively
    If the optional orientation vectors are not specified, the local element axes
    coincide with the global axes. Otherwise the local z-axis is defined by the
    cross product between the vectors x and yp vectors specified on the command line.
    """

    ops.element('zeroLength', eleID, nodeR, nodeC, '-mat', stiffMatID,
                stiffMatID, matID, '-dir', 1, 2, 6, '-orient', 1, 0, 0, 0, 1, 0)

################ Function: rotColumnSpring ################


def rotColumnSpring(eleID, nodeR, nodeC, matID, stiffMatID):
    """
    Create a zero length element to represent the column hinge
    Axial stiffness is extremely large
    Flexural stiffness is defined by Modified IMK material
    Input argument explanation:
    :params eleID: a unique ID to label the element
    :params nodeR: master node
    :params nodeC: slave node
    :params matID: the associated modified IMK material ID
    :params stiffMatID: the ID associated with the stiff material (defined in 'Variables')
    1,2,3 - translation along local x,y,z axes, respectively;
    4,5,6 - rotation about local x,y,z axes, respectively
    If the optional orientation vectors are not specified, the local element axes
    coincide with the global axes. Otherwise the local z-axis is defined by the
    cross product between the vectors x and yp vectors specified on the command line.
    """
    ops.element('zeroLength', eleID, nodeR, nodeC, '-mat', stiffMatID,
                stiffMatID, matID, '-dir', 1, 2, 6, '-orient', 0, 1, 0, 1, 0, 0)

################ Function: rotLeaningCol ################


def rotLeaningCol(eleID, nodeR, nodeC, stiffMatID):
    """
    Create a zero-stiffness elastic rotational spring for the leaning column
    while constraining the translational DOFs
    Argument explanation:
    :params eleID: unique element ID for the zero-stiffness rotational spring
    :params nodeR: ID of node which will be retained by multi-point constraint
    :params nodeC: ID of node which will be constrained by multi-point constraint
    """

    # Spring stiffness: very small number (not using zero) to avoid numerical convergence issuse
    K = 1e-9

    # Create the material and zero length element (spring)
    ops.uniaxialMaterial('Elastic', eleID,  K)
    ops.element('zeroLength', eleID, nodeR, nodeC, '-mat', stiffMatID,
                stiffMatID, eleID, '-dir', 1, 2, 6, '-orient', 0, 1, 0, 1, 0, 0)

################ Function: elemPanelZone2D ################


def elemPanelZone2D(eleID, nodeR, E, VerTransfTag, HorTransfTag):
    """
    Formal arguments
    eleID     - unique element ID for the zero-length rotational spring
    nodeR     - node ID for first point (top left) of panel zone --> this node creates all the others
    E         - Young's modulus
    G         - Shear modulus
    S_la      - Large number for J
    A_PZ      - area of rigid link that creates the panel zone
    I_PZ      - moment of inertia of Rigid link that creates the panel zone
    transfTag - geometric transformation
    """
    # define panel zone nodes
    node01 = nodeR  # top left of joint
    node02 = node01 + 1  # top left of joint
    node03 = node01 + 2  # top right of joint
    node04 = node01 + 3  # top right of joint
    node05 = node01 + 4  # btm right of joint
    node06 = node01 + 5  # btm right of joint
    node07 = node01 + 6  # btm left
    node08 = node01 + 7  # btm left
    node09 = node01 + 8  # mid left
    node10 = node01 + 9  # top center
    node11 = node01 + 10  # mid right
    node12 = node01 + 11  # btm center
    
    # create element IDs as a function of first input eleID (8 per panel zone)
    x1 = eleID  # top : left element
    x2 = x1 + 1  # top : right element
    x3 = x1 + 2  # right : top element
    x4 = x1 + 3  # right : btm element
    x5 = x1 + 4  # btm : right element
    x6 = x1 + 5  # btm : left element
    x7 = x1 + 6  # left : btm element
    x8 = x1 + 7  # left : top element
    
    A_PZ = 1.0e12  # area of panel zone element (make much larger than A of frame elements)
    Ipz = 1.0e12  # moment of inertia of panel zone element (make much larger tha I of frame elements)
    
    # create panel zone elements
    ops.element('elasticBeamColumn', x1, node02, node10, A_PZ, E, Ipz, HorTransfTag)
    ops.element('elasticBeamColumn', x2, node10, node03, A_PZ, E, Ipz, HorTransfTag)
    ops.element('elasticBeamColumn', x3, node04, node11, A_PZ, E, Ipz, VerTransfTag)
    ops.element('elasticBeamColumn', x4, node11, node05, A_PZ, E, Ipz, VerTransfTag)
    ops.element('elasticBeamColumn', x5, node06, node12, A_PZ, E, Ipz, HorTransfTag)
    ops.element('elasticBeamColumn', x6, node12, node07, A_PZ, E, Ipz, HorTransfTag)
    ops.element('elasticBeamColumn', x7, node08, node09, A_PZ, E, Ipz, VerTransfTag)
    ops.element('elasticBeamColumn', x8, node09, node01, A_PZ, E, Ipz, VerTransfTag)

################ Function: rotPanelZone2D ################


def rotPanelZone2D(eleID, nodeR, nodeC, E, Fy, dc, bf_c, tf_c, tp, db, Ry, As):
    """
    Procedure that creates a rotational spring and constrains the corner nodes of a panel zone
    :params eleID: unique element ID for this zero length rotational spring
    :params nodeR: node ID which will be retained by the multi-point constraint, top right of panel zone
    :params nodeC: node ID which will be constrained by the multi-point constraint, top right of panel zone
    :params E: modulus of elasticity
    :params Fy: yield strength
    :params dc: column depth
    :params bf_c: column flange width
    :params tf_c: column flange thickness
    :params tp: panel zone thickness
    :params db: beam depth
    :params Ry: expected value for yield strength --> Typical value is 1.2
    :params as: assumed strain hardening
    """
    # Trilinear Spring
    # Yield Shear
    Vy = 0.55 * Fy * dc * tp
    # Shear Modulus
    G = E / (2.0 * (1.0 + 0.30))
    # Elastic Stiffness
    Ke = 0.95 * G * tp * dc
    # Plastic Stiffness
    Kp = 0.95 * G * bf_c * (tf_c * tf_c) / db
    
    # Define Trilinear Equivalent Rotational Spring
    # Yield point for Trilinear Spring at gamma1_y
    gamma1_y = Vy / Ke
    M1y = gamma1_y * (Ke * db)
    # Second point for trilinear spring at 4 * gamma1_y
    gamma2_y = 4.0 * gamma1_y
    M2y = M1y + (Kp * db) * (gamma2_y - gamma1_y)
    # Third point for trilinear spring at 100 * gamma1_y
    gamma3_y = 100.0 * gamma1_y
    M3y = M2y + (As * Ke * db) * (gamma3_y - gamma2_y)
    
    # Hysteretic Material without pinching and damage (same mat ID as ELe ID)
    ops.uniaxialMaterial('Hysteretic', eleID, M1y, gamma1_y, M2y, gamma2_y, M3y, gamma3_y,
                         -M1y, -gamma1_y, -M2y, -gamma2_y, -M3y, -gamma3_y,
                         1, 1, 0.0, 0.0, 0.0)
    ops.element('zeroLength', eleID, nodeR, nodeC, '-mat', eleID, '-dir', 6)
    ops.equalDOF(nodeR, nodeC, 1, 2)
    # Constrain the translational DOF with a multi-point constraint
    # Left Top Corner of PZ
    nodeR_1 = nodeR - 2
    nodeR_2 = nodeR_1 + 1
    # Right Bottom Corner of PZ
    nodeR_5 = nodeR + 2
    nodeR_6 = nodeR_5 + 1
    # Left bottom corner
    nodeR_7 = nodeR + 4
    nodeR_8 = nodeR_7 + 1
    # Retained constrained DOF_1 DOF_2
    ops.equalDOF(nodeR_1, nodeR_2, 1, 2)
    ops.equalDOF(nodeR_5, nodeR_6, 1, 2)
    ops.equalDOF(nodeR_7, nodeR_8, 1, 2)