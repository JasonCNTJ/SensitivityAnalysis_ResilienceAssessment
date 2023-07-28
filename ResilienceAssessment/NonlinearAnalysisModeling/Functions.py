# Define functions and procedures
import openseespy.opensees as ops


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
